import os
import pandas as pd
from PIL import Image, ImageDraw, ImageFont
import re

# Load data
df = pd.read_csv('SIH_Teams_Members.csv')

# Template image
template_path = r'C:\Users\ArshPathan\OneDrive\Desktop\certificate\base certification.png'

# Output directory
output_dir = 'Certificates'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Fonts
try:
    font_name = ImageFont.truetype(r'C:\Windows\Fonts\georgiai.ttf', 42)
    font_team = ImageFont.truetype(r'C:\Windows\Fonts\georgiai.ttf', 32)
except:
    print("Could not load Cambria Italic, falling back to default.")
    font_name = ImageFont.load_default()
    font_team = ImageFont.load_default()

color = (0, 43, 94) # Dark blue, matches certificate theme

# Generate certificates
for index, row in df.iterrows():
    name = str(row['Member Name']).strip()
    team = str(row['Team Name']).strip()
    
    # Sanitize filename
    safe_name = re.sub(r'[^a-zA-Z0-9_\- ]', "", name).strip()
    safe_team = re.sub(r'[^a-zA-Z0-9_\- ]', "", team).strip()
    filename = f"{safe_team}_{safe_name}.png"
    filepath = os.path.join(output_dir, filename)
    
    img = Image.open(template_path)
    draw = ImageDraw.Draw(img)
    
    # Calculate text placement
    name_bbox = draw.textbbox((0, 0), name, font=font_name)
    name_w = name_bbox[2] - name_bbox[0]
    name_h = name_bbox[3] - name_bbox[1]

    team_bbox = draw.textbbox((0, 0), team, font=font_team)
    team_w = team_bbox[2] - team_bbox[0]
    team_h = team_bbox[3] - team_bbox[1]

    # Centers of the lines (Line for name is at y=474, team is at y=530)
    # Moving up by 12 pixels based on user feedback
    name_x = 819.5 - (name_w / 2)
    name_y = 458 - name_h

    team_x = 853 - (team_w / 2)
    team_y = 514 - team_h

    draw.text((name_x, name_y), name, fill=color, font=font_name)
    draw.text((team_x, team_y), team, fill=color, font=font_team)
    
    import time
    for attempt in range(5):
        try:
            img.save(filepath)
            break
        except Exception as e:
            if attempt == 4:
                print(f"Failed to save {filepath}: {e}")
            time.sleep(0.5)

print(f"Successfully generated {len(df)} certificates in the '{output_dir}' directory.")
