import matplotlib.pyplot as plt
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import os

# Create a User Flow Diagram for the Smart Education Tracking System
WIDTH, HEIGHT = 1800, 1200  # Increased canvas size for better spacing
image = Image.new('RGB', (WIDTH, HEIGHT), color='white')
draw = ImageDraw.Draw(image)

# Try to load font, use default if not available
try:
    title_font = ImageFont.truetype("arial.ttf", 22)
    header_font = ImageFont.truetype("arial.ttf", 18)
    normal_font = ImageFont.truetype("arial.ttf", 14)
    small_font = ImageFont.truetype("arial.ttf", 12)
except:
    title_font = ImageFont.load_default()
    header_font = ImageFont.load_default()
    normal_font = ImageFont.load_default()
    small_font = ImageFont.load_default()

# Draw title
draw.text((WIDTH//2-250, 30), "Smart Education Tracking System - User Flow Diagram", 
         fill="black", font=title_font)

# Function to draw boxes for screens/pages
def draw_screen(x, y, width, height, text, color="lightblue", is_action=False):
    if is_action:
        # Draw rounded rectangle for actions
        draw.rounded_rectangle([(x, y), (x + width, y + height)], radius=15, 
                            outline="black", fill=color, width=2)
    else:
        # Draw rectangle for screens
        draw.rectangle([(x, y), (x + width, y + height)], 
                    outline="black", fill=color, width=2)
    
    # Draw text
    lines = text.split('\n')
    total_height = len(lines) * 20
    start_y = y + (height - total_height) // 2
    
    for i, line in enumerate(lines):
        text_width = len(line) * 7
        draw.text((x + width//2 - text_width//2, start_y + i*20), 
                line, fill="black", font=normal_font)

# Function to draw arrows
def draw_arrow(start_x, start_y, end_x, end_y, text=None, curve=0):
    if curve == 0:
        # Draw straight line
        draw.line([(start_x, start_y), (end_x, end_y)], fill="black", width=2)
        
        # Calculate angle for arrowhead
        angle = np.arctan2(end_y - start_y, end_x - start_x)
        
    else:
        # Draw curved line
        # Calculate control point for curved line
        mid_x = (start_x + end_x) / 2
        mid_y = (start_y + end_y) / 2 + curve
        
        # Draw curved line using points along the quadratic Bezier curve
        points = []
        for t in np.linspace(0, 1, 50):
            # Quadratic Bezier curve formula
            x = (1-t)**2 * start_x + 2*(1-t)*t * mid_x + t**2 * end_x
            y = (1-t)**2 * start_y + 2*(1-t)*t * mid_y + t**2 * end_y
            points.append((x, y))
        
        for i in range(len(points) - 1):
            draw.line([points[i], points[i+1]], fill="black", width=2)
        
        # Calculate angle for arrowhead at the end point
        end_tangent_x = 2 * (1-0.98) * (mid_x - end_x) + 0.98 * 2 * (start_x - mid_x)
        end_tangent_y = 2 * (1-0.98) * (mid_y - end_y) + 0.98 * 2 * (start_y - mid_y)
        angle = np.arctan2(end_tangent_y, end_tangent_x) + np.pi
    
    # Draw arrowhead
    arrow_size = 15
    arrow_x1 = end_x - arrow_size * np.cos(angle - np.pi/6)
    arrow_y1 = end_y - arrow_size * np.sin(angle - np.pi/6)
    arrow_x2 = end_x - arrow_size * np.cos(angle + np.pi/6)
    arrow_y2 = end_y - arrow_size * np.sin(angle + np.pi/6)
    
    draw.polygon([(end_x, end_y), (arrow_x1, arrow_y1), (arrow_x2, arrow_y2)], 
                outline="black", fill="black")
    
    # Draw text label if provided
    if text:
        if curve == 0:
            # Adjust text position to avoid overlap
            text_x = (start_x + end_x) // 2 + 5
            text_y = (start_y + end_y) // 2 - 20
            
            # If arrow is mostly horizontal, place text above/below
            if abs(end_x - start_x) > abs(end_y - start_y):
                if end_y > start_y:
                    text_y = (start_y + end_y) // 2 - 25
                else:
                    text_y = (start_y + end_y) // 2 + 5
            # If arrow is mostly vertical, place text to right
            else:
                text_x = (start_x + end_x) // 2 + 10
        else:
            text_x = mid_x + 5
            text_y = mid_y - 15
            
        # Add white background for text with more padding
        text_width = len(text) * 6
        text_height = 20
        draw.rectangle([(text_x - 5, text_y - 5), 
                       (text_x + text_width + 5, text_y + text_height + 5)], 
                     outline=None, fill="white")
        
        draw.text((text_x, text_y), text, fill="black", font=small_font)

# Draw section headers
draw.text((WIDTH//4-100, 100), "STUDENT FLOW", fill="navy", font=header_font)
draw.text((3*WIDTH//4-100, 100), "TEACHER FLOW", fill="navy", font=header_font)

# Draw dividing line between flows
draw.line([(WIDTH//2, 90), (WIDTH//2, HEIGHT-70)], fill="gray", width=2)

# Student flow screens - Increased spacing between elements
login_screen_x, login_screen_y = WIDTH//4-100, 140
login_width, login_height = 200, 60
draw_screen(login_screen_x, login_screen_y, login_width, login_height, "Login / Register")

dashboard_x, dashboard_y = WIDTH//4-100, 240
dashboard_width, dashboard_height = 200, 60
draw_screen(dashboard_x, dashboard_y, dashboard_width, dashboard_height, "Student Dashboard", "lightyellow")

# Student branches - better horizontal spacing
profile_x, profile_y = WIDTH//4-400, 340
profile_width, profile_height = 180, 60
draw_screen(profile_x, profile_y, profile_width, profile_height, "Profile Management")

classes_x, classes_y = WIDTH//4-100, 340
classes_width, classes_height = 180, 60
draw_screen(classes_x, classes_y, classes_width, classes_height, "View Classes")

assignments_x, assignments_y = WIDTH//4+200, 340
assignments_width, assignments_height = 180, 60
draw_screen(assignments_x, assignments_y, assignments_width, assignments_height, "View Assignments")

# Student sub-flows - improved vertical spacing
join_class_x, join_class_y = WIDTH//4-100, 450
join_class_width, join_class_height = 180, 60
draw_screen(join_class_x, join_class_y, join_class_width, join_class_height, "Join Class", "lightgreen", True)

study_group_x, study_group_y = WIDTH//4-100, 560
study_group_width, study_group_height = 180, 60
draw_screen(study_group_x, study_group_y, study_group_width, study_group_height, "Join Study Group", "lightgreen", True)

submit_x, submit_y = WIDTH//4+200, 450
submit_width, submit_height = 180, 60
draw_screen(submit_x, submit_y, submit_width, submit_height, "Submit Assignment", "lightgreen", True)

grades_x, grades_y = WIDTH//4+200, 560
grades_width, grades_height = 180, 60
draw_screen(grades_x, grades_y, grades_width, grades_height, "View Grades")

ai_rec_x, ai_rec_y = WIDTH//4-400, 450
ai_rec_width, ai_rec_height = 180, 60
draw_screen(ai_rec_x, ai_rec_y, ai_rec_width, ai_rec_height, "AI Recommendations")

learning_style_x, learning_style_y = WIDTH//4-400, 560
learning_style_width, learning_style_height = 180, 60
draw_screen(learning_style_x, learning_style_y, learning_style_width, learning_style_height, "Learning Style\nAnalysis")

career_rec_x, career_rec_y = WIDTH//4-400, 670
career_rec_width, career_rec_height = 180, 60
draw_screen(career_rec_x, career_rec_y, career_rec_width, career_rec_height, "Career\nRecommendations")

study_plan_x, study_plan_y = WIDTH//4-100, 780
study_plan_width, study_plan_height = 200, 60
draw_screen(study_plan_x, study_plan_y, study_plan_width, study_plan_height, "Smart Study Plan", "lightpink")

messaging_x, messaging_y = WIDTH//4+200, 670
messaging_width, messaging_height = 180, 60
draw_screen(messaging_x, messaging_y, messaging_width, messaging_height, "Message Teachers")

leaderboard_x, leaderboard_y = WIDTH//4-100, 670
leaderboard_width, leaderboard_height = 180, 60
draw_screen(leaderboard_x, leaderboard_y, leaderboard_width, leaderboard_height, "View Leaderboard")

# Teacher flow screens
t_login_screen_x, t_login_screen_y = 3*WIDTH//4-100, 140
t_login_width, t_login_height = 200, 60
draw_screen(t_login_screen_x, t_login_screen_y, t_login_width, t_login_height, "Login / Register")

t_dashboard_x, t_dashboard_y = 3*WIDTH//4-100, 240
t_dashboard_width, t_dashboard_height = 200, 60
draw_screen(t_dashboard_x, t_dashboard_y, t_dashboard_width, t_dashboard_height, "Teacher Dashboard", "lightyellow")

# Teacher branches - better horizontal spacing
t_profile_x, t_profile_y = 3*WIDTH//4-400, 340
t_profile_width, t_profile_height = 180, 60
draw_screen(t_profile_x, t_profile_y, t_profile_width, t_profile_height, "Profile Management")

t_students_x, t_students_y = 3*WIDTH//4-100, 340
t_students_width, t_students_height = 180, 60
draw_screen(t_students_x, t_students_y, t_students_width, t_students_height, "Manage Students")

t_assignments_x, t_assignments_y = 3*WIDTH//4+200, 340
t_assignments_width, t_assignments_height = 180, 60
draw_screen(t_assignments_x, t_assignments_y, t_assignments_width, t_assignments_height, "Manage Assignments")

# Teacher sub-flows - improved vertical spacing
create_assignment_x, create_assignment_y = 3*WIDTH//4+200, 450
create_assignment_width, create_assignment_height = 180, 60
draw_screen(create_assignment_x, create_assignment_y, create_assignment_width, create_assignment_height, "Create Assignment", "lightgreen", True)

grade_assignment_x, grade_assignment_y = 3*WIDTH//4+200, 560
grade_assignment_width, grade_assignment_height = 180, 60
draw_screen(grade_assignment_x, grade_assignment_y, grade_assignment_width, grade_assignment_height, "Grade Assignments", "lightgreen", True)

enter_marks_x, enter_marks_y = 3*WIDTH//4-100, 450
enter_marks_width, enter_marks_height = 180, 60
draw_screen(enter_marks_x, enter_marks_y, enter_marks_width, enter_marks_height, "Enter Marks", "lightgreen", True)

view_performance_x, view_performance_y = 3*WIDTH//4-100, 560
view_performance_width, view_performance_height = 180, 60
draw_screen(view_performance_x, view_performance_y, view_performance_width, view_performance_height, "View Student\nPerformance")

post_notice_x, post_notice_y = 3*WIDTH//4-400, 450
post_notice_width, post_notice_height = 180, 60
draw_screen(post_notice_x, post_notice_y, post_notice_width, post_notice_height, "Post Class Notice", "lightgreen", True)

t_messaging_x, t_messaging_y = 3*WIDTH//4-400, 560
t_messaging_width, t_messaging_height = 180, 60
draw_screen(t_messaging_x, t_messaging_y, t_messaging_width, t_messaging_height, "Reply to Messages")

calendar_x, calendar_y = 3*WIDTH//4-100, 670
calendar_width, calendar_height = 200, 60
draw_screen(calendar_x, calendar_y, calendar_width, calendar_height, "Manage\nAcademic Calendar", "lightpink")

# Draw arrows for Student flow
draw_arrow(login_screen_x + login_width//2, login_screen_y + login_height, 
          dashboard_x + dashboard_width//2, dashboard_y, "Login Success")

# Dashboard to branches
draw_arrow(dashboard_x + dashboard_width//2 - 70, dashboard_y + dashboard_height, 
          profile_x + profile_width//2, profile_y, "View Profile")

draw_arrow(dashboard_x + dashboard_width//2, dashboard_y + dashboard_height, 
          classes_x + classes_width//2, classes_y, "View Classes")

draw_arrow(dashboard_x + dashboard_width//2 + 70, dashboard_y + dashboard_height, 
          assignments_x + assignments_width//2, assignments_y, "View Assignments")

# Profile to AI recommendations
draw_arrow(profile_x + profile_width//2, profile_y + profile_height, 
          ai_rec_x + ai_rec_width//2, ai_rec_y, "Get Recommendations")

# AI recommendations flows
draw_arrow(ai_rec_x + ai_rec_width//2, ai_rec_y + ai_rec_height, 
          learning_style_x + learning_style_width//2, learning_style_y, "Analyze")

draw_arrow(learning_style_x + learning_style_width//2, learning_style_y + learning_style_height, 
          career_rec_x + career_rec_width//2, career_rec_y, "Career Options")

# Classes to join class
draw_arrow(classes_x + classes_width//2, classes_y + classes_height, 
          join_class_x + join_class_width//2, join_class_y, "Select Class")

# Join class to study group
draw_arrow(join_class_x + join_class_width//2, join_class_y + join_class_height, 
          study_group_x + study_group_width//2, study_group_y, "Find Groups")

# Study group to leaderboard
draw_arrow(study_group_x + study_group_width//2, study_group_y + study_group_height, 
          leaderboard_x + leaderboard_width//2, leaderboard_y, "Check Rankings")

# Assignments to submit
draw_arrow(assignments_x + assignments_width//2, assignments_y + assignments_height, 
          submit_x + submit_width//2, submit_y, "Select to Submit")

# Submit to grades
draw_arrow(submit_x + submit_width//2, submit_y + submit_height, 
          grades_x + grades_width//2, grades_y, "Check Grades")

# Grades to messaging
draw_arrow(grades_x + grades_width//2, grades_y + grades_height, 
          messaging_x + messaging_width//2, messaging_y, "Contact Teacher")

# Smart study plan connections
draw_arrow(career_rec_x + career_rec_width, career_rec_y + career_rec_height//2, 
          study_plan_x, study_plan_y + study_plan_height//2, "Apply", 70)

draw_arrow(leaderboard_x + leaderboard_width//2, leaderboard_y + leaderboard_height, 
          study_plan_x + study_plan_width//4, study_plan_y, "Improve", 20)

draw_arrow(messaging_x, messaging_y + messaging_height//2, 
          study_plan_x + study_plan_width*3//4, study_plan_y, "Adjust Plan", 70)

# Draw arrows for Teacher flow
draw_arrow(t_login_screen_x + t_login_width//2, t_login_screen_y + t_login_height, 
          t_dashboard_x + t_dashboard_width//2, t_dashboard_y, "Login Success")

# Dashboard to branches
draw_arrow(t_dashboard_x + t_dashboard_width//2 - 70, t_dashboard_y + t_dashboard_height, 
          t_profile_x + t_profile_width//2, t_profile_y, "Manage Profile")

draw_arrow(t_dashboard_x + t_dashboard_width//2, t_dashboard_y + t_dashboard_height, 
          t_students_x + t_students_width//2, t_students_y, "View Students")

draw_arrow(t_dashboard_x + t_dashboard_width//2 + 70, t_dashboard_y + t_dashboard_height, 
          t_assignments_x + t_assignments_width//2, t_assignments_y, "Manage Assignments")

# Profile to post notice
draw_arrow(t_profile_x + t_profile_width//2, t_profile_y + t_profile_height, 
          post_notice_x + post_notice_width//2, post_notice_y, "Create Notice")

# Post notice to messaging
draw_arrow(post_notice_x + post_notice_width//2, post_notice_y + post_notice_height, 
          t_messaging_x + t_messaging_width//2, t_messaging_y, "Check Messages")

# Students to enter marks
draw_arrow(t_students_x + t_students_width//2, t_students_y + t_students_height, 
          enter_marks_x + enter_marks_width//2, enter_marks_y, "Enter Marks")

# Enter marks to view performance
draw_arrow(enter_marks_x + enter_marks_width//2, enter_marks_y + enter_marks_height, 
          view_performance_x + view_performance_width//2, view_performance_y, "View Analytics")

# Assignments to create
draw_arrow(t_assignments_x + t_assignments_width//2, t_assignments_y + t_assignments_height, 
          create_assignment_x + create_assignment_width//2, create_assignment_y, "Create New")

# Create to grade
draw_arrow(create_assignment_x + create_assignment_width//2, create_assignment_y + create_assignment_height, 
          grade_assignment_x + grade_assignment_width//2, grade_assignment_y, "Grade Submissions")

# Calendar connections
draw_arrow(t_messaging_x + t_messaging_width//2, t_messaging_y + t_messaging_height, 
          calendar_x + calendar_width//4, calendar_y, "Schedule Events", 20)

draw_arrow(view_performance_x + view_performance_width//2, view_performance_y + view_performance_height, 
          calendar_x + calendar_width//2, calendar_y, "Plan Activities", 20)

draw_arrow(grade_assignment_x, grade_assignment_y + grade_assignment_height//2, 
          calendar_x + calendar_width*3//4, calendar_y, "Set Deadlines", 70)

# Add legend
legend_x, legend_y = WIDTH//2 - 300, HEIGHT - 150
draw.rectangle([(legend_x, legend_y), (legend_x + 600, legend_y + 80)], outline="black")
draw.text((legend_x + 10, legend_y + 10), "Legend:", fill="black", font=header_font)

# Screen
draw_screen(legend_x + 100, legend_y + 20, 100, 40, "Screen", "lightblue")
draw.text((legend_x + 210, legend_y + 30), "System Page/Screen", fill="black", font=normal_font)

# Action
draw_screen(legend_x + 350, legend_y + 20, 100, 40, "Action", "lightgreen", True)
draw.text((legend_x + 460, legend_y + 30), "User Action", fill="black", font=normal_font)

# Save the image
image.save("user_flow_diagram.png")
print("User Flow Diagram saved as user_flow_diagram.png") 