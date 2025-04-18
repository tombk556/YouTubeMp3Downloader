from src.downloader import YouTubeMp3Downloader
from src.changemp3meta import ChangeMetaData
from flask import Flask, request, render_template, send_file
import secrets
import os

app = Flask(__name__)
app.secret_key = secrets.token_urlsafe(32)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/download', methods=["POST"])
def process():
    url = request.form['url']
    title = request.form['title']
    artist = request.form['artist']
    audio_file_name = f"{artist} - {title}"
    audio_file_path = f"./audio_content/{audio_file_name}.mp3"

    try:
        downloader = YouTubeMp3Downloader(url, audio_file_name)
        downloader.download()

        if not os.path.exists(audio_file_path):
            return "Audio file was not created successfully.", 500

        try:
            ChangeMetaData(audiofile=audio_file_path).change(title=title, artist=artist)
        except Exception as meta_error:
            print(f"Metadata update failed: {meta_error}")

        response = send_file(audio_file_path, as_attachment=True)
        return response

    except Exception as e:
        print(f"Error during download or processing: {e}")
        return f"An error occurred: {e}", 500

    finally:
        try:
            if os.path.exists(audio_file_path):
                os.remove(audio_file_path)
            if os.path.exists('audio_content/thumbnail.png'):
                os.remove('audio_content/thumbnail.png')
        except Exception as cleanup_error:
            print(f"Cleanup failed: {cleanup_error}")
