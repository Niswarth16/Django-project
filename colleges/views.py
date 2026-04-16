from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import CreateView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.utils import timezone
from datetime import date
from .models import CollegeProfile, Attendance, Mark
from students.models import StudentProfile
from courses.models import Course
from .forms import CollegeProfileForm, AttendanceForm, MarkForm

@login_required
def dashboard_view(request):
    return redirect('core:college_dashboard')

@login_required
def students_list_view(request):
    if not request.user.is_college():
        messages.error(request, 'Access denied.')
        return redirect('core:dashboard')
    
    search_query = request.GET.get('search', '')
    students = StudentProfile.objects.all()
    
    if search_query:
        students = students.filter(
            Q(user__username__icontains=search_query) |
            Q(enrollment_number__icontains=search_query) |
            Q(user__email__icontains=search_query) |
            Q(city__icontains=search_query)
        )
    
    return render(request, 'colleges/students_list.html', {
        'students': students,
        'search_query': search_query
    })

@login_required
def add_student_view(request):
    if not request.user.is_college():
        messages.error(request, 'Access denied.')
        return redirect('core:dashboard')
    
    if request.method == 'POST':
        # For now, just show a message
        messages.success(request, 'Student addition functionality will be implemented.')
        return redirect('colleges:students_list')
    
    return render(request, 'colleges/add_student.html')

@login_required
def edit_student_view(request, pk):
    if not request.user.is_college():
        messages.error(request, 'Access denied.')
        return redirect('core:dashboard')
    
    student = get_object_or_404(StudentProfile, pk=pk)
    
    if request.method == 'POST':
        # For now, just show a message
        messages.success(request, 'Student edit functionality will be implemented.')
        return redirect('colleges:students_list')
    
    return render(request, 'colleges/edit_student.html', {'student': student})

@login_required
def courses_manage_view(request):
    if not request.user.is_college():
        messages.error(request, 'Access denied.')
        return redirect('core:dashboard')
    
    courses = Course.objects.all()
    return render(request, 'colleges/courses_manage.html', {'courses': courses})

class CollegeProfileView(LoginRequiredMixin, UpdateView):
    model = CollegeProfile
    form_class = CollegeProfileForm
    template_name = 'colleges/profile.html'
    success_url = reverse_lazy('colleges:profile')
    
    def get_object(self):
        profile, created = CollegeProfile.objects.get_or_create(user=self.request.user)
        return profile
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'College profile updated successfully!')
        return response

@login_required
def attendance_view(request):
    if not request.user.is_college():
        messages.error(request, 'Access denied. Only teachers can mark attendance.')
        return redirect('core:dashboard')
    
    if request.method == 'POST':
        form = AttendanceForm(request.POST)
        if form.is_valid():
            try:
                attendance = form.save(commit=False)
                attendance.teacher = request.user
                attendance.save()
                messages.success(request, f'Attendance marked for {attendance.student.user.username}')
                return redirect('colleges:attendance')
            except Exception as e:
                messages.error(request, f'Error marking attendance: {str(e)}')
    else:
        form = AttendanceForm(initial={'date': date.today()})
    
    # Get today's attendance
    today_attendance = Attendance.objects.filter(
        teacher=request.user,
        date=date.today()
    ).select_related('student', 'student__user')
    
    # Calculate attendance counts
    present_count = today_attendance.filter(status='present').count()
    absent_count = today_attendance.filter(status='absent').count()
    late_count = today_attendance.filter(status='late').count()
    
    return render(request, 'colleges/attendance.html', {
        'form': form,
        'today_attendance': today_attendance,
        'present_count': present_count,
        'absent_count': absent_count,
        'late_count': late_count
    })

@login_required
def marks_view(request):
    if not request.user.is_college():
        messages.error(request, 'Access denied. Only teachers can manage marks.')
        return redirect('core:dashboard')
    
    if request.method == 'POST':
        form = MarkForm(request.POST)
        if form.is_valid():
            try:
                mark = form.save(commit=False)
                mark.teacher = request.user
                mark.save()
                messages.success(request, f'Marks added for {mark.student.user.username} in {mark.course.name}')
                return redirect('colleges:marks')
            except Exception as e:
                messages.error(request, f'Error adding marks: {str(e)}')
    else:
        form = MarkForm()
    
    # Get all marks for counting
    all_marks = Mark.objects.filter(
        teacher=request.user
    ).select_related('student', 'student__user', 'course').order_by('-created_at')
    
    # Calculate grade counts
    a_plus_count = all_marks.filter(grade='A+').count()
    a_count = all_marks.filter(grade='A').count()
    b_plus_count = all_marks.filter(grade='B+').count()
    b_count = all_marks.filter(grade='B').count()
    b_total = b_plus_count + b_count
    c_count = all_marks.filter(grade='C').count()
    
    # Get recent marks (slice after counting)
    recent_marks = all_marks[:10]
    
    return render(request, 'colleges/marks.html', {
        'form': form,
        'recent_marks': recent_marks,
        'a_plus_count': a_plus_count,
        'a_count': a_count,
        'b_count': b_total,
        'c_count': c_count
    })
