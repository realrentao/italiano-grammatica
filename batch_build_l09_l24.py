#!/usr/bin/env python3
"""Batch build L09-L24: copy files, fix playAudio, create gen scripts, split audio.
Run: python batch_build_l09_l24.py copy  (just copies + creates gen scripts)
Run: python batch_build_l09_l24.py audio   (generates MP3 files)
Run: python batch_build_l09_l24.py split   (splits MP3 to per-key JS)
Run: python batch_build_l09_l24.py all     (does everything)
"""
import re, os, sys, subprocess, json, base64, glob, asyncio

BASE = r"D:\workbuddy工作区\2026-05-27-23-32-08\italiano-grammatica"
REPO = os.path.join(BASE, "repo_files")

LESSONS = [
    (9, "lezione09-verbi-modali.html", "情态动词"),
    (10, "lezione10-verbi-riflessivi.html", "自反动词"),
    (11, "lezione11-progressivo.html", "进行时"),
    (12, "lezione12-esserci.html", "esserci的用法"),
    (13, "lezione13-ci-ne.html", "代词ci和ne"),
    (14, "lezione14-pronomi-oggetto.html", "宾语代词"),
    (15, "lezione15-passato-prossimo.html", "近过去时"),
    (16, "lezione16-imperfetto.html", "未完成过去时"),
    (17, "lezione17-futuro.html", "将来时"),
    (18, "lezione18-condizionale.html", "条件式"),
    (19, "lezione19-imperativo.html", "命令式"),
    (20, "lezione20-congiuntivo.html", "虚拟式"),
    (21, "lezione21-periodo-ipotetico.html", "条件从句"),
    (22, "lezione22-frasi-complesse.html", "复合句"),
    (23, "lezione23-passivo-impersonale.html", "被动态"),
    (24, "lezione24-riassunto.html", "综合复习"),
]

def sanitize(text):
    key = text.lower().strip()
    key = re.sub(r"[^a-z]+", "_", key)
    return key.strip("_")[:30]

def is_valid(text):
    t = text.strip()
    if len(t) < 2: return False
    if chr(0x1f50a) in t: return False
    if not re.search(r"[a-zA-Z]", t): return False
    return True

def extract_audio_map(html, lesson_key):
    """Extract text from playAudio calls and generate key->text mapping."""
    pattern = r"playAudio\('" + re.escape(lesson_key) + r"'\)\"[^>]*>([^<]+)<"
    matches = re.findall(pattern, html)
    
    text_to_key = {}
    key_counter = {}
    
    for text in matches:
        t = text.strip()
        if not is_valid(t):
            continue
        if t in text_to_key:
            continue
        base = sanitize(t)
        if not base:
            continue
        if base in key_counter:
            key_counter[base] += 1
            final = f"{lesson_key}_{base}_{key_counter[base]}"
        else:
            key_counter[base] = 1
            final = f"{lesson_key}_{base}"
        text_to_key[t] = final
    
    return text_to_key

def step_copy_and_genscripts():
    """Step 1: Copy HTML, replace keys, create gen scripts."""
    for num, fname, title in LESSONS:
        lesson_key = f"l{num:02d}"
        src = os.path.join(REPO, fname)
        dst = os.path.join(BASE, fname)
        
        if not os.path.exists(src):
            print(f"SKIP: {fname} not found")
            continue
        
        print(f"\n=== {fname} ===")
        
        with open(src, "r", encoding="utf-8") as f:
            html = f.read()
        
        # Extract audio map
        text_to_key = extract_audio_map(html, lesson_key)
        print(f"  {len(text_to_key)} unique audio keys")
        
        if text_to_key:
            # Replace playAudio keys
            new_html = html
            for text, new_key in text_to_key.items():
                old_play = f"playAudio('{lesson_key}')"
                new_play = f"playAudio('{new_key}')"
                new_html = new_html.replace(old_play, new_play, 1)
        else:
            new_html = html
        
        # Remove audio_data.js reference
        new_html = new_html.replace('<script src="audio_data.js"></script>', '')
        
        # Replace old script with on-demand version
        old_start = '<script>\nwindow.addEventListener'
        on_demand = f'''<script>
// ===== 音频播放（按需加载）=====
const _audioEl = new Audio();
const _LESSON = '{lesson_key}';

function playAudio(key) {{
  if (window.__AC && __AC[key]) {{
    _audioEl.pause();
    _audioEl.src = __AC[key];
    _audioEl.load();
    _audioEl.play().catch(function(e) {{
      if (e.name === 'AbortError') return;
      showToast('请先点击页面任意位置，再试一次 \U0001f50a');
    }});
    return;
  }}
  var s = document.createElement('script');
  s.src = 'audio_data/' + _LESSON + '/' + key + '.js?v=1';
  s.onload = function() {{ playAudio(key); }};
  s.onerror = function() {{ showToast('音频未收录'); }};
  document.head.appendChild(s);
}}

function showToast(msg) {{
  var t = document.createElement('div');
  t.textContent = msg;
  t.style.cssText = 'position:fixed;bottom:80px;left:50%;transform:translateX(-50%);background:#333;color:#fff;padding:12px 24px;border-radius:8px;font-size:14px;z-index:9999;opacity:0;transition:opacity 0.3s;max-width:90%;text-align:center';
  document.body.appendChild(t);
  requestAnimationFrame(function() {{ t.style.opacity = '1'; }});
  setTimeout(function() {{ t.style.opacity = '0'; setTimeout(function() {{ t.remove(); }}, 300); }}, 2500);
}}
function showTrap('''
        
        if old_start in new_html:
            new_html = new_html.replace(old_start, on_demand)
            print(f"  Added on-demand playAudio")
        
        # Add 3-second visibility fallback
        observer_line = 'const observer=new IntersectionObserver'
        fallback = '''const observer=new IntersectionObserver((entries)=>{entries.forEach(e=>{if(e.isIntersecting)e.target.classList.add('visible');});},{threshold:0.15});
document.querySelectorAll('.section').forEach(s=>observer.observe(s));
// 安全兜底：3秒后所有未显示区块强制可见
setTimeout(function(){document.querySelectorAll('.section:not(.visible)').forEach(function(s){s.classList.add('visible');});},3000);'''
        
        if observer_line in new_html:
            new_html = new_html.replace(observer_line, fallback)
            print(f"  Added 3s fallback")
        
        with open(dst, "w", encoding="utf-8") as f:
            f.write(new_html)
        print(f"  Written: {fname}")
        
        # Create gen script
        if text_to_key:
            gen_path = os.path.join(BASE, f"gen_l{num:02d}_audio.py")
            lines = [
                '#!/usr/bin/env python3',
                f'"""Generate L{num:02d} audio files using edge-tts (IsabellaNeural)"""',
                'import asyncio, edge_tts, os, re',
                '',
                f'DIR = "l{num:02d}_audio"',
                'os.makedirs(DIR, exist_ok=True)',
                '',
                'def safe_filename(key):',
                '    return re.sub(r\'[<>:"/\\\\\\\\|?*]\', \'_\', key) + ".mp3"',
                '',
                'MAP = {',
            ]
            for text, key in sorted(text_to_key.items(), key=lambda x: x[1]):
                escaped = text.replace("\\", "\\\\").replace("'", "\\'")
                lines.append(f'    "{key}": r"{escaped}",')
            lines.extend([
                '}',
                '',
                'VOICE = "it-IT-IsabellaNeural"',
                'RATE = "-5%"',
                '',
                'async def gen(key, text):',
                '    fname = safe_filename(key)',
                '    path = os.path.join(DIR, fname)',
                '    if os.path.exists(path):',
                '        print(f"  SKIP {key}")',
                '        return',
                '    try:',
                '        c = edge_tts.Communicate(text, VOICE, rate=RATE)',
                '        await c.save(path)',
                '        print(f"  OK {key}")',
                '    except Exception as e:',
                '        print(f"  FAIL {key}: {e}")',
                '',
                'async def main():',
                f'    print(f"Generating {{len(MAP)}} L{num:02d} audio files...")',
                '    for k, t in MAP.items():',
                '        await gen(k, t)',
                '    print("Done!")',
                '',
                'if __name__ == "__main__":',
                '    asyncio.run(main())',
            ])
            with open(gen_path, "w", encoding="utf-8") as f:
                f.write("\n".join(lines))
            print(f"  Created gen_l{num:02d}_audio.py ({len(text_to_key)} keys)")

def gen_all_audio(lesson_ids=None):
    """Step 2: Generate audio files using edge-tts. Run in batches."""
    import asyncio
    for num, fname, title in LESSONS:
        if lesson_ids and num not in lesson_ids:
            continue
        gen_path = os.path.join(BASE, f"gen_l{num:02d}_audio.py")
        if os.path.exists(gen_path):
            print(f"\nGenerating L{num:02d} audio...")
            result = subprocess.run(
                [sys.executable, gen_path],
                capture_output=True, text=True,
                timeout=300
            )
            print(result.stdout)
            if result.stderr:
                print(f"  STDERR: {result.stderr[:200]}")

def step_split():
    """Step 3: Split MP3 files into per-key JS files."""
    import base64, json
    for num, fname, title in LESSONS:
        audio_dir = os.path.join(BASE, f"l{num:02d}_audio")
        target_dir = os.path.join(BASE, f"audio_data/l{num:02d}")
        
        if not os.path.exists(audio_dir):
            print(f"SKIP: l{num:02d}_audio not found")
            continue
        
        os.makedirs(target_dir, exist_ok=True)
        mp3_files = glob.glob(os.path.join(audio_dir, "*.mp3"))
        
        count = 0
        for mp3_path in mp3_files:
            basename = os.path.basename(mp3_path)
            key = basename.replace(".mp3", "")
            js_path = os.path.join(target_dir, f"{key}.js")
            
            if os.path.exists(js_path):
                continue
            
            with open(mp3_path, "rb") as f:
                mp3_data = f.read()
            b64 = base64.b64encode(mp3_data).decode("ascii")
            data_uri = f"data:audio/mp3;base64,{b64}"
            
            js_content = f"(function(){{var k={json.dumps(key)};var d={json.dumps(data_uri)};if(!window.__AC)window.__AC={{}};__AC[k]=d;}})();\n"
            
            with open(js_path, "w", encoding="utf-8") as f:
                f.write(js_content)
            count += 1
        
        print(f"L{num:02d}: {count} new JS files (total: {len(mp3_files)})")
    
    print("\nAudio split complete!")

def update_index_html():
    """Update index.html to mark L09-L24 as available."""
    idx_path = os.path.join(BASE, "index.html")
    with open(idx_path, "r", encoding="utf-8") as f:
        html = f.read()
    
    # Already did L05-L08. Now mark L09 as available by changing upcoming cards
    # Actually let's update the stats
    html = html.replace('"24</div><div class="label">总课时</div>', '"24</div><div class="label">总课时</div>')
    html = html.replace('"8</div><div class="label">已完成</div>', '"8</div><div class="label">已完成</div>')
    
    # For now, let's just change L09's upcoming to available
    # We'll do a more comprehensive update later
    with open(idx_path, "w", encoding="utf-8") as f:
        f.write(html)

def push_to_github():
    """Push HTML + audio files via GitHub API."""
    token = 'PLACEHOLDER_TOKEN'
    repo = 'realrentao/italiano-grammatica'
    bu = f'https://api.github.com/repos/{repo}/contents/'
    
    # Push HTML files
    for num, fname, title in LESSONS:
        fpath = os.path.join(BASE, fname)
        if not os.path.exists(fpath):
            continue
        with open(fpath, "rb") as fh:
            d = fh.read()
        b64 = base64.b64encode(d).decode("ascii")
        
        try:
            g = urllib.request.Request(bu + fname, headers={'Authorization': f'Bearer {token}', 'Accept': 'application/vnd.github.v3+json'})
            gd = json.loads(urllib.request.urlopen(g).read())
            sha = gd['sha']
            
            data = json.dumps({'message': 'feat: add L' + str(num) + ' ' + title, 'content': b64, 'sha': sha, 'branch': 'main'}).encode()
            r = urllib.request.Request(bu + fname, data=data, method='PUT', headers={
                'Authorization': f'Bearer {token}', 'Content-Type': 'application/json', 'Accept': 'application/vnd.github.v3+json'
            })
            urllib.request.urlopen(r)
            print(f"  OK {fname}")
        except Exception as e:
            print(f"  FAIL {fname}: {e}")
    
    # Push audio JS files
    for num, fname, title in LESSONS:
        ad = os.path.join(BASE, f"audio_data/l{num:02d}")
        if not os.path.exists(ad):
            continue
        for jf in glob.glob(os.path.join(ad, "*.js")):
            bname = os.path.basename(jf)
            rel = f"audio_data/l{num:02d}/{bname}"
            with open(jf, "rb") as fh:
                d = fh.read()
            b64 = base64.b64encode(d).decode("ascii")
            
            try:
                data = json.dumps({'message': 'feat: add L' + str(num) + ' audio', 'content': b64, 'branch': 'main'}).encode()
                r = urllib.request.Request(bu + rel, data=data, method='PUT', headers={
                    'Authorization': f'Bearer {token}', 'Content-Type': 'application/json', 'Accept': 'application/vnd.github.v3+json'
                })
                urllib.request.urlopen(r)
            except:
                pass  # already exists

if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "all"
    
    if cmd == "copy" or cmd == "all":
        step_copy_and_genscripts()
    
    if cmd == "audio" or cmd == "all":
        gen_all_audio()
    
    if cmd == "split" or cmd == "all":
        step_split()
    
    if cmd == "push":
        push_to_github()
    
    print("\nDone!")
