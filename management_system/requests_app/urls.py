from django.urls import path
from . import views

urlpatterns = [
    path('download/<int:request_id>/', views.download_file, name='download_file'),

    path('student_dashboard/', views.student_dashboard, name='student_dashboard'),
    path('apply_od/', views.apply_od, name='apply_od'),
    path('apply_leave/', views.apply_leave, name='apply_leave'),
    path('tutor_dashboard/', views.tutor_dashboard, name='tutor_dashboard'),
    path('hod_dashboard/', views.hod_dashboard, name='hod_dashboard'),
    path('', views.user_login, name='login'),
    # Tutor actions
    path('tutor/approve_od/<int:od_id>/', views.approve_od, name='approve_od'),
    path('tutor/deny_od/<int:od_id>/', views.deny_od, name='deny_od'),
    path('tutor/approve_leave/<int:leave_id>/', views.approve_leave, name='approve_leave'),
    path('tutor/deny_leave/<int:leave_id>/', views.deny_leave, name='deny_leave'),

    # HoD actions
    path('hod/approve_od/<int:od_id>/', views.hod_approve_od, name='hod_approve_od'),
    path('hod/deny_od/<int:od_id>/', views.hod_deny_od, name='hod_deny_od'),
    path('hod/approve_leave/<int:leave_id>/', views.hod_approve_leave, name='hod_approve_leave'),
    path('hod/deny_leave/<int:leave_id>/', views.hod_deny_leave, name='hod_deny_leave'),
]
