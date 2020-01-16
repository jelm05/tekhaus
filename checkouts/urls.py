from django.conf.urls import url, include
from django.urls import path

from . import views

urlpatterns = [

    # All these are prepended with /checkouts/because of settings.py urlpatterns
    # Need to add a baseline url

    path('', views.dashboard, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),

    path('checkouts/', views.all_checkouts, name='all_checkouts'),
    path('checkout/new/', views.new_checkout, name='new'),
    path('checkout/return/', views.equipment_return, name='equipment_return'),
    path('checkout/<int:pk>/', views.checkout_detail, name='checkout_detail'),
    path('checkout/<int:pk>/complete/', views.complete, name='complete'),
    path('checkouts/past/', views.past_checkouts, name='past_checkouts'),

    path('students/', views.all_students, name='all_students'),
    path('student/<int:school_id>/', views.student_detail, name='student_detail'),
    path('student/<int:school_id>/edit/', views.edit_student, name='edit_student'),
    path('student/<int:school_id>/delete/', views.delete_student, name='delete_student'),

    path('equipment/', views.all_equipment, name='all_equipment'),
    path('equipment/<int:pk>/', views.equipment_detail, name='equipment_detail'),
    path('equipment/<int:pk>/edit/', views.edit_equipment, name='edit_equipment'),
    path('equipment/<int:pk>/delete/', views.delete_equipment, name='delete_equipment'),

    path('add/equipment/', views.add_new_equipment, name='add_new_equipment'),
    path('add/student/', views.add_new_student, name='add_new_student'),


    url(r'^select2/', include('django_select2.urls')),
]