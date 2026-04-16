from django.urls import path
from . import views_admin

app_name = 'admin_courses'

urlpatterns = [
    path('add-course/', views_admin.admin_add_course, name='add_course'),
    path('courses/', views_admin.AdminCourseListView.as_view(), name='courses_list'),
    path('edit-course/<int:course_id>/', views_admin.admin_edit_course, name='edit_course'),
    path('delete-course/<int:course_id>/', views_admin.admin_delete_course, name='delete_course'),
    path('toggle-course/<int:course_id>/', views_admin.admin_toggle_course_status, name='toggle_course'),
]
