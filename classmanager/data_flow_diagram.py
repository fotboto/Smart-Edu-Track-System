import matplotlib.pyplot as plt
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import os

# Create a data flow diagram for the Smart Education Tracking System
WIDTH, HEIGHT = 1800, 1500  # Further increased canvas size for better spacing
image = Image.new('RGB', (WIDTH, HEIGHT), color='white')
draw = ImageDraw.Draw(image)

# Try to load font, use default if not available
try:
    title_font = ImageFont.truetype("arial.ttf", 24)
    header_font = ImageFont.truetype("arial.ttf", 20)
    normal_font = ImageFont.truetype("arial.ttf", 16)
    small_font = ImageFont.truetype("arial.ttf", 14)
except:
    title_font = ImageFont.load_default()
    header_font = ImageFont.load_default()
    normal_font = ImageFont.load_default()
    small_font = ImageFont.load_default()

# Draw title
draw.text((WIDTH//2-300, 40), "Smart Education Tracking System - Data Flow Diagram", 
         fill="black", font=title_font)

# Draw entities (external sources/destinations)
def draw_entity(x, y, width, height, text):
    # Draw rectangle
    draw.rectangle([(x, y), (x + width, y + height)], 
                 outline="black", fill="lightblue", width=2)
    
    # Draw text
    lines = text.split('\n')
    line_height = 24  # Increased line height
    total_text_height = len(lines) * line_height
    text_start_y = y + (height - total_text_height) // 2  # Center text vertically
    
    for i, line in enumerate(lines):
        text_width = len(line) * 8  # Adjusted for larger font
        draw.text((x + width//2 - text_width//2, text_start_y + i*line_height), 
                 line, fill="black", font=normal_font)

# Draw processes (transforms)
def draw_process(x, y, radius, text):
    # Draw circle
    draw.ellipse([(x - radius, y - radius), (x + radius, y + radius)], 
               outline="black", fill="lightgreen", width=2)
    
    # Draw text
    lines = text.split('\n')
    line_height = 24  # Increased line height
    total_text_height = len(lines) * line_height
    text_start_y = y - total_text_height//2  # Center text vertically
    
    for i, line in enumerate(lines):
        text_width = len(line) * 8  # Adjusted for larger font
        draw.text((x - text_width//2, text_start_y + i*line_height), 
                 line, fill="black", font=normal_font)

# Draw data stores
def draw_datastore(x, y, width, height, text):
    # Draw open rectangle
    draw.rectangle([(x, y), (x + width, y + height)], 
                 outline="black", fill="lightyellow", width=2)
    
    # Draw line to separate ID
    draw.line([(x + 60, y), (x + 60, y + height)], fill="black", width=2)
    
    # Extract ID and name
    parts = text.split(':')
    id_text = parts[0]
    name_text = parts[1] if len(parts) > 1 else ""
    
    # Center ID text vertically
    id_text_width = len(id_text) * 8
    draw.text((x + 30 - id_text_width//2, y + height//2 - 12), 
             id_text, fill="black", font=normal_font)
    
    # Calculate maximum space for name (adjust based on available width)
    max_text_width = width - 70
    
    # If name is too long, split into multiple lines
    if len(name_text) * 8 > max_text_width:
        words = name_text.split()
        lines = []
        current_line = ""
        
        for word in words:
            if len(current_line + " " + word) * 8 <= max_text_width:
                current_line += (" " + word if current_line else word)
            else:
                lines.append(current_line)
                current_line = word
        
        if current_line:
            lines.append(current_line)
            
        # Draw each line of the name
        for i, line in enumerate(lines):
            line_y = y + height//2 - (len(lines) * 18)//2 + i * 18
            draw.text((x + 70, line_y), line, fill="black", font=normal_font)
    else:
        # Draw name as a single line
        draw.text((x + 70, y + height//2 - 12), name_text, fill="black", font=normal_font)

# Draw data flows (arrows)
def draw_dataflow(start_x, start_y, end_x, end_y, text, curved=False, curve_direction=1, curve_strength=50):
    # Draw arrow
    if curved:
        # Calculate control point for curved line
        mid_x = (start_x + end_x) / 2
        mid_y = (start_y + end_y) / 2
        
        # Offset control point perpendicular to line
        angle = np.arctan2(end_y - start_y, end_x - start_x) + (np.pi/2 * curve_direction)
        control_x = mid_x + curve_strength * np.cos(angle)
        control_y = mid_y + curve_strength * np.sin(angle)
        
        # Draw curved line using points along the quadratic Bezier curve
        points = []
        for t in np.linspace(0, 1, 100):
            # Quadratic Bezier curve formula
            x = (1-t)**2 * start_x + 2*(1-t)*t * control_x + t**2 * end_x
            y = (1-t)**2 * start_y + 2*(1-t)*t * control_y + t**2 * end_y
            points.append((x, y))
        
        for i in range(len(points) - 1):
            draw.line([points[i], points[i+1]], fill="black", width=2)  # Increased line width
        
        # Calculate direction for arrowhead
        t = 0.97  # Close to end point
        dx = (1-t) * 2 * (control_x - end_x) + t * 2 * (start_x - control_x)
        dy = (1-t) * 2 * (control_y - end_y) + t * 2 * (start_y - control_y)
        angle = np.arctan2(dy, dx)
    else:
        # Draw straight line
        draw.line([(start_x, start_y), (end_x, end_y)], fill="black", width=2)  # Increased line width
        angle = np.arctan2(end_y - start_y, end_x - start_x)
    
    # Draw arrowhead
    arrow_size = 12  # Increased arrow size
    arrow_x1 = end_x - arrow_size * np.cos(angle) - arrow_size/2 * np.sin(angle)
    arrow_y1 = end_y - arrow_size * np.sin(angle) + arrow_size/2 * np.cos(angle)
    arrow_x2 = end_x - arrow_size * np.cos(angle) + arrow_size/2 * np.sin(angle)
    arrow_y2 = end_y - arrow_size * np.sin(angle) - arrow_size/2 * np.cos(angle)
    
    draw.polygon([(end_x, end_y), (arrow_x1, arrow_y1), (arrow_x2, arrow_y2)], 
                outline="black", fill="black")
    
    # Draw text label with improved positioning
    if curved:
        # Calculate a point along the curve for text positioning
        t_text = 0.5  # Position text at midpoint of curve
        text_pos_x = (1-t_text)**2 * start_x + 2*(1-t_text)*t_text * control_x + t_text**2 * end_x
        text_pos_y = (1-t_text)**2 * start_y + 2*(1-t_text)*t_text * control_y + t_text**2 * end_y
        
        # Add small offset to avoid directly overlapping the line
        text_x = text_pos_x + 15 * np.cos(angle + np.pi/2)
        text_y = text_pos_y + 15 * np.sin(angle + np.pi/2)
    else:
        # Adjust text position for straight arrows
        text_x = start_x + (end_x - start_x) * 0.5  # Midpoint
        text_y = start_y + (end_y - start_y) * 0.5  # Midpoint
        
        # Add offset perpendicular to line
        perpendicular_angle = angle + np.pi/2
        offset = 25  # Increased offset for better visibility
        text_x += offset * np.cos(perpendicular_angle)
        text_y += offset * np.sin(perpendicular_angle)
    
    # Add white background with border for text with more padding
    text_width = len(text) * 8  # Adjusted for larger font
    text_height = 24  # Increased height
    draw.rectangle([(text_x - 10, text_y - 8), 
                   (text_x + text_width + 10, text_y + text_height + 2)], 
                 outline="gray", fill="white")
    
    draw.text((text_x, text_y), text, fill="black", font=normal_font)  # Using normal_font instead of small_font

# Define coordinates for diagram elements with better spacing

# External entities - adjusted positions with more space
student_x, student_y = 100, 220
student_width, student_height = 180, 80

teacher_x, teacher_y = 1500, 220
teacher_width, teacher_height = 180, 80

admin_x, admin_y = 750, 1300
admin_width, admin_height = 180, 80

# Main processes - increased spacing between processes and increased radius
auth_process_x, auth_process_y = 750, 280
auth_process_radius = 90

student_mgmt_x, student_mgmt_y = 300, 550
student_mgmt_radius = 90

teacher_mgmt_x, teacher_mgmt_y = 1200, 550
teacher_mgmt_radius = 90

assignment_x, assignment_y = 450, 800
assignment_radius = 90

marks_x, marks_y = 1050, 800
marks_radius = 90

ai_process_x, ai_process_y = 750, 1050
ai_process_radius = 90

# Data stores - adjusted positions and increased sizes
user_data_x, user_data_y = 750, 420
user_data_width, user_data_height = 300, 60

student_data_x, student_data_y = 150, 650
student_data_width, student_data_height = 300, 60

teacher_data_x, teacher_data_y = 1350, 650
teacher_data_width, teacher_data_height = 300, 60

assignment_data_x, assignment_data_y = 200, 950
assignment_data_width, assignment_data_height = 300, 60

marks_data_x, marks_data_y = 1300, 950
marks_data_width, marks_data_height = 300, 60

ai_data_x, ai_data_y = 600, 1200
ai_data_width, ai_data_height = 500, 60

# Draw external entities
draw_entity(student_x, student_y, student_width, student_height, "Student")
draw_entity(teacher_x, teacher_y, teacher_width, teacher_height, "Teacher")
draw_entity(admin_x, admin_y, admin_width, admin_height, "Admin")

# Draw processes
draw_process(auth_process_x, auth_process_y, auth_process_radius, "1.0\nUser\nAuthentication")
draw_process(student_mgmt_x, student_mgmt_y, student_mgmt_radius, "2.0\nStudent\nManagement")
draw_process(teacher_mgmt_x, teacher_mgmt_y, teacher_mgmt_radius, "3.0\nTeacher\nManagement")
draw_process(assignment_x, assignment_y, assignment_radius, "4.0\nAssignment\nManagement")
draw_process(marks_x, marks_y, marks_radius, "5.0\nMarks\nManagement")
draw_process(ai_process_x, ai_process_y, ai_process_radius, "6.0\nAI\nRecommendation\nEngine")

# Draw data stores
draw_datastore(user_data_x, user_data_y, user_data_width, user_data_height, "D1: User Accounts")
draw_datastore(student_data_x, student_data_y, student_data_width, student_data_height, "D2: Student Profiles")
draw_datastore(teacher_data_x, teacher_data_y, teacher_data_width, teacher_data_height, "D3: Teacher Profiles")
draw_datastore(assignment_data_x, assignment_data_y, assignment_data_width, assignment_data_height, "D4: Assignments")
draw_datastore(marks_data_x, marks_data_y, marks_data_width, marks_data_height, "D5: Student Marks")
draw_datastore(ai_data_x, ai_data_y, ai_data_width, ai_data_height, "D6: Learning Resources & Recommendations")

# Draw data flows (connecting everything) with adjusted coordinates

# Student to Authentication
draw_dataflow(student_x + student_width, student_y + 40, 
             auth_process_x - auth_process_radius, auth_process_y, 
             "Login Credentials")

# Teacher to Authentication
draw_dataflow(teacher_x, teacher_y + 40, 
             auth_process_x + auth_process_radius, auth_process_y, 
             "Login Credentials")

# Authentication to Data Store
draw_dataflow(auth_process_x, auth_process_y + auth_process_radius, 
             user_data_x + user_data_width//2, user_data_y, 
             "Verify/Update Credentials")

# Authentication to Student Management
draw_dataflow(auth_process_x - 60, auth_process_y + 60, 
             student_mgmt_x + 60, student_mgmt_y - 60, 
             "Authenticated Student", curved=True, curve_direction=-1, curve_strength=100)

# Authentication to Teacher Management
draw_dataflow(auth_process_x + 60, auth_process_y + 60, 
             teacher_mgmt_x - 60, teacher_mgmt_y - 60, 
             "Authenticated Teacher", curved=True, curve_direction=1, curve_strength=100)

# Student Management to Student Data
draw_dataflow(student_mgmt_x, student_mgmt_y + student_mgmt_radius, 
             student_data_x + student_data_width//2, student_data_y, 
             "Student Profile Data")

# Teacher Management to Teacher Data
draw_dataflow(teacher_mgmt_x, teacher_mgmt_y + teacher_mgmt_radius, 
             teacher_data_x + teacher_data_width//2, teacher_data_y, 
             "Teacher Profile Data")

# Student Management to Assignment Management
draw_dataflow(student_mgmt_x + student_mgmt_radius, student_mgmt_y + 30, 
             assignment_x - assignment_radius, assignment_y - 30, 
             "Assignment Requests", curved=True, curve_direction=1, curve_strength=100)

# Teacher Management to Assignment Management
draw_dataflow(teacher_mgmt_x - teacher_mgmt_radius, teacher_mgmt_y + 30, 
             assignment_x + assignment_radius, assignment_y - 30, 
             "Create/Update Assignments", curved=True, curve_direction=-1, curve_strength=100)

# Assignment Management to Assignment Data
draw_dataflow(assignment_x - 40, assignment_y + assignment_radius, 
             assignment_data_x + assignment_data_width//2, assignment_data_y, 
             "Assignment Data")

# Teacher Management to Marks Management
draw_dataflow(teacher_mgmt_x - 40, teacher_mgmt_y + teacher_mgmt_radius, 
             marks_x, marks_y - marks_radius, 
             "Enter Marks")

# Student Management to Marks Management
draw_dataflow(student_mgmt_x + student_mgmt_radius, student_mgmt_y + 50, 
             marks_x - marks_radius, marks_y - 30, 
             "View Marks", curved=True, curve_direction=1, curve_strength=100)

# Marks Management to Marks Data
draw_dataflow(marks_x + 40, marks_y + marks_radius, 
             marks_data_x + marks_data_width//2, marks_data_y, 
             "Student Marks Data")

# Student Data to AI Process
draw_dataflow(student_data_x + student_data_width//2, student_data_y + student_data_height, 
             ai_process_x - 60, ai_process_y - 60, 
             "Student Profile", curved=True, curve_direction=-1, curve_strength=100)

# Marks Data to AI Process
draw_dataflow(marks_data_x + marks_data_width//2, marks_data_y + marks_data_height, 
             ai_process_x + 60, ai_process_y - 60, 
             "Performance Data", curved=True, curve_direction=1, curve_strength=100)

# AI Process to AI Data
draw_dataflow(ai_process_x, ai_process_y + ai_process_radius, 
             ai_data_x + ai_data_width//2, ai_data_y, 
             "Generate Recommendations")

# AI Data to Student Management
draw_dataflow(ai_data_x, ai_data_y + ai_data_height//2, 
             student_mgmt_x, student_mgmt_y + student_mgmt_radius + 30, 
             "Smart Recommendations", curved=True, curve_direction=-1, curve_strength=200)

# Admin to Data Stores
draw_dataflow(admin_x + admin_width//2, admin_y, 
             user_data_x + user_data_width//2, user_data_y + user_data_height, 
             "Manage System Data", curved=True, curve_direction=1, curve_strength=250)

# Add legend with improved positioning
legend_x, legend_y = 100, 80
draw.rectangle([(legend_x, legend_y), (legend_x + 430, legend_y + 180)], outline="black")
draw.text((legend_x + 20, legend_y + 15), "Legend:", fill="black", font=header_font)

# Entity
draw.rectangle([(legend_x + 30, legend_y + 50), (legend_x + 100, legend_y + 80)], 
             outline="black", fill="lightblue", width=2)
draw.text((legend_x + 110, legend_y + 55), "External Entity", fill="black", font=normal_font)

# Process
draw.ellipse([(legend_x + 30, legend_y + 90), (legend_x + 100, legend_y + 130)], 
           outline="black", fill="lightgreen", width=2)
draw.text((legend_x + 110, legend_y + 100), "Process", fill="black", font=normal_font)

# Data Store
draw.rectangle([(legend_x + 210, legend_y + 50), (legend_x + 350, legend_y + 80)], 
             outline="black", fill="lightyellow", width=2)
draw.line([(legend_x + 260, legend_y + 50), (legend_x + 260, legend_y + 80)], fill="black", width=2)
draw.text((legend_x + 270, legend_y + 55), "Data Store", fill="black", font=normal_font)

# Data Flow
draw.line([(legend_x + 230, legend_y + 100), (legend_x + 330, legend_y + 100)], fill="black", width=2)
draw.polygon([(legend_x + 330, legend_y + 100), 
             (legend_x + 315, legend_y + 95), 
             (legend_x + 315, legend_y + 105)], 
           outline="black", fill="black")
draw.text((legend_x + 230, legend_y + 115), "Data Flow", fill="black", font=normal_font)

# Get current directory and save the image to a specific absolute path
absolute_path = os.path.abspath("data_flow_diagram.png")
image.save("data_flow_diagram.png")
print(f"Data Flow Diagram saved as {absolute_path}")
print(f"Current directory: {os.getcwd()}")
print(f"Directory contents: {os.listdir('.')}")
print(f"Is file created? {os.path.exists('data_flow_diagram.png')}") 