import matplotlib.pyplot as plt
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import os

# Create an activity diagram for the Smart Education Tracking System
WIDTH, HEIGHT = 1300, 1800
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
draw.text((WIDTH//2-150, 30), "Smart Education Tracking System - Activity Diagram", 
         fill="black", font=title_font)

# Define activity and decision nodes
def draw_activity(x, y, width, height, text):
    # Draw rounded rectangle
    draw.rounded_rectangle([(x, y), (x + width, y + height)], radius=10, 
                         outline="black", fill="lightblue", width=2)
    
    # Draw text (wrap if necessary)
    lines = []
    words = text.split()
    current_line = ""
    for word in words:
        if len(current_line + " " + word) * 6 < width - 10:
            current_line += (" " + word if current_line else word)
        else:
            lines.append(current_line)
            current_line = word
    if current_line:
        lines.append(current_line)
    
    for i, line in enumerate(lines):
        text_width = len(line) * 7
        draw.text((x + width//2 - text_width//2, y + 5 + i*20), line, fill="black", font=normal_font)

def draw_decision(x, y, size):
    # Draw diamond
    points = [
        (x, y + size//2),  # top
        (x + size//2, y + size),  # right
        (x + size, y + size//2),  # bottom
        (x + size//2, y)  # left
    ]
    draw.polygon(points, outline="black", fill="white", width=2)

def draw_start(x, y, radius):
    # Draw filled circle for start node
    draw.ellipse([(x - radius, y - radius), (x + radius, y + radius)], 
               outline="black", fill="black", width=2)

def draw_end(x, y, radius):
    # Draw double circle for end node
    draw.ellipse([(x - radius, y - radius), (x + radius, y + radius)], 
               outline="black", fill="white", width=2)
    draw.ellipse([(x - radius + 5, y - radius + 5), (x + radius - 5, y + radius - 5)], 
               outline="black", fill="black", width=2)

def draw_fork(x, y, width, height, horizontal=True):
    # Draw synchronization bar (fork/join)
    draw.rectangle([(x, y), (x + width, y + height)], 
                 outline="black", fill="black", width=2)

# Draw activities, decisions, and control flows

# Start node
start_x, start_y = WIDTH // 2, 100
draw_start(start_x, start_y, 15)

# User Registration
signup_x, signup_y = WIDTH // 2 - 100, 150
signup_width, signup_height = 200, 50
draw_activity(signup_x, signup_y, signup_width, signup_height, "User Registration (Student/Teacher)")

# User type decision
user_decision_x, user_decision_y = WIDTH // 2 - 50, 250
draw_decision(user_decision_x, user_decision_y, 100)

# Student and Teacher paths
student_x, student_y = WIDTH // 2 - 380, 350
student_width, student_height = 200, 50
draw_activity(student_x, student_y, student_width, student_height, "Student Dashboard")

teacher_x, teacher_y = WIDTH // 2 + 180, 350
teacher_width, teacher_height = 200, 50
draw_activity(teacher_x, teacher_y, teacher_width, teacher_height, "Teacher Dashboard")

# Student path activities
view_teachers_x, view_teachers_y = student_x, student_y + 100
view_teachers_width, view_teachers_height = 200, 50
draw_activity(view_teachers_x, view_teachers_y, view_teachers_width, view_teachers_height, "View Available Teachers")

join_class_x, join_class_y = student_x, view_teachers_y + 100
join_class_width, join_class_height = 200, 50
draw_activity(join_class_x, join_class_y, join_class_width, join_class_height, "Join Teacher's Class")

view_assignments_x, view_assignments_y = student_x, join_class_y + 100
view_assignments_width, view_assignments_height = 200, 50
draw_activity(view_assignments_x, view_assignments_y, view_assignments_width, view_assignments_height, "View Assignments")

# Assignment decision
assignment_decision_x, assignment_decision_y = student_x + 50, view_assignments_y + 100
draw_decision(assignment_decision_x, assignment_decision_y, 100)

complete_assignment_x, complete_assignment_y = student_x, assignment_decision_y + 120
complete_assignment_width, complete_assignment_height = 200, 50
draw_activity(complete_assignment_x, complete_assignment_y, complete_assignment_width, complete_assignment_height, "Complete and Submit Assignment")

check_grades_x, check_grades_y = student_x, complete_assignment_y + 100
check_grades_width, check_grades_height = 200, 50
draw_activity(check_grades_x, check_grades_y, check_grades_width, check_grades_height, "Check Grades and Feedback")

# Smart features fork
smart_fork_x, smart_fork_y = student_x + 80, check_grades_y + 100
draw_fork(smart_fork_x, smart_fork_y, 40, 10, horizontal=True)

# Smart features (parallel)
learning_style_x, learning_style_y = student_x - 280, smart_fork_y + 70
learning_style_width, learning_style_height = 200, 50
draw_activity(learning_style_x, learning_style_y, learning_style_width, learning_style_height, "Analyze Learning Style")

resource_rec_x, resource_rec_y = student_x, smart_fork_y + 70
resource_rec_width, resource_rec_height = 200, 50
draw_activity(resource_rec_x, resource_rec_y, resource_rec_width, resource_rec_height, "Get Resource Recommendations")

career_rec_x, career_rec_y = student_x + 280, smart_fork_y + 70
career_rec_width, career_rec_height = 200, 50
draw_activity(career_rec_x, career_rec_y, career_rec_width, career_rec_height, "View Career Recommendations")

# Smart features join
smart_join_x, smart_join_y = student_x + 80, resource_rec_y + 100
draw_fork(smart_join_x, smart_join_y, 40, 10, horizontal=True)

# Study plan
study_plan_x, study_plan_y = student_x, smart_join_y + 70
study_plan_width, study_plan_height = 200, 50
draw_activity(study_plan_x, study_plan_y, study_plan_width, study_plan_height, "Follow Smart Study Plan")

# Teacher path activities
manage_students_x, manage_students_y = teacher_x, teacher_y + 100
manage_students_width, manage_students_height = 200, 50
draw_activity(manage_students_x, manage_students_y, manage_students_width, manage_students_height, "Manage Class Students")

create_assignment_x, create_assignment_y = teacher_x, manage_students_y + 100
create_assignment_width, create_assignment_height = 200, 50
draw_activity(create_assignment_x, create_assignment_y, create_assignment_width, create_assignment_height, "Create Assignment")

# Assignment management fork
assignment_fork_x, assignment_fork_y = teacher_x + 80, create_assignment_y + 100
draw_fork(assignment_fork_x, assignment_fork_y, 40, 10, horizontal=True)

# Assignment management (parallel)
monitor_submissions_x, monitor_submissions_y = teacher_x - 280, assignment_fork_y + 70
monitor_submissions_width, monitor_submissions_height = 200, 50
draw_activity(monitor_submissions_x, monitor_submissions_y, monitor_submissions_width, monitor_submissions_height, "Monitor Assignment Submissions")

grade_submissions_x, grade_submissions_y = teacher_x, assignment_fork_y + 70
grade_submissions_width, grade_submissions_height = 200, 50
draw_activity(grade_submissions_x, grade_submissions_y, grade_submissions_width, grade_submissions_height, "Grade Student Submissions")

post_notices_x, post_notices_y = teacher_x + 280, assignment_fork_y + 70
post_notices_width, post_notices_height = 200, 50
draw_activity(post_notices_x, post_notices_y, post_notices_width, post_notices_height, "Post Class Notices")

# Assignment management join
assignment_join_x, assignment_join_y = teacher_x + 80, grade_submissions_y + 100
draw_fork(assignment_join_x, assignment_join_y, 40, 10, horizontal=True)

# Calendar
calendar_x, calendar_y = teacher_x, assignment_join_y + 70
calendar_width, calendar_height = 200, 50
draw_activity(calendar_x, calendar_y, calendar_width, calendar_height, "Manage Academic Calendar")

# End nodes
student_end_x, student_end_y = student_x + 100, study_plan_y + 120
draw_end(student_end_x, student_end_y, 15)

teacher_end_x, teacher_end_y = teacher_x + 100, calendar_y + 120
draw_end(teacher_end_x, teacher_end_y, 15)

# Draw arrows
def draw_arrow(start_x, start_y, end_x, end_y, label=None):
    draw.line([(start_x, start_y), (end_x, end_y)], fill="black", width=1)
    
    # Calculate angle for arrowhead
    angle = np.arctan2(end_y - start_y, end_x - start_x)
    arrow_size = 10
    
    # Draw arrowhead
    arrow_x1 = end_x - arrow_size * np.cos(angle) - arrow_size * np.sin(angle)
    arrow_y1 = end_y - arrow_size * np.sin(angle) + arrow_size * np.cos(angle)
    arrow_x2 = end_x - arrow_size * np.cos(angle) + arrow_size * np.sin(angle)
    arrow_y2 = end_y - arrow_size * np.sin(angle) - arrow_size * np.cos(angle)
    
    draw.polygon([(end_x, end_y), (arrow_x1, arrow_y1), (arrow_x2, arrow_y2)], fill="black")
    
    # Add label if provided
    if label:
        mid_x = (start_x + end_x) // 2
        mid_y = (start_y + end_y) // 2
        
        # Adjust label position based on arrow direction
        if abs(end_x - start_x) > abs(end_y - start_y):
            # Horizontal arrow - place label above or below
            label_y = mid_y - 15 if mid_y > HEIGHT // 2 else mid_y + 15
            label_x = mid_x + 5
        else:
            # Vertical arrow - place label to the side
            label_x = mid_x + 15
            label_y = mid_y - 5
            
        # Add white background for text
        text_width = len(label) * 6
        text_height = 14
        draw.rectangle([(label_x - 3, label_y - 3), 
                       (label_x + text_width + 3, label_y + text_height)], 
                     outline=None, fill="white")
            
        draw.text((label_x, label_y), label, fill="blue", font=normal_font)

# Start to registration
draw_arrow(start_x, start_y + 15, signup_x + 100, signup_y)

# Registration to user type decision
draw_arrow(signup_x + 100, signup_y + signup_height, user_decision_x + 50, user_decision_y)

# Decision to student dashboard
draw_arrow(user_decision_x, user_decision_y + 50, student_x + 100, student_y, "Student")

# Decision to teacher dashboard
draw_arrow(user_decision_x + 100, user_decision_y + 50, teacher_x + 100, teacher_y, "Teacher")

# Student path arrows
draw_arrow(student_x + 100, student_y + student_height, view_teachers_x + 100, view_teachers_y)
draw_arrow(view_teachers_x + 100, view_teachers_y + view_teachers_height, join_class_x + 100, join_class_y)
draw_arrow(join_class_x + 100, join_class_y + join_class_height, view_assignments_x + 100, view_assignments_y)
draw_arrow(view_assignments_x + 100, view_assignments_y + view_assignments_height, assignment_decision_x + 50, assignment_decision_y)

# Assignment decision arrows
draw_arrow(assignment_decision_x + 50, assignment_decision_y + 100, complete_assignment_x + 100, complete_assignment_y, "Complete")
draw_arrow(assignment_decision_x + 100, assignment_decision_y + 50, view_assignments_x + 300, view_assignments_y + 25, "Skip")

# Connect skip back to assignments
points = [(view_assignments_x + 300, view_assignments_y + 25), 
          (view_assignments_x + 300, view_assignments_y - 25),
          (view_assignments_x + 100, view_assignments_y - 25),
          (view_assignments_x + 100, view_assignments_y)]
for i in range(len(points) - 1):
    draw.line([points[i], points[i+1]], fill="black", width=1)

# Complete assignment to check grades
draw_arrow(complete_assignment_x + 100, complete_assignment_y + complete_assignment_height, check_grades_x + 100, check_grades_y)

# Check grades to smart fork
draw_arrow(check_grades_x + 100, check_grades_y + check_grades_height, smart_fork_x + 20, smart_fork_y)

# Smart fork to parallel activities
draw_arrow(smart_fork_x + 20, smart_fork_y + 10, learning_style_x + 100, learning_style_y)
draw_arrow(smart_fork_x + 20, smart_fork_y + 10, resource_rec_x + 100, resource_rec_y)
draw_arrow(smart_fork_x + 20, smart_fork_y + 10, career_rec_x + 100, career_rec_y)

# Parallel activities to smart join
draw_arrow(learning_style_x + 100, learning_style_y + learning_style_height, smart_join_x + 20, smart_join_y)
draw_arrow(resource_rec_x + 100, resource_rec_y + resource_rec_height, smart_join_x + 20, smart_join_y)
draw_arrow(career_rec_x + 100, career_rec_y + career_rec_height, smart_join_x + 20, smart_join_y)

# Smart join to study plan
draw_arrow(smart_join_x + 20, smart_join_y + 10, study_plan_x + 100, study_plan_y)

# Study plan to end
draw_arrow(study_plan_x + 100, study_plan_y + study_plan_height, student_end_x, student_end_y)

# Teacher path arrows
draw_arrow(teacher_x + 100, teacher_y + teacher_height, manage_students_x + 100, manage_students_y)
draw_arrow(manage_students_x + 100, manage_students_y + manage_students_height, create_assignment_x + 100, create_assignment_y)
draw_arrow(create_assignment_x + 100, create_assignment_y + create_assignment_height, assignment_fork_x + 20, assignment_fork_y)

# Assignment fork to parallel activities
draw_arrow(assignment_fork_x + 20, assignment_fork_y + 10, monitor_submissions_x + 100, monitor_submissions_y)
draw_arrow(assignment_fork_x + 20, assignment_fork_y + 10, grade_submissions_x + 100, grade_submissions_y)
draw_arrow(assignment_fork_x + 20, assignment_fork_y + 10, post_notices_x + 100, post_notices_y)

# Parallel activities to assignment join
draw_arrow(monitor_submissions_x + 100, monitor_submissions_y + monitor_submissions_height, assignment_join_x + 20, assignment_join_y)
draw_arrow(grade_submissions_x + 100, grade_submissions_y + grade_submissions_height, assignment_join_x + 20, assignment_join_y)
draw_arrow(post_notices_x + 100, post_notices_y + post_notices_height, assignment_join_x + 20, assignment_join_y)

# Assignment join to calendar
draw_arrow(assignment_join_x + 20, assignment_join_y + 10, calendar_x + 100, calendar_y)

# Calendar to end
draw_arrow(calendar_x + 100, calendar_y + calendar_height, teacher_end_x, teacher_end_y)

# Add legend
legend_x, legend_y = 50, 1650
draw.rectangle((legend_x, legend_y, legend_x + 400, legend_y + 150), outline="black")
draw.text((legend_x + 10, legend_y + 10), "Legend:", fill="black", font=header_font)

# Activity
draw_activity(legend_x + 20, legend_y + 40, 150, 30, "Activity")
draw.text((legend_x + 180, legend_y + 45), "Activity Node", fill="black", font=normal_font)

# Decision
draw_decision(legend_x + 30, legend_y + 80, 50)
draw.text((legend_x + 180, legend_y + 95), "Decision Node", fill="black", font=normal_font)

# Start
draw_start(legend_x + 40, legend_y + 145, 15)
draw.text((legend_x + 60, legend_y + 140), "Start Node", fill="black", font=normal_font)

# End
draw_end(legend_x + 120, legend_y + 145, 15)
draw.text((legend_x + 140, legend_y + 140), "End Node", fill="black", font=normal_font)

# Fork/Join
draw_fork(legend_x + 220, legend_y + 140, 40, 10, horizontal=True)
draw.text((legend_x + 270, legend_y + 135), "Fork/Join Node", fill="black", font=normal_font)

# Save the image
image.save("activity_diagram.png")
print("Activity Diagram saved as activity_diagram.png") 