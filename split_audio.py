#!/usr/bin/env python3
"""Split audio_lXX.js into individual per-key JS files for on-demand loading."""
import re, os, json

SCRIPT_DIR = r"D:\workbuddy工作区\2026-05-27-23-32-08\italiano-grammatica"
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "audio_data")

LESSONS = [
    ("audio_l01.js", "l01"),
    ("audio_l02.js", "l02"),
    ("audio_l03.js", "l03"),
    ("audio_l04.js", "l04"),
]

def parse_audio_js(filepath):
    """Parse audio_lXX.js and extract key-value pairs."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find the AUDIO_DATA object
    # Match: "key": "data:audio/mp3;base64,...",
    pattern = r'"([^"]+)"\s*:\s*"(data:audio/mp3;base64,[^"]+)"'
    matches = re.findall(pattern, content)
    
    print(f"  Found {len(matches)} entries")
    return matches

def write_individual_file(key, data_uri, lesson_dir):
    """Write one key's data as a self-contained JS file."""
    # Escape backslashes and quotes for JS string
    filepath = os.path.join(lesson_dir, f"{key}.js")
    
    # Generate JS that sets a property on window.__AC (Audio Cache)
    # Using immediate IIFE so it runs as soon as the script is loaded
    js_content = f'(function(){{var k={json.dumps(key)};var d={json.dumps(data_uri)};if(!window.__AC)window.__AC={{}};__AC[k]=d;}})();\n'
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(js_content)
    
    size = os.path.getsize(filepath)
    return size

def main():
    for js_file, lesson_id in LESSONS:
        js_path = os.path.join(SCRIPT_DIR, js_file)
        if not os.path.exists(js_path):
            print(f"SKIP: {js_file} not found")
            continue
        
        lesson_dir = os.path.join(OUTPUT_DIR, lesson_id)
        os.makedirs(lesson_dir, exist_ok=True)
        
        print(f"\nProcessing {js_file} ({lesson_id})...")
        entries = parse_audio_js(js_path)
        
        total_size = 0
        for key, data_uri in entries:
            size = write_individual_file(key, data_uri, lesson_dir)
            total_size += size
        
        print(f"  Wrote {len(entries)} files, total {total_size/1024:.0f} KB")
    
    print(f"\nDone! All files in {OUTPUT_DIR}")

if __name__ == "__main__":
    main()
