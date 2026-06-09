#!/usr/bin/env python3
"""Generate L07 audio files using edge-tts (IsabellaNeural)"""
import asyncio, edge_tts, os, re

DIR = "l07_audio"
os.makedirs(DIR, exist_ok=True)

# Sanitize filename for Windows compatibility
def safe_filename(key):
    return re.sub(r'[<>:"/\\|?*]', '_', key) + ".mp3"

MAP = {
    "l07": r"",
    "l07_capire_cap_isc_o_cap_isc_i": r"capire → cap-isc-o/cap-isc-i...",
    "l07_cosa_fai_di_lavoro": r"Cosa fai di lavoro?",
    "l07_insegno_l_italiano": r"Insegno l\'italiano.",
    "l07_io_capisc_o": r"io capisc-o 我理解",
    "l07_io_parl_o": r"io parl-o 我说",
    "l07_io_part_o": r"io part-o 我出发",
    "l07_io_scriv_o": r"io scriv-o 我写",
    "l07_loro_parl_ano": r"loro parl-ano 他们说",
    "l07_loro_scriv_ono": r"loro scriv-ono 他们写",
    "l07_lui_capisc_e": r"lui capisc-e 他理解",
    "l07_lui_parl_a": r"lui parl-a 他说",
    "l07_lui_part_e": r"lui part-e 他出发",
    "l07_lui_scriv_e": r"lui scriv-e 他写",
    "l07_noi_cap_iamo": r"noi cap-iamo 我们理解",
    "l07_noi_parl_iamo": r"noi parl-iamo 我们说",
    "l07_noi_part_iamo": r"noi part-iamo 我们出发",
    "l07_noi_scriv_iamo": r"noi scriv-iamo 我们写",
    "l07_parlare_parl_o_parl_i_parl_a": r"parlare → parl-o/parl-i/parl-a...",
    "l07_parli_anche_inglese": r"Parli anche inglese?",
    "l07_partire_part_o_part_i_part_e": r"partire → part-o/part-i/part-e...",
    "l07_s_parlo_inglese_e_francese": r"Sì, parlo inglese e francese.",
    "l07_scrivere_scriv_o_scriv_i_scriv": r"scrivere → scriv-o/scriv-i/scriv-e...",
    "l07_tu_capisc_i": r"tu capisc-i 你理解",
    "l07_tu_parl_i": r"tu parl-i 你说",
    "l07_tu_part_i": r"tu part-i 你出发",
    "l07_tu_scriv_i": r"tu scriv-i 你写",
    "l07_voi_parl_ate": r"voi parl-ate 你们说",
    "l07_voi_scriv_ite": r"voi scriv-ite 你们写",
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
    print(f"Generating {len(MAP)} L07 audio files...")
    for k, t in MAP.items():
        await gen(k, t)
    print("Done!")

if __name__ == "__main__":
    asyncio.run(main())