import eyed3

class ChangeMetaData:
    
    def __init__(self, audiofile: str) -> None:
        self.audiofile = audiofile
        
    def change(self, title, artist):
        file = eyed3.load(self.audiofile)
        
        file.tag.title = title
        file.tag.artist = artist
        file.tag.images.set(3, open("audio_content/thumbnail.png", "rb").read(), "image/png")
        
        return file.tag.save()
        