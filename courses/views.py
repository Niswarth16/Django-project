from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import ListView, DetailView
from .models import Course, Enrollment
from students.models import StudentProfile

class CourseListView(ListView):
    model = Course
    template_name = 'courses/list.html'
    context_object_name = 'courses'
    paginate_by = 12
    
    def get_queryset(self):
        return Course.objects.filter(is_active=True).order_by('name')

class CourseDetailView(DetailView):
    model = Course
    template_name = 'courses/detail.html'
    context_object_name = 'course'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated and self.request.user.is_student():
            try:
                student_profile = self.request.user.studentprofile
                context['is_enrolled'] = Enrollment.objects.filter(
                    student=student_profile, 
                    course=self.object
                ).exists()
            except StudentProfile.DoesNotExist:
                context['is_enrolled'] = False
        else:
            context['is_enrolled'] = False
        return context

@login_required
def enroll_view(request, pk):
    if not request.user.is_student():
        messages.error(request, 'Only students can enroll in courses.')
        return redirect('courses:list')
    
    course = get_object_or_404(Course, pk=pk)
    
    try:
        student_profile = request.user.studentprofile
    except StudentProfile.DoesNotExist:
        messages.error(request, 'Please complete your student profile first.')
        return redirect('students:register')
    
    # Check if already enrolled
    if Enrollment.objects.filter(student=student_profile, course=course).exists():
        messages.warning(request, 'You are already enrolled in this course.')
        return redirect('courses:detail', pk=pk)
    
    # Create enrollment
    Enrollment.objects.create(
        student=student_profile,
        course=course,
        status='pending'
    )
    
    messages.success(request, f'You have successfully enrolled in {course.name}. Your enrollment is pending approval.')
    return redirect('courses:detail', pk=pk)
