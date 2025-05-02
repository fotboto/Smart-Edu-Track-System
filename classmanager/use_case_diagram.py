import matplotlib.pyplot as plt
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import os

# Create a use case diagram for the Smart Education Tracking System
WIDTH, HEIGHT = 1800, 1600  # Further increased canvas size for better spacing
image = Image.new('RGB', (WIDTH, HEIGHT), color='white')
draw = ImageDraw.Draw(image)

# Try to load font, use default if not available
try:
    title_font = ImageFont.truetype("arial.ttf", 24)
    header_font = ImageFont.truetype("arial.ttf", 20)
    normal_font = ImageFont.truetype("arial.ttf", 18)
    small_font = ImageFont.truetype("arial.ttf", 16)
except:
    title_font = ImageFont.load_default()
    header_font = ImageFont.load_default()
    normal_font = ImageFont.load_default()
    small_font = ImageFont.load_default()

# Draw title
draw.text((WIDTH//2-300, 30), "Smart Education Tracking System - Use Case Diagram", 
         fill="black", font=title_font)

# Draw system boundary
bound_x, bound_y = 450, 150
bound_width, bound_height = 1100, 1250
draw.rectangle([(bound_x, bound_y), (bound_x + bound_width, bound_y + bound_height)], 
             outline="black", width=2)
draw.text((bound_x + bound_width//2 - 175, bound_y + 20), 
         "Smart Education Tracking System", fill="black", font=header_font)

# Draw actors
def draw_actor(x, y, name):
    # Draw circle for head
    radius = 25
    draw.ellipse([(x-radius, y-radius), (x+radius, y+radius)], outline="black", width=2)
    
    # Draw body
    body_height = 70
    draw.line([(x, y+radius), (x, y+radius+body_height)], fill="black", width=2)
    
    # Draw arms
    arm_length = 40
    arm_height = y+radius+25
    draw.line([(x-arm_length, arm_height), (x+arm_length, arm_height)], fill="black", width=2)
    
    # Draw legs
    leg_height = 60
    leg_offset = 40
    leg_y = y + radius + body_height
    draw.line([(x, leg_y), (x-leg_offset, leg_y+leg_height)], fill="black", width=2)
    draw.line([(x, leg_y), (x+leg_offset, leg_y+leg_height)], fill="black", width=2)
    
    # Draw name with improved text centering
    text_width = draw.textlength(name, font=normal_font)
    draw.text((x-text_width//2, y+radius+body_height+leg_height+15), 
             name, fill="black", font=normal_font)
    
    return y+radius+body_height+leg_height+15 + 40  # return bottom y coord of actor + padding

# Draw use cases
def draw_use_case(x, y, width, height, text):
    # Draw ellipse
    draw.ellipse([(x, y), (x+width, y+height)], outline="black", fill="lightblue", width=2)
    
    # Calculate text dimensions to center properly
    lines = text.split('\n')
    line_height = 26
    total_height = len(lines) * line_height
    text_y = y + (height - total_height) // 2
    
    # Draw each line of text centered
    for i, line in enumerate(lines):
        text_width = draw.textlength(line, font=normal_font)
        draw.text((x + width//2 - text_width//2, text_y + i*line_height), 
                 line, fill="black", font=normal_font)
    
    return x, y, x+width, y+height  # return bounding box coordinates

# Draw relationship lines
def draw_relationship(start_x, start_y, end_x, end_y, text=None, style="solid", arrow_end=False):
    # Draw line based on style
    if style == "solid":
        draw.line([(start_x, start_y), (end_x, end_y)], fill="black", width=2)
    elif style == "dashed":
        # Draw dashed line
        dash_length = 12
        distance = ((end_x - start_x)**2 + (end_y - start_y)**2)**0.5
        dx = (end_x - start_x) / distance
        dy = (end_y - start_y) / distance
        
        i = 0
        while i < distance:
            start_dash = min(i, distance)
            end_dash = min(i + dash_length, distance)
            
            if i % (dash_length * 2) == 0:  # Draw dash for every other segment
                draw.line([
                    (start_x + dx * start_dash, start_y + dy * start_dash),
                    (start_x + dx * end_dash, start_y + dy * end_dash)
                ], fill="black", width=2)
            
            i += dash_length
    
    # Draw arrow if needed
    if arrow_end:
        # Calculate arrow angle
        angle = np.arctan2(end_y - start_y, end_x - start_x)
        
        # Draw arrowhead
        arrow_size = 15
        arrow_x1 = end_x - arrow_size * np.cos(angle) - arrow_size/2 * np.sin(angle)
        arrow_y1 = end_y - arrow_size * np.sin(angle) + arrow_size/2 * np.cos(angle)
        arrow_x2 = end_x - arrow_size * np.cos(angle) + arrow_size/2 * np.sin(angle)
        arrow_y2 = end_y - arrow_size * np.sin(angle) - arrow_size/2 * np.cos(angle)
        
        draw.polygon([(end_x, end_y), (arrow_x1, arrow_y1), (arrow_x2, arrow_y2)], 
                    outline="black", fill="black")
    
    # Draw relationship text if provided
    if text:
        # Position text alongside line
        mid_x = (start_x + end_x) / 2
        mid_y = (start_y + end_y) / 2
        
        # Offset text to not overlap line
        offset = 30  # Increased offset
        angle = np.arctan2(end_y - start_y, end_x - start_x)
        perp_angle = angle + np.pi/2
        text_x = mid_x + offset * np.cos(perp_angle)
        text_y = mid_y + offset * np.sin(perp_angle) - 15  # Move up slightly
        
        # Add white background with border for text legibility
        text_width = draw.textlength(text, font=normal_font)
        text_height = 30
        draw.rectangle([
            (text_x - 10, text_y - 5), 
            (text_x + text_width + 10, text_y + text_height)
        ], fill="white", outline="gray")
        
        # Draw text with normal_font (larger) and in blue color for better visibility
        draw.text((text_x, text_y), text, fill="blue", font=normal_font)

# Add legend
legend_x, legend_y = 100, 80
legend_width, legend_height = 400, 200
draw.rectangle([(legend_x, legend_y), (legend_x + legend_width, legend_y + legend_height)], 
             outline="black", width=1)
draw.text((legend_x + 20, legend_y + 15), "Legend:", fill="black", font=header_font)

# Draw actor in legend
mini_actor_x, mini_actor_y = legend_x + 50, legend_y + 70
radius = 15
draw.ellipse([(mini_actor_x-radius, mini_actor_y-radius), 
             (mini_actor_x+radius, mini_actor_y+radius)], outline="black", width=2)
draw.line([(mini_actor_x, mini_actor_y+radius), 
          (mini_actor_x, mini_actor_y+radius+30)], fill="black", width=2)
draw.line([(mini_actor_x-20, mini_actor_y+radius+15), 
          (mini_actor_x+20, mini_actor_y+radius+15)], fill="black", width=2)
draw.line([(mini_actor_x, mini_actor_y+radius+30), 
          (mini_actor_x-15, mini_actor_y+radius+50)], fill="black", width=2)
draw.line([(mini_actor_x, mini_actor_y+radius+30), 
          (mini_actor_x+15, mini_actor_y+radius+50)], fill="black", width=2)
draw.text((mini_actor_x + 40, mini_actor_y + 10), "Actor", fill="black", font=normal_font)

# Draw use case in legend
mini_usecase_x, mini_usecase_y = legend_x + 220, legend_y + 70
draw.ellipse([(mini_usecase_x, mini_usecase_y), 
             (mini_usecase_x+100, mini_usecase_y+40)], 
           outline="black", fill="lightblue", width=2)
draw.text((mini_usecase_x+25, mini_usecase_y+10), "Use Case", fill="black", font=normal_font)

# Draw relationships in legend
# Association
legend_start_x, legend_start_y = legend_x + 50, legend_y + 130
legend_end_x, legend_end_y = legend_x + 120, legend_y + 130
draw.line([(legend_start_x, legend_start_y), (legend_end_x, legend_end_y)], 
         fill="black", width=2)
draw.text((legend_end_x + 15, legend_start_y - 5), "Association", fill="black", font=normal_font)

# Include/Extend
legend_start_x, legend_start_y = legend_x + 50, legend_y + 170
legend_end_x, legend_end_y = legend_x + 120, legend_y + 170
# Draw dashed line
dash_length = 12
distance = legend_end_x - legend_start_x
i = 0
while i < distance:
    if i % (dash_length * 2) == 0:
        draw.line([
            (legend_start_x + i, legend_start_y),
            (legend_start_x + min(i + dash_length, distance), legend_start_y)
        ], fill="black", width=2)
    i += dash_length

# Draw arrow
arrow_size = 12
draw.polygon([
    (legend_end_x, legend_end_y),
    (legend_end_x - arrow_size, legend_end_y - arrow_size/2),
    (legend_end_x - arrow_size, legend_end_y + arrow_size/2)
], outline="black", fill="black")

# Draw Include/Extend text with white background and blue text
include_text = "Include/Extend"
text_width = draw.textlength(include_text, font=normal_font)
text_x = legend_end_x + 15
text_y = legend_start_y - 5
draw.rectangle([
    (text_x - 5, text_y - 5),
    (text_x + text_width + 5, text_y + 25)
], fill="white", outline="gray")
draw.text((text_x, text_y), include_text, fill="blue", font=normal_font)

# Draw actors with greater spacing
student_x, student_y = 200, 350
teacher_x, teacher_y = 200, 750
admin_x, admin_y = 200, 1150
student_bottom = draw_actor(student_x, student_y, "Student")
teacher_bottom = draw_actor(teacher_x, teacher_y, "Teacher")
admin_bottom = draw_actor(admin_x, admin_y, "Admin")

# Draw use cases with larger size and improved spacing
usecase_width, usecase_height = 280, 80
margin = 120  # Increased vertical margin between use cases

# Placement coordinates for use cases with more horizontal spacing
uc1_x, uc1_y = 600, 180
uc2_x, uc2_y = 1000, 180
uc3_x, uc3_y = 600, 280
uc4_x, uc4_y = 1000, 280
uc5_x, uc5_y = 600, 400
uc6_x, uc6_y = 1000, 400
uc7_x, uc7_y = 600, 520
uc8_x, uc8_y = 1000, 520
uc9_x, uc9_y = 600, 640
uc10_x, uc10_y = 1000, 640
uc11_x, uc11_y = 600, 760
uc12_x, uc12_y = 1000, 760
uc13_x, uc13_y = 600, 880
uc14_x, uc14_y = 1000, 880
uc15_x, uc15_y = 600, 1000
uc16_x, uc16_y = 1000, 1000
uc17_x, uc17_y = 600, 1120
uc18_x, uc18_y = 1000, 1120
uc19_x, uc19_y = 600, 1240
uc20_x, uc20_y = 1000, 1240
uc21_x, uc21_y = 800, 1360

# Draw all use cases with text properly centered
uc1_box = draw_use_case(uc1_x, uc1_y, usecase_width, usecase_height, "Sign Up / Login")
uc2_box = draw_use_case(uc2_x, uc2_y, usecase_width, usecase_height, "Recover Account")
uc3_box = draw_use_case(uc3_x, uc3_y, usecase_width, usecase_height, "View/Update\nProfile")
uc4_box = draw_use_case(uc4_x, uc4_y, usecase_width, usecase_height, "Manage\nPreferences")
uc5_box = draw_use_case(uc5_x, uc5_y, usecase_width, usecase_height, "Browse\nAssignments")
uc6_box = draw_use_case(uc6_x, uc6_y, usecase_width, usecase_height, "Create\nAssignments")
uc7_box = draw_use_case(uc7_x, uc7_y, usecase_width, usecase_height, "Submit\nAssignments")
uc8_box = draw_use_case(uc8_x, uc8_y, usecase_width, usecase_height, "Grade\nAssignments")
uc9_box = draw_use_case(uc9_x, uc9_y, usecase_width, usecase_height, "View Grades")
uc10_box = draw_use_case(uc10_x, uc10_y, usecase_width, usecase_height, "Input Grades")
uc11_box = draw_use_case(uc11_x, uc11_y, usecase_width, usecase_height, "Generate\nPerformance Report")
uc12_box = draw_use_case(uc12_x, uc12_y, usecase_width, usecase_height, "Provide\nFeedback")
uc13_box = draw_use_case(uc13_x, uc13_y, usecase_width, usecase_height, "View\nRecommendations")
uc14_box = draw_use_case(uc14_x, uc14_y, usecase_width, usecase_height, "Manage\nResources")
uc15_box = draw_use_case(uc15_x, uc15_y, usecase_width, usecase_height, "Attend\nClasses")
uc16_box = draw_use_case(uc16_x, uc16_y, usecase_width, usecase_height, "Manage\nAttendance")
uc17_box = draw_use_case(uc17_x, uc17_y, usecase_width, usecase_height, "View\nStatistics")
uc18_box = draw_use_case(uc18_x, uc18_y, usecase_width, usecase_height, "Generate\nReports")
uc19_box = draw_use_case(uc19_x, uc19_y, usecase_width, usecase_height, "Manage\nUsers")
uc20_box = draw_use_case(uc20_x, uc20_y, usecase_width, usecase_height, "Manage\nClasses")
uc21_box = draw_use_case(uc21_x, uc21_y, usecase_width, usecase_height, "System\nBackup/Restore")

# Draw relationships for student with varying starting points to prevent overlap
draw_relationship(student_x + 30, student_y + 50, uc1_box[0], uc1_box[1] + usecase_height//2)
draw_relationship(student_x + 35, student_y + 70, uc3_box[0], uc3_box[1] + usecase_height//2)
draw_relationship(student_x + 40, student_y + 90, uc5_box[0], uc5_box[1] + usecase_height//2)
draw_relationship(student_x + 45, student_y + 110, uc7_box[0], uc7_box[1] + usecase_height//2)
draw_relationship(student_x + 50, student_y + 130, uc9_box[0], uc9_box[1] + usecase_height//2)
draw_relationship(student_x + 55, student_y + 150, uc13_box[0], uc13_box[1] + usecase_height//2)
draw_relationship(student_x + 60, student_y + 170, uc15_box[0], uc15_box[1] + usecase_height//2)

# Draw relationships for teacher with varying starting points
draw_relationship(teacher_x + 30, teacher_y + 50, uc1_box[0], uc1_box[1] + usecase_height//2)
draw_relationship(teacher_x + 35, teacher_y + 70, uc3_box[0], uc3_box[1] + usecase_height//2)
draw_relationship(teacher_x + 40, teacher_y + 90, uc6_box[0], uc6_box[1] + usecase_height//2)
draw_relationship(teacher_x + 45, teacher_y + 110, uc8_box[0], uc8_box[1] + usecase_height//2)
draw_relationship(teacher_x + 50, teacher_y + 130, uc10_box[0], uc10_box[1] + usecase_height//2)
draw_relationship(teacher_x + 55, teacher_y + 150, uc11_box[0], uc11_box[1] + usecase_height//2)
draw_relationship(teacher_x + 60, teacher_y + 170, uc12_box[0], uc12_box[1] + usecase_height//2)
draw_relationship(teacher_x + 65, teacher_y + 190, uc14_box[0], uc14_box[1] + usecase_height//2)
draw_relationship(teacher_x + 70, teacher_y + 210, uc16_box[0], uc16_box[1] + usecase_height//2)
draw_relationship(teacher_x + 75, teacher_y + 230, uc17_box[0], uc17_box[1] + usecase_height//2)

# Draw relationships for admin with varying starting points
draw_relationship(admin_x + 30, admin_y + 50, uc1_box[0], uc1_box[1] + usecase_height//2)
draw_relationship(admin_x + 40, admin_y + 70, uc18_box[0], uc18_box[1] + usecase_height//2)
draw_relationship(admin_x + 50, admin_y + 90, uc19_box[0], uc19_box[1] + usecase_height//2)
draw_relationship(admin_x + 60, admin_y + 110, uc20_box[0], uc20_box[1] + usecase_height//2)
draw_relationship(admin_x + 70, admin_y + 130, uc21_box[0], uc21_box[1] + usecase_height//2)

# Draw include/extend relationships with better visibility
draw_relationship(uc1_box[2], uc1_box[1] + usecase_height//3, 
                 uc2_box[0], uc2_box[1] + usecase_height//3, 
                 "<<extend>>", style="dashed", arrow_end=True)

draw_relationship(uc3_box[2], uc3_box[1] + usecase_height//3, 
                 uc4_box[0], uc4_box[1] + usecase_height//3, 
                 "<<include>>", style="dashed", arrow_end=True)

draw_relationship(uc7_box[1] + usecase_height//2, uc7_box[3], 
                 uc9_box[1] + usecase_height//2, uc9_box[1], 
                 "<<include>>", style="dashed", arrow_end=True)

draw_relationship(uc8_box[1] + usecase_height//2, uc8_box[3], 
                 uc10_box[1] + usecase_height//2, uc10_box[1], 
                 "<<include>>", style="dashed", arrow_end=True)

draw_relationship(uc16_box[1] + usecase_height//2, uc16_box[3], 
                 uc17_box[1] + usecase_height//2, uc17_box[1], 
                 "<<include>>", style="dashed", arrow_end=True)

draw_relationship(uc17_box[1] + usecase_height//2, uc17_box[3], 
                 uc18_box[1] + usecase_height//2, uc18_box[1], 
                 "<<include>>", style="dashed", arrow_end=True)

# Get current directory and save the image to a specific absolute path
absolute_path = os.path.abspath("use_case_diagram.png")
image.save("use_case_diagram.png")
print(f"Use Case Diagram saved as {absolute_path}")
print(f"Current directory: {os.getcwd()}")
print(f"Directory contents: {os.listdir('.')}")
print(f"Is file created? {os.path.exists('use_case_diagram.png')}") 