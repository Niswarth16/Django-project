from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.db.models import Q
from accounts.models import User
from students.models import StudentProfile
from colleges.models import CollegeProfile
from accounts.forms_admin import AdminTeacherRegistrationForm, AdminStudentRegistrationForm
from datetime import date

User = get_user_model()

@login_required
def admin_add_teacher(request):
    if not request.user.is_admin_user():
        messages.error(request, 'Access denied. Only admin users can add teachers.')
        return redirect('/admin-dashboard/')
    
    if request.method == 'POST':
        form = AdminTeacherRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                # Create user account
                user = User.objects.create_user(
                    username=form.cleaned_data['username'],
                    email=form.cleaned_data['email'],
                    password=form.cleaned_data['password'],
                    user_type='college',
                    is_approved=True  # Admin can directly approve
                )
                
                # Create institute profile
                institute_profile = CollegeProfile.objects.create(
                    user=user,
                    phone=form.cleaned_data['phone'],
                    email=form.cleaned_data['email']
                )
                
                messages.success(request, f'Teacher "{user.username}" has been registered successfully!')
                return redirect('/admin-dashboard/')
                
            except Exception as e:
                messages.error(request, f'Error creating teacher: {str(e)}')
    else:
        form = AdminTeacherRegistrationForm()
    
    return render(request, 'admin/add_teacher.html', {'form': form})

@login_required
def admin_add_student(request):
    if not request.user.is_admin_user():
        messages.error(request, 'Access denied. Only admin users can add students.')
        return redirect('/admin-dashboard/')
    
    if request.method == 'POST':
        form = AdminStudentRegistrationForm(request.POST)
        if form.is_valid():
            try:
                # Create user account
                user = User.objects.create_user(
                    username=form.cleaned_data['username'],
                    password=form.cleaned_data['password'],
                    user_type='student',
                    is_approved=True  # Admin can directly approve
                )
                
                # Create student profile
                student_profile = StudentProfile.objects.create(
                    user=user,
                    enrollment_number=form.cleaned_data['enrollment_number'],
                    date_of_birth=form.cleaned_data['date_of_birth'],
                    gender=form.cleaned_data['gender']
                )
                
                messages.success(request, f'Student "{user.username}" has been registered successfully!')
                return redirect('/admin-dashboard/')
                
            except Exception as e:
                messages.error(request, f'Error creating student: {str(e)}')
    else:
        form = AdminStudentRegistrationForm()
    
    return render(request, 'admin/add_student.html', {'form': form})

class StudentRequestListView(ListView):
    model = User
    template_name = 'admin/student_requests.html'
    context_object_name = 'pending_users'
    paginate_by = 10
    
    def get_queryset(self):
        return User.objects.filter(
            is_approved=False,
            user_type='student'
        ).order_by('-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Student Registration Requests'
        return context

@login_required
def approve_student_request(request, user_id):
    if not request.user.is_admin_user():
        messages.error(request, 'Access denied.')
        return redirect('/admin-panel/student-requests/')
    
    try:
        user = User.objects.get(id=user_id, user_type='student')
        user.is_approved = True
        user.save()
        messages.success(request, f'Student "{user.username}" has been approved!')
    except User.DoesNotExist:
        messages.error(request, 'Student not found.')
    
    return redirect('/admin-panel/student-requests/')

@login_required
def reject_student_request(request, user_id):
    if not request.user.is_admin_user():
        messages.error(request, 'Access denied.')
        return redirect('/admin-panel/student-requests/')
    
    try:
        user = User.objects.get(id=user_id, user_type='student')
        username = user.username
        user.delete()
        messages.warning(request, f'Student request "{username}" has been rejected and deleted.')
    except User.DoesNotExist:
        messages.error(request, 'Student not found.')
    
    return redirect('/admin-panel/student-requests/')
