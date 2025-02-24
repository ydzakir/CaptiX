import os
import subprocess
import whisper
import yt_dlp
import time
import sys
import re
from datetime import datetime

def opening_booting():
    print("\n\n")
    print("***************************************")
    print("        Welcome to CaptiX             ")
    print("   Your Video to Audio + Auto-Caption ")
    print("         Created by dzasofalum         ")
    print("      Powered by OpenAI Whisper       ")
    print("***************************************")
    time.sleep(2)
    print("\nInitializing...")
    time.sleep(2)
    sys.stdout.write("Loading modules")
    for _ in range(5):
        time.sleep(1)
        sys.stdout.write(".")
        sys.stdout.flush()
    print("\nReady to go!")
    time.sleep(1)
    print("\nCaptiX is now ready. Let's get started!\n")

# Call opening booting
opening_booting()

def minutes_to_seconds(minutes):
    return int(minutes) * 60

def sanitize_title(title):
    return re.sub(r'[^a-zA-Z0-9-_ ]', '', title).replace(" ", "_")

def download_video(url, start_min=None, end_min=None):
    ydl_opts = {
        'format': 'best',
        'outtmpl': '%(title)s.%(ext)s',
        'noplaylist': True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=True)
        title = sanitize_title(info_dict['title'])
        output_file = f"{title}.mp4"
    if start_min is not None and end_min is not None:
        trimmed_file = f"trimmed_{title}.mp4"
        start_sec, end_sec = minutes_to_seconds(start_min), minutes_to_seconds(end_min)
        subprocess.run(["ffmpeg", "-i", output_file, "-ss", str(start_sec), "-to", str(end_sec), "-c", "copy", trimmed_file, "-y"])
        return trimmed_file
    return output_file

def convert_to_audio(video_file, start_min=None, end_min=None):
    audio_file = generate_output_filename("output_audio", "mp3")
    start_sec = minutes_to_seconds(start_min) if start_min else 0
    end_sec = minutes_to_seconds(end_min) if end_min else None
    if end_sec:
        subprocess.run(["ffmpeg", "-i", video_file, "-ss", str(start_sec), "-to", str(end_sec), "-q:a", "2", "-map", "a", audio_file, "-y"])
    else:
        subprocess.run(["ffmpeg", "-i", video_file, "-q:a", "2", "-map", "a", audio_file, "-y"])
    return audio_file

def generate_output_filename(prefix, extension):
    return f"{prefix}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{extension}"

def show_supported_languages():
    print("\n🌍 Daftar bahasa yang tersedia:")
    for code, lang in whisper.tokenizer.LANGUAGES.items():
        print(f"{code} - {lang}")
    print("\n")

def extract_auto_caption(audio_file, lang="id"):
    print("\n⏳ Memproses auto-caption dengan Whisper...")
    model = whisper.load_model("small")
    result = model.transcribe(audio_file, language=lang)
    caption_file = generate_output_filename("auto_caption", "txt")
    with open(caption_file, "w", encoding="utf-8") as f:
        for segment in result["segments"]:
            f.write(f"[{int(segment['start']//60)}:{int(segment['start']%60):02d} - {int(segment['end']//60)}:{int(segment['end']%60):02d}] {segment['text']}\n")
    print(f"\n✅ Auto-caption selesai! Bahasa yang digunakan: {lang.upper()}\n📄 Caption disimpan dalam: {caption_file}")

def main():
    print("🎥 Pilih metode input video:")
    print("1. Gunakan link (YouTube, TikTok, Facebook, Instagram, Twitter)")
    print("2. Unggah file lokal")
    choice = input("Masukkan pilihan (1/2): ")
    if choice == "1":
        url = input("Masukkan URL video: ")
        print("Pilih opsi download:")
        print("1. Download video secara utuh")
        print("2. Download video dengan memotong dari menit ke menit tertentu")
        download_choice = input("Masukkan pilihan (1/2): ")
        if download_choice == "1":
            video_file = download_video(url)
            start_min, end_min = None, None
        elif download_choice == "2":
            start_min = input("Mulai dari menit ke: ")
            end_min = input("Sampai menit ke: ")
            video_file = download_video(url, start_min, end_min)
        else:
            print("❌ Pilihan tidak valid!")
            return
    elif choice == "2":
        video_file = input("Masukkan path file video: ")
        trim_choice = input("Apakah ingin memotong video? (y/n): ").strip().lower()
        if trim_choice == "y":
            start_min = input("Mulai dari menit ke: ")
            end_min = input("Sampai menit ke: ")
        else:
            start_min, end_min = None, None
    else:
        print("❌ Pilihan tidak valid!")
        return
    print("\n🔄 Mengonversi bagian video yang dipilih ke MP3...")
    audio_file = convert_to_audio(video_file, start_min, end_min)
    print(f"✅ Konversi selesai! File audio: {audio_file}")
    auto_caption = input("Apakah ingin mengambil auto-caption? (y/n): ").strip().lower()
    if auto_caption == "y":
        print("\n🌍 Default bahasa: Indonesia (id)")
        change_lang = input("Ingin menggunakan bahasa lain? (y/n): ").strip().lower()
        if change_lang == "y":
            show_supported_languages()
            lang_code = input("Masukkan kode bahasa yang diinginkan: ").strip().lower()
        else:
            lang_code = "id"
        extract_auto_caption(audio_file, lang_code)

if __name__ == "__main__":
    main()
