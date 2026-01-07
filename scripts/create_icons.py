#!/usr/bin/env python3
"""
Create app icons for Demo Prep Tool
"""

from PIL import Image, ImageDraw, ImageFont
import os

def create_icon(text, bg_color, text_color, output_path, size=512):
    """Create a simple app icon"""
    # Create image
    img = Image.new('RGB', (size, size), bg_color)
    draw = ImageDraw.Draw(img)

    # Try to use a system font
    try:
        font = ImageFont.truetype('/System/Library/Fonts/Helvetica.ttc', size // 3)
    except:
        font = ImageFont.load_default()

    # Calculate text position (centered)
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    x = (size - text_width) // 2
    y = (size - text_height) // 2

    # Draw text
    draw.text((x, y), text, fill=text_color, font=font)

    # Add rounded corners
    mask = Image.new('L', (size, size), 0)
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.rounded_rectangle([(0, 0), (size, size)], radius=size//8, fill=255)

    # Apply mask
    output = Image.new('RGB', (size, size), (255, 255, 255))
    output.paste(img, (0, 0), mask)

    # Save
    output.save(output_path, 'PNG')
    print(f"Created icon: {output_path}")

# Create icons
script_dir = os.path.dirname(os.path.abspath(__file__))

# Start icon (gradient blue/purple)
create_icon('▶', (102, 126, 234), (255, 255, 255),
            os.path.join(script_dir, 'start_icon.png'))

# Stop icon (red)
create_icon('■', (220, 53, 69), (255, 255, 255),
            os.path.join(script_dir, 'stop_icon.png'))

print("\nIcons created successfully!")
print("To apply them to the apps, you can:")
print("1. Right-click on the .app file")
print("2. Select 'Get Info'")
print("3. Drag the PNG icon onto the small icon in the top left of the Info window")
