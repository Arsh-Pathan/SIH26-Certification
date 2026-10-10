from PIL import Image, ImageDraw, ImageFont
import os

img = Image.open(r'C:\Users\ArshPathan\OneDrive\Desktop\certificate .png')
draw = ImageDraw.Draw(img)

# Try cambria italic
font_path = r'C:\Windows\Fonts\cambriai.ttf'
try:
    font_name = ImageFont.truetype(font_path, 40)
    font_team = ImageFont.truetype(font_path, 30)
except:
    font_name = ImageFont.load_default()
    font_team = ImageFont.load_default()

name = "Prathamesh Hunasnale"
team = "AGRO-MINDS"

# Mr./Ms. is at x=441, y=437 (line)
# We want the text to sit on the line. 
# textbbox returns (left, top, right, bottom)
name_bbox = draw.textbbox((0, 0), name, font=font_name)
name_w = name_bbox[2] - name_bbox[0]
name_h = name_bbox[3] - name_bbox[1]

team_bbox = draw.textbbox((0, 0), team, font=font_team)
team_w = team_bbox[2] - team_bbox[0]
team_h = team_bbox[3] - team_bbox[1]

# The line length is 766 for the name, starting at 441. Center is 441 + 766/2 = 824
# The team line starts at 536, length 513. Center is 536 + 513/2 = 792.5

name_x = 824 - (name_w / 2)
name_y = 432 - name_h # slightly above the line

team_x = 792 - (team_w / 2)
team_y = 492 - team_h

# Draw text in dark blue or black. Let's use #002b5e (a dark navy)
color = (0, 43, 94)

draw.text((name_x, name_y), name, fill=color, font=font_name)
draw.text((team_x, team_y), team, fill=color, font=font_team)

img.save('test_cert.png')
print("Saved test_cert.png")
