import ssl
from moviepy.audio.io.AudioFileClip import AudioFileClip
from os import listdir, remove, rename
from os.path import isfile, join
import urllib.request
import yt_dlp

class YouTubeMp3Downloader:
    def __init__(self, url_link: str, name: str) -> None:
        self.url_link = url_link
        self.name = name

    def download(self):
        """
        Download mp4 file from YouTube. 
        The mp4 file will be stored in the audio_content folder.
        The mp4 file will be converted into mp3 and stored in the audio_content folder with the specified name.
        """
        ssl._create_default_https_context = ssl._create_unverified_context
        
        # Define the options for yt-dlp
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': 'audio_content/%(title)s.%(ext)s',
        }

        # Download the audio file
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([self.url_link])
        
        # Get the downloaded mp3 file name in the audio_content folder
        mypath = "audio_content"
        mp3_file_name = [f for f in listdir(mypath) if isfile(join(mypath, f)) and f.endswith('.mp3')][0]
        mp3_file_location = f"audio_content/{mp3_file_name}"
        final_mp3_file = f"audio_content/{self.name}.mp3"

        # Rename the downloaded file to the desired mp3 file name
        rename(mp3_file_location, final_mp3_file)

        # Download the thumbnail
        ydl_opts_thumbnail = {'skip_download': True, 'writesubtitles': False, 'writeautomaticsub': False, 'writethumbnail': True, 'outtmpl': 'audio_content/thumbnail'}
        with yt_dlp.YoutubeDL(ydl_opts_thumbnail) as ydl:
            ydl.download([self.url_link])
        thumbnail_url = f"audio_content/{self.name}.png"
        urllib.request.urlretrieve(f"{self.url_link}.png", thumbnail_url)

        # Clean up
        for file in listdir(mypath):
            if file.endswith('.webp'):  # delete the webp file created by yt-dlp
                remove(join(mypath, file))

        print(f"Downloaded and converted to {final_mp3_file}. Thumbnail saved as {thumbnail_url}.")

# Example usage:
# downloader = YouTubeMp3Downloader("https://www.youtube.com/watch?v=dQw4w9WgXcQ", "example")
# downloader.download()
