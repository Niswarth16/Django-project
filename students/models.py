from django.db import models
from django.conf import settings

class StudentProfile(models.Model):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    )
    
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    enrollment_number = models.CharField(max_length=20, unique=True)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.enrollment_number}"

class Result(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    course = models.ForeignKey('courses.Course', on_delete=models.CASCADE)
    semester = models.PositiveIntegerField()
    subject = models.CharField(max_length=100)
    marks_obtained = models.PositiveIntegerField()
    total_marks = models.PositiveIntegerField()
    grade = models.CharField(max_length=2)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.student.user.username} - {self.course.name} - {self.subject}"
    
    @property
    def percentage(self):
        return (self.marks_obtained / self.total_marks) * 100

class Certificate(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    certificate_type = models.CharField(max_length=100)
    certificate_file = models.FileField(upload_to='certificates/')
    issue_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.student.user.username} - {self.certificate_type}"
