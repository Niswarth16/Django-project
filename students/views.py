from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import CreateView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import StudentProfile, Result, Certificate
from courses.models import Course, Enrollment
from .forms import StudentProfileForm
from django.db.models import Q
from django.contrib.auth import get_user_model
from .forms import TeacherStudentRegistrationForm

User = get_user_model()

class StudentRegistrationView(LoginRequiredMixin, CreateView):
    model = StudentProfile
    form_class = StudentProfileForm
    template_name = 'students/register.html'
    success_url = reverse_lazy('students:profile')
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        response = super().form_valid(form)
        messages.success(self.request, 'Student profile created successfully!')
        return response

@login_required
def profile_view(request):
    try:
        profile = request.user.studentprofile
    except StudentProfile.DoesNotExist:
        return redirect('students:register')
    
    return render(request, 'students/profile.html', {'profile': profile})

@login_required
def results_view(request):
    try:
        profile = request.user.studentprofile
        results = Result.objects.filter(student=profile).order_by('-created_at')
    except StudentProfile.DoesNotExist:
        results = []
    
    return render(request, 'students/results.html', {'results': results})

@login_required
def certificates_view(request):
    try:
        profile = request.user.studentprofile
        certificates = Certificate.objects.filter(student=profile).order_by('-created_at')
    except StudentProfile.DoesNotExist:
        certificates = []
    
    return render(request, 'students/certificates.html', {'certificates': certificates})

@login_required
def courses_view(request):
    try:
        profile = request.user.studentprofile
        enrollments = Enrollment.objects.filter(student=profile).select_related('course')
        available_courses = Course.objects.filter(is_active=True)
    except StudentProfile.DoesNotExist:
        enrollments = []
        available_courses = Course.objects.filter(is_active=True)
    
    return render(request, 'students/courses.html', {
        'enrollments': enrollments,
        'available_courses': available_courses
    })

@login_required
def students_list_view(request):
    if not request.user.is_admin_user() and not request.user.is_college():
        messages.error(request, 'Access denied.')
        return redirect('core:dashboard')
    
    search_query = request.GET.get('search', '')
    students = StudentProfile.objects.all()
    
    if search_query:
        students = students.filter(
            Q(user__username__icontains=search_query) |
            Q(enrollment_number__icontains=search_query)
        )
    
    # Calculate statistics
    approved_count = students.filter(user__is_approved=True).count()
    pending_count = students.filter(user__is_approved=False).count()
    
    return render(request, 'students/students_list.html', {
        'students': students,
        'search_query': search_query,
        'approved_count': approved_count,
        'pending_count': pending_count
    })

@login_required
def teacher_student_registration(request):
    if not request.user.is_college():
        messages.error(request, 'Access denied. Only teachers can register students.')
        return redirect('core:dashboard')
    
    if request.method == 'POST':
        form = TeacherStudentRegistrationForm(request.POST)
        if form.is_valid():
            try:
                # Create user account
                user = User.objects.create_user(
                    username=form.cleaned_data['username'],
                    password=form.cleaned_data['password'],
                    user_type='student',
                    is_approved=False  # Pending admin approval
                )
                
                # Create student profile
                student_profile = StudentProfile.objects.create(
                    user=user,
                    enrollment_number=form.cleaned_data['enrollment_number'],
                    date_of_birth=form.cleaned_data['date_of_birth'],
                    gender=form.cleaned_data['gender']
                )
                
                messages.success(request, f'Student "{user.username}" registered successfully! The account is pending admin approval.')
                return redirect('colleges:dashboard')
                
            except Exception as e:
                messages.error(request, f'Error creating student: {str(e)}')
    else:
        form = TeacherStudentRegistrationForm()
    
    return render(request, 'students/teacher_student_registration.html', {'form': form})
