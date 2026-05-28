#!/usr/bin/env python3
"""Generate L03 audio files using edge-tts (IsabellaNeural voice)"""
import asyncio
import edge_tts
import os

OUTPUT_DIR = "l03_audio"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# All L03 audio keys mapped to Italian text for TTS
AUDIO_MAP = {
    # Title
    "l03_title": "Lezione tre. Gli articoli.",
    # Definite articles - masculine singular
    "l03_il_libro": "il libro",
    "l03_il_gatto": "il gatto",
    "l03_il_fiore": "il fiore",
    "l03_il_tavolo": "il tavolo",
    "l03_il_caffe": "il caffè",
    "l03_il_problema": "il problema",
    "l03_il_sistema": "il sistema",
    # Definite articles - masculine plural
    "l03_i_libri": "i libri",
    "l03_i_gatti": "i gatti",
    "l03_i_fiori": "i fiori",
    # lo/gli words
    "l03_lo_studente": "lo studente",
    "l03_lo_zoo": "lo zoo",
    "l03_lo_psicologo": "lo psicologo",
    "l03_lo_gnomo": "lo gnomo",
    "l03_lo_xilofono": "lo xilofono",
    "l03_lo_pneumatico": "lo pneumatico",
    "l03_lo_zaino": "lo zaino",
    "l03_lo_spagnolo": "lo spagnolo",
    "l03_lo_specchio": "lo specchio",
    "l03_gli_studenti": "gli studenti",
    "l03_gli_zii": "gli zii",
    "l03_gli_amici": "gli amici",
    # Definite articles - feminine
    "l03_la_casa": "la casa",
    "l03_la_pizza": "la pizza",
    "l03_la_chiave": "la chiave",
    "l03_la_scuola": "la scuola",
    "l03_la_macchina": "la macchina",
    "l03_la_stazione": "la stazione",
    "l03_le_case": "le case",
    "l03_le_pizze": "le pizze",
    "l03_le_chiavi": "le chiavi",
    "l03_le_scuole": "le scuole",
    "l03_le_universita": "le università",
    # l' words
    "l03_l_amico": "l'amico",
    "l03_l_amica": "l'amica",
    "l03_l_universita": "l'università",
    # Indefinite articles
    "l03_un_libro": "un libro",
    "l03_un_amico": "un amico",
    "l03_uno_studente": "uno studente",
    "l03_uno_zio": "uno zio",
    "l03_una_casa": "una casa",
    "l03_una_pizza": "una pizza",
    "l03_un_amica": "un'amica",
    "l03_un_isola": "un'isola",
    # Preposizioni articolate
    "l03_del": "del, dello, dell'",
    "l03_al": "al, allo, all'",
    "l03_dal": "dal, dallo",
    "l03_nel": "nel, nello, nell'",
    "l03_sul": "sul, sullo",
    "l03_della": "della, delle",
    # Dialogue
    "l03_dlg1": "Hai un libro italiano?",
    "l03_dlg2": "Sì, ho il libro di grammatica.",
    "l03_dlg3": "Mi presti il libro?",
    "l03_dlg4": "Certo, eccolo!",
    "l03_dlg_full": "Hai un libro italiano? Sì, ho il libro di grammatica. Mi presti il libro? Certo, eccolo!",
}

VOICE = "it-IT-IsabellaNeural"
RATE = "-5%"  # slightly slower for clarity

async def generate_one(key, text):
    output_path = os.path.join(OUTPUT_DIR, f"{key}.mp3")
    if os.path.exists(output_path):
        print(f"  SKIP {key} (exists)")
        return
    try:
        communicate = edge_tts.Communicate(text, VOICE, rate=RATE)
        await communicate.save(output_path)
        print(f"  OK {key}")
    except Exception as e:
        print(f"  FAIL {key}: {e}")

async def main():
    print(f"Generating {len(AUDIO_MAP)} L03 audio files...")
    for key, text in AUDIO_MAP.items():
        await generate_one(key, text)
    print(f"Done! Files in {OUTPUT_DIR}/")

if __name__ == "__main__":
    asyncio.run(main())
