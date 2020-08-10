import json

from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404, loader

from .forms import NewCheckoutForm, NewReservationForm, ReturnCheckoutForm, AddNewEquipmentForm, AddNewStudentForm, \
    AddNewAdminAccount, EditAdminAccount, ReservationStartForm, AcceptOrDenyReservation, NewCheckoutFromReservation

from .models import Student, Equipment, Checkout, Reservation, User

from datetime import datetime, date

from django.contrib.auth.decorators import login_required
from django.contrib import messages

from checkouts.utils import render_to_pdf, grab_all_equipment

from django.db.models import Q

from .tasks import post_checkout_confirmation_email


def error404(request, exception):
    data = {}
    return render(request, 'checkouts/404.html', data)


def error500(request):
    data = {}
    return render(request, 'checkouts/500.html', data)


def calendar(request):
    active_checkouts = Checkout.objects.filter(completed=False)
    accepted_reservations = Reservation.objects.filter(accepted=True, completed=False)
    pending_reservations = Reservation.objects.filter(accepted=False, completed=False)
    return render(request, 'checkouts/calendar.html', context={
        'active_checkouts': active_checkouts,
        'accepted_reservations': accepted_reservations,
        'pending_reservations': pending_reservations
    })


@login_required()
def dashboard(request):
    # template = loader.get_template('checkouts/dashboard.html')
    today = date.today()

    recent_checkouts = Checkout.objects.filter(completed=False).order_by('-due_date')[:5]
    checkouts_due_today = Checkout.objects.filter(completed=False, due_date=today)
    overdue_checkouts = Checkout.objects.filter(completed=False, due_date__lt=today)
    active_checkouts = recent_checkouts.count()
    unavailable_equipment = Equipment.objects.filter(availability=False)
    active_users = Student.objects.filter(active=True).count()
    inactive_users = Student.objects.filter(active=False).count()
    pending_reservations = Reservation.objects.filter(completed=False, accepted=False)
    accepted_reservations = Reservation.objects.filter(accepted=True, completed=False)

    return render(request, 'checkouts/dashboard.html', context={
        'recent_checkouts': recent_checkouts,
        'checkouts_due_today': checkouts_due_today,
        'overdue_checkouts': overdue_checkouts,
        'active_checkouts': active_checkouts,
        'unavailable_equipment': unavailable_equipment,
        'active_users': active_users,
        'inactive_users': inactive_users,
        'pending_reservations': pending_reservations,
        'accepted_reservations': accepted_reservations
    })


@login_required()
def admin_account(request):
    admin_account = get_object_or_404(User, pk=request.user.id)
    checkouts_processed = Checkout.objects.filter(processed_by=admin_account)
    return render(request, 'checkouts/admin-account.html', context={'checkouts_processed': checkouts_processed})


@login_required()
def edit_admin_account(request, pk):
    admin_account = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        form = EditAdminAccount(request.POST, instance=admin_account)
        if form.is_valid():
            form.save()
            return redirect('admin_account')

    else:
        form = EditAdminAccount(instance=admin_account)
    return render(request, 'checkouts/edit-admin.html', context={'admin_account': admin_account, 'form': form})


@login_required()
def admin_account_detail(request, pk):
    admin_account = get_object_or_404(User, pk=pk)
    return render(request, 'checkouts/admin-account-detail.html', context={'admin_account': admin_account})


def add_new_admin(request):
    if request.method == 'POST':
        form = AddNewAdminAccount(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            return redirect('admin_account_details', pk=user.pk)
    else:
        form = AddNewAdminAccount()

    return render(request, 'checkouts/add-new-admin.html', {'form': form})


# CHECKOUT VIEWS
@login_required()
def all_checkouts(request):
    all_checkouts = Checkout.objects.filter(completed=False).order_by('-due_date')
    today = datetime.today()
    context = {
        'all_checkouts': all_checkouts,
        'today': today
    }
    return render(request, 'checkouts/all-checkouts.html', context=context)


@login_required()
def checkout_detail(request, pk):
    checkout = get_object_or_404(Checkout, pk=pk)
    return render(request, 'checkouts/detail-checkout.html', context={'checkout': checkout})


@login_required()
def past_checkouts(request):
    past_checkouts = Checkout.objects.filter(completed=True).order_by('-pk')
    return render(request, 'checkouts/past-checkouts.html', context={'past_checkouts': past_checkouts})


@login_required()
def new_checkout(request):
    if request.method == 'POST':
        form = NewCheckoutForm(request.POST)

        if form.is_valid():
            new_checkout = form.save()

            new_checkout.processed_by = request.user
            new_checkout.notes = form.cleaned_data.get('notes')

            # THESE RETURN ALL SEPARATE QUERY SETS
            checkout_student = form.cleaned_data.get('student')
            cameras = form.cleaned_data.get('cameras')
            lights = form.cleaned_data.get('lights')
            computers = form.cleaned_data.get('computers')
            projectors = form.cleaned_data.get('projectors')
            audio = form.cleaned_data.get('audio')
            misc = form.cleaned_data.get('misc')

            # MERGING ALL THE QUERY SETS
            selected_equipment = cameras | lights | computers | projectors | audio | misc

            for equipment in selected_equipment:
                checkout_student.current_equipment.add(equipment)
                equipment.current_user = checkout_student
                equipment.availability = False
                equipment.save()

            new_checkout.save()

            # CELERY TASK
            post_checkout_confirmation_email.delay(new_checkout.pk)

            return redirect('complete_checkout', pk=new_checkout.pk)
    else:
        form = NewCheckoutForm()

    return render(request, 'checkouts/new-checkout.html', {'form': form})


@login_required()
def complete_checkout(request, pk):
    checkout = get_object_or_404(Checkout, pk=pk)
    return render(request, 'checkouts/complete-checkout.html', context={'checkout': checkout})


def completed_checkout_pdf(request, pk):
    checkout = get_object_or_404(Checkout, pk=pk)

    # ORIGINAL:
    # cameras = checkout.cameras.all()
    # lights = checkout.lights.all()
    # computers = checkout.computers.all()
    # projectors = checkout.projectors.all()
    # audio = checkout.audio.all()
    # misc = checkout.misc.all()
    # equipment = cameras | lights | computers | projectors | audio | misc

    # TRY UTIL
    equipment = grab_all_equipment(checkout)

    data = {
        'checkout_number': checkout,
        'first_name': checkout.student.first_name,
        'last_name': checkout.student.last_name,
        'user_id': checkout.student.school_id,
        'date_issued': checkout.borrow_date,
        'due_date': checkout.due_date,
        'staff_first': checkout.processed_by.first_name,
        'staff_last': checkout.processed_by.last_name,
        'notes': checkout.notes,
        'equipment': equipment,
    }
    pdf = render_to_pdf('pdf/completed-checkout-pdf.html', data)
    return HttpResponse(pdf, content_type='application/pdf')


@login_required()
def return_list_checkouts(request):
    return_list_checkouts = Checkout.objects.filter(completed=False).order_by('-due_date')
    return render(request, 'checkouts/return-list-checkouts.html', context={
        'return_list_checkouts': return_list_checkouts,
    })


@login_required()
def return_checkout(request, pk):
    checkout_to_return = Checkout.objects.get(id=pk)

    # ORIGINAL
    # cameras = checkout_to_return.cameras.all()
    # lights = checkout_to_return.lights.all()
    # computers = checkout_to_return.computers.all()
    # projectors = checkout_to_return.projectors.all()
    # audio = checkout_to_return.audio.all()
    # misc = checkout_to_return.misc.all()
    # associated_equipment = cameras | lights | computers | projectors | audio | misc

    # TRY UTIL
    associated_equipment = grab_all_equipment(checkout_to_return)

    if request.method == 'POST':
        form = ReturnCheckoutForm(request.POST)
        if form.is_valid():

            for equipment in associated_equipment:
                checkout_to_return.student.current_equipment.remove(equipment)
                equipment.current_user = None
                equipment.availability = True
                equipment.past_checkouts.add(checkout_to_return)
                equipment.save()

            old_notes = checkout_to_return.notes
            new_notes = form.cleaned_data.get('notes')

            # if there's nothing in one of these fields, it's none type, can't add to string
            if old_notes is None:
                updated_notes = new_notes
                checkout_to_return.notes = updated_notes
            elif isinstance(old_notes, str):
                updated_notes = old_notes + '\n' + new_notes
                checkout_to_return.notes = updated_notes

            checkout_to_return.return_date = date.today()
            checkout_to_return.completed = True
            checkout_to_return.save()

            return redirect('complete_checkout_return', pk=checkout_to_return.pk)

    else:
        form = ReturnCheckoutForm()

    return render(request, 'checkouts/return-checkout.html', context={
        'checkout_to_return': checkout_to_return,
        'associated_equipment': associated_equipment,
        'form': form
    })


@login_required()
def complete_checkout_return(request, pk):
    returned_checkout = get_object_or_404(Checkout, pk=pk)
    return render(request, 'checkouts/complete-checkout-return.html', context={'returned_checkout': returned_checkout})


# STUDENT VIEWS
@login_required()
def all_students(request):
    all_students = Student.objects.order_by('last_name')
    past_checkouts = Checkout.objects.order_by('-borrow_date').filter(completed=True)[:3]
    template = loader.get_template('checkouts/all-students.html')
    context = {
        'all_students': all_students,
        'past_checkouts': past_checkouts
    }
    return HttpResponse(template.render(context, request))


@login_required()
def student_detail(request, school_id):
    student = get_object_or_404(Student, school_id=school_id)
    current_equipment = student.current_equipment.all()
    current_checkouts = Checkout.objects.filter(completed=False, student=student)
    user_past_checkouts = Checkout.objects.order_by('-borrow_date').filter(completed=True, student=student)
    return render(request, 'checkouts/detail-student.html', context={
        'student': student,
        'current_equipment': current_equipment,
        'current_checkouts': current_checkouts,
        'user_past_checkouts': user_past_checkouts
    })

@login_required()
def add_new_student(request):
    if request.method == 'POST':
        form = AddNewStudentForm(request.POST)
        if form.is_valid():
            form.save()
            school_id = form.cleaned_data.get('school_id')
            return redirect('student_detail', school_id=school_id)
    else:
        form = AddNewStudentForm()

    return render(request, 'checkouts/add-new-student.html', {'form': form})


@login_required()
def edit_student(request, school_id):
    instance = get_object_or_404(Student, school_id=school_id)

    if request.method == 'POST':
        # Using same form to edit as we did to add new equipment
        # Need request.POST to update the db
        form = AddNewStudentForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            return redirect('student_detail', school_id=instance.school_id)
    else:
        # Dont need request.POST because we want the form to be autopopulated
        form = AddNewStudentForm(instance=instance)

    return render(request, 'checkouts/edit-student.html', {'form': form})


@login_required()
def delete_student(request, school_id):
    student = get_object_or_404(Student, school_id=school_id)

    if request.method == 'POST':
        student.delete()
        messages.success(request, "Student successfully deleted.")
        return redirect('all_students')

    return render(request, 'checkouts/delete-student.html', context={'student': student})


# EQUIPMENT VIEWS
def all_equipment(request):
    all_equipment = Equipment.objects.all()
    template = loader.get_template('checkouts/all-equipment.html')
    context = {'all_equipment': all_equipment}
    return HttpResponse(template.render(context, request))


@login_required()
def equipment_detail(request, pk):
    equipment = get_object_or_404(Equipment, pk=pk)
    equipment_past_checkouts = equipment.past_checkouts.all()
    return render(request, 'checkouts/detail-equipment.html', context={
        'equipment': equipment,
        'equipment_past_checkouts': equipment_past_checkouts,
        # 'is_requested': is_requested
    })


@login_required()
def add_new_equipment(request):
    if request.method == 'POST':
        form = AddNewEquipmentForm(request.POST)
        if form.is_valid():
            add_new_equipment = form.save()
            return redirect('equipment_detail', pk=add_new_equipment.pk)
    else:
        form = AddNewEquipmentForm()

    return render(request, 'checkouts/add-new-equipment.html', {'form': form})


@login_required()
def edit_equipment(request, pk):
    instance = get_object_or_404(Equipment, pk=pk)
    # instance = Equipment.objects.get(id=pk)

    if request.method == 'POST':
        # Using same form to edit as we did to add new equipment
        # Need request.POST to update the db
        form = AddNewEquipmentForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            return redirect('equipment_detail', pk=instance.pk)
    else:
        # Dont need request.POST because we want the form to be autopopulated
        form = AddNewEquipmentForm(instance=instance)

    return render(request, 'checkouts/edit-equipment.html', {'form': form})


@login_required()
def delete_equipment(request, pk):
    equipment = get_object_or_404(Equipment, pk=pk)

    if request.method == 'POST':
        equipment.delete()
        messages.success(request, "Equipment successfully deleted.")
        return redirect('all_equipment')

    return render(request, 'checkouts/delete-equipment.html', context={'equipment': equipment})


# RESERVATION VIEWS
@login_required()
def past_reservations(request):
    past_reservations = Reservation.objects.filter(completed=True).order_by('-pk')
    return render(request, 'checkouts/past-reservations.html', context={'past_reservations': past_reservations})


@login_required()
def reservation_detail(request, pk):
    reservation = get_object_or_404(Reservation, pk=pk)
    return render(request, 'checkouts/detail-reservation.html', context={'reservation': reservation})


@login_required()
def accepted_reservations(request):
    accepted_reservations = Reservation.objects.filter(accepted=True, completed=False)
    return render(request, 'checkouts/accepted-reservations.html', context={'accepted_reservations': accepted_reservations})


@login_required()
def pending_reservations(request):
    pending_reservations = Reservation.objects.filter(accepted=False, completed=False)
    return render(request, 'checkouts/pending-reservations.html', context={'pending_reservations': pending_reservations})


@login_required()
def accept_pending_reservation(request, pk):
    accepted_res = get_object_or_404(Reservation, pk=pk)
    # cameras = accepted_res.cameras.all()
    # lights = accepted_res.lights.all()
    # computers = accepted_res.computers.all()
    # projectors = accepted_res.projectors.all()
    # audio = accepted_res.audio.all()
    # misc = accepted_res.misc.all()
    # associated_equipment = cameras | lights | computers | projectors | audio | misc

    if request.method == 'POST':
        form = AcceptOrDenyReservation(request.POST)
        if form.is_valid():

            # for equipment in associated_equipment:
            #     # equipment.reservation_request = None
            #     equipment.availability = False
            #     equipment.save()

            accepted_res.accepted = True
            accepted_res.save()
            return redirect('reservation_detail', pk=accepted_res.id)

    form = AcceptOrDenyReservation()
    return render(request, 'checkouts/pending-res-accept.html', context={
        'accepted_res': accepted_res,
        'form': form
    })


@login_required()
def deny_pending_reservation(request, pk):
    denied_res = get_object_or_404(Reservation, pk=pk)

    if request.method == 'POST':
        form = AcceptOrDenyReservation(request.POST)
        if form.is_valid():

            # ORIGINAL
            # cameras = denied_res.cameras.all()
            # lights = denied_res.lights.all()
            # computers = denied_res.computers.all()
            # projectors = denied_res.projectors.all()
            # audio = denied_res.audio.all()
            # misc = denied_res.misc.all()
            # associated_equipment = cameras | lights | computers | projectors | audio | misc

            # TRY UTIL
            associated_equipment = grab_all_equipment(denied_res)

            for equipment in associated_equipment:
                equipment.reservation_request = None
                equipment.availability = True
                equipment.save()

            denied_res.accepted = False
            denied_res.completed = True
            denied_res.save()
            return redirect('reservation_detail', pk=denied_res.id)

    form = AcceptOrDenyReservation()
    return render(request, 'checkouts/pending-res-deny.html', context={
        'denied_res': denied_res,
        'form': form
    })


@login_required()
def mark_complete_reservation(request, pk):
    res_to_complete = get_object_or_404(Reservation, pk=pk)

    if request.method == 'POST':
        form = AcceptOrDenyReservation(request.POST)
        if form.is_valid():
            res_to_complete.completed = True
            res_to_complete.save()
            return redirect('reservation_detail', pk=res_to_complete.id)

    form = AcceptOrDenyReservation()
    return render(request, 'checkouts/mark-complete-reservation.html', context={
        'res_to_complete': res_to_complete,
        'form': form
    })


def start_reservation(request):
    if request.method == 'GET':
        form = ReservationStartForm(request.GET)
        if form.is_valid():
            query = request.GET.get('search', False)
            try:
                user = Student.objects.get(school_id=query)
                return redirect('new_reservation', pk=user.id)
            except:
                messages.error(request, "There's no associated user with specified ID.")
    else:
        form = ReservationStartForm()
    return render(request, 'checkouts/new-reservation-start.html', context={'form': form})


def new_reservation(request, pk):
    user = Student.objects.get(pk=pk)
    if request.method == 'POST':
        form = NewReservationForm(request.POST)
        if form.is_valid():
            new_reservation = form.save(commit=False)
            new_reservation.requested_by = user

            # MUST SAVE FIRST TO CREATE ID, TO ADD THE EQUIPMENT IN M2M RELATIONSHIP
            new_reservation.save()

            cameras = form.cleaned_data.get('cameras')
            lights = form.cleaned_data.get('lights')
            computers = form.cleaned_data.get('computers')
            projectors = form.cleaned_data.get('projectors')
            audio = form.cleaned_data.get('audio')
            misc = form.cleaned_data.get('misc')
            new_reservation.notes = form.cleaned_data.get('notes')

            new_reservation.cameras.set(cameras)
            new_reservation.lights.set(lights)
            new_reservation.computers.set(computers)
            new_reservation.projectors.set(projectors)
            new_reservation.audio.set(audio)
            new_reservation.misc.set(misc)

            selected_equipment = cameras | lights | computers | projectors | audio | misc
            for equipment in selected_equipment:
                equipment.reservation_request = new_reservation
                equipment.save()

            user.reservation_request = new_reservation
            new_reservation.save()

            return redirect('complete_reservation', pk=new_reservation.pk)
    form = NewReservationForm()
    return render(request, 'checkouts/new-reservation-form.html', context={'form': form, 'user': user})


def complete_reservation(request, pk):
    reservation = get_object_or_404(Reservation, pk=pk)
    return render(request, 'checkouts/complete-reservation.html', context={'reservation': reservation})


def completed_reservation_pdf(request, pk):
    reservation = get_object_or_404(Reservation, pk=pk)

    # ORIGINAL
    # cameras = reservation.cameras.all()
    # lights = reservation.lights.all()
    # computers = reservation.computers.all()
    # projectors = reservation.projectors.all()
    # audio = reservation.audio.all()
    # misc = reservation.misc.all()
    # equipment = cameras | lights | computers | projectors | audio | misc

    # TRY UTIL
    equipment = grab_all_equipment(reservation)

    data = {
        'reservation_number': reservation,
        'first_name': reservation.requested_by.first_name,
        'last_name': reservation.requested_by.last_name,
        'user_id': reservation.requested_by.school_id,
        'date_issued': reservation.request_date,
        'due_date': reservation.due_date,
        'notes': reservation.notes,
        'equipment': equipment,
    }
    pdf = render_to_pdf('pdf/completed-reservation-pdf.html', data)
    return HttpResponse(pdf, content_type='application/pdf')


@login_required()
def reservation_checkout(request, pk):
    reservation = get_object_or_404(Reservation, pk=pk)
    initial_data = {
        'student': reservation.requested_by,
        'cameras': reservation.cameras.all(),
        'lights': reservation.lights.all(),
        'computers': reservation.computers.all(),
        'projectors': reservation.projectors.all(),
        'audio': reservation.audio.all(),
        'misc': reservation.misc.all(),
        'notes': reservation.notes,
        'due_date': reservation.due_date
    }

    if request.method == 'POST':
        form = NewCheckoutFromReservation(request.POST, initial=initial_data)
        if form.is_valid():
            reservation_checkout = form.save()
            reservation_checkout.processed_by = request.user
            reservation_checkout.notes = form.cleaned_data.get('notes')

            # # # THESE RETURN ALL SEPARATE QUERY SETS
            checkout_user = form.cleaned_data.get('student')
            cameras = form.cleaned_data.get('cameras')
            lights = form.cleaned_data.get('lights')
            computers = form.cleaned_data.get('computers')
            projectors = form.cleaned_data.get('projectors')
            audio = form.cleaned_data.get('audio')
            misc = form.cleaned_data.get('misc')

            # # # MERGING ALL THE QUERY SETS
            selected_equipment = cameras | lights | computers | projectors | audio | misc

            for equipment in selected_equipment:
                checkout_user.current_equipment.add(equipment)
                equipment.current_user = checkout_user
                equipment.reservation_request = None
                equipment.availability = False
                equipment.save()

            checkout_user.reservation_request = None

            reservation.completed = True
            reservation_checkout.save()
            reservation.save()
            return redirect('complete_checkout', pk=reservation_checkout.pk)
    else:
        form = NewCheckoutFromReservation(initial=initial_data)
    return render(request, 'checkouts/new-checkout-from-reservation.html', context={
        'reservation': reservation,
        'form': form
    })


# USED IN HEADER
def autocompleteSearch(request):
    if request.is_ajax():
        search_text = request.GET.get('term', '')
        search_qs = Student.objects.filter(
            Q(first_name__contains=search_text) | Q(last_name__contains=search_text) | Q(school_id__contains=search_text)
        )
        results = []
        for r in search_qs:
            output = "{} {} ({})".format(r.first_name, r.last_name, r.school_id)
            results.append(output)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)





