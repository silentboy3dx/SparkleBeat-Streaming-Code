from song import Song
from glob import glob


class Playlist:
    def __init__(self):
        self.files_array = []
        self.songs_array = []
        
        self.current_index = 0
        self.loop_playlist = False
        self.is_currently_stopped = True
        self.is_currently_playing = True
        self.loop = False
        
        self.stop_playing()
        pass
    
    def set_loop(self, value):
        self.loop_playlist = value
    
    def is_playing(self):
        return self.is_currently_playing
    
    def is_stopped(self):
        return self.is_currently_stopped
    
    def from_directory(self, directory):
        self.files_array = glob(directory + "/*.[mM][Pp]3")
        self.files_array.sort()
        
        for file in self.files_array:
            self.songs_array.append(Song(file))
    
    def get_all_songs(self):
        return self.songs_array
    
    def get_current_song(self):
        return self.songs_array[self.current_index]
    
    def start(self):
        self.stop_current_song()
        self.start_playing()
    

    
    def start_playing(self):
        self.is_currently_playing = True
        self.is_currently_stopped = False
        self.current_index = 0
    
    def stop_playing(self):
        self.current_index = 0
        self.is_currently_stopped = True
        self.is_currently_playing = False
    
    def previous_song(self):
        old_song = self.get_current_song()
        songs_length = len(self.songs_array) - 1
        
        if self.current_index - 1 < 0:
            if self.loop_playlist:
                self.current_index = songs_length
            else:
                if self.current_index == 0 and self.is_currently_playing:
                    self.stop_playing()
                
                self.current_index = 0
        else:
            self.current_index -= 1
        
        if old_song:
            old_song.stop()
    
    def next_song(self):
        old_song = self.get_current_song()
        songs_length = len(self.songs_array) - 1
        
        if self.current_index + 1 > songs_length:
            if self.loop_playlist:
                self.current_index = 0
            else:
                if self.current_index == songs_length and self.is_currently_playing:
                    self.stop_playing()
                
                self.current_index = songs_length
        else:
            self.current_index += 1
        
        if old_song:
            old_song.stop()
        
        self.play_current_song()
    
    def play_current_song(self):
        song = self.get_current_song()
        song.play()
    
    def pause_current_song(self):
        song = self.get_current_song()
        song.pause()
    
    def stop_current_song(self):
        song = self.get_current_song()
        song.stop()
