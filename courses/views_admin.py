from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import ListView
from django.db.models import Q, Count
from .models import Course
from .forms_admin import AdminCourseForm

@login_required
def admin_add_course(request):
    if not request.user.is_admin_user():
        messages.error(request, 'Access denied. Only admin users can add courses.')
        return redirect('/admin-dashboard/')
    
    if request.method == 'POST':
        form = AdminCourseForm(request.POST)
        if form.is_valid():
            try:
                course = form.save()
                messages.success(request, f'Course "{course.name}" has been created successfully!')
                return redirect('/admin-dashboard/')
            except Exception as e:
                messages.error(request, f'Error creating course: {str(e)}')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = AdminCourseForm()
    
    return render(request, 'admin/add_course.html', {'form': form})

@login_required
def admin_edit_course(request, course_id):
    if not request.user.is_admin_user():
        messages.error(request, 'Access denied. Only admin users can edit courses.')
        return redirect('/admin-dashboard/')
    
    try:
        course = Course.objects.get(id=course_id)
    except Course.DoesNotExist:
        messages.error(request, 'Course not found.')
        return redirect('/admin-panel/courses/')
    
    if request.method == 'POST':
        form = AdminCourseForm(request.POST, instance=course)
        if form.is_valid():
            try:
                course = form.save()
                messages.success(request, f'Course "{course.name}" has been updated successfully!')
                return redirect('/admin-panel/courses/')
            except Exception as e:
                messages.error(request, f'Error updating course: {str(e)}')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = AdminCourseForm(instance=course)
    
    return render(request, 'admin/edit_course.html', {'form': form, 'course': course})

@login_required
def admin_delete_course(request, course_id):
    if not request.user.is_admin_user():
        messages.error(request, 'Access denied. Only admin users can delete courses.')
        return redirect('/admin-panel/courses/')
    
    try:
        course = Course.objects.get(id=course_id)
        course_name = course.name
        course.delete()
        messages.success(request, f'Course "{course_name}" has been deleted successfully!')
    except Course.DoesNotExist:
        messages.error(request, 'Course not found.')
    except Exception as e:
        messages.error(request, f'Error deleting course: {str(e)}')
    
    return redirect('/admin-panel/courses/')

@login_required
def admin_toggle_course_status(request, course_id):
    if not request.user.is_admin_user():
        messages.error(request, 'Access denied. Only admin users can manage courses.')
        return redirect('/admin-panel/courses/')
    
    try:
        course = Course.objects.get(id=course_id)
        course.is_active = not course.is_active
        course.save()
        
        status = "activated" if course.is_active else "deactivated"
        messages.success(request, f'Course "{course.name}" has been {status} successfully!')
    except Course.DoesNotExist:
        messages.error(request, 'Course not found.')
    except Exception as e:
        messages.error(request, f'Error updating course status: {str(e)}')
    
    return redirect('/admin-panel/courses/')

class AdminCourseListView(ListView):
    model = Course
    template_name = 'admin/courses_list.html'
    context_object_name = 'courses'
    paginate_by = 10
    
    def get_queryset(self):
        queryset = Course.objects.all().order_by('-created_at')
        
        search_query = self.request.GET.get('search', '')
        course_type = self.request.GET.get('course_type', '')
        status = self.request.GET.get('status', '')
        
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) |
                Q(course_code__icontains=search_query) |
                Q(description__icontains=search_query)
            )
        
        if course_type:
            queryset = queryset.filter(course_type=course_type)
        
        if status:
            if status == 'active':
                queryset = queryset.filter(is_active=True)
            elif status == 'inactive':
                queryset = queryset.filter(is_active=False)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Course Management'
        context['search_query'] = self.request.GET.get('search', '')
        context['course_types'] = Course.COURSE_TYPE_CHOICES
        context['selected_course_type'] = self.request.GET.get('course_type', '')
        context['selected_status'] = self.request.GET.get('status', '')
        
        # Calculate statistics
        courses = Course.objects.all()
        context['total_courses'] = courses.count()
        context['active_courses'] = courses.filter(is_active=True).count()
        context['inactive_courses'] = courses.filter(is_active=False).count()
        
        # Calculate average students per course
        if context['total_courses'] > 0:
            # This is a placeholder - you'd need to implement actual student enrollment tracking
            context['avg_students_per_course'] = 0.0  # Will be updated when enrollment is implemented
        else:
            context['avg_students_per_course'] = 0.0
        
        # Course type statistics
        context['course_type_stats'] = []
        for course_type in Course.COURSE_TYPE_CHOICES:
            count = courses.filter(course_type=course_type[0]).count()
            context['course_type_stats'].append({
                'type': course_type[1],
                'count': count
            })
        
        return context
