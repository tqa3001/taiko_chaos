import os
import yt_dlp

def get_mp3_from_youtube(name, url, max_duration_minutes=5):
    ydl_opts_meta = {
        'quiet': True,
        'skip_download': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts_meta) as ydl:
        info = ydl.extract_info(url, download=False)
        duration_sec = info.get('duration', 0)
        if duration_sec > max_duration_minutes * 60:
            print(f"Aborting since video is too long: {duration_sec / 60:.2f} minutes")
            return
    
    save_dir = 'input'
    os.makedirs(save_dir, exist_ok=True)
    outtmpl = os.path.join(save_dir, f'{name}.%(ext)s')
                           
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': outtmpl,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'quiet': False,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
        print(f"Download completed: ${outtmpl}")

get_mp3_from_youtube("The Adults Are Talking", "https://www.youtube.com/watch?v=o4qsjmLxhow", 5.5)