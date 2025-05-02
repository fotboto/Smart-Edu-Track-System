import matplotlib.pyplot as plt
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import os

# Create a sequence diagram for the assignment submission workflow
WIDTH, HEIGHT = 1800, 1400  # Further increased canvas size
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
draw.text((WIDTH//2-350, 40), "Smart Education Tracking System - Assignment Workflow Sequence Diagram", 
         fill="black", font=title_font)

# Define lifelines with more horizontal spacing
lifelines = [
    {"name": "Student", "x": 200},
    {"name": "Teacher", "x": 550},
    {"name": "Assignment System", "x": 900},
    {"name": "Submission System", "x": 1250},
    {"name": "Recommendation System", "x": 1600}
]

# Draw lifeline headers
header_y = 150  # Increased top margin
header_height = 50
for lifeline in lifelines:
    x = lifeline["x"]
    # Draw header box
    draw.rectangle([(x - 80, header_y), (x + 80, header_y + header_height)], 
                 outline="black", fill="lightblue", width=2)
    # Draw header text
    text = lifeline["name"]
    text_width = draw.textlength(text, font=normal_font)
    draw.text((x - text_width//2, header_y + 15), text, fill="black", font=normal_font)
    
    # Draw dashed lifeline
    dash_length = 12
    y = header_y + header_height
    while y < HEIGHT - 100:  # Adjusted bottom margin
        draw.line([(x, y), (x, y + dash_length)], fill="black", width=2)
        y += dash_length * 2

# Draw activation bars for each lifeline - increased vertical spacing
activations = [
    {"lifeline": "Student", "start_y": 220, "end_y": 300},  # Increased bar heights
    {"lifeline": "Assignment System", "start_y": 260, "end_y": 360},
    {"lifeline": "Student", "start_y": 410, "end_y": 490},
    {"lifeline": "Teacher", "start_y": 380, "end_y": 580},
    {"lifeline": "Assignment System", "start_y": 460, "end_y": 560},
    {"lifeline": "Student", "start_y": 610, "end_y": 710},
    {"lifeline": "Submission System", "start_y": 660, "end_y": 760},
    {"lifeline": "Assignment System", "start_y": 710, "end_y": 780},
    {"lifeline": "Teacher", "start_y": 780, "end_y": 880},
    {"lifeline": "Student", "start_y": 910, "end_y": 990},
    {"lifeline": "Recommendation System", "start_y": 950, "end_y": 1050},
    {"lifeline": "Student", "start_y": 1080, "end_y": 1170}
]

for activation in activations:
    lifeline = next((l for l in lifelines if l["name"] == activation["lifeline"]), None)
    if lifeline:
        x = lifeline["x"]
        start_y = activation["start_y"]
        end_y = activation["end_y"]
        # Draw activation bar
        draw.rectangle([(x - 15, start_y), (x + 15, end_y)], 
                     outline="black", fill="lightyellow", width=2)

# Draw message arrows - increased spacing between messages
messages = [
    {"from": "Student", "to": "Assignment System", "y": 260, "text": "View Available Assignments"},
    {"from": "Assignment System", "to": "Student", "y": 340, "text": "Display Assignment List", "dashed": True},
    {"from": "Teacher", "to": "Assignment System", "y": 460, "text": "Create New Assignment"},
    {"from": "Assignment System", "to": "Teacher", "y": 540, "text": "Assignment Created", "dashed": True},
    {"from": "Student", "to": "Submission System", "y": 660, "text": "Submit Assignment Solution"},
    {"from": "Submission System", "to": "Assignment System", "y": 710, "text": "Record Submission"},
    {"from": "Assignment System", "to": "Teacher", "y": 780, "text": "Notify New Submission"},
    {"from": "Teacher", "to": "Student", "y": 850, "text": "Grade Assignment & Provide Feedback"},
    {"from": "Student", "to": "Recommendation System", "y": 950, "text": "Request Learning Resources"},
    {"from": "Recommendation System", "to": "Student", "y": 1030, "text": "Provide Smart Recommendations", "dashed": True},
    {"from": "Student", "to": "Student", "y": 1120, "text": "Study Recommended Material", "self": True}
]

# Draw messages
for message in messages:
    from_lifeline = next((l for l in lifelines if l["name"] == message["from"]), None)
    to_lifeline = next((l for l in lifelines if l["name"] == message["to"]), None)
    
    if from_lifeline and to_lifeline:
        from_x = from_lifeline["x"]
        to_x = to_lifeline["x"]
        y = message["y"]
        
        # Self message (loop back to self)
        if "self" in message and message["self"]:
            # Draw loop
            draw.line([(from_x + 15, y), (from_x + 70, y)], 
                     fill="black", width=2)
            draw.line([(from_x + 70, y), (from_x + 70, y + 30)], 
                     fill="black", width=2)
            draw.line([(from_x + 70, y + 30), (from_x + 15, y + 30)], 
                     fill="black", width=2)
            
            # Draw arrowhead
            draw.polygon([(from_x + 15, y + 30), (from_x + 25, y + 25), (from_x + 25, y + 35)], 
                        outline="black", fill="black")
            
            # Draw text with better positioning
            text_x = from_x + 80
            text_y = y + 5
            
            # Add background for text with border
            text_width = draw.textlength(message["text"], font=normal_font)
            text_height = 24
            draw.rectangle([(text_x - 5, text_y - 5), 
                          (text_x + text_width + 5, text_y + text_height)], 
                        outline="gray", fill="white")
            
            draw.text((text_x, text_y), message["text"], fill="black", font=normal_font)
        else:
            # Regular message between lifelines
            # Draw line (solid or dashed)
            if "dashed" in message and message["dashed"]:
                # Draw dashed line
                dash_length = 12
                segment_length = abs(to_x - from_x)
                num_segments = segment_length // (dash_length * 2)
                segment_size = segment_length / num_segments / 2
                
                current_x = from_x
                end_x = to_x
                step_size = segment_size if to_x > from_x else -segment_size
                
                while (to_x > from_x and current_x < end_x) or (to_x < from_x and current_x > end_x):
                    next_x = current_x + step_size
                    draw.line([(current_x, y), (next_x, y)], fill="black", width=2)
                    current_x = next_x + step_size
            else:
                # Draw solid line
                draw.line([(from_x, y), (to_x, y)], fill="black", width=2)
            
            # Draw arrowhead
            arrow_size = 12
            if to_x > from_x:
                draw.polygon([(to_x - arrow_size, y - arrow_size/2), (to_x, y), (to_x - arrow_size, y + arrow_size/2)], 
                            outline="black", fill="black")
            else:
                draw.polygon([(to_x + arrow_size, y - arrow_size/2), (to_x, y), (to_x + arrow_size, y + arrow_size/2)], 
                            outline="black", fill="black")
            
            # Draw text with improved positioning and background
            text_x = (from_x + to_x) // 2 - draw.textlength(message["text"], font=normal_font) // 2
            text_y = y - 35  # Moved higher to avoid overlap
            
            # Add white background with border
            text_width = draw.textlength(message["text"], font=normal_font)
            text_height = 24
            draw.rectangle([(text_x - 5, text_y - 5), 
                          (text_x + text_width + 5, text_y + text_height)], 
                        outline="gray", fill="white")
            
            draw.text((text_x, text_y), message["text"], fill="black", font=normal_font)

# Add notes/explanations with improved positioning
notes = [
    {"x": 40, "y": 250, "width": 140, "height": 70, "text": "Student checks available assignments"},
    {"x": 40, "y": 450, "width": 140, "height": 70, "text": "Teacher creates and posts a new assignment"},
    {"x": 40, "y": 650, "width": 140, "height": 80, "text": "Student completes and submits assignment solution"},
    {"x": 40, "y": 800, "width": 140, "height": 70, "text": "Teacher grades the submission"},
    {"x": 40, "y": 980, "width": 140, "height": 90, "text": "Smart system recommends additional resources based on performance"}
]

for note in notes:
    # Draw note rectangle with folded corner and border
    draw.rectangle([(note["x"], note["y"]), (note["x"] + note["width"], note["y"] + note["height"])], 
                 outline="black", fill="lightyellow", width=2)
    # Draw folded corner
    corner_size = 15
    draw.line([(note["x"] + note["width"] - corner_size, note["y"]), 
              (note["x"] + note["width"], note["y"] + corner_size)], fill="black", width=2)
    draw.line([(note["x"] + note["width"] - corner_size, note["y"]), 
              (note["x"] + note["width"] - corner_size, note["y"] + corner_size), 
              (note["x"] + note["width"], note["y"] + corner_size)], fill="black", width=2)
    
    # Draw text (wrap if necessary)
    lines = []
    words = note["text"].split()
    current_line = ""
    for word in words:
        if draw.textlength(current_line + " " + word, font=normal_font) < note["width"] - 15:
            current_line += (" " + word if current_line else word)
        else:
            lines.append(current_line)
            current_line = word
    if current_line:
        lines.append(current_line)
    
    # Calculate total text height to center vertically
    line_height = 24
    total_height = len(lines) * line_height
    start_y = note["y"] + (note["height"] - total_height) // 2
    
    for i, line in enumerate(lines):
        line_x = note["x"] + 5
        line_y = start_y + i * line_height
        draw.text((line_x, line_y), line, fill="black", font=normal_font)

# Add legend
legend_x, legend_y = WIDTH - 450, HEIGHT - 170
draw.rectangle((legend_x, legend_y, legend_x + 400, legend_y + 120), outline="black", width=2)
draw.text((legend_x + 15, legend_y + 15), "Legend:", fill="black", font=header_font)

# Draw solid arrow
draw.line([(legend_x + 15, legend_y + 50), (legend_x + 130, legend_y + 50)], fill="black", width=2)
draw.polygon([(legend_x + 130, legend_y + 50), (legend_x + 120, legend_y + 45), (legend_x + 120, legend_y + 55)], 
            outline="black", fill="black")
# Draw text with background
sync_msg = "Synchronous Message"
text_width = draw.textlength(sync_msg, font=normal_font)
draw.rectangle([(legend_x + 140, legend_y + 40), (legend_x + 140 + text_width + 10, legend_y + 65)],
              fill="white", outline="gray")
draw.text((legend_x + 145, legend_y + 45), sync_msg, fill="black", font=normal_font)

# Draw dashed arrow
dash_length = 8
x = legend_x + 15
y = legend_y + 85
for i in range(14):
    draw.line([(x + i*dash_length, y), (x + (i+1)*dash_length, y)], fill="black", width=2)
    i += 2
draw.polygon([(legend_x + 130, legend_y + 85), (legend_x + 120, legend_y + 80), (legend_x + 120, legend_y + 90)], 
            outline="black", fill="black")
# Draw text with background
return_msg = "Return Message"
text_width = draw.textlength(return_msg, font=normal_font)
draw.rectangle([(legend_x + 140, legend_y + 75), (legend_x + 140 + text_width + 10, legend_y + 100)],
              fill="white", outline="gray")
draw.text((legend_x + 145, legend_y + 80), return_msg, fill="black", font=normal_font)

# Save the image
image.save("sequence_diagram.png")
print("Sequence Diagram saved as sequence_diagram.png") 