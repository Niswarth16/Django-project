from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ('student', 'Student'),
        ('college', 'Institute'),
        ('admin', 'Admin'),
    )
    
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='student')
    phone = models.CharField(max_length=15, blank=True, null=True)
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.username} ({self.get_user_type_display()})"

    def is_student(self):
        return self.user_type == 'student'

    def is_college(self):
        return self.user_type == 'college'

    def is_admin_user(self):
        return self.user_type == 'admin'
