from django.conf.urls import url, include
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('new/', views.new, name='new'),
    path('return/', views.equipment_return, name='equipment_return'),
    path('<int:pk>/complete/', views.complete, name='complete'),
    path('past/', views.past_checkouts, name='past_checkouts'),

    path('students/', views.all_students, name='all_students'),
    path('student/<int:school_id>/', views.student_detail, name='student_detail'),

    path('equipment/', views.all_equipment, name='all_equipment'),
    path('equipment/<int:pk>/', views.equipment_detail, name='equipment_detail'),

    url(r'^select2/', include('django_select2.urls')),
]