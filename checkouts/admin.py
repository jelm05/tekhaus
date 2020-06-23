from django.contrib import admin
from .models import Student, Equipment, Checkout, Reservation


admin.site.register(Student)
admin.site.register(Equipment)
admin.site.register(Checkout)
admin.site.register(Reservation)

