from django import forms
from .models import Course

class AdminCourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = [
            'name', 'course_code', 'course_type', 'fees'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Bachelor of Computer Science'}),
            'course_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., BCS-101'}),
            'course_type': forms.Select(attrs={'class': 'form-control'}),
            'fees': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'step': '0.01'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name != 'is_active':
                field.widget.attrs['class'] = 'form-control'
        
        # Add help text
        self.fields['name'].help_text = "Enter the full course name"
        self.fields['course_code'].help_text = "Unique course identifier"
        self.fields['course_type'].help_text = "Select the type of course"
        self.fields['fees'].help_text = "Course fees in local currency"
    
    def clean_course_code(self):
        course_code = self.cleaned_data.get('course_code')
        if course_code:
            course_code = course_code.upper()
            # Check if course code already exists (excluding current instance)
            existing_course = Course.objects.filter(course_code=course_code)
            if self.instance.pk:
                existing_course = existing_course.exclude(pk=self.instance.pk)
            if existing_course.exists():
                raise forms.ValidationError("Course code already exists. Please use a different code.")
        return course_code
    
    def clean_fees(self):
        fees = self.cleaned_data.get('fees')
        if fees is not None and fees < 0:
            raise forms.ValidationError("Fees cannot be negative.")
        return fees
    
    
