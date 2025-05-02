from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from django.conf import settings
import misaka
from django.utils import timezone
# Create your models here.

class User(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)


class Student(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True,related_name='Student')
    name=models.CharField(max_length=250)
    roll_no = models.CharField(max_length=50)
    email = models.EmailField(max_length=254)
    phone = models.IntegerField()
    student_profile_pic = models.ImageField(upload_to="classroom/student_profile_pic",blank=True)

    def get_absolute_url(self):
        return reverse('classroom:student_detail',kwargs={'pk':self.pk})

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['roll_no']

class Teacher(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True,related_name='Teacher')
    name = models.CharField(max_length=250)
    subject_name = models.CharField(max_length=250)
    email = models.EmailField(max_length=254)
    phone = models.IntegerField()
    teacher_profile_pic = models.ImageField(upload_to="classroom/teacher_profile_pic",blank=True)
    class_students = models.ManyToManyField(Student,through="StudentsInClass")

    def get_absolute_url(self):
        return reverse('classroom:teacher_detail',kwargs={'pk':self.pk})

    def __str__(self):
        return self.name

class StudentMarks(models.Model):
    teacher = models.ForeignKey(Teacher,related_name='given_marks',on_delete=models.CASCADE)
    student = models.ForeignKey(Student,related_name="marks",on_delete=models.CASCADE)
    subject_name = models.CharField(max_length=250)
    marks_obtained = models.IntegerField()
    maximum_marks = models.IntegerField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.subject_name

class StudentsInClass(models.Model):
    teacher = models.ForeignKey(Teacher,related_name="class_teacher",on_delete=models.CASCADE)
    student = models.ForeignKey(Student,related_name="user_student_name",on_delete=models.CASCADE)

    def __str__(self):
        return self.student.name

    class Meta:
        unique_together = ('teacher','student')

class MessageToTeacher(models.Model):
    student = models.ForeignKey(Student,related_name='student',on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher,related_name='messages',on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)
    message = models.TextField()
    message_html = models.TextField(editable=False)

    def __str__(self):
        return self.message

    def save(self,*args,**kwargs):
        self.message_html = misaka.html(self.message)
        super().save(*args,**kwargs)

    class Meta:
        ordering = ['-created_at']
        unique_together = ['student','message']

class ClassNotice(models.Model):
    teacher = models.ForeignKey(Teacher,related_name='teacher',on_delete=models.CASCADE)
    students = models.ManyToManyField(Student,related_name='class_notice')
    created_at = models.DateTimeField(auto_now=True)
    message = models.TextField()
    message_html = models.TextField(editable=False)

    def __str__(self):
        return self.message

    def save(self,*args,**kwargs):
        self.message_html = misaka.html(self.message)
        super().save(*args,**kwargs)

    class Meta:
        ordering = ['-created_at']
        unique_together = ['teacher','message']

class ClassAssignment(models.Model):
    student = models.ManyToManyField(Student,related_name='student_assignment')
    teacher = models.ForeignKey(Teacher,related_name='teacher_assignment',on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)
    assignment_name = models.CharField(max_length=250)
    assignment = models.FileField(upload_to='assignments')

    def __str__(self):
        return self.assignment_name

    class Meta:
        ordering = ['-created_at']

class SubmitAssignment(models.Model):
    student = models.ForeignKey(Student,related_name='student_submit',on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher,related_name='teacher_submit',on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)
    submitted_assignment = models.ForeignKey(ClassAssignment,related_name='submission_for_assignment',on_delete=models.CASCADE)
    submit = models.FileField(upload_to='Submission')

    def __str__(self):
        return "Submitted"+str(self.submitted_assignment.assignment_name)

    class Meta:
        ordering = ['-created_at']

# ...existing code...

class MarksGiven(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='marks_given')
    subject_name = models.CharField(max_length=100, default="General")
    marks_obtained = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    maximum_marks = models.DecimalField(max_digits=5, decimal_places=2, default=100)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.student.username} - {self.subject_name}"

class ResourceRecommendation(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='recommendations')
    subject_name = models.CharField(max_length=100, default="General")
    resource_title = models.CharField(max_length=255, default="Resource")
    resource_link = models.URLField(default="https://example.com")
    resource_description = models.TextField(default="Resource description")
    created_at = models.DateTimeField(auto_now_add=True)
    is_youtube = models.BooleanField(default=False)
    is_ai_recommended = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.subject_name} resource for {self.student.name}"

class LearningStyle(models.Model):
    """Model to store student's learning style preferences"""
    STYLE_CHOICES = (
        ('visual', 'Visual Learner'),
        ('auditory', 'Auditory Learner'),
        ('reading', 'Reading/Writing Learner'),
        ('kinesthetic', 'Kinesthetic Learner'),
    )
    
    student = models.OneToOneField(Student, on_delete=models.CASCADE, related_name='learning_style')
    primary_style = models.CharField(max_length=20, choices=STYLE_CHOICES)
    secondary_style = models.CharField(max_length=20, choices=STYLE_CHOICES, blank=True, null=True)
    visual_score = models.FloatField(default=0)
    auditory_score = models.FloatField(default=0)
    reading_score = models.FloatField(default=0)
    kinesthetic_score = models.FloatField(default=0)
    last_updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.student.name}'s learning style: {self.primary_style}"

class StudyGroup(models.Model):
    """Model for peer study groups"""
    name = models.CharField(max_length=100)
    subject = models.CharField(max_length=100)
    description = models.TextField()
    members = models.ManyToManyField(Student, related_name='study_groups')
    created_by = models.ForeignKey(Student, on_delete=models.SET_NULL, null=True, related_name='created_groups')
    is_active = models.BooleanField(default=True)
    meeting_link = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} - {self.subject}"

class PerformanceGoal(models.Model):
    """Model for student performance goals"""
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='goals')
    subject = models.CharField(max_length=100)
    target_score = models.IntegerField()
    current_score = models.IntegerField(blank=True, null=True)
    deadline = models.DateField()
    is_achieved = models.BooleanField(default=False)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['deadline']
    
    def __str__(self):
        return f"{self.student.name}'s goal for {self.subject}: {self.target_score}"

class StudySession(models.Model):
    """Model to track student study sessions"""
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='study_sessions')
    subject = models.CharField(max_length=100)
    duration_minutes = models.IntegerField()
    productivity_rating = models.IntegerField(choices=[(i, i) for i in range(1, 11)])
    notes = models.TextField(blank=True)
    session_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-session_date']
    
    def __str__(self):
        return f"{self.student.name}'s {self.subject} session on {self.session_date}"

class LeaderboardEntry(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='leaderboard_entries')
    total_score = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    avg_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    rank = models.PositiveIntegerField(null=True, blank=True)
    last_updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.student.name} - Score: {self.total_score} - Rank: {self.rank or 'Unranked'}"
    
    class Meta:
        ordering = ['-avg_percentage']

class SmartStudyPlan(models.Model):
    student = models.ForeignKey(Student, related_name='study_plans', on_delete=models.CASCADE)
    subject = models.CharField(max_length=100)
    weak_areas = models.TextField()
    recommended_hours = models.IntegerField(default=5)
    study_material = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.student.name}'s {self.subject} Study Plan"
        
    class Meta:
        ordering = ['-created_at']

class CareerRecommendation(models.Model):
    """Model for AI-generated career recommendations based on student performance and interests"""
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='career_recommendations')
    career_title = models.CharField(max_length=255)
    career_description = models.TextField()
    match_score = models.FloatField(default=0.0)  # 0-1 score indicating match strength
    skills_needed = models.TextField(default="")
    education_required = models.CharField(max_length=255, default="")
    resource_link = models.URLField(default="https://www.linkedin.com/jobs/")
    created_at = models.DateTimeField(auto_now_add=True)
    is_ai_recommended = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['-match_score', '-created_at']
    
    def __str__(self):
        return f"{self.career_title} for {self.student.name}"

class AcademicCalendar(models.Model):
    """Model for academic calendar events that can be created by teachers"""
    title = models.CharField(max_length=255)
    description = models.TextField()
    event_date = models.DateField()
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='calendar_events')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    attachment = models.FileField(upload_to='calendar_attachments/', blank=True, null=True)
    
    class Meta:
        ordering = ['event_date', 'title']
    
    def __str__(self):
        return f"{self.title} - {self.event_date}"
    
    def get_absolute_url(self):
        return reverse('classroom:calendar_detail', kwargs={'pk': self.pk})