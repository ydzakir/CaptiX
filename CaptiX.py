import time
import sys
import os
import subprocess
import whisper
import yt_dlp

# Opening Booting Function
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

# Call opening booting at the beginning
opening_booting()

# Fungsi konversi menit ke detik
def minutes_to_seconds(minutes):
    return int(minutes) * 60

# Fungsi mengunduh video dari YouTube dan memotongnya
def download_youtube_video(url, start_min, end_min):
    start_sec = minutes_to_seconds(start_min)
    end_sec = minutes_to_seconds(end_min)
    
    output_file = "downloaded_video.mp4"

    ydl_opts = {
        'format': 'best',
        'outtmpl': output_file
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    # File video yang sudah dipotong
    trimmed_file = "trimmed_video.mp4"
    subprocess.run([
        "ffmpeg", "-i", output_file, "-ss", str(start_sec), "-to", str(end_sec),
        "-c", "copy", trimmed_file, "-y"
    ])
    
    return trimmed_file

# Fungsi mengonversi bagian video yang dipilih ke MP3
def convert_to_audio(video_file, start_min, end_min):
    start_sec = minutes_to_seconds(start_min)
    end_sec = minutes_to_seconds(end_min)

    audio_file = "output_audio.mp3"
    subprocess.run([
        "ffmpeg", "-i", video_file, "-ss", str(start_sec), "-to", str(end_sec),
        "-q:a", "2", "-map", "a", audio_file, "-y"
    ])
    return audio_file

# Fungsi untuk menampilkan bahasa yang didukung oleh Whisper
def show_supported_languages():
    whisper_langs = whisper.tokenizer.LANGUAGES
    print("\n🌍 Daftar bahasa yang tersedia:")
    for code, lang in whisper_langs.items():
        print(f"{code} - {lang}")
    print("\n")

# Fungsi ekstraksi auto-caption menggunakan Whisper
def extract_auto_caption(audio_file, lang="id"):
    print("\n⏳ Memproses auto-caption dengan Whisper...")

    model = whisper.load_model("medium")
    result = model.transcribe(audio_file, language=lang)

    caption_file = "auto_caption.txt"
    with open(caption_file, "w", encoding="utf-8") as f:
        for segment in result["segments"]:
            start = segment["start"]
            end = segment["end"]
            text = segment["text"]
            f.write(f"[{int(start//60)}:{int(start%60):02d} - {int(end//60)}:{int(end%60):02d}] {text}\n")

    detected_lang = lang if lang else result["language"]
    print(f"\n✅ Auto-caption selesai! Bahasa yang digunakan: {detected_lang.upper()}")
    print(f"📄 Caption disimpan dalam: {caption_file}")

# Menu utama
def main():
    print("🎥 Pilih metode input video:")
    print("1. Gunakan link YouTube")
    print("2. Unggah file lokal")
    
    choice = input("Masukkan pilihan (1/2): ")

    if choice == "1":
        url = input("Masukkan URL YouTube: ")
        start_min = input("Mulai dari menit ke: ")
        end_min = input("Sampai menit ke: ")

        video_file = download_youtube_video(url, start_min, end_min)
    
    elif choice == "2":
        video_file = input("Masukkan path file video: ")
        start_min = input("Mulai dari menit ke: ")
        end_min = input("Sampai menit ke: ")
    
    else:
        print("❌ Pilihan tidak valid!")
        return
    
    print("\n🔄 Mengonversi bagian video yang dipilih ke MP3...")
    audio_file = convert_to_audio(video_file, start_min, end_min)
    print("✅ Konversi selesai! File audio: output_audio.mp3")

    # Pilihan untuk mengambil auto-caption
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
    else:
        print("👋 Selesai! Keluar dari program.")

if __name__ == "__main__":
    main()
