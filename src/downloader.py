import ssl
from os import listdir, remove, rename
from os.path import isfile, join
import urllib.request
import yt_dlp
from PIL import Image

class YouTubeMp3Downloader:
    def __init__(self, url_link: str, name: str, cookies_path: str = "cookies.txt") -> None:
        self.url_link = url_link
        self.name = name
        self.cookies_path = cookies_path

    def download(self):
        """
        Download audio from YouTube as mp3.
        Uses cookies if needed for authentication or CAPTCHA bypass.
        """
        ssl._create_default_https_context = ssl._create_unverified_context

        ydl_opts = {
            'format': 'bestaudio/best',
            'cookiefile': self.cookies_path,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': 'audio_content/%(title)s.%(ext)s',
            'quiet': False,
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info_dict = ydl.extract_info(self.url_link, download=True)
                title = info_dict.get('title', 'Unknown Title')
                thumbnail_url = info_dict.get('thumbnail', None)
        except yt_dlp.utils.DownloadError as e:
            print(f"Download failed: {e}")
            return

        mypath = "audio_content"
        mp3_file_name = [f for f in listdir(mypath) if isfile(join(mypath, f)) and f.endswith('.mp3')][0]
        mp3_file_location = f"audio_content/{mp3_file_name}"
        final_mp3_file = f"audio_content/{self.name}.mp3"
        rename(mp3_file_location, final_mp3_file)

        if thumbnail_url:
            try:
                print(f"Thumbnail URL: {thumbnail_url}")
                thumbnail_original = f"audio_content/{self.name}.webp"
                thumbnail_converted = f"audio_content/thumbnail.png"
                urllib.request.urlretrieve(thumbnail_url, thumbnail_original)

                image = Image.open(thumbnail_original)
                image.save(thumbnail_converted, 'PNG')
                print(f"Thumbnail saved as {thumbnail_converted}.")
                remove(thumbnail_original)
            except Exception as e:
                print(f"Failed to download or convert thumbnail: {e}")
        else:
            print("No thumbnail available.")

        for file in listdir(mypath):
            if file.endswith('.webp'):
                remove(join(mypath, file))

        print(f"Downloaded and converted to {final_mp3_file}.")
