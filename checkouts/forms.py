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
        self.fields["equipment_to_lend"].queryset = Equipment.objects.filter(availability=True)

    class Meta:
        model = Checkout
        fields = ['student', 'equipment_to_lend', 'borrow_date', 'due_date']

        widgets = {
            'equipment_to_lend': Select2MultipleWidget(),
        }

        labels = {
            'equipment_to_lend': 'Equipment',
        }




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

