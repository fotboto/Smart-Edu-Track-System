import matplotlib.pyplot as plt
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import os

# Create a diagram showing the relationships between models
WIDTH, HEIGHT = 1200, 1500
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
draw.text((WIDTH//2-150, 20), "Smart Education Tracking System - ER Diagram", fill="black", font=title_font)

# Define model boxes
models = [
    {"name": "User", "x": 150, "y": 100, "width": 250, "height": 120, "fields": [
        "username", "email", "password", "is_student (Boolean)", "is_teacher (Boolean)"
    ]},
    {"name": "Student", "x": 150, "y": 300, "width": 250, "height": 150, "fields": [
        "user (OneToOne)", "name", "roll_no", "email", "phone", "student_profile_pic"
    ]},
    {"name": "Teacher", "x": 150, "y": 500, "width": 250, "height": 160, "fields": [
        "user (OneToOne)", "name", "subject_name", "email", "phone", "teacher_profile_pic", "class_students (M2M)"
    ]},
    {"name": "StudentMarks", "x": 450, "y": 300, "width": 250, "height": 150, "fields": [
        "teacher (FK)", "student (FK)", "subject_name", "marks_obtained", "maximum_marks", "created_at"
    ]},
    {"name": "StudentsInClass", "x": 450, "y": 500, "width": 250, "height": 100, "fields": [
        "teacher (FK)", "student (FK)"
    ]},
    {"name": "MessageToTeacher", "x": 750, "y": 100, "width": 250, "height": 150, "fields": [
        "student (FK)", "teacher (FK)", "created_at", "message", "message_html"
    ]},
    {"name": "ClassNotice", "x": 750, "y": 300, "width": 250, "height": 150, "fields": [
        "teacher (FK)", "students (M2M)", "created_at", "message", "message_html"
    ]},
    {"name": "ClassAssignment", "x": 750, "y": 500, "width": 250, "height": 150, "fields": [
        "student (M2M)", "teacher (FK)", "created_at", "assignment_name", "assignment"
    ]},
    {"name": "SubmitAssignment", "x": 750, "y": 700, "width": 250, "height": 150, "fields": [
        "student (FK)", "teacher (FK)", "created_at", "submitted_assignment (FK)", "submit"
    ]},
    {"name": "ResourceRecommendation", "x": 450, "y": 700, "width": 250, "height": 180, "fields": [
        "student (FK)", "subject_name", "resource_title", "resource_link", "resource_description", "is_youtube", "is_ai_recommended"
    ]},
    {"name": "LearningStyle", "x": 150, "y": 700, "width": 250, "height": 180, "fields": [
        "student (OneToOne)", "primary_style", "secondary_style", "visual_score", "auditory_score", "reading_score", "kinesthetic_score"
    ]},
    {"name": "StudyGroup", "x": 450, "y": 950, "width": 250, "height": 180, "fields": [
        "name", "subject", "description", "members (M2M)", "created_by (FK)", "is_active", "meeting_link"
    ]},
    {"name": "LeaderboardEntry", "x": 150, "y": 950, "width": 250, "height": 150, "fields": [
        "student (FK)", "total_score", "avg_percentage", "rank", "last_updated"
    ]},
    {"name": "CareerRecommendation", "x": 750, "y": 950, "width": 250, "height": 180, "fields": [
        "student (FK)", "career_title", "career_description", "match_score", "skills_needed", "education_required", "resource_link"
    ]},
]

# Draw each model
for model in models:
    # Draw box
    draw.rectangle([(model["x"], model["y"]), (model["x"] + model["width"], model["y"] + model["height"])], 
                 outline="black", width=2)
    
    # Draw header
    draw.rectangle([(model["x"], model["y"]), (model["x"] + model["width"], model["y"] + 30)], 
                 fill="lightblue", outline="black", width=2)
    
    # Draw model name
    draw.text((model["x"] + 10, model["y"] + 5), model["name"], fill="black", font=header_font)
    
    # Draw fields
    for i, field in enumerate(model["fields"]):
        draw.text((model["x"] + 10, model["y"] + 40 + i*20), field, fill="black", font=normal_font)

# Draw relationships
relationships = [
    # User relationships
    {"from": "User", "to": "Student", "type": "1-1", "points": [(275, 220), (275, 300)]},
    {"from": "User", "to": "Teacher", "type": "1-1", "points": [(150, 160), (100, 160), (100, 580), (150, 580)]},
    
    # Student relationships
    {"from": "Student", "to": "StudentMarks", "type": "1-N", "points": [(400, 350), (450, 350)]},
    {"from": "Student", "to": "StudentsInClass", "type": "1-N", "points": [(275, 450), (275, 550), (450, 550)]},
    {"from": "Student", "to": "MessageToTeacher", "type": "1-N", "points": [(400, 320), (750, 170)]},
    {"from": "Student", "to": "SubmitAssignment", "type": "1-N", "points": [(275, 450), (275, 750), (750, 750)]},
    {"from": "Student", "to": "ResourceRecommendation", "type": "1-N", "points": [(275, 450), (400, 450), (400, 780)]},
    {"from": "Student", "to": "LearningStyle", "type": "1-1", "points": [(275, 450), (275, 700)]},
    {"from": "Student", "to": "LeaderboardEntry", "type": "1-1", "points": [(275, 450), (275, 950)]},
    {"from": "Student", "to": "StudyGroup", "type": "M-N", "points": [(275, 450), (275, 1050), (450, 1050)]},
    {"from": "Student", "to": "CareerRecommendation", "type": "1-N", "points": [(275, 450), (275, 1030), (750, 1030)]},
    
    # Teacher relationships
    {"from": "Teacher", "to": "StudentMarks", "type": "1-N", "points": [(400, 520), (575, 520), (575, 450)]},
    {"from": "Teacher", "to": "StudentsInClass", "type": "1-N", "points": [(400, 550), (450, 550)]},
    {"from": "Teacher", "to": "MessageToTeacher", "type": "1-N", "points": [(400, 520), (850, 520), (850, 250)]},
    {"from": "Teacher", "to": "ClassNotice", "type": "1-N", "points": [(400, 520), (750, 370)]},
    {"from": "Teacher", "to": "ClassAssignment", "type": "1-N", "points": [(400, 550), (750, 550)]},
    {"from": "Teacher", "to": "SubmitAssignment", "type": "1-N", "points": [(400, 580), (700, 580), (700, 750), (750, 750)]},
    
    # Other relationships
    {"from": "ClassAssignment", "to": "SubmitAssignment", "type": "1-N", "points": [(850, 650), (850, 700)]},
]

# Draw the relationships
for rel in relationships:
    # Get model positions
    for point1, point2 in zip(rel["points"], rel["points"][1:]):
        draw.line([point1, point2], fill="black", width=2)
    
    # Draw relationship type near the line midpoint
    if len(rel["points"]) >= 2:
        midpoint_idx = len(rel["points"]) // 2 - 1
        midpoint = rel["points"][midpoint_idx]
        next_point = rel["points"][midpoint_idx + 1]
        
        mid_x = (midpoint[0] + next_point[0]) // 2
        mid_y = (midpoint[1] + next_point[1]) // 2
        
        draw.text((mid_x + 5, mid_y - 10), rel["type"], fill="blue", font=normal_font)

# Legend
legend_x, legend_y = 400, 1200
draw.text((legend_x, legend_y), "Relationship Types:", fill="black", font=header_font)
draw.text((legend_x, legend_y + 30), "1-1: One-to-One", fill="blue", font=normal_font)
draw.text((legend_x, legend_y + 50), "1-N: One-to-Many", fill="blue", font=normal_font)
draw.text((legend_x, legend_y + 70), "M-N: Many-to-Many", fill="blue", font=normal_font)

# Save the image
image.save("er_diagram.png")
print("ER Diagram saved as er_diagram.png") 