from django.urls import path
from . import views_admin

app_name = 'admin'

urlpatterns = [
    path('add-teacher/', views_admin.admin_add_teacher, name='add_teacher'),
    path('add-student/', views_admin.admin_add_student, name='add_student'),
    path('student-requests/', views_admin.StudentRequestListView.as_view(), name='student_requests'),
    path('approve-student/<int:user_id>/', views_admin.approve_student_request, name='approve_student'),
    path('reject-student/<int:user_id>/', views_admin.reject_student_request, name='reject_student'),
]
