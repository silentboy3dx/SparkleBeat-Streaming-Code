import os


class Song:
    def __init__(self, file):
        self.is_playing = False
        self.is_paused = False
        self.is_stopped = True
        self.file = file
        self.basename = os.path.basename(self.file)
    
    def play(self):
        self.is_playing = True
        self.is_paused = False
        self.is_stopped = False
    
    def pause(self):
        self.is_playing = False
        self.is_paused = True
        self.is_stopped = False
    
    def stop(self):
        self.is_playing = False
        self.is_paused = False
        self.is_stopped = True
    
    def playing(self):
        return self.is_playing
    
    def get_filename(self):
        return self.file
    
    def get_song_name(self):
        """
    Format song name from filename
    strips "mp3" and changes _ to " "
    Used for metadata
    """
        result = self.basename.split("/")[-1].split(".")
        result = (
            ".".join(result[:len(result) - 1]).replace("_", " ").replace("-", " - ")
        )
        return result
