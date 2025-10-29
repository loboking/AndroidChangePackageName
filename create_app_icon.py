#!/usr/bin/env python3
"""
Create a simple app icon for Android Project Rebuilder
"""

from PIL import Image, ImageDraw, ImageFont
import os
import sys

# Force UTF-8 encoding for Windows console
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# Create resources directory
os.makedirs('resources', exist_ok=True)

# Create 1024x1024 icon (highest resolution for macOS)
size = 1024
img = Image.new('RGB', (size, size), color='#667eea')

# Create gradient effect
draw = ImageDraw.Draw(img)
for i in range(size):
    # Gradient from #667eea to #764ba2
    r = int(102 + (118 - 102) * (i / size))
    g = int(126 + (75 - 126) * (i / size))
    b = int(234 + (162 - 234) * (i / size))
    draw.line([(0, i), (size, i)], fill=(r, g, b))

# Add a rounded rectangle background
margin = 100
rect_size = size - 2 * margin
overlay = Image.new('RGBA', (size, size), (0, 0, 0, 0))
overlay_draw = ImageDraw.Draw(overlay)

# Draw rounded rectangle
radius = 150
overlay_draw.rounded_rectangle(
    [margin, margin, margin + rect_size, margin + rect_size],
    radius=radius,
    fill=(255, 255, 255, 40)
)

# Composite overlay onto gradient
img = img.convert('RGBA')
img = Image.alpha_composite(img, overlay)

# Add Android robot icon (simple representation with text)
try:
    # Try to use a large font
    font_size = 400
    try:
        font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", font_size)
    except:
        font = ImageFont.load_default()
except:
    font = None

# Draw text "APR" (Android Project Rebuilder)
final_draw = ImageDraw.Draw(img)
text = "APR"

if font:
    # Get text bbox
    bbox = final_draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
else:
    # Rough estimate for default font
    text_width = 200
    text_height = 50

# Center the text
text_x = (size - text_width) // 2
text_y = (size - text_height) // 2 - 50

final_draw.text((text_x, text_y), text, fill=(255, 255, 255, 255), font=font)

# Add subtitle
subtitle = "Rebuilder"
if font:
    small_font_size = 120
    try:
        small_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", small_font_size)
    except:
        small_font = font
else:
    small_font = None

if small_font:
    bbox = final_draw.textbbox((0, 0), subtitle, font=small_font)
    subtitle_width = bbox[2] - bbox[0]
    subtitle_x = (size - subtitle_width) // 2
    subtitle_y = text_y + text_height + 50
    final_draw.text((subtitle_x, subtitle_y), subtitle, fill=(255, 255, 255, 200), font=small_font)

# Save as PNG
img = img.convert('RGB')
img.save('resources/icon.png')
print("✓ Created resources/icon.png (1024x1024)")

# For macOS .icns, we need multiple sizes
# Let's create them and use iconutil
icon_sizes = [16, 32, 64, 128, 256, 512, 1024]
iconset_dir = 'resources/icon.iconset'
os.makedirs(iconset_dir, exist_ok=True)

for icon_size in icon_sizes:
    resized = img.resize((icon_size, icon_size), Image.Resampling.LANCZOS)
    resized.save(f'{iconset_dir}/icon_{icon_size}x{icon_size}.png')
    if icon_size <= 512:  # Also create @2x versions
        resized_2x = img.resize((icon_size * 2, icon_size * 2), Image.Resampling.LANCZOS)
        resized_2x.save(f'{iconset_dir}/icon_{icon_size}x{icon_size}@2x.png')

print(f"✓ Created icon set in {iconset_dir}")
print("✓ To create .icns file, run: iconutil -c icns resources/icon.iconset")
