from django import forms

from .models import Course, Department, Enrollment, Student


class StyledModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'w-full rounded-lg border border-slate-300 px-3 py-2.5 text-sm focus:border-indigo-500 focus:ring-indigo-500'


class StudentForm(StyledModelForm):
    class Meta:
        model = Student
        fields = ['student_id', 'first_name', 'last_name', 'email', 'phone', 'date_of_birth', 'gender', 'address', 'department', 'enrollment_date', 'profile_image']
        widgets = {'date_of_birth': forms.DateInput(attrs={'type': 'date'}), 'enrollment_date': forms.DateInput(attrs={'type': 'date'}), 'address': forms.Textarea(attrs={'rows': 3})}


class DepartmentForm(StyledModelForm):
    class Meta:
        model = Department
        fields = ['name', 'description']
        widgets = {'description': forms.Textarea(attrs={'rows': 4})}


class CourseForm(StyledModelForm):
    class Meta:
        model = Course
        fields = ['name', 'code', 'description', 'credits', 'department']
        widgets = {'description': forms.Textarea(attrs={'rows': 3})}


class EnrollmentForm(StyledModelForm):
    class Meta:
        model = Enrollment
        fields = ['student', 'course']