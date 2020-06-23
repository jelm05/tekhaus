from django import forms
from datetime import datetime

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from .models import Student, Equipment, Checkout, Reservation
# from .models import Equipment
# from .models import Checkout

from django_select2.forms import (ModelSelect2Widget, Select2Widget, Select2MultipleWidget)
from checkouts.mixins import ReadOnlyFieldsMixin


class NewCheckoutForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        # self.user = kwargs.pop('user', None)

        super(NewCheckoutForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

        # self.fields["processed_by"] = self.user
        self.fields["cameras"].queryset = Equipment.objects.filter(category='camera', availability=True)
        self.fields["lights"].queryset = Equipment.objects.filter(category='light', availability=True)
        self.fields["computers"].queryset = Equipment.objects.filter(category='computer', availability=True)
        self.fields["projectors"].queryset = Equipment.objects.filter(category='projector', availability=True)
        self.fields["audio"].queryset = Equipment.objects.filter(category='audio', availability=True)
        self.fields["misc"].queryset = Equipment.objects.filter(category='misc', availability=True)
        # self.fields["borrow_date"].widget.attrs.update({'data-provide': 'datepicker'})
        # self.fields["due_date"].widget.attrs.update({'data-provide': 'datepicker'})
        self.fields["borrow_date"].widget.attrs.update({'class': 'form-control datepicker'})
        self.fields["due_date"].widget.attrs.update({'class': 'form-control datepicker'})

    class Meta:
        model = Checkout
        exclude = ['processed_by']
        fields = ['student', 'cameras', 'lights', 'computers', 'projectors', 'audio', 'misc', 'borrow_date', 'due_date', 'notes']

        widgets = {
            # 'processed_by': forms.TextInput(attrs={'disabled': True}),
            'student': Select2Widget(),
            'cameras': Select2MultipleWidget(),
            'lights': Select2MultipleWidget(),
            'computers': Select2MultipleWidget(),
            'projectors': Select2MultipleWidget(),
            'audio': Select2MultipleWidget(),
            'misc': Select2MultipleWidget(),
            # 'borrow_date': DateInput(format='%m/%d/%Y'),
            # 'due_date': DateInput(format='%m/%d/%Y'),
            'borrow_date': forms.DateInput(format='%m/%d/%Y'),
            'due_date': forms.DateInput(format='%m/%d/%Y'),
        }

        labels = {
            'cameras': 'Cameras',
        }


class ReturnCheckoutForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ReturnCheckoutForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    confirmation = forms.BooleanField(required=True)

    class Meta:
        model = Checkout
        exclude = ['student', 'processed_by', 'cameras', 'lights', 'computers', 'projectors', 'audio', 'misc', 'borrow_date', 'due_date', 'return_date', 'completed']
        fields = ['notes', 'confirmation']

        labels = {
            'notes': 'Return Notes'
        }


class ReservationStartForm(forms.Form):
    search = forms.IntegerField()

    def __init__(self, *args, **kwargs):
        super(ReservationStartForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class NewReservationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(NewReservationForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

        # self.fields["requested_by"].queryset = Student.objects.filter(school_id=8910)
        # self.fields["requested_by"].widget.attrs['disabled'] = True
        self.fields["cameras"].queryset = Equipment.objects.filter(category='camera', availability=True, reservation_request=None)
        self.fields["lights"].queryset = Equipment.objects.filter(category='light', availability=True, reservation_request=None)
        self.fields["computers"].queryset = Equipment.objects.filter(category='computer', availability=True, reservation_request=None)
        self.fields["projectors"].queryset = Equipment.objects.filter(category='projector', availability=True, reservation_request=None)
        self.fields["audio"].queryset = Equipment.objects.filter(category='audio', availability=True, reservation_request=None)
        self.fields["misc"].queryset = Equipment.objects.filter(category='misc', availability=True, reservation_request=None)
        self.fields["request_date"].widget.attrs.update({'class': 'form-control datepicker'})
        self.fields["due_date"].widget.attrs.update({'class': 'form-control datepicker'})

    class Meta:
        model = Reservation
        exclude = ['accepted', 'completed']
        fields = ['cameras', 'lights', 'computers', 'projectors', 'audio', 'misc', 'request_date', 'due_date', 'notes']

        widgets = {
            'cameras': Select2MultipleWidget(),
            'lights': Select2MultipleWidget(),
            'computers': Select2MultipleWidget(),
            'projectors': Select2MultipleWidget(),
            'audio': Select2MultipleWidget(),
            'misc': Select2MultipleWidget(),
            'request_date': forms.DateInput(format='%m/%d/%Y'),
            'due_date': forms.DateInput(format='%m/%d/%Y'),
        }


class NewCheckoutFromReservation(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(NewCheckoutFromReservation, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

        self.fields["borrow_date"].widget.attrs.update({'class': 'form-control datepicker'})
        self.fields["due_date"].widget.attrs.update({'class': 'form-control datepicker'})

    class Meta:
        model = Checkout
        exclude = ['processed_by']
        fields = ['student', 'cameras', 'lights', 'computers', 'projectors', 'audio', 'misc', 'borrow_date', 'due_date', 'notes']

        widgets = {
            'student': Select2Widget(),
            'cameras': Select2MultipleWidget(),
            'lights': Select2MultipleWidget(),
            'computers': Select2MultipleWidget(),
            'projectors': Select2MultipleWidget(),
            'audio': Select2MultipleWidget(),
            'misc': Select2MultipleWidget(),
            'borrow_date': forms.DateInput(format='%m/%d/%Y'),
            'due_date': forms.DateInput(format='%m/%d/%Y'),
        }

        labels = {
            'cameras': 'Cameras',
        }


class AcceptOrDenyReservation(forms.ModelForm):
    # def __init__(self, *args, **kwargs):
    #     super(AcceptOrDenyReservation, self).__init__(*args, **kwargs)
    #     for visible in self.visible_fields():
    #         visible.field.widget.attrs['class'] = 'form-control'

    confirmation = forms.BooleanField(required=True)

    class Meta:
        model = Reservation
        exclude = ['requested_by', 'cameras', 'lights', 'computers', 'projectors', 'audio', 'misc', 'request_date', 'due_date', 'notes', 'accepted', 'completed']
        fields = ['confirmation']

        labels = {
            'confirmation': 'Confirmation'
        }


class AddNewEquipmentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AddNewEquipmentForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Equipment
        exclude = ['availability', 'current_user', 'past_checkouts']
        fields = ['name', 'category', 'serial_num', 'desc', 'details']


class AddNewStudentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AddNewStudentForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Student
        exclude = ['current_equipment', 'past_equipment']
        fields = ['school_id', 'first_name', 'last_name', 'primary_email', 'secondary_email', 'grad_year', 'active']


class AddNewAdminAccount(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(AddNewAdminAccount, self).__init__(*args, **kwargs)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']


class EditAdminAccount(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(EditAdminAccount, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = User
        exclude = ['password1', 'password2']
        fields = ['username', 'first_name', 'last_name', 'email']



