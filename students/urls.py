from django.urls import path
from . import views

app_name = 'students'

urlpatterns = [
    path('register/', views.StudentRegistrationView.as_view(), name='register'),
    path('profile/', views.profile_view, name='profile'),
    path('results/', views.results_view, name='results'),
    path('certificates/', views.certificates_view, name='certificates'),
    path('courses/', views.courses_view, name='courses'),
    path('teacher-register/', views.teacher_student_registration, name='teacher_register'),
    path('', views.students_list_view, name='students_list'),
]
