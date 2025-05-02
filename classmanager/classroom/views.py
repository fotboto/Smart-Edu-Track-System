from django.shortcuts import render,get_object_or_404,redirect
from .models import User, MarksGiven, ResourceRecommendation, StudentMarks, StudentsInClass, Student, Teacher, MessageToTeacher, AcademicCalendar
import json, random, re
from django.views import generic
from django.views.generic import (View,TemplateView,
                                ListView,DetailView,
                                CreateView,UpdateView,
                                DeleteView)
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.
from classroom.forms import UserForm,TeacherProfileForm,StudentProfileForm,MarksForm,MessageForm,NoticeForm,AssignmentForm,SubmitForm,TeacherProfileUpdateForm,StudentProfileUpdateForm,CalendarForm
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout,update_session_auth_hash
from django.http import HttpResponseRedirect,HttpResponse,JsonResponse
from classroom import models
from classroom.models import ClassAssignment, SubmitAssignment, CareerRecommendation
from django.contrib.auth.forms import PasswordChangeForm
from django.db.models import Q, Avg, Sum, F, ExpressionWrapper, FloatField
import requests
from django.forms import inlineformset_factory
from django.utils import timezone
import numpy as np
import pandas as pd
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import MinMaxScaler
from sklearn.feature_extraction.text import TfidfVectorizer
import misaka
from django.db import IntegrityError
import matplotlib
matplotlib.use('Agg')
from django.views.decorators.csrf import csrf_exempt


def student_marks_list(request, pk):
    student = get_object_or_404(User, pk=pk)
    given_marks = MarksGiven.objects.filter(student=student)
    
    # Debug print
    print("Found marks:", given_marks.count())
    
    marks_data = []
    for mark in given_marks:
        marks_data.append({
            'subject_name': str(mark.subject_name),
            'marks_obtained': float(mark.marks_obtained),
            'maximum_marks': float(mark.maximum_marks)
        })
    
    # Debug print
    print("Prepared data:", marks_data)
    
    context = {
        'student': student,
        'given_marks': given_marks,
        'marks_json': json.dumps(marks_data)
    }
    return render(request, 'classroom/student_marks_list.html', context)

# For Teacher Sign Up
def TeacherSignUp(request):
    user_type = 'teacher'
    registered = False

    if request.method == "POST":
        user_form = UserForm(data = request.POST)
        teacher_profile_form = TeacherProfileForm(data = request.POST)

        if user_form.is_valid() and teacher_profile_form.is_valid():
            user = user_form.save()
            # Set is_teacher attribute if it exists on the User model
            if hasattr(user, 'is_teacher'):
                user.is_teacher = True
            user.save()

            profile = teacher_profile_form.save(commit=False)
            profile.user = user
            profile.save()

            registered = True
            
            # After successful registration, redirect to login
            messages.success(request, "Registration successful! You can now log in.")
            return redirect('classroom:login')
        else:
            print(user_form.errors,teacher_profile_form.errors)
    else:
        user_form = UserForm()
        teacher_profile_form = TeacherProfileForm()

    return render(request,'classroom/teacher_signup.html',{'user_form':user_form,'teacher_profile_form':teacher_profile_form,'registered':registered,'user_type':user_type})


###  For Student Sign Up
def StudentSignUp(request):
    user_type = 'student'
    registered = False

    if request.method == "POST":
        user_form = UserForm(data = request.POST)
        student_profile_form = StudentProfileForm(data = request.POST)

        if user_form.is_valid() and student_profile_form.is_valid():
            user = user_form.save()
            # Set is_student attribute if it exists on the User model
            if hasattr(user, 'is_student'):
                user.is_student = True
            user.save()

            profile = student_profile_form.save(commit=False)
            profile.user = user
            profile.save()

            registered = True
            
            # After successful registration, redirect to login
            messages.success(request, "Registration successful! You can now log in.")
            return redirect('classroom:login')
        else:
            print(user_form.errors,student_profile_form.errors)
    else:
        user_form = UserForm()
        student_profile_form = StudentProfileForm()

    return render(request,'classroom/student_signup.html',{'user_form':user_form,'student_profile_form':student_profile_form,'registered':registered,'user_type':user_type})

## Sign Up page which will ask whether you are teacher or student.
def SignUp(request):
    return render(request,'classroom/signup.html',{})

## login view.
def user_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username,password=password)

        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('home'))

            else:
                return HttpResponse("Account not active")

        else:
            messages.error(request, "Invalid Details")
            return redirect('classroom:login')
    else:
        return render(request,'classroom/login.html',{})

## logout view.
@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))

## User Profile of student.
class StudentDetailView(LoginRequiredMixin,DetailView):
    context_object_name = "student"
    model = models.Student
    template_name = 'classroom/student_detail_page.html'

## User Profile for teacher.
class TeacherDetailView(LoginRequiredMixin,DetailView):
    context_object_name = "teacher"
    model = models.Teacher
    template_name = 'classroom/teacher_detail_page.html'

## Profile update for students.
@login_required
def StudentUpdateView(request,pk):
    profile_updated = False
    student = get_object_or_404(models.Student,pk=pk)
    if request.method == "POST":
        form = StudentProfileUpdateForm(request.POST,instance=student)
        if form.is_valid():
            profile = form.save(commit=False)
            if 'student_profile_pic' in request.FILES:
                profile.student_profile_pic = request.FILES['student_profile_pic']
            profile.save()
            profile_updated = True
    else:
        form = StudentProfileUpdateForm(request.POST or None,instance=student)
    return render(request,'classroom/student_update_page.html',{'profile_updated':profile_updated,'form':form})

## Profile update for teachers.
@login_required
def TeacherUpdateView(request,pk):
    profile_updated = False
    teacher = get_object_or_404(models.Teacher,pk=pk)
    
    # Check if the logged-in user is the owner of this profile
    if not hasattr(request.user, 'Teacher') or request.user.Teacher.pk != teacher.pk:
        messages.error(request, "You do not have permission to edit this profile.")
        return HttpResponseRedirect(reverse('classroom:teacher_details',kwargs={'teacher_id':pk}))
    
    # Debug output
    print(f"Request method: {request.method}")
    if request.method == "POST":
        print(f"POST data: {request.POST}")
        print(f"FILES data: {request.FILES}")
        
        form = TeacherProfileUpdateForm(request.POST, request.FILES, instance=teacher)
        if form.is_valid():
            print(f"Form is valid: {form.cleaned_data}")
            profile = form.save(commit=False)
            if 'teacher_profile_pic' in request.FILES:
                profile.teacher_profile_pic = request.FILES['teacher_profile_pic']
            profile.save()
            profile_updated = True
            messages.success(request, "Profile updated successfully!")
            # Redirect back to teacher details page after successful update
            return HttpResponseRedirect(reverse('classroom:teacher_details',kwargs={'teacher_id':pk}))
        else:
            print(f"Form errors: {form.errors}")
            messages.error(request, "There was an error updating your profile. Please check the form.")
    else:
        form = TeacherProfileUpdateForm(instance=teacher)
    
    return render(request,'classroom/teacher_update_page.html',{'profile_updated':profile_updated,'form':form})

## List of all students that teacher has added in their class.
def class_students_list(request):
    query = request.GET.get("q", None)
    students = StudentsInClass.objects.filter(teacher=request.user.Teacher)
    students_list = [x.student for x in students]
    qs = Student.objects.all()
    if query is not None:
        qs = qs.filter(
                Q(name__icontains=query)
                )
    qs_one = []
    for x in qs:
        if x in students_list:
            qs_one.append(x)
        else:
            pass
    context = {
        "class_students_list": qs_one,
    }
    template = "classroom/class_students_list.html"
    return render(request, template, context)

class ClassStudentsListView(LoginRequiredMixin,DetailView):
    model = models.Teacher
    template_name = "classroom/class_students_list.html"
    context_object_name = "teacher"

## For Marks obtained by the student in all subjects.
class StudentAllMarksList(LoginRequiredMixin,DetailView):
    model = models.Student
    template_name = "classroom/student_allmarks_list.html"
    context_object_name = "student"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        student = self.get_object()
        
        # Prepare marks data for chart
        marks_data = []
        
        for mark in student.marks.all():
            percentage = (mark.marks_obtained / mark.maximum_marks) * 100
            marks_data.append({
                'subject_name': mark.subject_name,
                'marks_obtained': mark.marks_obtained,
                'maximum_marks': mark.maximum_marks,
                'percentage': round(percentage, 2)
            })
        
        context['marks_json'] = json.dumps(marks_data)
        
        # Generate resource recommendations if needed
        self.generate_recommendations(student, marks_data)
        
        # Get only AI recommendations
        context['recommendations'] = ResourceRecommendation.objects.filter(student=student, is_ai_recommended=True)
        
        return context
    
    def generate_recommendations(self, student, marks_data):
        # Remove all non-AI recommendations
        ResourceRecommendation.objects.filter(student=student, is_ai_recommended=False).delete()
        
        # Generate AI recommendations
        ai_recommendations = generate_ai_recommendations(student)
        update_ai_recommendations(student, ai_recommendations)

def generate_youtube_link(subject, concept=None):
    """Generate a YouTube search link for educational content"""
    base_url = "https://www.youtube.com/results?search_query="
    search_terms = []
    
    # Add subject
    search_terms.append(subject.replace(" ", "+"))
    
    # Add concept if provided
    if concept:
        search_terms.append(concept.replace(" ", "+"))
        
    # Add educational terms
    educational_terms = ["lecture", "tutorial", "explained", "for+students"]
    search_terms.append(random.choice(educational_terms))
    
    # Join all terms
    query = "+".join(search_terms)
    
    return base_url + query

def update_leaderboard():
    """
    This function is disabled as the leaderboard functionality has been removed.
    """
    pass  # Leaderboard functionality removed

## To give marks to a student.
@login_required
def add_marks(request,pk):
    student = get_object_or_404(Student,pk=pk)
    if request.method == "POST":
        form = MarksForm(request.POST)
        if form.is_valid():
            marks = form.save(commit=False)
            marks.student = student
            marks.teacher = request.user.Teacher
            marks.save()
            
            # Remove any non-AI recommendations
            ResourceRecommendation.objects.filter(student=student, is_ai_recommended=False).delete()
            
            # After adding marks, regenerate AI recommendations
            ai_recommendations = generate_ai_recommendations(student)
            update_ai_recommendations(student, ai_recommendations)
            
            # Generate career recommendations based on new marks
            update_career_recommendations(student)
            
            # Leaderboard functionality removed
            # update_leaderboard()
            
            return redirect('classroom:submit_list')
    else:
        form = MarksForm()
    return render(request,'classroom/add_marks.html',{'form':form,'student':student})

## For updating marks.
@login_required
def update_marks(request,pk):
    marks = get_object_or_404(StudentMarks, pk=pk)
    student = marks.student
    
    if request.method == "POST":
        form = MarksForm(request.POST, instance=marks)
        if form.is_valid():
            updated_marks = form.save()
            
            # Remove any non-AI recommendations
            ResourceRecommendation.objects.filter(student=student, is_ai_recommended=False).delete()
            
            # After updating marks, regenerate AI recommendations
            ai_recommendations = generate_ai_recommendations(student)
            update_ai_recommendations(student, ai_recommendations)
            
            # Generate career recommendations based on updated marks
            update_career_recommendations(student)
            
            # Leaderboard functionality removed
            # update_leaderboard()
            
            return redirect('classroom:student_marks_list', pk=marks.student.pk)
    else:
        form = MarksForm(instance=marks)
    return render(request,'classroom/update_marks.html',{'form':form})

@login_required
def delete_marks(request, pk):
    marks = get_object_or_404(StudentMarks, pk=pk)
    student_pk = marks.student.pk
    if request.method == "POST":
        marks.delete()
        # Leaderboard functionality removed
        # update_leaderboard()
        return redirect('classroom:student_marks_list', pk=student_pk)
    return render(request,'classroom/delete_marks_confirm.html',{'marks':marks})

## For writing notice which will be sent to all class students.
@login_required
def add_notice(request):
    notice_sent = False
    teacher = request.user.Teacher
    students = StudentsInClass.objects.filter(teacher=teacher)
    students_list = [x.student for x in students]

    if request.method == "POST":
        notice = NoticeForm(request.POST)
        if notice.is_valid():
            object = notice.save(commit=False)
            object.teacher = teacher
            object.save()
            object.students.add(*students_list)
            notice_sent = True
    else:
        notice = NoticeForm()
    return render(request,'classroom/write_notice.html',{'notice':notice,'notice_sent':notice_sent})

## For student writing message to teacher.
@login_required
def write_message(request,pk):
    message_sent = False
    teacher = get_object_or_404(models.Teacher,pk=pk)

    if request.method == "POST":
        form = MessageForm(request.POST)
        if form.is_valid():
            mssg = form.save(commit=False)
            mssg.teacher = teacher
            mssg.student = request.user.Student
            mssg.save()
            message_sent = True
    else:
        form = MessageForm()
    return render(request,'classroom/write_message.html',{'form':form,'teacher':teacher,'message_sent':message_sent})

## For the list of all the messages teacher have received.
@login_required
def messages_list(request,pk):
    teacher = get_object_or_404(models.Teacher,pk=pk)
    return render(request,'classroom/messages_list.html',{'teacher':teacher})

## Student can see all notice given by their teacher.
@login_required
def class_notice(request,pk):
    student = get_object_or_404(models.Student,pk=pk)
    return render(request,'classroom/class_notice_list.html',{'student':student})

## To see the list of all the marks given by the techer to a specific student.
@login_required
def student_marks_list(request, pk):
    student = get_object_or_404(models.Student, pk=pk)
    teacher = request.user.Teacher
    given_marks = StudentMarks.objects.filter(teacher=teacher, student=student)
    
    # Generate marks data for chart
    marks_data = []
    
    for mark in given_marks:
        percentage = (mark.marks_obtained / mark.maximum_marks) * 100
        marks_data.append({
            'subject_name': mark.subject_name,
            'marks_obtained': mark.marks_obtained,
            'maximum_marks': mark.maximum_marks,
            'percentage': round(percentage, 2)
        })
    
    # Remove all non-AI recommendations
    ResourceRecommendation.objects.filter(student=student, is_ai_recommended=False).delete()
    
    # Generate AI-based recommendations
    ai_recommendations = generate_ai_recommendations(student)
    
    # Save AI recommendations to database
    update_ai_recommendations(student, ai_recommendations)
    
    # Get AI recommendations
    recommendations = ResourceRecommendation.objects.filter(student=student, is_ai_recommended=True)
    
    return render(request, 'classroom/student_marks_list.html', {
        'student': student,
        'given_marks': given_marks,
        'marks_json': json.dumps(marks_data),
        'recommendations': recommendations,
        'is_ai_enabled': True
    })

## To add student in the class.
class add_student(LoginRequiredMixin,generic.RedirectView):

    def get_redirect_url(self,*args,**kwargs):
        return reverse('classroom:students_list')

    def get(self,request,*args,**kwargs):
        student = get_object_or_404(models.Student,pk=self.kwargs.get('pk'))

        try:
            StudentsInClass.objects.create(teacher=self.request.user.Teacher,student=student)
        except:
            messages.warning(self.request,'warning, Student already in class!')
        else:
            messages.success(self.request,'{} successfully added!'.format(student.name))

        return super().get(request,*args,**kwargs)

@login_required
def student_added(request):
    return render(request,'classroom/student_added.html',{})

## List of students which are not added by teacher in their class.
def students_list(request):
    query = request.GET.get("q", None)
    students = StudentsInClass.objects.filter(teacher=request.user.Teacher)
    students_list = [x.student for x in students]
    qs = Student.objects.all()
    if query is not None:
        qs = qs.filter(
                Q(name__icontains=query)
                )
    qs_one = []
    for x in qs:
        if x in students_list:
            pass
        else:
            qs_one.append(x)

    context = {
        "students_list": qs_one,
    }
    template = "classroom/students_list.html"
    return render(request, template, context)

## List of all the teacher present in the portal.
def teachers_list(request):
    query = request.GET.get("q", None)
    qs = Teacher.objects.all()
    if query is not None:
        qs = qs.filter(
                Q(name__icontains=query)
                )

    context = {
        "teachers_list": qs,
    }
    template = "classroom/teachers_list.html"
    return render(request, template, context)


####################################################

## Teacher uploading assignment.
@login_required
def upload_assignment(request):
    assignment_uploaded = False
    teacher = request.user.Teacher
    students = Student.objects.filter(user_student_name__teacher=request.user.Teacher)
    if request.method == 'POST':
        form = AssignmentForm(request.POST, request.FILES)
        if form.is_valid():
            upload = form.save(commit=False)
            upload.teacher = teacher
            students = Student.objects.filter(user_student_name__teacher=request.user.Teacher)
            upload.save()
            upload.student.add(*students)
            assignment_uploaded = True
    else:
        form = AssignmentForm()
    return render(request,'classroom/upload_assignment.html',{'form':form,'assignment_uploaded':assignment_uploaded})

## Students getting the list of all the assignments uploaded by their teacher.
@login_required
def class_assignment(request):
    student = request.user.Student
    assignment = SubmitAssignment.objects.filter(student=student)
    assignment_list = [x.submitted_assignment for x in assignment]
    return render(request,'classroom/class_assignment.html',{'student':student,'assignment_list':assignment_list})

## List of all the assignments uploaded by the teacher himself.
@login_required
def assignment_list(request):
    teacher = request.user.Teacher
    return render(request,'classroom/assignment_list.html',{'teacher':teacher})

## For updating the assignments later.
@login_required
def update_assignment(request,id=None):
    obj = get_object_or_404(ClassAssignment, id=id)
    form = AssignmentForm(request.POST or None, instance=obj)
    context = {
        "form": form
    }
    if form.is_valid():
        obj = form.save(commit=False)
        if 'assignment' in request.FILES:
            obj.assignment = request.FILES['assignment']
        obj.save()
        messages.success(request, "Updated Assignment".format(obj.assignment_name))
        return redirect('classroom:assignment_list')
    template = "classroom/update_assignment.html"
    return render(request, template, context)

## For deleting the assignment.
@login_required
def assignment_delete(request, id=None):
    obj = get_object_or_404(ClassAssignment, id=id)
    if request.method == "POST":
        obj.delete()
        messages.success(request, "Assignment Removed")
        return redirect('classroom:assignment_list')
    context = {
        "object": obj,
    }
    template = "classroom/assignment_delete.html"
    return render(request, template, context)

## For students submitting their assignment.
@login_required
def submit_assignment(request, id=None):
    student = request.user.Student
    assignment = get_object_or_404(ClassAssignment, id=id)
    teacher = assignment.teacher
    if request.method == 'POST':
        form = SubmitForm(request.POST, request.FILES)
        if form.is_valid():
            upload = form.save(commit=False)
            upload.teacher = teacher
            upload.student = student
            upload.submitted_assignment = assignment
            upload.save()
            return redirect('classroom:class_assignment')
    else:
        form = SubmitForm()
    return render(request,'classroom/submit_assignment.html',{'form':form,})

## To see all the submissions done by the students.
@login_required
def submit_list(request):
    teacher = request.user.Teacher
    return render(request,'classroom/submit_list.html',{'teacher':teacher})

##################################################################################################

## For changing password.
@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST , user=request.user)

        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, "Password changed")
            return redirect('home')
        else:
            return redirect('classroom:change_password')
    else:
        form = PasswordChangeForm(user=request.user)
        args = {'form':form}
        return render(request,'classroom/change_password.html',args)

@login_required
def feature_unavailable(request):
    """Display a message that a feature is unavailable"""
    context = {
        'feature_name': 'Leaderboard',
        'message': 'The leaderboard feature has been temporarily disabled for maintenance.',
        'alternative': 'You can view your individual performance in the Marks List section.'
    }
    return render(request, 'classroom/feature_unavailable.html', context)

## Students getting the list of all their assignments
@login_required
def student_assignment(request):
    student = request.user.Student
    assignments = ClassAssignment.objects.filter(student=student)
    return render(request, 'classroom/student_assignment.html', {'student': student, 'assignments': assignments})

## List of teachers who have added the student to their class
@login_required
def my_teachers(request):
    student = request.user.Student
    # Find all teachers who have added this student to their class
    student_classes = StudentsInClass.objects.filter(student=student)
    teachers = [student_class.teacher for student_class in student_classes]
    
    context = {
        "teachers_list": teachers,
        "student": student
    }
    template = "classroom/my_teachers.html"
    return render(request, template, context)

## For teacher replying to student messages
@login_required
def reply_message(request, message_id):
    message = get_object_or_404(models.MessageToTeacher, id=message_id)
    student = message.student
    teacher = request.user.Teacher
    
    # Verify the teacher is the recipient of the message
    if message.teacher != teacher:
        messages.error(request, "You don't have permission to reply to this message.")
        return redirect('classroom:messages_list', pk=teacher.pk)
    
    if request.method == "POST":
        reply_text = request.POST.get('reply_text')
        if reply_text:
            # Create a reply notice visible to this student only
            reply = models.ClassNotice.objects.create(
                teacher=teacher,
                message=f"Reply to your message: {reply_text}"
            )
            reply.students.add(student)
            
            # Update original message to mark as replied
            message.message += f"\n\n[REPLIED]"
            message.save()
            
            messages.success(request, "Reply sent successfully!")
            return redirect('classroom:messages_list', pk=teacher.pk)
    
    return render(request, 'classroom/reply_message.html', {
        'message': message,
        'student': student
    })

def home(request):
    return render(request, 'classroom/home.html')

def contact(request):
    return render(request, 'classroom/contact.html')

def register(request):
    return render(request, 'classroom/register.html')

def student_registration(request):
    # Handle student registration
    return render(request, 'classroom/student_registration.html')

def teacher_details(request, teacher_id):
    teacher = get_object_or_404(Teacher, pk=teacher_id)
    class_students = StudentsInClass.objects.filter(teacher=teacher)
    teacher_assignment = ClassAssignment.objects.filter(teacher=teacher)
    messages = MessageToTeacher.objects.filter(teacher=teacher)
    
    context = {
        'teacher': teacher,
        'class_students': class_students,
        'class_teacher': teacher,
        'email': teacher.email,
        'given_marks': StudentMarks.objects.filter(teacher=teacher),
        'messages': messages,
        'name': teacher.name,
        'phone': teacher.phone,
        'subject_name': teacher.subject_name,
        'teacher_assignment': teacher_assignment,
        'teacher_profile_pic': teacher.teacher_profile_pic,
        'teacher_submit': teacher,
        'user': teacher.user,
        'user_id': teacher.pk
    }
    
    return render(request, 'classroom/teacher_details.html', context)

def subject_details(request, subject_id):
    # Display subject details
    return render(request, 'classroom/subject_details.html')

def resource_details(request, resource_id):
    # Display resource details
    return render(request, 'classroom/resource_details.html')

def update_profile(request):
    # Update user profile
    return render(request, 'classroom/update_profile.html')

def filter_teachers_by_subject(request):
    # Filter teachers by subject
    return render(request, 'classroom/filtered_teachers.html')

def class_notes_list(request, subject_id):
    # Display class notes for a subject
    return render(request, 'classroom/class_notes_list.html')

def ask_doubt(request):
    # Ask doubt to a teacher
    return render(request, 'classroom/ask_doubt.html')

def resources_list(request, subject_id):
    # Display resources for a subject
    return render(request, 'classroom/resources_list.html')

def announcement_list(request):
    # Display announcements
    return render(request, 'classroom/announcements.html')

def assignment_detail(request, assignment_id):
    # Display assignment details
    return render(request, 'classroom/assignment_detail.html')

def marks_list(request):
    # Display marks for a student
    return render(request, 'classroom/marks_list.html')

def attendance_list(request):
    # Display attendance for a student
    return render(request, 'classroom/attendance_list.html')

def recommended_resources(request):
    # Display recommended resources for a student
    return render(request, 'classroom/recommended_resources.html')

def marks_data(request):
    # API endpoint for marks data
    data = {
        'labels': ['Mathematics', 'Science', 'English', 'History', 'Geography'],
        'datasets': [
            {
                'label': 'Marks',
                'data': [85, 72, 90, 78, 88],
                'backgroundColor': 'rgba(75, 192, 192, 0.2)',
                'borderColor': 'rgba(75, 192, 192, 1)',
                'borderWidth': 1
            }
        ]
    }
    return JsonResponse(data)

def attendance_data(request):
    # API endpoint for attendance data
    data = {
        'labels': ['January', 'February', 'March', 'April', 'May'],
        'datasets': [
            {
                'label': 'Attendance',
                'data': [90, 85, 88, 92, 95],
                'backgroundColor': 'rgba(54, 162, 235, 0.2)',
                'borderColor': 'rgba(54, 162, 235, 1)',
                'borderWidth': 1
            }
        ]
    }
    return JsonResponse(data)

# Function to generate AI-based recommendations
def generate_ai_recommendations(student, all_students=None):
    """
    Generate AI-based recommendations for a student based on:
    1. Performance analysis
    2. Subject characteristics
    3. Performance trends
    """
    # Get all marks for the student
    student_marks = StudentMarks.objects.filter(student=student)
    
    if not student_marks.exists():
        return []  # No marks data to base recommendations on
    
    # Create a DataFrame from student's marks
    student_data = []
    for mark in student_marks:
        subject_name = mark.subject_name.lower()
        percentage = (mark.marks_obtained / mark.maximum_marks) * 100
        student_data.append({
            'subject': subject_name,
            'percentage': percentage,
            'marks_obtained': mark.marks_obtained,
            'maximum_marks': mark.maximum_marks,
            'teacher': mark.teacher.name
        })
    
    # Convert to DataFrame for easier analysis
    student_df = pd.DataFrame(student_data)
    
    if student_df.empty:
        return []
    
    # Step 1: Identify weak subjects (below 75%)
    weak_subjects = []
    for _, row in student_df.iterrows():
        if row['percentage'] < 75:
            weak_subjects.append(row['subject'])
    
    # Remove duplicates
    weak_subjects = list(set(weak_subjects))
    
    if len(weak_subjects) == 0:
        return []  # No weak subjects identified
    
    # Step 2: Get recommendations based on subject characteristics
    recommendations = []
    
    # Dictionary of subject categories and related resources
    subject_categories = {
        'python': {
            'category': 'programming',
            'related_topics': ['data structures', 'algorithms', 'functions', 'oop'],
            'resources': [
                {
                    'title': 'Interactive Python Learning',
                    'link': 'https://www.codecademy.com/learn/learn-python-3',
                    'description': 'Interactive tutorials with hands-on coding exercises tailored to your learning pace.',
                    'type': 'interactive'
                },
                {
                    'title': 'Advanced Python Concepts',
                    'link': 'https://realpython.com/',
                    'description': 'Deep dive tutorials focusing on the concepts you need to strengthen.',
                    'type': 'article'
                },
                {
                    'title': 'Python Video Tutorials',
                    'link': 'https://www.youtube.com/results?search_query=python+programming+tutorial',
                    'description': 'Visual learning resources with step-by-step explanations of difficult concepts.',
                    'type': 'video'
                }
            ]
        },
        'java': {
            'category': 'programming',
            'related_topics': ['data structures', 'algorithms', 'oop', 'swing', 'spring'],
            'resources': [
                {
                    'title': 'Interactive Java Learning',
                    'link': 'https://www.codecademy.com/learn/learn-java',
                    'description': 'Interactive tutorials with hands-on coding exercises for Java programming.',
                    'type': 'interactive'
                },
                {
                    'title': 'Java Programming Concepts',
                    'link': 'https://docs.oracle.com/javase/tutorial/',
                    'description': 'Comprehensive Java tutorials covering all core concepts and advanced topics.',
                    'type': 'article'
                },
                {
                    'title': 'Java Video Tutorials',
                    'link': 'https://www.youtube.com/results?search_query=java+programming+tutorial',
                    'description': 'Visual learning resources with step-by-step explanations of Java concepts.',
                    'type': 'video'
                }
            ]
        },
        'html': {
            'category': 'web development',
            'related_topics': ['css', 'javascript', 'dom', 'forms'],
            'resources': [
                {
                    'title': 'Interactive HTML/CSS Practice',
                    'link': 'https://www.freecodecamp.org/learn/responsive-web-design/',
                    'description': 'Build projects while learning HTML with interactive challenges.',
                    'type': 'interactive'
                },
                {
                    'title': 'HTML5 & CSS3 Fundamentals',
                    'link': 'https://developer.mozilla.org/en-US/docs/Web/HTML',
                    'description': 'Comprehensive reference and tutorials on modern HTML techniques.',
                    'type': 'article'
                },
                {
                    'title': 'Web Development Video Series',
                    'link': 'https://www.youtube.com/results?search_query=html+css+tutorial',
                    'description': 'Visual tutorials covering HTML from basic to advanced topics.',
                    'type': 'video'
                }
            ]
        },
        'math': {
            'category': 'mathematics',
            'related_topics': ['algebra', 'calculus', 'statistics', 'geometry'],
            'resources': [
                {
                    'title': 'Interactive Math Practice',
                    'link': 'https://www.khanacademy.org/math',
                    'description': 'Practice problems and video explanations for mathematics concepts.',
                    'type': 'interactive'
                },
                {
                    'title': 'Mathematics Explained',
                    'link': 'https://www.mathsisfun.com/',
                    'description': 'Simple explanations of mathematics concepts with visual aids.',
                    'type': 'article'
                },
                {
                    'title': 'Math Video Tutorials',
                    'link': 'https://www.youtube.com/results?search_query=mathematics+tutorial',
                    'description': 'Step-by-step video explanations of mathematical concepts and problem solving.',
                    'type': 'video'
                }
            ]
        }
    }
    
    # Step 4: Generate personalized recommendations
    for subject in weak_subjects:
        # Find the most appropriate category
        subject_key = None
        for key in subject_categories:
            if key in subject.lower():
                subject_key = key
                break
        
        # If we don't have specific resources for this subject, use generic recommendation
        if not subject_key:
            # Create a generic YouTube recommendation
            youtube_link = generate_youtube_link(subject)
            recommendations.append({
                'subject_name': subject,
                'resource_title': f"YouTube Tutorials: {subject}",
                'resource_link': youtube_link,
                'resource_description': f"Helpful video tutorials to improve your understanding of {subject}.",
                'is_youtube': True,
                'is_ai_recommended': True
            })
            continue
            
        # Select relevant resources
        category_info = subject_categories[subject_key]
        
        # Personalize based on performance
        subject_data = student_df[student_df['subject'] == subject]
        subject_performance = subject_data['percentage'].mean()
        
        # Choose appropriate resource types based on performance level
        if subject_performance < 50:  # Very weak - recommend interactive and video
            recommended_types = ['interactive', 'video']
        elif subject_performance < 65:  # Weak - recommend all types
            recommended_types = ['interactive', 'article', 'video']
        else:  # Moderate - recommend articles for deeper understanding
            recommended_types = ['article', 'interactive']
        
        # Filter resources by type
        filtered_resources = []
        for resource in category_info['resources']:
            if resource['type'] in recommended_types:
                filtered_resources.append(resource)
        
        # If no resources match the criteria, include all resources
        if not filtered_resources:
            filtered_resources = category_info['resources']
        
        # Select one resource (random selection)
        selected_resource = random.choice(filtered_resources)
        
        # Add to recommendations
        recommendations.append({
            'subject_name': subject,
            'resource_title': selected_resource['title'],
            'resource_link': selected_resource['link'],
            'resource_description': selected_resource['description'],
            'is_youtube': selected_resource['type'] == 'video',
            'is_ai_recommended': True
        })
    
    return recommendations

# Function to save AI recommendations to the database
def update_ai_recommendations(student, recommendations):
    """Update the database with AI-generated recommendations"""
    # Delete existing AI recommendations
    ResourceRecommendation.objects.filter(student=student, is_ai_recommended=True).delete()
    
    # Save new AI recommendations
    for rec in recommendations:
        ResourceRecommendation.objects.create(
            student=student,
            subject_name=rec['subject_name'],
            resource_title=rec['resource_title'],
            resource_link=rec['resource_link'],
            resource_description=rec['resource_description'],
            is_youtube=rec['is_youtube'],
            is_ai_recommended=True
        )

# Original function to generate YouTube links
def generate_youtube_link(subject):
    """Generate a YouTube search link for educational content about a subject"""
    base_url = "https://www.youtube.com/results?search_query="
    search_query = f"{subject}+tutorial+learning+education"
    return base_url + search_query

def generate_ai_career_recommendations(student):
    """
    Generate AI-based career recommendations for a student based on:
    1. Academic performance in different subjects
    2. Subject strengths and weaknesses
    3. Career-subject compatibility
    """
    # Get all marks for the student
    student_marks = StudentMarks.objects.filter(student=student)
    
    if not student_marks.exists():
        return []  # No marks data to base recommendations on
    
    # Create a DataFrame from student's marks
    student_data = []
    for mark in student_marks:
        subject_name = mark.subject_name.lower()
        percentage = (mark.marks_obtained / mark.maximum_marks) * 100
        student_data.append({
            'subject': subject_name,
            'percentage': percentage,
            'marks_obtained': mark.marks_obtained,
            'maximum_marks': mark.maximum_marks
        })
    
    # Convert to DataFrame for easier analysis
    student_df = pd.DataFrame(student_data)
    
    # Group by subject and calculate average percentage
    subject_avg = student_df.groupby('subject')['percentage'].mean().reset_index()
    
    # Dictionary mapping subjects to related career fields
    subject_career_map = {
        'math': [
            {
                'career': 'Data Scientist',
                'description': 'Analyze complex data to help organizations make better decisions.',
                'skills': 'Statistics, Programming, Machine Learning, Data Visualization',
                'education': 'Bachelor\'s or Master\'s in Computer Science, Statistics, or related field',
                'link': 'https://www.linkedin.com/jobs/data-scientist-jobs/'
            },
            {
                'career': 'Actuarial Analyst',
                'description': 'Assess financial risks using mathematical and statistical methods.',
                'skills': 'Statistical Analysis, Risk Assessment, Financial Modeling',
                'education': 'Bachelor\'s in Mathematics, Actuarial Science, or Statistics',
                'link': 'https://www.linkedin.com/jobs/actuarial-jobs/'
            },
            {
                'career': 'Quantitative Analyst',
                'description': 'Develop mathematical models for financial investments and risk management.',
                'skills': 'Advanced Mathematics, Programming, Financial Modeling',
                'education': 'Master\'s or PhD in Mathematics, Physics, or Financial Engineering',
                'link': 'https://www.linkedin.com/jobs/quantitative-analyst-jobs/'
            }
        ],
        'physics': [
            {
                'career': 'Research Scientist',
                'description': 'Conduct experiments and research to innovate and solve complex problems.',
                'skills': 'Analytical Thinking, Laboratory Techniques, Research Methodology',
                'education': 'PhD in Physics or related field',
                'link': 'https://www.linkedin.com/jobs/research-scientist-jobs/'
            },
            {
                'career': 'Aerospace Engineer',
                'description': 'Design and build aircraft, spacecraft, satellites, and missiles.',
                'skills': 'CAD Software, Analytical Skills, Problem-solving',
                'education': 'Bachelor\'s or Master\'s in Aerospace Engineering',
                'link': 'https://www.linkedin.com/jobs/aerospace-engineer-jobs/'
            }
        ],
        'chemistry': [
            {
                'career': 'Chemical Engineer',
                'description': 'Apply chemistry principles to solve problems involving chemicals, fuel, drugs, and food.',
                'skills': 'Process Engineering, Chemical Analysis, Problem-solving',
                'education': 'Bachelor\'s or Master\'s in Chemical Engineering',
                'link': 'https://www.linkedin.com/jobs/chemical-engineer-jobs/'
            },
            {
                'career': 'Pharmacologist',
                'description': 'Research and testing of drug compounds and how they interact with biological systems.',
                'skills': 'Laboratory Techniques, Research, Data Analysis',
                'education': 'PharmD or PhD in Pharmacology',
                'link': 'https://www.linkedin.com/jobs/pharmacologist-jobs/'
            }
        ],
        'biology': [
            {
                'career': 'Biotechnologist',
                'description': 'Apply technology to biological systems for product and process development.',
                'skills': 'Laboratory Techniques, Analytical Skills, Research Methods',
                'education': 'Bachelor\'s or Master\'s in Biotechnology or related field',
                'link': 'https://www.linkedin.com/jobs/biotechnology-jobs/'
            },
            {
                'career': 'Clinical Research Associate',
                'description': 'Monitor clinical trials to ensure compliance with protocol and regulations.',
                'skills': 'Clinical Research, Regulatory Knowledge, Data Management',
                'education': 'Bachelor\'s in Life Sciences or related field',
                'link': 'https://www.linkedin.com/jobs/clinical-research-associate-jobs/'
            }
        ],
        'programming': [
            {
                'career': 'Software Developer',
                'description': 'Design, build, and maintain computer programs and applications.',
                'skills': 'Programming Languages, Problem-solving, Software Design',
                'education': 'Bachelor\'s in Computer Science or related field',
                'link': 'https://www.linkedin.com/jobs/software-developer-jobs/'
            },
            {
                'career': 'Mobile App Developer',
                'description': 'Create applications for mobile devices and platforms.',
                'skills': 'Mobile Development, Programming, UI/UX Design',
                'education': 'Bachelor\'s in Computer Science or related field',
                'link': 'https://www.linkedin.com/jobs/mobile-app-developer-jobs/'
            }
        ],
        'java': [
            {
                'career': 'Java Developer',
                'description': 'Build enterprise-level applications, Android apps, and back-end systems using Java.',
                'skills': 'Java Programming, Spring Framework, Database Management',
                'education': 'Bachelor\'s in Computer Science or related field',
                'link': 'https://www.linkedin.com/jobs/java-developer-jobs/'
            },
            {
                'career': 'Software Architect',
                'description': 'Design software systems and specify technical standards.',
                'skills': 'Software Design, System Architecture, Team Leadership',
                'education': 'Bachelor\'s or Master\'s in Computer Science',
                'link': 'https://www.linkedin.com/jobs/software-architect-jobs/'
            }
        ],
        'english': [
            {
                'career': 'Content Strategist',
                'description': 'Develop and implement content initiatives across digital platforms.',
                'skills': 'Content Planning, Writing, SEO, Content Management',
                'education': 'Bachelor\'s in English, Communications, or Marketing',
                'link': 'https://www.linkedin.com/jobs/content-strategist-jobs/'
            },
            {
                'career': 'Technical Writer',
                'description': 'Create instruction manuals, how-to guides, and other documentation.',
                'skills': 'Writing, Documentation, Information Architecture',
                'education': 'Bachelor\'s in English, Technical Writing, or related field',
                'link': 'https://www.linkedin.com/jobs/technical-writer-jobs/'
            }
        ],
        'history': [
            {
                'career': 'Historian',
                'description': 'Research, analyze, and interpret the past through sources.',
                'skills': 'Research, Analysis, Writing, Critical Thinking',
                'education': 'Master\'s or PhD in History',
                'link': 'https://www.linkedin.com/jobs/historian-jobs/'
            },
            {
                'career': 'Museum Curator',
                'description': 'Acquire, store, and exhibit collections in museums.',
                'skills': 'Collections Management, Research, Exhibition Planning',
                'education': 'Master\'s in Museum Studies, History, or Art History',
                'link': 'https://www.linkedin.com/jobs/museum-curator-jobs/'
            }
        ]
    }
    
    # Cross-discipline careers for multiple subject strengths
    interdisciplinary_careers = {
        'math_programming': [
            {
                'career': 'Machine Learning Engineer',
                'description': 'Develop self-learning algorithms and systems that improve autonomously.',
                'skills': 'Machine Learning, Programming, Mathematics, Data Structures',
                'education': 'Master\'s in Computer Science or related field',
                'link': 'https://www.linkedin.com/jobs/machine-learning-engineer-jobs/'
            }
        ],
        'biology_chemistry': [
            {
                'career': 'Biochemist',
                'description': 'Study chemical processes within living organisms.',
                'skills': 'Laboratory Techniques, Analytical Skills, Research',
                'education': 'PhD in Biochemistry or related field',
                'link': 'https://www.linkedin.com/jobs/biochemist-jobs/'
            }
        ],
        'physics_math': [
            {
                'career': 'Quantum Computing Researcher',
                'description': 'Explore quantum algorithms and develop quantum computing technology.',
                'skills': 'Quantum Mechanics, Advanced Mathematics, Programming',
                'education': 'PhD in Physics, Computer Science, or Mathematics',
                'link': 'https://www.linkedin.com/jobs/quantum-computing-jobs/'
            }
        ]
    }
    
    recommendations = []
    
    # Identify strong subjects (75% or higher)
    strong_subjects = subject_avg[subject_avg['percentage'] >= 75]['subject'].tolist()
    
    # Generate career recommendations based on strengths
    for subject in strong_subjects:
        # Match subject with career options
        for key in subject_career_map:
            if key in subject.lower():
                # Get career options for this subject
                career_options = subject_career_map[key]
                
                # Calculate match score based on performance
                subject_performance = subject_avg[subject_avg['subject'] == subject]['percentage'].values[0]
                match_score = min(subject_performance / 100, 0.95)  # Cap at 0.95
                
                # Randomly select one career recommendation
                selected_career = random.choice(career_options)
                
                recommendations.append({
                    'career_title': selected_career['career'],
                    'career_description': selected_career['description'],
                    'match_score': match_score,
                    'skills_needed': selected_career['skills'],
                    'education_required': selected_career['education'],
                    'resource_link': selected_career['link'],
                    'is_ai_recommended': True
                })
    
    # Check for interdisciplinary recommendations
    if len(strong_subjects) > 1:
        for combo, careers in interdisciplinary_careers.items():
            subjects_in_combo = combo.split('_')
            matching_subjects = [s for s in strong_subjects if any(sub in s.lower() for sub in subjects_in_combo)]
            
            if len(matching_subjects) >= len(subjects_in_combo):
                # Calculate average performance across these subjects
                avg_performance = np.mean([
                    subject_avg[subject_avg['subject'] == subject]['percentage'].values[0]
                    for subject in matching_subjects
                ])
                
                match_score = min(avg_performance / 100, 0.98)  # Cap at 0.98 (higher for interdisciplinary)
                
                # Add interdisciplinary career recommendation
                selected_career = random.choice(careers)
                recommendations.append({
                    'career_title': selected_career['career'],
                    'career_description': selected_career['description'],
                    'match_score': match_score,
                    'skills_needed': selected_career['skills'],
                    'education_required': selected_career['education'],
                    'resource_link': selected_career['link'],
                    'is_ai_recommended': True
                })
    
    # If no strong subjects or no matches, provide general recommendations
    if not recommendations:
        general_careers = [
            {
                'career': 'Business Analyst',
                'description': 'Analyze business processes and recommend improvements.',
                'skills': 'Data Analysis, Problem-solving, Communication',
                'education': 'Bachelor\'s in Business, IT, or related field',
                'link': 'https://www.linkedin.com/jobs/business-analyst-jobs/'
            },
            {
                'career': 'Digital Marketing Specialist',
                'description': 'Develop and implement digital marketing strategies.',
                'skills': 'Social Media Marketing, SEO, Analytics, Content Creation',
                'education': 'Bachelor\'s in Marketing or related field',
                'link': 'https://www.linkedin.com/jobs/digital-marketing-specialist-jobs/'
            }
        ]
        
        # Choose a general career recommendation
        selected_career = random.choice(general_careers)
        recommendations.append({
            'career_title': selected_career['career'],
            'career_description': selected_career['description'],
            'match_score': 0.5,  # Medium confidence for general recommendations
            'skills_needed': selected_career['skills'],
            'education_required': selected_career['education'],
            'resource_link': selected_career['link'],
            'is_ai_recommended': True
        })
    
    # Sort recommendations by match score (highest first)
    recommendations.sort(key=lambda x: x['match_score'], reverse=True)
    
    # Limit to top 3 recommendations
    return recommendations[:3]

def update_career_recommendations(student):
    """Update the database with AI-generated career recommendations"""
    # Delete existing career recommendations
    CareerRecommendation.objects.filter(student=student).delete()
    
    # Generate new recommendations
    recommendations = generate_ai_career_recommendations(student)
    
    # Save new recommendations
    for rec in recommendations:
        CareerRecommendation.objects.create(
            student=student,
            career_title=rec['career_title'],
            career_description=rec['career_description'],
            match_score=rec['match_score'],
            skills_needed=rec['skills_needed'],
            education_required=rec['education_required'],
            resource_link=rec['resource_link'],
            is_ai_recommended=rec['is_ai_recommended']
        )

@login_required
def career_recommendations(request, pk):
    """View to display AI-powered career recommendations for a student"""
    student = get_object_or_404(Student, pk=pk)
    
    # Check if viewing own profile or has permission
    if request.user.is_authenticated and hasattr(request.user, 'Student'):
        if request.user.Student != student:
            return redirect('classroom:student_detail')
    
    # Get career recommendations for this student
    recommendations = CareerRecommendation.objects.filter(student=student)
    
    # If no recommendations exist, generate them
    if not recommendations.exists():
        new_recommendations = generate_ai_career_recommendations(student)
        update_career_recommendations(student)
        recommendations = CareerRecommendation.objects.filter(student=student)
    
    # Get student marks for context
    student_marks = StudentMarks.objects.filter(student=student)
    
    # Calculate overall performance
    total_marks = 0
    total_max = 0
    subjects_count = student_marks.count()
    
    for mark in student_marks:
        total_marks += mark.marks_obtained
        total_max += mark.maximum_marks
    
    overall_percentage = (total_marks / total_max * 100) if total_max > 0 else 0
    
    context = {
        'student': student,
        'career_recommendations': recommendations,
        'student_marks': student_marks,
        'overall_percentage': overall_percentage,
        'subjects_count': subjects_count
    }
    
    return render(request, 'classroom/career_recommendations.html', context)

@login_required
def calendar_list(request):
    """View all calendar events"""
    # Get events sorted by date
    events = AcademicCalendar.objects.all().order_by('event_date')
    
    # Organize events by month for display
    events_by_month = {}
    for event in events:
        month_key = event.event_date.strftime('%B %Y')
        if month_key not in events_by_month:
            events_by_month[month_key] = []
        events_by_month[month_key].append(event)
    
    context = {
        'events_by_month': events_by_month,
        'is_teacher': hasattr(request.user, 'Teacher')
    }
    return render(request, 'classroom/calendar_list.html', context)

@login_required
def calendar_detail(request, pk):
    """View details of a calendar event"""
    event = get_object_or_404(AcademicCalendar, pk=pk)
    context = {
        'event': event,
        'is_teacher': hasattr(request.user, 'Teacher')
    }
    return render(request, 'classroom/calendar_detail.html', context)

@login_required
def calendar_create(request):
    """Create a new calendar event (teachers only)"""
    if not hasattr(request.user, 'Teacher'):
        messages.error(request, "Only teachers can create calendar events")
        return redirect('classroom:calendar_list')
    
    if request.method == 'POST':
        form = CalendarForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save(commit=False)
            event.teacher = request.user.Teacher
            event.save()
            messages.success(request, "Calendar event created successfully")
            return redirect('classroom:calendar_list')
    else:
        form = CalendarForm()
    
    return render(request, 'classroom/calendar_form.html', {
        'form': form,
        'title': 'Create Calendar Event'
    })

@login_required
def calendar_update(request, pk):
    """Update an existing calendar event (teachers only)"""
    event = get_object_or_404(AcademicCalendar, pk=pk)
    
    # Check if the user is the creator of the event
    if not hasattr(request.user, 'Teacher') or request.user.Teacher != event.teacher:
        messages.error(request, "You can only edit calendar events you created")
        return redirect('classroom:calendar_list')
    
    if request.method == 'POST':
        form = CalendarForm(request.POST, request.FILES, instance=event)
        if form.is_valid():
            form.save()
            messages.success(request, "Calendar event updated successfully")
            return redirect('classroom:calendar_list')
    else:
        form = CalendarForm(instance=event)
    
    return render(request, 'classroom/calendar_form.html', {
        'form': form,
        'title': 'Update Calendar Event',
        'event': event
    })

@login_required
def calendar_delete(request, pk):
    """Delete a calendar event (teachers only)"""
    event = get_object_or_404(AcademicCalendar, pk=pk)
    
    # Check if the user is the creator of the event
    if not hasattr(request.user, 'Teacher') or request.user.Teacher != event.teacher:
        messages.error(request, "You can only delete calendar events you created")
        return redirect('classroom:calendar_list')
    
    if request.method == 'POST':
        event.delete()
        messages.success(request, "Calendar event deleted successfully")
        return redirect('classroom:calendar_list')
    
    return render(request, 'classroom/calendar_confirm_delete.html', {'event': event})