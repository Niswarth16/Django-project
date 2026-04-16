from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('college-dashboard/', views.college_dashboard, name='college_dashboard'),
    path('student-dashboard/', views.student_dashboard, name='student_dashboard'),
]
