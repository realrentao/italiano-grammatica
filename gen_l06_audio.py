#!/usr/bin/env python3
"""Generate L06 audio files using edge-tts (IsabellaNeural)"""
import asyncio, edge_tts, os, re

DIR = "l06_audio"
os.makedirs(DIR, exist_ok=True)

# Sanitize filename for Windows compatibility
def safe_filename(key):
    return re.sub(r'[<>:"/\\|?*]', '_', key) + ".mp3"

MAP = {
    "l06": r"",
    "l06_di_chi_questo_libro": r"Di chi è questo libro?",
    "l06_e_quella_macchina": r"E quella macchina?",
    "l06_il_mio_libro": r"il mio libro 我的书",
    "l06_il_mio_libro_di_italiano": r"È il mio libro di italiano.",
    "l06_il_suo_amico": r"il suo amico 他的朋友",
    "l06_io": r"io 我",
    "l06_io_mio_mia": r"io / mio / mia",
    "l06_la_mia_mamma": r"la mia mamma 我妈←要冠词",
    "l06_la_sua_macchina_di_marco": r"È la sua macchina, di Marco.",
    "l06_la_tua_casa": r"la tua casa 你的房子",
    "l06_lei": r"lei 她/您",
    "l06_loro": r"loro 他们/她们",
    "l06_lui": r"lui 他",
    "l06_lui_suo_sua": r"lui / suo / sua",
    "l06_mio_padre": r"mio padre 我爸←省冠词",
    "l06_noi": r"noi 我们",
    "l06_noi_nostro_nostra": r"noi / nostro / nostra",
    "l06_tu": r"tu 你",
    "l06_tu_tuo_tua": r"tu / tuo / tua",
    "l06_tua_madre": r"tua madre 你妈←省冠词",
    "l06_voi": r"voi 你们",
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
    print(f"Generating {len(MAP)} L06 audio files...")
    for k, t in MAP.items():
        await gen(k, t)
    print("Done!")

if __name__ == "__main__":
    asyncio.run(main())