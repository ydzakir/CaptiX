# CaptiX
CaptiX is a simple yet powerful Python-based application that converts YouTube videos or local video files into audio (MP3 format) and automatically generates captions using OpenAI's Whisper model.
# CaptiX - Video to Audio + Auto-Caption Tool

**CaptiX** is an application developed by dzasofalum to convert YouTube videos or local video files into MP3 format and generate captions using OpenAI's Whisper model. It’s perfect for video content creators, transcriptionists, or anyone who needs to convert videos into text.

---

## Features:
- **Download YouTube videos**: Supports downloading videos using a YouTube link.
- **Trim Video**: Allows you to select a start and end time in minutes for trimming the video before conversion.
- **Convert to Audio**: Convert videos to MP3 audio format.
- **Auto-Captions**: Extract captions from audio using OpenAI’s Whisper model, with language detection.
- **Language Support**: Whisper supports multiple languages including Indonesian by default.

---

## Installation

To use **CaptiX**, follow these steps:

### 1. Install Dependencies:

CaptiX requires Python 3.x and the following libraries:

- yt-dlp (for downloading videos)
- ffmpeg (for video processing and audio conversion)
- openai-whisper (for transcribing audio)
- subprocess (to run system commands)
- os (for handling file operations)

You can install the dependencies using `pip`:

```bash
pip install yt-dlp openai-whisper

## Additionally, you need ffmpeg installed on your system.

For Windows: Download ffmpeg
For Linux/Mac: Install ffmpeg using apt-get or brew.
2. Clone the Repository:
git clone https://github.com/yourusername/CaptiX.git
cd CaptiX
How to Use:
Run the Application:
---
## After setting up, run the script using the following command:
python captiX.py

Choose Input:

Link: Enter a YouTube video URL.
File: Upload a local video file.
Trim Video (For YouTube):

Enter the start and end time in minutes.
Convert to MP3:

The video will be converted to audio after trimming.
Auto-Caption:

After conversion, you’ll be asked if you want to extract auto-captions.
If "yes", captions will be extracted using Whisper, and you'll see the detected language.
Exit:

The application will exit after completing the process.
Example Usage:
$ python captiX.py

Enter YouTube video URL or file path: [URL or path]
Start time (minutes): 1
End time (minutes): 5
Do you want auto-captions? (y/n): y

## License
CaptiX is licensed under the MIT License.
License
CaptiX is licensed under the MIT License.
