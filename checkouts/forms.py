from django import forms
from datetime import datetime

from .models import Student
from .models import Equipment
from .models import Checkout

from django_select2.forms import (ModelSelect2Widget, Select2Widget, Select2MultipleWidget)


class NewCheckoutForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(NewCheckoutForm, self).__init__(*args, **kwargs)
        # self.fields["equipment_to_lend"].widget = forms.widgets.ModelChoiceField()
        self.fields["cameras"].queryset = Equipment.objects.filter(category='camera', availability=True)
        self.fields["lights"].queryset = Equipment.objects.filter(category='light', availability=True)
        self.fields["computers"].queryset = Equipment.objects.filter(category='computer', availability=True)
        self.fields["projectors"].queryset = Equipment.objects.filter(category='projector', availability=True)
        self.fields["audio"].queryset = Equipment.objects.filter(category='audio', availability=True)
        self.fields["misc"].queryset = Equipment.objects.filter(category='misc', availability=True)

    class Meta:
        model = Checkout
        fields = ['student', 'cameras', 'lights', 'computers', 'projectors', 'audio', 'misc', 'borrow_date', 'due_date']

        widgets = {
            'cameras': Select2MultipleWidget(),
            'lights': Select2MultipleWidget(),
            'computers': Select2MultipleWidget(),
            'projectors': Select2MultipleWidget(),
            'audio': Select2MultipleWidget(),
            'misc': Select2MultipleWidget(),
        }

        labels = {
            'cameras': 'Cameras',
        }


class AddNewEquipmentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AddNewEquipmentForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Equipment
        exclude = ['availability', 'current_user', 'past_checkouts']
        fields = ['name', 'category', 'desc', 'details', 'serial_num']


class AddNewStudentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AddNewStudentForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Student
        exclude = ['current_equipment', 'past_equipment']
        fields = ['school_id', 'first_name', 'last_name', 'grad_year']


class EquipmentReturnForm(forms.Form):
        check_in = forms.BooleanField(required=True)


# class NewCheckoutForm(forms.Form):
#     id = forms.IntegerField(required=False, widget=forms.HiddenInput())
#     student = forms.ModelChoiceField(queryset=Student.objects.all())
#     equipment = forms.ModelMultipleChoiceField(queryset=Equipment.objects.filter(availability=True))
#     borrow_date = forms.DateField(
#         initial=datetime.now(),
#         widget=forms.DateInput(format='%m/%d/%Y'),
#         input_formats=('%m/%d/%Y', )
#         )
#     due_date = forms.DateField(
#         initial=datetime.now(),
#         widget=forms.DateInput(format='%m/%d/%Y'),
#         input_formats=('%m/%d/%Y', )
#         )

