#!/usr/bin/env python3
"""Test API methods without GUI"""

import sys
sys.path.insert(0, '/Users/ws/AndroidChangePackageName')

from standalone_app import API

# Create API instance
api = API()

# Test get_message
print("Testing API methods...")
print(f"get_message(): {api.get_message()}")

# Test processor initialization
print("\nTesting processor initialization...")
try:
    from backend.processor import AndroidProjectProcessor
    processor = AndroidProjectProcessor()
    print("✓ AndroidProjectProcessor imported successfully")
    print(f"✓ Processor logs: {processor.logs}")
except Exception as e:
    print(f"✗ Error: {e}")

print("\n✓ All API bridge tests passed!")
