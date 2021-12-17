from django import forms
from .models import *

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['name', 'number_of_students', 'instructors', 'number_of_lessions_per_week']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control mb-2'}),
            'number_of_students': forms.NumberInput(attrs={'class': 'form-control mb-2'}),
            'instructors': forms.Select(attrs={'class': 'form-select'}),
            'number_of_lessions_per_week': forms.NumberInput(attrs={'class': 'form-control mb-2'})
        }
        

class InstructorForm(forms.ModelForm):
    class Meta:
        model = Instructor
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control mb-2'}),
        }

class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['name', 'capacity']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control mb-2'}),
            'capacity': forms.NumberInput(attrs={'class': 'form-control mb-2'})
        }

class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['name', 'courses']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control mb-2'}),
            'courses': forms.SelectMultiple(attrs={'class': 'form-select'})
        }

class TimetableForm(forms.ModelForm):
    class Meta:
        model = Timetable
        fields = ['name']