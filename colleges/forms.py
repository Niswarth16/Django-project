from django import forms
from .models import CollegeProfile, Attendance, Mark
from students.models import StudentProfile
from courses.models import Course

class CollegeProfileForm(forms.ModelForm):
    class Meta:
        model = CollegeProfile
        fields = [
            'institute_name', 'institute_code', 'address', 'city', 'state',
            'pincode', 'phone', 'email', 'website', 'affiliation',
            'established_year', 'logo', 'description'
        ]
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
            'description': forms.Textarea(attrs={'rows': 4}),
            'established_year': forms.NumberInput(attrs={'min': 1900, 'max': 2100}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name not in ['logo', 'description', 'address']:
                field.widget.attrs.update({'class': 'form-control'})
            elif field_name in ['description', 'address']:
                field.widget.attrs.update({'class': 'form-control'})

class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ['student', 'date', 'status']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'student': forms.Select(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filter only approved students
        self.fields['student'].queryset = StudentProfile.objects.filter(user__is_approved=True)

class MarkForm(forms.ModelForm):
    class Meta:
        model = Mark
        fields = ['student', 'course', 'marks_obtained', 'total_marks']
        widgets = {
            'student': forms.Select(attrs={'class': 'form-control'}),
            'course': forms.Select(attrs={'class': 'form-control'}),
            'marks_obtained': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'total_marks': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filter only approved students and active courses
        self.fields['student'].queryset = StudentProfile.objects.filter(user__is_approved=True)
        self.fields['course'].queryset = Course.objects.filter(is_active=True)
    
    def clean(self):
        cleaned_data = super().clean()
        marks_obtained = cleaned_data.get('marks_obtained')
        total_marks = cleaned_data.get('total_marks')
        
        if marks_obtained and total_marks:
            if marks_obtained > total_marks:
                raise forms.ValidationError("Marks obtained cannot be greater than total marks.")
            if marks_obtained < 0:
                raise forms.ValidationError("Marks obtained cannot be negative.")
            if total_marks <= 0:
                raise forms.ValidationError("Total marks must be greater than 0.")
        
        return cleaned_data
