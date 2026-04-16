from django.db import models
from django.conf import settings

class Course(models.Model):
    COURSE_TYPE_CHOICES = (
        ('degree', 'Degree'),
        ('diploma', 'Diploma'),
        ('certificate', 'Certificate'),
    )
    
    DURATION_CHOICES = (
        (1, '1 Year'),
        (2, '2 Years'),
        (3, '3 Years'),
        (4, '4 Years'),
        (5, '5 Years'),
    )
    
    name = models.CharField(max_length=200)
    course_code = models.CharField(max_length=20, unique=True)
    course_type = models.CharField(max_length=20, choices=COURSE_TYPE_CHOICES)
    duration = models.PositiveIntegerField(choices=DURATION_CHOICES)
    description = models.TextField()
    eligibility = models.TextField()
    fees = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} ({self.course_code})"

class Enrollment(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('completed', 'Completed'),
    )
    
    student = models.ForeignKey('students.StudentProfile', on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    enrollment_date = models.DateField(auto_now_add=True)
    completion_date = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.student.user.username} - {self.course.name}"
    
    class Meta:
        unique_together = ['student', 'course']
