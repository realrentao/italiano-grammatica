#!/usr/bin/env python3
"""Generate L05 audio files using edge-tts (IsabellaNeural)"""
import asyncio, edge_tts, os, re

DIR = "l05_audio"
os.makedirs(DIR, exist_ok=True)

# Sanitize filename for Windows compatibility
def safe_filename(key):
    return re.sub(r'[<>:"/\\|?*]', '_', key) + ".mp3"

MAP = {
    "l05": r"",
    "l05_buono_migliore": r"buono→migliore 更好",
    "l05_cattivo_peggiore": r"cattivo→peggiore 更坏",
    "l05_chi_pi_alto_marco_o_luca": r"Chi è più alto, Marco o Luca?",
    "l05_e_chi_il_pi_bravo": r"E chi è il più bravo?",
    "l05_giulia_la_pi_intelligente": r"Giulia! È la più intelligente.",
    "l05_grande_maggiore": r"grande→maggiore 更大",
    "l05_il_pi_bravo": r"il più bravo",
    "l05_la_pi_bella": r"la più bella 最美",
    "l05_luca_pi_alto_di_marco": r"Luca è più alto di Marco.",
    "l05_meno_grande_di": r"meno grande di 不如大",
    "l05_meno_veloce_di": r"meno veloce di",
    "l05_pi_grande_di": r"più grande di",
    "l05_pi_intelligente_di": r"più intelligente di 比更聪明",
    "l05_pi_veloce_di": r"più veloce di 比更快",
    "l05_piccolo_minore": r"piccolo→minore 更小",
    "l05_tanto_alto_quanto": r"tanto alto quanto",
    "l05_tanto_bella_quanto": r"tanto bella quanto 一样美",
}

VOICE = "it-IT-IsabellaNeural"
RATE = "-5%"

async def gen(key, text):
    fname = safe_filename(key)
    path = os.path.join(DIR, fname)
    if os.path.exists(path):
        print(f"  SKIP {key}")
        return
    try:
        c = edge_tts.Communicate(text, VOICE, rate=RATE)
        await c.save(path)
        print(f"  OK {key}")
    except Exception as e:
        print(f"  FAIL {key}: {e}")

async def main():
    print(f"Generating {len(MAP)} L05 audio files...")
    for k, t in MAP.items():
        await gen(k, t)
    print("Done!")

if __name__ == "__main__":
    asyncio.run(main())