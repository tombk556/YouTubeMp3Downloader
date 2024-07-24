import ssl
from os import listdir, remove, rename
from os.path import isfile, join
import urllib.request
import yt_dlp
from PIL import Image

class YouTubeMp3Downloader:
    def __init__(self, url_link: str, name: str) -> None:
        self.url_link = url_link
        self.name = name

    def download(self):
        """
        Download audio from YouTube as mp3.
        The mp3 file will be stored in the audio_content folder with the specified name.
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

        # Download the audio file and extract info
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(self.url_link, download=True)
            title = info_dict.get('title', 'Unknown Title')
            thumbnail_url = info_dict.get('thumbnail', None)
        
        # Get the downloaded mp3 file name in the audio_content folder
        mypath = "audio_content"
        mp3_file_name = [f for f in listdir(mypath) if isfile(join(mypath, f)) and f.endswith('.mp3')][0]
        mp3_file_location = f"audio_content/{mp3_file_name}"
        final_mp3_file = f"audio_content/{self.name}.mp3"

        # Rename the downloaded file to the desired mp3 file name
        rename(mp3_file_location, final_mp3_file)

        # Download and convert the thumbnail
        if thumbnail_url:
            try:
                # Download the thumbnail
                print(f"Thumbnail URL: {thumbnail_url}")
                thumbnail_original = f"audio_content/{self.name}.webp"
                thumbnail_converted = f"audio_content/thumbnail.png"
                urllib.request.urlretrieve(thumbnail_url, thumbnail_original)
                
                # Convert the thumbnail to PNG
                image = Image.open(thumbnail_original)
                image.save(thumbnail_converted, 'PNG')
                print(f"Thumbnail saved as {thumbnail_converted}.")

                # Clean up the original thumbnail file
                remove(thumbnail_original)
            except Exception as e:
                print(f"Failed to download or convert thumbnail: {e}")
        else:
            print("No thumbnail available.")

        # Clean up any unnecessary files (e.g., .webp files)
        for file in listdir(mypath):
            if file.endswith('.webp'):  # delete any webp files created by yt-dlp
                remove(join(mypath, file))

        print(f"Downloaded and converted to {final_mp3_file}.")

# Example usage:
# downloader = YouTubeMp3Downloader("https://www.youtube.com/watch?v=dQw4w9WgXcQ", "example")
# downloader.download()
