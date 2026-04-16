from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from accounts.models import User
from students.models import StudentProfile, Result
from colleges.models import CollegeProfile
from courses.models import Course, Enrollment

def home(request):
    return render(request, 'core/home.html')

@login_required
def dashboard(request):
    user = request.user
    
    if user.is_admin_user():
        return admin_dashboard(request)
    elif user.is_college():
        return college_dashboard(request)
    else:
        return student_dashboard(request)

@login_required
def admin_dashboard(request):
    total_students = StudentProfile.objects.count()
    approved_students = StudentProfile.objects.filter(user__is_approved=True).count()
    total_colleges = CollegeProfile.objects.count()
    total_courses = Course.objects.count()
    pending_users = User.objects.filter(is_approved=False).count()
    
    context = {
        'total_students': total_students,
        'approved_students': approved_students,
        'total_colleges': total_colleges,
        'total_courses': total_courses,
        'pending_users': pending_users,
        'recent_users': User.objects.order_by('-created_at')[:5],
    }
    return render(request, 'core/admin_dashboard.html', context)

@login_required
def college_dashboard(request):
    try:
        college_profile = request.user.collegeprofile
    except:
        college_profile = None
    
    total_students = StudentProfile.objects.count()
    total_courses = Course.objects.count()
    active_enrollments = Enrollment.objects.filter(status='approved').count()
    
    context = {
        'college_profile': college_profile,
        'total_students': total_students,
        'total_courses': total_courses,
        'active_enrollments': active_enrollments,
        'recent_students': StudentProfile.objects.order_by('-user__created_at')[:5],
    }
    return render(request, 'core/college_dashboard.html', context)

@login_required
def student_dashboard(request):
    try:
        student_profile = request.user.studentprofile
        enrollments = Enrollment.objects.filter(student=student_profile)
        results = Result.objects.filter(student=student_profile)
        
        context = {
            'student_profile': student_profile,
            'enrollments': enrollments,
            'results': results,
            'total_courses': enrollments.count(),
            'completed_courses': enrollments.filter(status='completed').count(),
        }
    except:
        context = {
            'student_profile': None,
            'enrollments': [],
            'results': [],
            'total_courses': 0,
            'completed_courses': 0,
        }
    
    return render(request, 'core/student_dashboard.html', context)
