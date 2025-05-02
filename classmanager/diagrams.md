# Smart Education Tracking System - Diagrams for Blackbook

## 1. Entity-Relationship (ER) Diagram

The system comprises the following key entities and relationships:

### Entities:

1. **User**
   - Attributes: username, email, password, is_student (boolean), is_teacher (boolean)
   - Primary key: id

2. **Student**
   - Attributes: name, roll_no, email, phone, student_profile_pic
   - Primary key: user (OneToOne relation with User)
   - Relationships:
     - One Student can have many StudentMarks
     - One Student can be in many StudentsInClass
     - One Student can send many MessageToTeacher
     - One Student can have many ResourceRecommendations
     - One Student has one LearningStyle
     - One Student can be in many StudyGroups
     - One Student can have many PerformanceGoals
     - One Student can have many StudySessions
     - One Student has one LeaderboardEntry
     - One Student can have many SmartStudyPlans
     - One Student can have many CareerRecommendations

3. **Teacher**
   - Attributes: name, subject_name, email, phone, teacher_profile_pic
   - Primary key: user (OneToOne relation with User)
   - Relationships:
     - One Teacher can create many StudentMarks
     - One Teacher can have many StudentsInClass
     - One Teacher can receive many MessageToTeacher
     - One Teacher can create many ClassNotices
     - One Teacher can create many ClassAssignments
     - One Teacher can have many SubmitAssignments
     - One Teacher can create many AcademicCalendar events

4. **StudentMarks**
   - Attributes: subject_name, marks_obtained, maximum_marks, created_at
   - Foreign keys: teacher, student
   - Relationships:
     - Many StudentMarks belong to one Student
     - Many StudentMarks are created by one Teacher

5. **StudentsInClass**
   - Foreign keys: teacher, student
   - Relationships:
     - Many StudentsInClass entries belong to one Teacher
     - Many StudentsInClass entries involve one Student

6. **MessageToTeacher**
   - Attributes: created_at, message, message_html
   - Foreign keys: student, teacher
   - Relationships:
     - Many MessageToTeacher are sent by one Student
     - Many MessageToTeacher are received by one Teacher

7. **ClassNotice**
   - Attributes: created_at, message, message_html
   - Foreign keys: teacher, many-to-many with students
   - Relationships:
     - Many ClassNotices are created by one Teacher
     - Many ClassNotices can be sent to many Students

8. **ClassAssignment**
   - Attributes: created_at, assignment_name, assignment
   - Foreign keys: teacher, many-to-many with students
   - Relationships:
     - Many ClassAssignments are created by one Teacher
     - Many ClassAssignments can be assigned to many Students

9. **SubmitAssignment**
   - Attributes: created_at, submit
   - Foreign keys: student, teacher, submitted_assignment
   - Relationships:
     - Many SubmitAssignments are submitted by one Student
     - Many SubmitAssignments are received by one Teacher
     - Many SubmitAssignments are for one ClassAssignment

10. **ResourceRecommendation**
    - Attributes: subject_name, resource_title, resource_link, resource_description, created_at, is_youtube, is_ai_recommended
    - Foreign key: student
    - Relationships:
      - Many ResourceRecommendations are for one Student

11. **LearningStyle**
    - Attributes: primary_style, secondary_style, visual_score, auditory_score, reading_score, kinesthetic_score, last_updated
    - Foreign key: student (one-to-one)
    - Relationships:
      - One LearningStyle belongs to one Student

12. **StudyGroup**
    - Attributes: name, subject, description, is_active, meeting_link, created_at
    - Foreign keys: created_by, many-to-many with members
    - Relationships:
      - Many StudyGroups are created by one Student
      - Many StudyGroups can have many Student members

13. **PerformanceGoal**
    - Attributes: subject, target_score, current_score, deadline, is_achieved, notes, created_at
    - Foreign key: student
    - Relationships:
      - Many PerformanceGoals belong to one Student

14. **StudySession**
    - Attributes: subject, duration_minutes, productivity_rating, notes, session_date, created_at
    - Foreign key: student
    - Relationships:
      - Many StudySessions belong to one Student

15. **LeaderboardEntry**
    - Attributes: total_score, avg_percentage, rank, last_updated
    - Foreign key: student
    - Relationships:
      - One LeaderboardEntry belongs to one Student

16. **SmartStudyPlan**
    - Attributes: subject, weak_areas, recommended_hours, study_material, created_at, last_updated
    - Foreign key: student
    - Relationships:
      - Many SmartStudyPlans belong to one Student

17. **CareerRecommendation**
    - Attributes: career_title, career_description, match_score, skills_needed, education_required, resource_link, created_at, is_ai_recommended
    - Foreign key: student
    - Relationships:
      - Many CareerRecommendations belong to one Student

18. **AcademicCalendar**
    - Attributes: title, description, event_date, created_at, updated_at, attachment
    - Foreign key: teacher
    - Relationships:
      - Many AcademicCalendar events are created by one Teacher

## 2. Use Case Diagram

### Actors:
1. **Student**
2. **Teacher**
3. **Admin**

### Student Use Cases:
1. Sign Up / Login
2. View/Update Profile
3. View Teachers
4. Join Classes
5. View Assignments
6. Submit Assignments
7. View Marks
8. Send Messages to Teachers
9. View Leaderboard
10. View Recommendations
11. Generate Smart Study Plans (extends View Recommendations)
12. Analyze Learning Style (extends View Recommendations)
13. Get Career Recommendations (extends View Recommendations)
14. Join Study Groups (extends Join Classes)
15. Set Performance Goals (extends View Marks)

### Teacher Use Cases:
1. Sign Up / Login
2. View/Update Profile
3. Manage Students
4. Create Assignments
5. Grade Assignments
6. Post Notices
7. Enter Marks
8. Reply to Messages
9. View Student Performance
10. Manage Academic Calendar

### Admin Use Cases:
1. Login
2. Manage Academic Calendar (shared with Teacher)

### Relationships:
- "View Marks" includes "View Student Performance"
- "View Recommendations" extends to "Generate Smart Study Plans"
- "View Recommendations" extends to "Analyze Learning Style"
- "View Recommendations" extends to "Get Career Recommendations"
- "Join Classes" extends to "Join Study Groups"
- "View Marks" extends to "Set Performance Goals"

## 3. Class Diagram

### Core Classes:

1. **User (AbstractUser)**
   - Attributes:
     - username: CharField
     - email: EmailField
     - password: CharField
     - is_student: BooleanField
     - is_teacher: BooleanField
   - Methods:
     - authenticate()
     - get_full_name()

2. **Student**
   - Attributes:
     - user: OneToOneField(User)
     - name: CharField
     - roll_no: CharField
     - email: EmailField
     - phone: IntegerField
     - student_profile_pic: ImageField
   - Methods:
     - get_absolute_url()
     - __str__()

3. **Teacher**
   - Attributes:
     - user: OneToOneField(User)
     - name: CharField
     - subject_name: CharField
     - email: EmailField
     - phone: IntegerField
     - teacher_profile_pic: ImageField
     - class_students: ManyToManyField(Student, through=StudentsInClass)
   - Methods:
     - get_absolute_url()
     - __str__()

4. **StudentMarks**
   - Attributes:
     - teacher: ForeignKey(Teacher)
     - student: ForeignKey(Student)
     - subject_name: CharField
     - marks_obtained: IntegerField
     - maximum_marks: IntegerField
     - created_at: DateTimeField
   - Methods:
     - __str__()

5. **StudentsInClass**
   - Attributes:
     - teacher: ForeignKey(Teacher)
     - student: ForeignKey(Student)
   - Methods:
     - __str__()

6. **MessageToTeacher**
   - Attributes:
     - student: ForeignKey(Student)
     - teacher: ForeignKey(Teacher)
     - created_at: DateTimeField
     - message: TextField
     - message_html: TextField
   - Methods:
     - __str__()
     - save()

7. **ClassNotice**
   - Attributes:
     - teacher: ForeignKey(Teacher)
     - students: ManyToManyField(Student)
     - created_at: DateTimeField
     - message: TextField
     - message_html: TextField
   - Methods:
     - __str__()
     - save()

8. **ClassAssignment**
   - Attributes:
     - student: ManyToManyField(Student)
     - teacher: ForeignKey(Teacher)
     - created_at: DateTimeField
     - assignment_name: CharField
     - assignment: FileField
   - Methods:
     - __str__()

9. **SubmitAssignment**
   - Attributes:
     - student: ForeignKey(Student)
     - teacher: ForeignKey(Teacher)
     - created_at: DateTimeField
     - submitted_assignment: ForeignKey(ClassAssignment)
     - submit: FileField
   - Methods:
     - __str__()

10. **ResourceRecommendation**
    - Attributes:
      - student: ForeignKey(Student)
      - subject_name: CharField
      - resource_title: CharField
      - resource_link: URLField
      - resource_description: TextField
      - created_at: DateTimeField
      - is_youtube: BooleanField
      - is_ai_recommended: BooleanField
    - Methods:
      - __str__()

11. **LearningStyle**
    - Attributes:
      - student: OneToOneField(Student)
      - primary_style: CharField
      - secondary_style: CharField
      - visual_score: FloatField
      - auditory_score: FloatField
      - reading_score: FloatField
      - kinesthetic_score: FloatField
      - last_updated: DateTimeField
    - Methods:
      - __str__()

12. **StudyGroup**
    - Attributes:
      - name: CharField
      - subject: CharField
      - description: TextField
      - members: ManyToManyField(Student)
      - created_by: ForeignKey(Student)
      - is_active: BooleanField
      - meeting_link: URLField
      - created_at: DateTimeField
    - Methods:
      - __str__()

13. **PerformanceGoal**
    - Attributes:
      - student: ForeignKey(Student)
      - subject: CharField
      - target_score: IntegerField
      - current_score: IntegerField
      - deadline: DateField
      - is_achieved: BooleanField
      - notes: TextField
      - created_at: DateTimeField
    - Methods:
      - __str__()

14. **StudySession**
    - Attributes:
      - student: ForeignKey(Student)
      - subject: CharField
      - duration_minutes: IntegerField
      - productivity_rating: IntegerField
      - notes: TextField
      - session_date: DateField
      - created_at: DateTimeField
    - Methods:
      - __str__()

15. **LeaderboardEntry**
    - Attributes:
      - student: ForeignKey(Student)
      - total_score: DecimalField
      - avg_percentage: DecimalField
      - rank: PositiveIntegerField
      - last_updated: DateTimeField
    - Methods:
      - __str__()

16. **SmartStudyPlan**
    - Attributes:
      - student: ForeignKey(Student)
      - subject: CharField
      - weak_areas: TextField
      - recommended_hours: IntegerField
      - study_material: TextField
      - created_at: DateTimeField
      - last_updated: DateTimeField
    - Methods:
      - __str__()

17. **CareerRecommendation**
    - Attributes:
      - student: ForeignKey(Student)
      - career_title: CharField
      - career_description: TextField
      - match_score: FloatField
      - skills_needed: TextField
      - education_required: CharField
      - resource_link: URLField
      - created_at: DateTimeField
      - is_ai_recommended: BooleanField
    - Methods:
      - __str__()

18. **AcademicCalendar**
    - Attributes:
      - title: CharField
      - description: TextField
      - event_date: DateField
      - teacher: ForeignKey(Teacher)
      - created_at: DateTimeField
      - updated_at: DateTimeField
      - attachment: FileField
    - Methods:
      - __str__()
      - get_absolute_url()

## 4. Sequence Diagram: Assignment Workflow

The assignment workflow involves interactions between Students, Teachers, Assignment System, Submission System, and Recommendation System.

### Sequence:
1. Student → Assignment System: View Available Assignments
2. Assignment System → Student: Display Assignment List
3. Teacher → Assignment System: Create New Assignment
4. Assignment System → Teacher: Assignment Created
5. Student → Submission System: Submit Assignment Solution
6. Submission System → Assignment System: Record Submission
7. Assignment System → Teacher: Notify New Submission
8. Teacher → Student: Grade Assignment & Provide Feedback
9. Student → Recommendation System: Request Learning Resources
10. Recommendation System → Student: Provide Smart Recommendations
11. Student → Student: Study Recommended Material

## 5. Activity Diagram

### Student Activities:
1. Start → User Registration
2. User Registration → Student Dashboard
3. Student Dashboard → View Available Teachers
4. View Available Teachers → Join Teacher's Class
5. Join Teacher's Class → View Assignments
6. View Assignments → [Decision: Complete or Skip]
   - If Complete → Complete and Submit Assignment
   - If Skip → Back to View Assignments
7. Complete and Submit Assignment → Check Grades and Feedback
8. Check Grades and Feedback → Fork:
   - Analyze Learning Style
   - Get Resource Recommendations
   - View Career Recommendations
9. Join to Smart Study Plan
10. Smart Study Plan → End

### Teacher Activities:
1. Start → User Registration
2. User Registration → Teacher Dashboard
3. Teacher Dashboard → Manage Class Students
4. Manage Class Students → Create Assignment
5. Create Assignment → Fork:
   - Monitor Assignment Submissions
   - Grade Student Submissions
   - Post Class Notices
6. Join to Manage Academic Calendar
7. Manage Academic Calendar → End

## 6. Deployment Diagram

### Nodes:
1. **Client**
   - Stereotype: device
   - Components:
     - Web Browser (execution environment)
     - Client UI (artifact)

2. **Application Server**
   - Stereotype: execution environment
   - Components:
     - Django Web Server (execution environment)
     - Student Module (artifact)
     - Teacher Module (artifact)
     - Assignment Module (artifact)
     - Smart Recommendation Engine (artifact)

3. **Database Server**
   - Stereotype: execution environment
   - Components:
     - SQLite Database (execution environment)
     - User Data (artifact)
     - Education Data (artifact)

4. **File Server**
   - Stereotype: device
   - Components:
     - File System (execution environment)
     - Assignments (artifact)
     - Student Submissions (artifact)

5. **AI Services**
   - Stereotype: execution environment
   - Components:
     - Learning Style Analyzer (artifact)
     - Resource Recommender (artifact)
     - Career Path Predictor (artifact)
     - Performance Analyzer (artifact)

### Connections:
1. Client → Application Server: HTTP/HTTPS
2. Application Server → Database Server: SQL
3. Application Server → File Server: File I/O
4. Application Server → AI Services: API Calls

All components are contained within the Smart Education Tracking System boundary. 