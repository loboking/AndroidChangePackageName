#!/usr/bin/env python3
"""
Create Windows .ico icon file from existing icon.png
"""

from PIL import Image
import os
import sys

# Force UTF-8 encoding for Windows console
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

print("Creating Windows .ico icon...")

# Load existing icon
img = Image.open('resources/icon.png')

# Windows icon sizes
icon_sizes = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]

# Save as .ico with multiple sizes
img.save('resources/icon.ico', format='ICO', sizes=icon_sizes)

print("[OK] Created resources/icon.ico")
print(f"  Sizes: {', '.join([f'{w}x{h}' for w, h in icon_sizes])}")

# Verify file creation
if os.path.exists('resources/icon.ico'):
    size = os.path.getsize('resources/icon.ico')
    print(f"  File size: {size/1024:.1f} KB")
    print("\n[SUCCESS] Windows icon ready!")
else:
    print("\n[ERROR] Failed to create icon")
    sys.exit(1)
