from django.contrib import admin
from django.urls import path, include
from app import views as app_views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.urls import re_path as url 
from django.views.static import serve
from app import views
from app.forms import LoginForm, EmployeePasswordChangeForm
urlpatterns = [
    path('admin/', admin.site.urls),
    # path('change-password/', EmployeePasswordChangeView.as_view(), name='change-password'),
    path('add-employee/', views.add_employee, name='add-employee'),
    # path('add-employee-profile/', views.add_employee_profile, name='add-employee-profile'),
    path('add-project/', views.add_project, name='add-project'),
    path('add-resource/', views.add_resource, name='add-resource'),
    path('add-task/', views.add_task, name='add-task'),
    path('add-ips/', views.add_ips, name='add-ips'),
    path('task-hours-view/', views.task_hours_view, name='task-hours-view'),
    path('view-employee/', views.view_employee, name='view-employee'),
    path('employee-details/', views.employee_details, name='employee-details'),
    # path('view-employee-profile/', views.employee_profile_list, name='view-employee-profile'),
    path('view-project/', views.view_project, name='view-project'),
    path('view-task/', views.view_task, name='view-task'),
    path('view-ips/', views.view_ips, name='view-ips'),
    path('view-resource/', views.view_resource, name='view-resource'),
    path('view-ips-all/', views.view_ips_all, name='view-ips-all'),
    path('edit-employee/<int:pk>/', views.edit_employee, name='edit-employee'), 
    # path('edit-employee-profile/<int:pk>/', views.edit_employee_profile, name='edit-employee-profile'), 
    path('edit-ips/<int:pk>/', views.edit_ips, name='edit-ips'), 
    path('edit-resource/<int:pk>/', views.edit_resource, name='edit-resource'), 
    path('edit-task/<int:pk>/', views.edit_task, name='edit-task'), 
    path('edit-project/<int:pk>/', views.edit_project, name='edit-project'), 
    path('delete-employee/<int:pk>/', views.delete_employee, name='delete-employee'),
    # path('delete-employee-profile/<int:pk>/', views.delete_employee_profile, name='delete-employee-profile'),
    path('delete-ips/<int:pk>/', views.delete_ips, name='delete-ips'),
    path('delete-resource/<int:pk>/', views.delete_resource, name='delete-resource'),
    path('delete-task/<int:pk>/', views.delete_task, name='delete-task'),
    path('delete-project/<int:pk>/', views.delete_project, name='delete-project'),
    path('login/', views.employee_login, name='login'),
    path('logout/', views.employee_logout, name='logout'),
    path('', views.employee_login, name='home'),
    path('employee-profile/', views.employee_profile, name='employee-profile'),
    path('report-view/', views.report_view, name='report-view'),
    path('passwordchange/', auth_views.PasswordChangeView.as_view(template_name='app/password_change_form.html',form_class=EmployeePasswordChangeForm), name='passwordchange'),
    path('passwordchangedone/', auth_views.PasswordChangeDoneView.as_view(template_name='app/password_change_done.html'),name='password_change_done'),

    # path('checkin/', views.checkin, name='checkin'),
    # path('checkout/', views.checkout, name='checkout'),
    path('attendance-record/', views.attendance_record, name='attendance_record'),
    path('my-attendance-record/', views.my_attendance_record, name='my_attendance_record'),
    path('employee-dashboard/', views.employee_dashboard, name='employee-dashboard'),

    path('reset_password/', auth_views.PasswordResetView.as_view(template_name="app/forgotpassword.html"), name='reset_password'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name="app/password_reset_sent.html"), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="app/password_reset_confirm.html"), name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name="app/password_reset_done.html"), name='password_reset_complete'),

    url(r'^media/(?P<path>.*)$', serve,
        {'document_root': settings.MEDIA_ROOT}),
    url(r'^static/(?P<path>.*)$', serve,
        {'document_root': settings.STATIC_ROOT}),

] 