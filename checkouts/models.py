from django.db import models
from datetime import datetime, date

from django.contrib.auth.models import User


class Student(models.Model):
    school_id = models.IntegerField(verbose_name='School ID')
    first_name = models.CharField(max_length=100, verbose_name='First Name')
    last_name = models.CharField(max_length=100, verbose_name='Last Name')
    primary_email = models.EmailField(max_length=100, verbose_name='Primary Email')
    secondary_email = models.EmailField(max_length=100, verbose_name='Secondary Email', blank=True)
    grad_year = models.IntegerField(verbose_name='Expected Graduation Year')
    active = models.BooleanField(default=True, verbose_name='Active')
    current_equipment = models.ManyToManyField('Equipment', related_name='current_equipment', blank=True)
    past_equipment = models.ManyToManyField('Equipment', related_name='past_equipment', blank=True)
    reservation_request = models.ForeignKey('Reservation', null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        # return "%s %s" % (self.first_name, self.last_name)
        return "{} {}".format(self.first_name, self.last_name)

    class Meta:
        verbose_name = 'Student'
        verbose_name_plural = 'Students'


class Equipment(models.Model):
    name = models.CharField(max_length=100)
    CATEGORIES = [
        ('camera', 'Camera'),
        ('light', 'Light'),
        ('computer', 'Computer'),
        ('projector', 'Projector'),
        ('audio', 'Audio'),
        ('misc', 'Miscellaneous'),
    ]
    category = models.CharField(choices=CATEGORIES, max_length=10)
    desc = models.CharField(max_length=255, verbose_name='Description')
    details = models.CharField(max_length=255, verbose_name='Additional Details')
    serial_num = models.CharField(max_length=50, verbose_name='Serial Number')
    availability = models.BooleanField(default=True, verbose_name='Available?')
    current_user = models.ForeignKey(Student, null=True, blank=True, on_delete=models.CASCADE)
    past_checkouts = models.ManyToManyField('Checkout', related_name='past_checkouts', blank=True)
    reservation_request = models.ForeignKey('Reservation', null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return "{}".format(self.name)

    class Meta:
        verbose_name = 'Equipment'
        verbose_name_plural = 'Equipment'


class Checkout(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    processed_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    cameras = models.ManyToManyField(
        'Equipment',
        limit_choices_to={'category': 'camera'},
        related_name='cameras',
        blank=True)
    lights = models.ManyToManyField(
        'Equipment',
        limit_choices_to={'category': 'light'},
        related_name='lights',
        blank=True)
    computers = models.ManyToManyField(
        'Equipment',
        limit_choices_to={'category': 'computer'},
        related_name='computers',
        blank=True)
    projectors = models.ManyToManyField(
        'Equipment',
        limit_choices_to={'category': 'projector'},
        related_name='projectors',
        blank=True)
    audio = models.ManyToManyField(
        'Equipment',
        limit_choices_to={'category': 'audio'},
        related_name='audio',
        blank=True)
    misc = models.ManyToManyField(
        'Equipment',
        limit_choices_to={'category': 'misc'},
        related_name='miscellaneous',
        blank=True)
    borrow_date = models.DateField(null=False, blank=False, default=datetime.today, verbose_name='Date Borrowed')
    due_date = models.DateField(null=False, blank=False, default=datetime.today, verbose_name='Due Date')
    return_date = models.DateField(null=True, blank=True, verbose_name='Date Returned')
    completed = models.BooleanField(default=False)
    notes = models.TextField(null=True, blank=True, verbose_name='Checkout Notes')

    @property
    def is_past_due(self):
        return date.today() > self.due_date

    def __str__(self):
        return "Checkout #{}".format(self.id)


class Reservation(models.Model):
    requested_by = models.ForeignKey(Student, on_delete=models.CASCADE)
    cameras = models.ManyToManyField(
        'Equipment',
        limit_choices_to={'category': 'camera'},
        related_name='reservation_cameras',
        blank=True)
    lights = models.ManyToManyField(
        'Equipment',
        limit_choices_to={'category': 'light'},
        related_name='reservation_lights',
        blank=True)
    computers = models.ManyToManyField(
        'Equipment',
        limit_choices_to={'category': 'computer'},
        related_name='reservation_computers',
        blank=True)
    projectors = models.ManyToManyField(
        'Equipment',
        limit_choices_to={'category': 'projector'},
        related_name='reservation_projectors',
        blank=True)
    audio = models.ManyToManyField(
        'Equipment',
        limit_choices_to={'category': 'audio'},
        related_name='reservation_audio',
        blank=True)
    misc = models.ManyToManyField(
        'Equipment',
        limit_choices_to={'category': 'misc'},
        related_name='reservation_miscellaneous',
        blank=True)
    request_date = models.DateField(null=False, blank=False, default=datetime.today, verbose_name='Request Date')
    due_date = models.DateField(null=False, blank=False, default=datetime.today, verbose_name='Due Date')
    notes = models.TextField(null=True, blank=True, verbose_name='Reservation Notes')
    accepted = models.BooleanField(default=False)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return "Reservation #{}".format(self.id)

