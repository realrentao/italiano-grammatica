#!/usr/bin/env python3
"""Merge L03 audio MP3 files into audio_data.js as base64 entries"""
import base64
import os
import re

AUDIO_DIR = "l03_audio"
JS_FILE = "audio_data.js"

# Read existing audio_data.js
with open(JS_FILE, 'r', encoding='utf-8') as f:
    content = f.read()

# Find the closing }; line
lines = content.split('\n')
close_line = None
for i, line in enumerate(lines):
    if line.strip() == '};':
        close_line = i
        break

if close_line is None:
    print("ERROR: Could not find closing }; in audio_data.js")
    exit(1)

print(f"Found closing }}; at line {close_line + 1}")

# Generate base64 entries for all l03_audio files
entries = []
mp3_files = sorted([f for f in os.listdir(AUDIO_DIR) if f.endswith('.mp3')])

for mp3_file in mp3_files:
    key = mp3_file.replace('.mp3', '')
    mp3_path = os.path.join(AUDIO_DIR, mp3_file)
    with open(mp3_path, 'rb') as f:
        mp3_data = f.read()
    b64 = base64.b64encode(mp3_data).decode('ascii')
    entries.append(f'  "{key}": "data:audio/mp3;base64,{b64}"')
    print(f"  OK {key} ({len(mp3_data)} bytes)")

# Insert before closing };
# Remove old closing };
new_lines = lines[:close_line]

# Ensure last line before }; ends with comma
last_content_line = new_lines[-1].rstrip()
if last_content_line and not last_content_line.endswith(','):
    new_lines[-1] = last_content_line + ','

# Add new entries
new_lines.extend(entries)
new_lines.append('};')

# Update count in comment
new_content = '\n'.join(new_lines)

# Count total entries
old_count = len(re.findall(r'"[^"]+"\s*:', content.split('};')[0]))
new_count = old_count + len(entries)
new_content = new_content.replace(f'// {old_count} audio entries', f'// {new_count} audio entries')

with open(JS_FILE, 'w', encoding='utf-8') as f:
    f.write(new_content)

print(f"Merged {len(entries)} L03 entries. Total: {old_count} -> {new_count}")
