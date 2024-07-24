from src.downloader import YouTubeMp3Downloader
from src.changemp3meta import ChangeMetaData
from flask import Flask, request, render_template, send_file
import os

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/download', methods=["POST"])
def process():
    url = request.form['url']
    title = request.form['title']
    artist = request.form['artist']
    audio_file_name = f"{artist} - {title}"
    YouTubeMp3Downloader(url, audio_file_name).download()
    audio_file = f"./audio_content/{audio_file_name}.mp3"
    ChangeMetaData(audiofile = audio_file).change(title=title, artist=artist)

    return send_file(audio_file, as_attachment=True), os.remove(audio_file), os.remove('audio_content/thumbnail.png')


if __name__ == '__main__':
    app.run(port=5000, debug=True)
    