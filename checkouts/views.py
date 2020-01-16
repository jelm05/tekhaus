from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404, loader

from .forms import NewCheckoutForm, EquipmentReturnForm, AddNewEquipmentForm, AddNewStudentForm
from .models import Student, Equipment, Checkout

from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.contrib import messages

@login_required()
def dashboard(request):
    # template = loader.get_template('checkouts/dashboard.html')
    return render(request, 'checkouts/dashboard.html')


# CHECKOUT VIEWS
@login_required()
def all_checkouts(request):
    all_checkouts = Checkout.objects.filter(completed=False).order_by('-due_date')
    today = datetime.today()
    template = loader.get_template('checkouts/all-checkouts.html')
    context = {
        'all_checkouts': all_checkouts,
        'today': today
    }
    return HttpResponse(template.render(context, request))


def checkout_detail(request, pk):
    checkout = get_object_or_404(Checkout, pk=pk)
    return render(request, 'checkouts/detail-checkout.html', context={'checkout': checkout})


@login_required()
def new_checkout(request):
    if request.method == 'POST':
        form = NewCheckoutForm(request.POST)
        if form.is_valid():
            new_checkout = form.save()

            # THESE RETURN ALL SEPARATE QUERY SETS
            checkout_student = form.cleaned_data.get('student')
            cameras = form.cleaned_data.get('cameras')
            lights = form.cleaned_data.get('lights')
            computers = form.cleaned_data.get('computers')
            projectors = form.cleaned_data.get('projectors')
            audio = form.cleaned_data.get('audio')
            misc = form.cleaned_data.get('misc')

            # selected_equipment: <class 'django.db.models.query.QuerySet'>
            # checkout_student: <class 'checkouts.models.Student'>
            # new_checkout: <class 'checkouts.models.Checkout'>

            # MERGING ALL THE QUERY SETS
            selected_equipment = cameras | lights | computers | projectors | audio | misc

            for equipment in selected_equipment:
                checkout_student.current_equipment.add(equipment)
                equipment.current_user = checkout_student
                equipment.availability = False
                equipment.save()

            new_checkout.save()
            return redirect('complete', pk=new_checkout.pk)
    else:
        form = NewCheckoutForm()

    return render(request, 'checkouts/new-checkout.html', {'form': form})


@login_required()
def complete(request, pk):
    checkout = get_object_or_404(Checkout, pk=pk)
    equipment = checkout.student.current_equipment.all()
    return render(request, 'checkouts/complete.html', context={'checkout': checkout, 'equipment': equipment})


# WORKING BUT NEEDS ERRORS
@login_required()
def equipment_return(request):
    all_checkouts = Checkout.objects.filter(completed=False).order_by('-due_date')

    if request.method == 'POST':
        form = EquipmentReturnForm()
        if form.is_valid:
            checkout_id = int(request.POST.get('checkout_id'))
            checkout = Checkout.objects.get(id=checkout_id)
            checkout_student = checkout.student

            equipment_to_return = checkout.student.current_equipment.all()

            for equipment in equipment_to_return:
                equipment.current_user = None
                equipment.availability = True
                equipment.save()

            checkout_student.current_equipment.clear()

            checkout.completed = True
            checkout.save()

            return render(request, 'checkouts/equipment-return.html', context={
                'form': form,
                'all_checkouts': all_checkouts,
            })
    else:
        form = EquipmentReturnForm()
    return render(request, 'checkouts/equipment-return.html', context={
        'form': form,
        'all_checkouts': all_checkouts,
    })


def past_checkouts(request):
    past_checkouts = Checkout.objects.filter(completed=True)
    template = loader.get_template('checkouts/past-checkouts.html')
    context = {
        'past_checkouts': past_checkouts,
    }
    return HttpResponse(template.render(context, request))


# STUDENT VIEWS
@login_required()
def all_students(request):
    all_students = Student.objects.order_by('last_name')
    past_checkouts = Checkout.objects.order_by('-borrow_date').filter(completed=True)
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
    return render(request, 'checkouts/detail-student.html', context={'student': student, 'current_equipment': current_equipment})


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


def equipment_detail(request, pk):
    equipment = get_object_or_404(Equipment, pk=pk)
    return render(request, 'checkouts/detail-equipment.html', context={'equipment': equipment})


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




