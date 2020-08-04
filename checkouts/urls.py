from django.conf.urls import url, include
from django.urls import path

from django.contrib.auth import views as auth_views


from . import views


urlpatterns = [

    # All these are prepended with /checkouts/because of settings.py urlpatterns
    # Need to add a baseline url

    # url(r'^admin/', admin.site.urls),
    # url(r'^login/$', auth_views.login),
    # url(r'^logout/$', auth_views.logout),
    # url(r'^', include('mysite.urls')),
    # url('^', include('django.contrib.auth.urls')),


    path('', views.dashboard, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),

    path('accounts/', include('django.contrib.auth.urls')),
    path('account/password_change/', auth_views.PasswordChangeView.as_view(
        template_name='registration/password-change.html'), name='password_change'
    ),
    path('account/password_change/complete/', auth_views.PasswordChangeDoneView.as_view(
        template_name='registration/password-change-done.html'), name='password_change_done'
    ),

    path('password/reset/', auth_views.PasswordResetView.as_view(
        template_name='registration/password-reset.html',
        html_email_template_name='registration/password_reset_html_email.html',
        email_template_name='registration/password_reset_email.txt',
        subject_template_name='registration/password_reset_subject.txt',), name='password_reset'),
    path('password/reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='registration/password-reset-done.html'), name='password_reset_done'),
    path('password/reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='registration/password-reset-confirm.html'), name='password_reset_confirm'),
    path('password/reset/complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='registration/password-reset-complete.html'), name='password_reset_complete'),


    path('account/', views.admin_account, name='admin_account'),
    path('account/<int:pk>/edit/', views.edit_admin_account, name='edit_admin_account'),
    path('account/<int:pk>/details/', views.admin_account_detail, name='admin_account_details'),

    path('calendar/', views.calendar, name='calendar'),

    path('checkouts/', views.all_checkouts, name='all_checkouts'),
    path('checkout/new/', views.new_checkout, name='new_checkout'),
    path('checkout/return/list/', views.return_list_checkouts, name='return_list_checkouts'),
    path('checkout/return/<int:pk>/', views.return_checkout, name='return_checkout'),
    path('checkout/return/<int:pk>/complete/', views.complete_checkout_return, name='complete_checkout_return'),
    path('checkout/<int:pk>/', views.checkout_detail, name='checkout_detail'),
    path('checkout/<int:pk>/complete/', views.complete_checkout, name='complete_checkout'),
    path('checkout/<int:pk>/pdf/', views.completed_checkout_pdf, name='completed_checkout_pdf'),
    path('checkouts/past/', views.past_checkouts, name='past_checkouts'),

    path('users/', views.all_students, name='all_students'),
    path('user/<int:school_id>/', views.student_detail, name='student_detail'),
    path('user/<int:school_id>/edit/', views.edit_student, name='edit_student'),
    path('user/<int:school_id>/delete/', views.delete_student, name='delete_student'),

    path('equipment/', views.all_equipment, name='all_equipment'),
    path('equipment/<int:pk>/', views.equipment_detail, name='equipment_detail'),
    path('equipment/<int:pk>/edit/', views.edit_equipment, name='edit_equipment'),
    path('equipment/<int:pk>/delete/', views.delete_equipment, name='delete_equipment'),

    path('add/equipment/', views.add_new_equipment, name='add_new_equipment'),
    path('add/user/', views.add_new_student, name='add_new_student'),
    path('add/admin/', views.add_new_admin, name='add_new_admin'),

    path('reservation/', views.start_reservation, name='start_reservation'),
    path('reservation/<int:pk>/', views.reservation_detail, name='reservation_detail'),
    path('reservation/<int:pk>/new/', views.new_reservation, name='new_reservation'),
    path('reservation/<int:pk>/complete/', views.complete_reservation, name='complete_reservation'),
    path('reservation/<int:pk>/pdf/', views.completed_reservation_pdf, name='completed_reservation_pdf'),
    path('reservations/pending/', views.pending_reservations, name='pending_reservations'),
    path('reservation/<int:pk>/checkout/new/', views.reservation_checkout, name='reservation_checkout'),
    path('reservations/accepted/', views.accepted_reservations, name='accepted_reservations'),
    path('reservations/<int:pk>/accept/', views.accept_pending_reservation, name='accept_pending_reservation'),
    path('reservations/<int:pk>/deny/', views.deny_pending_reservation, name='deny_pending_reservation'),
    path('reservations/<int:pk>/mark/complete/', views.mark_complete_reservation, name='mark_complete_reservation'),
    path('reservations/past/', views.past_reservations, name='past_reservations'),

    # path('search/', views.search, name='search'),
    # url(r'^search_users/$', views.search_users, name='search_users'),

    # url(r'^pdf/$', views.completed_checkout_pdf, name='completed_checkout_pdf'),
    url(r'^ajax_calls/search/', views.autocompleteSearch),
    url(r'^select2/', include('django_select2.urls')),
]
