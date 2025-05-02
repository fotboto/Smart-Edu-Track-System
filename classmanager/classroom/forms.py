from django import forms
from django.contrib.auth.forms import UserCreationForm
from classroom.models import User,Teacher,Student,StudentMarks,MessageToTeacher,ClassNotice,ClassAssignment,SubmitAssignment,SmartStudyPlan,AcademicCalendar
from django.db import transaction
from django.core.exceptions import ValidationError

## User Login Form (Applied in both student and teacher login)
class UserForm(UserCreationForm):
    class Meta():
        model = User
        fields = ['username','password1','password2']
        widgets = {
                'username': forms.TextInput(attrs={'class':'answer'}),
                'password1': forms.PasswordInput(attrs={'class':'answer'}),
                'password2': forms.PasswordInput(attrs={'class':'answer'}),
                }
        
## Teacher Registration Form 
class TeacherProfileForm(forms.ModelForm):
    class Meta():
        model =  Teacher
        fields = ['name','subject_name','phone','email']
        widgets = {
                'name': forms.TextInput(attrs={'class':'answer'}),
                'subject_name': forms.TextInput(attrs={'class':'answer'}),
                'phone': forms.NumberInput(attrs={'class':'answer'}),
                'email': forms.EmailInput(attrs={'class':'answer'}),
                }

## Teacher Profile Update Form
class TeacherProfileUpdateForm(forms.ModelForm):
    class Meta():
        model = Teacher
        fields = ['name','subject_name','email','phone','teacher_profile_pic']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'subject_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.NumberInput(attrs={'class': 'form-control'}),
            'teacher_profile_pic': forms.FileInput(attrs={'class': 'form-control-file'}),
        }

## Student Registration Form
class StudentProfileForm(forms.ModelForm):
    class Meta():
        model =  Student
        fields = ['name','roll_no','phone','email']
        widgets = {
                'name': forms.TextInput(attrs={'class':'answer'}),
                'roll_no': forms.NumberInput(attrs={'class':'answer'}),
                'phone': forms.NumberInput(attrs={'class':'answer'}),
                'email': forms.EmailInput(attrs={'class':'answer'}),
                }

## Student profile update form
class StudentProfileUpdateForm(forms.ModelForm):
    class Meta():
        model = Student
        fields = ['name','roll_no','email','phone','student_profile_pic']
        
## Form for uploading marks and also for updating it.
class MarksForm(forms.ModelForm):
    class Meta():
        model = StudentMarks
        fields = ['subject_name','marks_obtained','maximum_marks']

## Writing message to teacher        
class MessageForm(forms.ModelForm):
    class Meta():
        model = MessageToTeacher
        fields = ['message']

## Writing notice in the class        
class NoticeForm(forms.ModelForm):
    class Meta():
        model = ClassNotice
        fields = ['message']

## Form for uploading or updating assignment (teachers only)       
class AssignmentForm(forms.ModelForm):
    class Meta():
        model = ClassAssignment
        fields = ['assignment_name','assignment']

## Form for submitting assignment (Students only)        
class SubmitForm(forms.ModelForm):
    class Meta():
        model = SubmitAssignment
        fields = ['submit']

class UserLoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))

class TeacherRegistrationForm(forms.ModelForm):
    SUBJECT_CHOICES = [
        ('Mathematics', 'Mathematics'),
        ('Physics', 'Physics'),
        ('Chemistry', 'Chemistry'),
        ('Biology', 'Biology'),
        ('Computer Science', 'Computer Science'),
        ('English', 'English'),
        ('History', 'History'),
        ('Geography', 'Geography'),
    ]
    
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}))
    subjects_taught = forms.MultipleChoiceField(choices=SUBJECT_CHOICES, widget=forms.CheckboxSelectMultiple)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        
        if password and confirm_password and password != confirm_password:
            raise ValidationError("Passwords do not match")
        return cleaned_data

class StudentRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}))
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        
        if password and confirm_password and password != confirm_password:
            raise ValidationError("Passwords do not match")
        return cleaned_data

class CalendarForm(forms.ModelForm):
    event_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    
    class Meta:
        model = AcademicCalendar
        fields = ['title', 'description', 'event_date', 'attachment']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }
