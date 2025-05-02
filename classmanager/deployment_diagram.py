import matplotlib.pyplot as plt
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import os

# Create a deployment diagram for the Smart Education Tracking System
WIDTH, HEIGHT = 1200, 900
image = Image.new('RGB', (WIDTH, HEIGHT), color='white')
draw = ImageDraw.Draw(image)

# Try to load font, use default if not available
try:
    title_font = ImageFont.truetype("arial.ttf", 20)
    header_font = ImageFont.truetype("arial.ttf", 16)
    normal_font = ImageFont.truetype("arial.ttf", 14)
    small_font = ImageFont.truetype("arial.ttf", 12)
except:
    title_font = ImageFont.load_default()
    header_font = ImageFont.load_default()
    normal_font = ImageFont.load_default()
    small_font = ImageFont.load_default()

# Draw title
draw.text((WIDTH//2-200, 20), "Smart Education Tracking System - Deployment Diagram", 
         fill="black", font=title_font)

# Draw nodes (deployment units)
def draw_node(x, y, width, height, title, components=None, stereotype=None):
    # Draw 3D box effect
    offset = 15
    # Draw back rectangle
    draw.rectangle([(x + offset, y), (x + width, y + height - offset)], 
                 outline="black", fill="lightgrey", width=2)
    # Draw top face
    draw.polygon([(x, y), (x + offset, y), (x + width, y), (x + width - offset, y)], 
                outline="black", fill="lightgrey", width=2)
    # Draw right face
    draw.polygon([(x + width, y), (x + width, y + height - offset), 
                  (x + width - offset, y + height), (x + width - offset, y + offset)], 
                outline="black", fill="lightgrey", width=2)
    
    # Draw main rectangle
    draw.rectangle([(x, y), (x + width - offset, y + height)], 
                 outline="black", fill="white", width=2)
    
    # Draw title separator
    title_height = 30
    draw.line([(x, y + title_height), (x + width - offset, y + title_height)], 
             fill="black", width=2)
    
    # Draw title
    if stereotype:
        draw.text((x + 10, y + 5), f"<<{stereotype}>>", fill="black", font=small_font)
        draw.text((x + 10, y + 20), title, fill="black", font=header_font)
    else:
        draw.text((x + 10, y + 5), title, fill="black", font=header_font)
    
    # Draw components if provided
    if components:
        for i, component in enumerate(components):
            comp_y = y + title_height + 20 + i * 50
            # Draw component box
            draw.rectangle([(x + 20, comp_y), (x + width - offset - 20, comp_y + 40)], 
                         outline="black", fill="white", width=1)
            
            # Draw component icon (small box with two tabs on left)
            icon_x, icon_y = x + 30, comp_y + 5
            icon_width, icon_height = 15, 15
            draw.rectangle([(icon_x, icon_y), (icon_x + icon_width, icon_y + icon_height)], 
                         outline="black", fill="white", width=1)
            draw.rectangle([(icon_x - 5, icon_y + 3), (icon_x, icon_y + 6)], 
                         outline="black", fill="white", width=1)
            draw.rectangle([(icon_x - 5, icon_y + 9), (icon_x, icon_y + 12)], 
                         outline="black", fill="white", width=1)
            
            # Draw component name
            comp_name, comp_stereotype = component
            if comp_stereotype:
                draw.text((icon_x + icon_width + 10, comp_y + 5), f"<<{comp_stereotype}>>", 
                         fill="black", font=small_font)
                draw.text((icon_x + icon_width + 10, comp_y + 20), comp_name, 
                         fill="black", font=normal_font)
            else:
                draw.text((icon_x + icon_width + 10, comp_y + 10), comp_name, 
                         fill="black", font=normal_font)

# Draw connections between nodes
def draw_connection(start_x, start_y, end_x, end_y, label=None, style="solid"):
    # Draw line based on style
    if style == "solid":
        draw.line([(start_x, start_y), (end_x, end_y)], fill="black", width=2)
    elif style == "dashed":
        # Draw dashed line
        dash_length = 10
        dist = np.sqrt((end_x - start_x)**2 + (end_y - start_y)**2)
        num_dashes = int(dist / (dash_length * 2))
        if num_dashes == 0:
            num_dashes = 1
        
        for i in range(num_dashes):
            t1 = i / num_dashes
            t2 = (i + 0.5) / num_dashes
            
            x1 = start_x + (end_x - start_x) * t1
            y1 = start_y + (end_y - start_y) * t1
            x2 = start_x + (end_x - start_x) * t2
            y2 = start_y + (end_y - start_y) * t2
            
            draw.line([(x1, y1), (x2, y2)], fill="black", width=2)
    
    # Add arrowhead
    arrow_size = 10
    angle = np.arctan2(end_y - start_y, end_x - start_x)
    
    arrow_x1 = end_x - arrow_size * np.cos(angle) - arrow_size/2 * np.sin(angle)
    arrow_y1 = end_y - arrow_size * np.sin(angle) + arrow_size/2 * np.cos(angle)
    arrow_x2 = end_x - arrow_size * np.cos(angle) + arrow_size/2 * np.sin(angle)
    arrow_y2 = end_y - arrow_size * np.sin(angle) - arrow_size/2 * np.cos(angle)
    
    draw.polygon([(end_x, end_y), (arrow_x1, arrow_y1), (arrow_x2, arrow_y2)], 
                outline="black", fill="black")
    
    # Add label if provided
    if label:
        mid_x = (start_x + end_x) // 2
        mid_y = (start_y + end_y) // 2
        text_width = len(label) * 6
        draw.rectangle([(mid_x - text_width//2 - 5, mid_y - 15), 
                       (mid_x + text_width//2 + 5, mid_y + 5)], 
                     outline=None, fill="white")
        draw.text((mid_x - text_width//2, mid_y - 10), label, fill="black", font=normal_font)

# Draw client node
client_x, client_y = 200, 100
client_width, client_height = 300, 150
draw_node(client_x, client_y, client_width, client_height, "Client", 
         components=[
             ("Web Browser", "execution environment"),
             ("Client UI", "artifact")
         ],
         stereotype="device")

# Draw application server node
app_server_x, app_server_y = 700, 100
app_server_width, app_server_height = 400, 350
draw_node(app_server_x, app_server_y, app_server_width, app_server_height, "Application Server", 
         components=[
             ("Django Web Server", "execution environment"),
             ("Student Module", "artifact"),
             ("Teacher Module", "artifact"),
             ("Assignment Module", "artifact"),
             ("Smart Recommendation Engine", "artifact")
         ],
         stereotype="execution environment")

# Draw database server node
db_server_x, db_server_y = 200, 350
db_server_width, db_server_height = 300, 200
draw_node(db_server_x, db_server_y, db_server_width, db_server_height, "Database Server", 
         components=[
             ("SQLite Database", "execution environment"),
             ("User Data", "artifact"),
             ("Education Data", "artifact")
         ],
         stereotype="execution environment")

# Draw file server node
file_server_x, file_server_y = 200, 600
file_server_width, file_server_height = 300, 150
draw_node(file_server_x, file_server_y, file_server_width, file_server_height, "File Server", 
         components=[
             ("File System", "execution environment"),
             ("Assignments", "artifact"),
             ("Student Submissions", "artifact")
         ],
         stereotype="device")

# Draw AI services node
ai_services_x, ai_services_y = 700, 500
ai_services_width, ai_services_height = 400, 250
draw_node(ai_services_x, ai_services_y, ai_services_width, ai_services_height, "AI Services", 
         components=[
             ("Learning Style Analyzer", "artifact"),
             ("Resource Recommender", "artifact"),
             ("Career Path Predictor", "artifact"),
             ("Performance Analyzer", "artifact")
         ],
         stereotype="execution environment")

# Draw connections
# Client to App Server
draw_connection(client_x + client_width - 15, client_y + 75, 
               app_server_x, app_server_y + 75, 
               "HTTP/HTTPS", "solid")

# App Server to Database
draw_connection(app_server_x, app_server_y + 250, 
               db_server_x + db_server_width - 15, db_server_y + 100, 
               "SQL", "solid")

# App Server to File Server
draw_connection(app_server_x + 100, app_server_y + app_server_height, 
               file_server_x + file_server_width - 15, file_server_y + 75, 
               "File I/O", "solid")

# App Server to AI Services
draw_connection(app_server_x + 200, app_server_y + app_server_height, 
               ai_services_x + 200, ai_services_y, 
               "API Calls", "solid")

# Add system boundary
draw.rectangle([(100, 50), (WIDTH - 100, HEIGHT - 50)], 
             outline="black", width=2)
draw.text((110, 60), "Smart Education Tracking System", fill="black", font=header_font)

# Add legend
legend_x, legend_y = WIDTH - 350, HEIGHT - 180
draw.rectangle((legend_x, legend_y, legend_x + 300, legend_y + 150), outline="black")
draw.text((legend_x + 10, legend_y + 10), "Legend:", fill="black", font=header_font)

legend_items = [
    ("Device", "Hardware component"),
    ("Execution Environment", "Software platform/runtime"),
    ("Artifact", "Deployable component")
]

for i, (item, desc) in enumerate(legend_items):
    draw.text((legend_x + 20, legend_y + 40 + i*30), f"<<{item}>>", fill="black", font=normal_font)
    draw.text((legend_x + 140, legend_y + 40 + i*30), desc, fill="black", font=small_font)

# Save the image
image.save("deployment_diagram.png")
print("Deployment Diagram saved as deployment_diagram.png") 