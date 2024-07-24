from downloader import YouTubeMp3Downloader
from changemp3meta import ChangeMetaData

url = "https://www.youtube.com/watch?v=2-vZrzbE9f4"
title = "Freewheel Burning"
artist = "Judas Priest"
audio_file_name = f"{artist} - {title}"

song = YouTubeMp3Downloader(url, audio_file_name)
song.download()


audio_file = f"./audio_content/{audio_file_name}.mp3"
ChangeMetaData(audiofile = audio_file).change(title=title, artist=artist)