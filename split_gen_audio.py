#!/usr/bin/env python3
"""Split generated MP3 files into per-key JS files in audio_data/. Also fix navbar links."""
import os, base64, re, glob, json

BASE = r"D:\workbuddy工作区\2026-05-27-23-32-08\italiano-grammatica"

LESSONS = [
    (5, "l05_audio", "audio_data/l05", "lezione05-comparativo-superlativo.html", "lezione04-aggettivi.html", "lezione06-pronomi-possessivi.html"),
    (6, "l06_audio", "audio_data/l06", "lezione06-pronomi-possessivi.html", "lezione05-comparativo-superlativo.html", "lezione07-verbo-presente.html"),
    (7, "l07_audio", "audio_data/l07", "lezione07-verbo-presente.html", "lezione06-pronomi-possessivi.html", "lezione08-verbi-irregolari.html"),
    (8, "l08_audio", "audio_data/l08", "lezione08-verbi-irregolari.html", "lezione07-verbo-presente.html", "lezione09-non-exist.html"),
]

LESSON_LINKS = {
    5: ("lezione04-aggettivi.html", "lezione06-pronomi-possessivi.html"),
    6: ("lezione05-comparativo-superlativo.html", "lezione07-verbo-presente.html"),
    7: ("lezione06-pronomi-possessivi.html", "lezione08-verbi-irregolari.html"),
    8: ("lezione07-verbo-presente.html", "index.html"),
}

for num, audio_dir, target_dir, html_file, prev, nxt in LESSONS:
    audio_path = os.path.join(BASE, audio_dir)
    target_path = os.path.join(BASE, target_dir)
    html_path = os.path.join(BASE, html_file)
    
    if not os.path.exists(audio_path):
        print(f"SKIP: {audio_dir} not found")
        continue
    
    os.makedirs(target_path, exist_ok=True)
    
    # Read all MP3 files and convert to individual JS files
    mp3_files = glob.glob(os.path.join(audio_path, "*.mp3"))
    print(f"\n{audio_dir}: {len(mp3_files)} MP3 files")
    
    count = 0
    for mp3_path in mp3_files:
        basename = os.path.basename(mp3_path)
        key = basename.replace(".mp3", "")  # key = filename without extension
        
        with open(mp3_path, "rb") as f:
            mp3_data = f.read()
        
        b64 = base64.b64encode(mp3_data).decode("ascii")
        data_uri = f"data:audio/mp3;base64,{b64}"
        
        js_path = os.path.join(target_path, f"{key}.js")
        key_escaped = key.replace("'", "\\'")
        js_content = f"(function(){{var k={json.dumps(key)};var d={json.dumps(data_uri)};if(!window.__AC)window.__AC={{}};__AC[k]=d;}})();\n"
        
        with open(js_path, "w", encoding="utf-8") as f:
            f.write(js_content)
        
        count += 1
    
    print(f"  Created {count} JS files in {target_dir}")
    
    # Fix navbar links in the HTML
    if os.path.exists(html_path):
        with open(html_path, "r", encoding="utf-8") as f:
            html = f.read()
        
        # Update nav links
        prev_link, next_link = LESSON_LINKS[num]
        
        # Replace previous lesson link (find lezione04 or podobne)
        # Look for href="lezioneXX-... in nav buttons
        nav_btns = re.findall(r'href="(lezione\d{2}[^"]*)"', html)
        for link in nav_btns:
            # Try to match old previous/next links
            pass
        
        # Simpler: just replace specific patterns
        # Previous link
        old_prev = f'href="lezione04-aggettivi.html"'
        new_prev = f'href="{prev_link}"'
        # Only replace if it was the old one
        if old_prev in html and prev_link != "lezione04-aggettivi.html":
            html = html.replace(old_prev, new_prev, 1)
        
        # Next link
        old_next = f'href="lezione06-pronomi-possessivi.html"'
        new_next = f'href="{next_link}"'
        if old_next in html and next_link != "lezione06-pronomi-possessivi.html":
            html = html.replace(old_next, new_next, 1)
        
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"  Updated nav links in {html_file}")

print("\nDone! Audio split complete.")
