#!/usr/bin/env python3
"""Generate L08 audio files using edge-tts (IsabellaNeural)"""
import asyncio, edge_tts, os, re

DIR = "l08_audio"
os.makedirs(DIR, exist_ok=True)

# Sanitize filename for Windows compatibility
def safe_filename(key):
    return re.sub(r'[<>:"/\\|?*]', '_', key) + ".mp3"

MAP = {
    "l08": r"",
    "l08_andare_vado_vai_va_andiamo_and": r"andare: vado/vai/va/andiamo/andate/vanno",
    "l08_avere_ho_hai_ha_abbiamo_avete_": r"avere: ho/hai/ha/abbiamo/avete/hanno",
    "l08_cosa_fai_oggi": r"Cosa fai oggi?",
    "l08_dai_vieni_con_noi": r"Dai, vieni con noi!",
    "l08_essere_sono_sei_siamo_siete_so": r"essere: sono/sei/è/siamo/siete/sono",
    "l08_fare_faccio_fai_fa_facciamo_fa": r"fare: faccio/fai/fa/facciamo/fate/fanno",
    "l08_io_faccio": r"io faccio 我做",
    "l08_io_ho": r"io ho 我有",
    "l08_io_sono": r"io sono 我是",
    "l08_io_sto_a_casa_faccio_i_compiti": r"Io sto a casa, faccio i compiti.",
    "l08_io_vado": r"io vado 我去",
    "l08_loro_hanno": r"loro hanno 他们有",
    "l08_loro_sono": r"loro sono 他们是",
    "l08_lui_fa": r"lui fa 他做",
    "l08_lui_lei": r"lui/lei è 他/她是",
    "l08_lui_lei_ha": r"lui/lei ha 他/她有",
    "l08_lui_va": r"lui va 他去",
    "l08_noi_abbiamo": r"noi abbiamo 我们有",
    "l08_noi_andiamo": r"noi andiamo 我们去",
    "l08_noi_facciamo": r"noi facciamo 我们做",
    "l08_noi_siamo": r"noi siamo 我们是",
    "l08_tu_fai": r"tu fai 你做",
    "l08_tu_hai": r"tu hai 你有",
    "l08_tu_sei": r"tu sei 你是",
    "l08_tu_vai": r"tu vai 你去",
    "l08_vado_a_scuola_e_tu": r"Vado a scuola. E tu?",
    "l08_voi_avete": r"voi avete 你们有",
    "l08_voi_siete": r"voi siete 你们是",
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
    print(f"Generating {len(MAP)} L08 audio files...")
    for k, t in MAP.items():
        await gen(k, t)
    print("Done!")

if __name__ == "__main__":
    asyncio.run(main())