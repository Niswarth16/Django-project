from django.urls import path
from . import views

app_name = 'colleges'

urlpatterns = [
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('students/', views.students_list_view, name='students_list'),
    path('students/add/', views.add_student_view, name='add_student'),
    path('students/<int:pk>/edit/', views.edit_student_view, name='edit_student'),
    path('courses/', views.courses_manage_view, name='courses_manage'),
    path('attendance/', views.attendance_view, name='attendance'),
    path('marks/', views.marks_view, name='marks'),
    path('profile/', views.CollegeProfileView.as_view(), name='profile'),
]
