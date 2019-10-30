from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404, loader

from .forms import NewCheckoutForm, EquipmentReturnForm
from .models import Student, Equipment, Checkout

from datetime import datetime

# CHECKOUT VIEWS
def index(request):
    all_checkouts = Checkout.objects.order_by('-due_date')
    # equipment = Checkout.equipment_to_lend
    today = datetime.today()
    template = loader.get_template('checkouts/all-checkouts.html')
    context = {
        'all_checkouts': all_checkouts,
        'today': today
    }
    return HttpResponse(template.render(context, request))


def new(request):
    if request.method == 'POST':
        form = NewCheckoutForm(request.POST)
        if form.is_valid():
            # WORKING:
            new_checkout = form.save()
            selected_equipment = form.cleaned_data.get('equipment_to_lend')

            def add_equipment(selected_equipment):
                checkout_student = form.cleaned_data['student']
                selected_equipment.update(current_user=checkout_student)
                selected_equipment.update(availability=False)

                for equipment in selected_equipment:
                    new_checkout.equipment_to_lend.add(equipment)
                    checkout_student.current_equipment.add(equipment)

            add_equipment(selected_equipment)
            new_checkout.save()
            return redirect('complete', pk=new_checkout.pk)
    else:
        form = NewCheckoutForm()

    return render(request, 'checkouts/new.html', {'form': form})


def complete(request, pk):
    checkout = get_object_or_404(Checkout, pk=pk)
    equipment = checkout.equipment_to_lend.all()
    return render(request, 'checkouts/complete.html', context={'checkout': checkout, 'equipment': equipment})


# EQUIPMENT RETURN VIEWS
# def show_equipment_return(request):
#     all_checkouts = Checkout.objects.order_by('-due_date')
#     if request.method == 'POST':
#         form = EquipmentReturnForm(data=request.POST)
#         if form.is_valid():
#             form.save()
#         else:
#             form = EquipmentReturnForm()
#         context = RequestContext(request)
#         return render_to_response('checkouts/equipment-return.html', {
#             'form': form,
#             'all_checkouts': all_checkouts,
#         }, RequestContext(request))


# WORKING BUT NEEDS ERRORS
def equipment_return(request):
    all_checkouts = Checkout.objects.order_by('-due_date')

    if request.method == 'POST':
        form = EquipmentReturnForm()
        if form.is_valid:
            # all_checkouts = Checkout.objects.order_by('-due_date')
            checkout_id = int(request.POST.get('checkout_id'))
            checkout = Checkout.objects.get(id=checkout_id)
            checkout.completed = True
            checkout.delete()
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
def all_students(request):
    all_students = Student.objects.order_by('last_name')
    template = loader.get_template('checkouts/all-students.html')
    context = {'all_students': all_students}
    return HttpResponse(template.render(context, request))

def student_detail(request, school_id):
    student = get_object_or_404(Student, school_id=school_id)
    current_equipment = student.current_equipment.all()
    return render(request, 'checkouts/student-detail.html', context={'student': student, 'current_equipment': current_equipment})


# EQUIPMENT VIEWS
def all_equipment(request):
    all_equipment = Equipment.objects.all()
    template = loader.get_template('checkouts/all-equipment.html')
    context = {'all_equipment': all_equipment}
    return HttpResponse(template.render(context, request))

def equipment_detail(request, pk):
    equipment = get_object_or_404(Equipment, pk=pk)
    return render(request, 'checkouts/equipment-detail.html', context={'equipment': equipment})