import matplotlib.pyplot as plt
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import os

# Create a diagram showing the class structure
WIDTH, HEIGHT = 1400, 1800
image = Image.new('RGB', (WIDTH, HEIGHT), color='white')
draw = ImageDraw.Draw(image)

# Try to load font, use default if not available
try:
    title_font = ImageFont.truetype("arial.ttf", 20)
    header_font = ImageFont.truetype("arial.ttf", 16)
    normal_font = ImageFont.truetype("arial.ttf", 14)
except:
    title_font = ImageFont.load_default()
    header_font = ImageFont.load_default()
    normal_font = ImageFont.load_default()

# Draw title
draw.text((WIDTH//2-150, 20), "Smart Education Tracking System - Class Diagram", fill="black", font=title_font)

# Define classes with attributes and methods
classes = [
    {
        "name": "User (AbstractUser)",
        "x": 600, "y": 80, "width": 300, "height": 120,
        "attributes": [
            "username", "email", "password", "is_student: boolean", "is_teacher: boolean"
        ],
        "methods": ["authenticate()", "get_full_name()"]
    },
    {
        "name": "Student",
        "x": 200, "y": 300, "width": 300, "height": 200,
        "attributes": [
            "user: User (OneToOne)", "name: CharField", "roll_no: CharField", 
            "email: EmailField", "phone: IntegerField", "student_profile_pic: ImageField"
        ],
        "methods": ["get_absolute_url()", "__str__()"]
    },
    {
        "name": "Teacher",
        "x": 900, "y": 300, "width": 300, "height": 200,
        "attributes": [
            "user: User (OneToOne)", "name: CharField", "subject_name: CharField", 
            "email: EmailField", "phone: IntegerField", "teacher_profile_pic: ImageField",
            "class_students: ManyToMany(Student)"
        ],
        "methods": ["get_absolute_url()", "__str__()"]
    },
    {
        "name": "StudentMarks",
        "x": 550, "y": 300, "width": 300, "height": 180,
        "attributes": [
            "teacher: ForeignKey(Teacher)", "student: ForeignKey(Student)",
            "subject_name: CharField", "marks_obtained: IntegerField",
            "maximum_marks: IntegerField", "created_at: DateTimeField"
        ],
        "methods": ["__str__()"]
    },
    {
        "name": "StudentsInClass",
        "x": 550, "y": 520, "width": 300, "height": 120,
        "attributes": [
            "teacher: ForeignKey(Teacher)", "student: ForeignKey(Student)"
        ],
        "methods": ["__str__()"]
    },
    {
        "name": "MessageToTeacher",
        "x": 200, "y": 520, "width": 300, "height": 180,
        "attributes": [
            "student: ForeignKey(Student)", "teacher: ForeignKey(Teacher)",
            "created_at: DateTimeField", "message: TextField",
            "message_html: TextField"
        ],
        "methods": ["__str__()", "save()"]
    },
    {
        "name": "ClassNotice",
        "x": 900, "y": 520, "width": 300, "height": 180,
        "attributes": [
            "teacher: ForeignKey(Teacher)", "students: ManyToMany(Student)",
            "created_at: DateTimeField", "message: TextField",
            "message_html: TextField"
        ],
        "methods": ["__str__()", "save()"]
    },
    {
        "name": "ClassAssignment",
        "x": 900, "y": 720, "width": 300, "height": 180,
        "attributes": [
            "student: ManyToMany(Student)", "teacher: ForeignKey(Teacher)",
            "created_at: DateTimeField", "assignment_name: CharField",
            "assignment: FileField"
        ],
        "methods": ["__str__()"]
    },
    {
        "name": "SubmitAssignment",
        "x": 550, "y": 720, "width": 300, "height": 180,
        "attributes": [
            "student: ForeignKey(Student)", "teacher: ForeignKey(Teacher)",
            "created_at: DateTimeField", "submitted_assignment: ForeignKey(ClassAssignment)",
            "submit: FileField"
        ],
        "methods": ["__str__()"]
    },
    {
        "name": "ResourceRecommendation",
        "x": 200, "y": 720, "width": 300, "height": 200,
        "attributes": [
            "student: ForeignKey(Student)", "subject_name: CharField",
            "resource_title: CharField", "resource_link: URLField",
            "resource_description: TextField", "created_at: DateTimeField",
            "is_youtube: BooleanField", "is_ai_recommended: BooleanField"
        ],
        "methods": ["__str__()"]
    },
    {
        "name": "LearningStyle",
        "x": 200, "y": 940, "width": 300, "height": 220,
        "attributes": [
            "student: OneToOne(Student)", "primary_style: CharField",
            "secondary_style: CharField", "visual_score: FloatField",
            "auditory_score: FloatField", "reading_score: FloatField",
            "kinesthetic_score: FloatField", "last_updated: DateTimeField"
        ],
        "methods": ["__str__()"]
    },
    {
        "name": "StudyGroup",
        "x": 550, "y": 940, "width": 300, "height": 200,
        "attributes": [
            "name: CharField", "subject: CharField", "description: TextField",
            "members: ManyToMany(Student)", "created_by: ForeignKey(Student)",
            "is_active: BooleanField", "meeting_link: URLField",
            "created_at: DateTimeField"
        ],
        "methods": ["__str__()"]
    },
    {
        "name": "PerformanceGoal",
        "x": 900, "y": 940, "width": 300, "height": 200,
        "attributes": [
            "student: ForeignKey(Student)", "subject: CharField",
            "target_score: IntegerField", "current_score: IntegerField",
            "deadline: DateField", "is_achieved: BooleanField",
            "notes: TextField", "created_at: DateTimeField"
        ],
        "methods": ["__str__()"]
    },
    {
        "name": "StudySession",
        "x": 550, "y": 1160, "width": 300, "height": 180,
        "attributes": [
            "student: ForeignKey(Student)", "subject: CharField",
            "duration_minutes: IntegerField", "productivity_rating: IntegerField",
            "notes: TextField", "session_date: DateField",
            "created_at: DateTimeField"
        ],
        "methods": ["__str__()"]
    },
    {
        "name": "LeaderboardEntry",
        "x": 900, "y": 1160, "width": 300, "height": 160,
        "attributes": [
            "student: ForeignKey(Student)", "total_score: DecimalField",
            "avg_percentage: DecimalField", "rank: PositiveIntegerField",
            "last_updated: DateTimeField"
        ],
        "methods": ["__str__()"]
    },
    {
        "name": "SmartStudyPlan",
        "x": 200, "y": 1160, "width": 300, "height": 180,
        "attributes": [
            "student: ForeignKey(Student)", "subject: CharField",
            "weak_areas: TextField", "recommended_hours: IntegerField",
            "study_material: TextField", "created_at: DateTimeField",
            "last_updated: DateTimeField"
        ],
        "methods": ["__str__()"]
    },
    {
        "name": "CareerRecommendation",
        "x": 550, "y": 1360, "width": 300, "height": 200,
        "attributes": [
            "student: ForeignKey(Student)", "career_title: CharField",
            "career_description: TextField", "match_score: FloatField",
            "skills_needed: TextField", "education_required: CharField",
            "resource_link: URLField", "created_at: DateTimeField",
            "is_ai_recommended: BooleanField"
        ],
        "methods": ["__str__()"]
    },
    {
        "name": "AcademicCalendar",
        "x": 900, "y": 1360, "width": 300, "height": 180,
        "attributes": [
            "title: CharField", "description: TextField", 
            "event_date: DateField", "teacher: ForeignKey(Teacher)",
            "created_at: DateTimeField", "updated_at: DateTimeField",
            "attachment: FileField"
        ],
        "methods": ["__str__()", "get_absolute_url()"]
    }
]

# Draw each class
for cls in classes:
    # Draw class box
    draw.rectangle([(cls["x"], cls["y"]), (cls["x"] + cls["width"], cls["y"] + cls["height"])], 
                 outline="black", width=2)
    
    # Draw class name header
    header_height = 30
    draw.rectangle([(cls["x"], cls["y"]), (cls["x"] + cls["width"], cls["y"] + header_height)], 
                 fill="lightblue", outline="black", width=2)
    draw.text((cls["x"] + 10, cls["y"] + 5), cls["name"], fill="black", font=header_font)
    
    # Draw separator line below attributes
    attrs_height = len(cls["attributes"]) * 20 + 10
    separator_y = cls["y"] + header_height + attrs_height
    draw.line([(cls["x"], separator_y), (cls["x"] + cls["width"], separator_y)], fill="black", width=2)
    
    # Draw attributes
    for i, attr in enumerate(cls["attributes"]):
        draw.text((cls["x"] + 10, cls["y"] + header_height + 10 + i*20), attr, fill="black", font=normal_font)
    
    # Draw methods
    for i, method in enumerate(cls["methods"]):
        draw.text((cls["x"] + 10, separator_y + 10 + i*20), method, fill="black", font=normal_font)

# Draw inheritance relationship
inheritance = [
    {"from": "Student", "to": "User (AbstractUser)"},
    {"from": "Teacher", "to": "User (AbstractUser)"}
]

# Draw associations
associations = [
    {"from": "Student", "to": "StudentMarks", "label": "1", "to_label": "*"},
    {"from": "Teacher", "to": "StudentMarks", "label": "1", "to_label": "*"},
    {"from": "Teacher", "to": "StudentsInClass", "label": "1", "to_label": "*"},
    {"from": "Student", "to": "StudentsInClass", "label": "1", "to_label": "*"},
    {"from": "Student", "to": "MessageToTeacher", "label": "1", "to_label": "*"},
    {"from": "Teacher", "to": "MessageToTeacher", "label": "1", "to_label": "*"},
    {"from": "Teacher", "to": "ClassNotice", "label": "1", "to_label": "*"},
    {"from": "Student", "to": "ClassNotice", "label": "*", "to_label": "*"},
    {"from": "Teacher", "to": "ClassAssignment", "label": "1", "to_label": "*"},
    {"from": "Student", "to": "ClassAssignment", "label": "*", "to_label": "*"},
    {"from": "Student", "to": "SubmitAssignment", "label": "1", "to_label": "*"},
    {"from": "Teacher", "to": "SubmitAssignment", "label": "1", "to_label": "*"},
    {"from": "ClassAssignment", "to": "SubmitAssignment", "label": "1", "to_label": "*"},
    {"from": "Student", "to": "ResourceRecommendation", "label": "1", "to_label": "*"},
    {"from": "Student", "to": "LearningStyle", "label": "1", "to_label": "1"},
    {"from": "Student", "to": "StudyGroup", "label": "*", "to_label": "*"},
    {"from": "Student", "to": "PerformanceGoal", "label": "1", "to_label": "*"},
    {"from": "Student", "to": "StudySession", "label": "1", "to_label": "*"},
    {"from": "Student", "to": "LeaderboardEntry", "label": "1", "to_label": "1"},
    {"from": "Student", "to": "SmartStudyPlan", "label": "1", "to_label": "*"},
    {"from": "Student", "to": "CareerRecommendation", "label": "1", "to_label": "*"},
    {"from": "Teacher", "to": "AcademicCalendar", "label": "1", "to_label": "*"}
]

# Draw inheritance relationships
for rel in inheritance:
    from_cls = next((c for c in classes if c["name"] == rel["from"]), None)
    to_cls = next((c for c in classes if c["name"] == rel["to"]), None)
    
    if from_cls and to_cls:
        # Draw line from child to parent
        from_x = from_cls["x"] + from_cls["width"]//2
        from_y = from_cls["y"]
        to_x = to_cls["x"] + to_cls["width"]//2
        to_y = to_cls["y"] + to_cls["height"]
        
        # Midpoint
        mid_x = (from_x + to_x) // 2
        
        # Draw lines
        draw.line([(from_x, from_y), (from_x, from_y - 30), (mid_x, from_y - 30), (mid_x, to_y + 30), (to_x, to_y + 30), (to_x, to_y)], 
                 fill="black", width=2)
        
        # Draw triangle for inheritance
        triangle_size = 10
        draw.polygon([(to_x, to_y), (to_x - triangle_size, to_y + triangle_size), 
                     (to_x + triangle_size, to_y + triangle_size)], 
                    outline="black", fill="white")

# Draw association relationships
for rel in associations:
    from_cls = next((c for c in classes if c["name"] == rel["from"]), None)
    to_cls = next((c for c in classes if c["name"] == rel["to"]), None)
    
    if from_cls and to_cls:
        # Determine connection points based on relative positions
        if from_cls["y"] < to_cls["y"]:  # from above to below
            from_x = from_cls["x"] + from_cls["width"]//2
            from_y = from_cls["y"] + from_cls["height"]
            to_x = to_cls["x"] + to_cls["width"]//2
            to_y = to_cls["y"]
        elif from_cls["y"] > to_cls["y"]:  # from below to above
            from_x = from_cls["x"] + from_cls["width"]//2
            from_y = from_cls["y"]
            to_x = to_cls["x"] + to_cls["width"]//2
            to_y = to_cls["y"] + to_cls["height"]
        elif from_cls["x"] < to_cls["x"]:  # from left to right
            from_x = from_cls["x"] + from_cls["width"]
            from_y = from_cls["y"] + from_cls["height"]//2
            to_x = to_cls["x"]
            to_y = to_cls["y"] + to_cls["height"]//2
        else:  # from right to left
            from_x = from_cls["x"]
            from_y = from_cls["y"] + from_cls["height"]//2
            to_x = to_cls["x"] + to_cls["width"]
            to_y = to_cls["y"] + to_cls["height"]//2
        
        # Draw line
        draw.line([(from_x, from_y), (to_x, to_y)], fill="black", width=1)
        
        # Draw labels
        if "label" in rel:
            # Calculate label position (slightly offset from the line)
            label_x = from_x + 5 if from_x < to_x else from_x - 15
            label_y = from_y - 15 if from_y > to_y else from_y + 5
            draw.text((label_x, label_y), rel["label"], fill="blue", font=normal_font)
        
        if "to_label" in rel:
            # Calculate label position (slightly offset from the line)
            label_x = to_x + 5 if to_x > from_x else to_x - 15
            label_y = to_y - 15 if to_y > from_y else to_y + 5
            draw.text((label_x, label_y), rel["to_label"], fill="blue", font=normal_font)

# Add a legend
legend_x, legend_y = 100, 1600
draw.rectangle((legend_x, legend_y, legend_x + 400, legend_y + 120), outline="black")
draw.text((legend_x + 10, legend_y + 10), "Legend:", fill="black", font=header_font)
draw.text((legend_x + 10, legend_y + 40), "Inheritance (extends)", fill="black", font=normal_font)
draw.line([(legend_x + 200, legend_y + 40), (legend_x + 250, legend_y + 40)], fill="black", width=2)
draw.polygon([(legend_x + 250, legend_y + 40), (legend_x + 240, legend_y + 35), (legend_x + 240, legend_y + 45)], 
            outline="black", fill="white")

draw.text((legend_x + 10, legend_y + 70), "Association", fill="black", font=normal_font)
draw.line([(legend_x + 200, legend_y + 70), (legend_x + 250, legend_y + 70)], fill="black", width=1)
draw.text((legend_x + 180, legend_y + 65), "1", fill="blue", font=normal_font)
draw.text((legend_x + 255, legend_y + 65), "*", fill="blue", font=normal_font)

draw.text((legend_x + 10, legend_y + 100), "1 = One, * = Many", fill="black", font=normal_font)

# Save the image
image.save("class_diagram.png")
print("Class Diagram saved as class_diagram.png") 