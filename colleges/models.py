from django.db import models
from django.conf import settings

class CollegeProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    institute_name = models.CharField(max_length=200)
    institute_code = models.CharField(max_length=20, unique=True)
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    website = models.URLField(blank=True, null=True)
    affiliation = models.CharField(max_length=200)
    established_year = models.PositiveIntegerField()
    logo = models.ImageField(upload_to='college_logos/', blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.institute_name} ({self.institute_code})"

    def get_total_students(self):
        from students.models import StudentProfile
        return StudentProfile.objects.filter(user__is_approved=True).count()

class Attendance(models.Model):
    STATUS_CHOICES = (
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('late', 'Late'),
    )
    
    student = models.ForeignKey('students.StudentProfile', on_delete=models.CASCADE)
    teacher = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, limit_choices_to={'user_type': 'college'})
    date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    remarks = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['student', 'date']
    
    def __str__(self):
        return f"{self.student.user.username} - {self.date} - {self.status}"

class Mark(models.Model):
    student = models.ForeignKey('students.StudentProfile', on_delete=models.CASCADE)
    teacher = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, limit_choices_to={'user_type': 'college'})
    course = models.ForeignKey('courses.Course', on_delete=models.CASCADE)
    exam_type = models.CharField(max_length=100)  # Mid-term, Final, Quiz, etc.
    marks_obtained = models.DecimalField(max_digits=5, decimal_places=2)
    total_marks = models.DecimalField(max_digits=5, decimal_places=2)
    grade = models.CharField(max_length=5, blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.student.user.username} - {self.course.name} - {self.exam_type}"
    
    def save(self, *args, **kwargs):
        # Calculate grade based on percentage
        if self.marks_obtained and self.total_marks:
            percentage = (self.marks_obtained / self.total_marks) * 100
            if percentage >= 90:
                self.grade = 'A+'
            elif percentage >= 80:
                self.grade = 'A'
            elif percentage >= 70:
                self.grade = 'B+'
            elif percentage >= 60:
                self.grade = 'B'
            elif percentage >= 50:
                self.grade = 'C'
            elif percentage >= 40:
                self.grade = 'D'
            else:
                self.grade = 'F'
        super().save(*args, **kwargs)
