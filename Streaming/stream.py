import shout
import random
from song import Song


class Stream:
    def __init__(
            self,
            mount_point,
            music_directory,
            station_url,
            genre,
            name,
            description,
            stream_host,
            stream_port,
            stream_password,
    ):
        self.shout = shout.Shout()
        self.shout.audio_info = {
            shout.SHOUT_AI_BITRATE: "128",
            shout.SHOUT_AI_SAMPLERATE: "44100",
            shout.SHOUT_AI_CHANNELS: "5",
        }
        self.shout.format = "mp3"  # using mp3 but it can also be ogg vorbis
        self.shout.genre = genre
        self.ogv = 0
        
        # self.config = get_config()
        self.shout.host = stream_host
        self.shout.port = int(stream_port)
        self.shout.password = stream_password
        self.shout.mount = mount_point
        
        # self.logger = get_logger(name)
        
        self.shout.name = name
        self.shout.url = station_url
        self.music_directory = music_directory
        self.shout.description = description
        self.song_conter = 0
        
        self.shout.open()
        
        self.current_playlist = None
        self.current_jingles = None
        self.current_advertisements = None
        self.current_song = None
        self.jingle_or_advertisement_chance = 40
        self.jingle_chance = 20
        self.advertisement_chance = 10
        self.force_next = False
        
        self.callbacks = {
            'nextsong': [],
        }
    
    def nextsong(self):
        def inner(f):
            self.callbacks['nextsong'].append(f)
            return f
        
        return inner
    
    def advertise_new_song(self):
        for callback in self.callbacks['nextsong']:
            callback(self.get_current_song())
    
    def set_playlist(self, playlist):
        self.stop()
        self.current_playlist = playlist
    
    def set_advertisements(self, advertisements):
        self.current_advertisements = advertisements
    
    def set_jingles(self, jingles):
        self.current_jingles = jingles
    
    def get_current_song(self):
        return self.current_song
    
    def next_song(self):
        self.force_next = True
        
    def start(self):
        self.shout.close()
        self.shout.open()
        
        if self.current_playlist:
            
            self.current_playlist.start_playing()
            
            while self.current_playlist.is_playing():
                self.current_song = self.current_playlist.get_current_song();
                self.advertise_new_song()
                self.stream_audio(self.current_playlist.get_current_song())
                
                rng = random.randrange(1, 100 - self.jingle_or_advertisement_chance, 1)
                
                if rng >= self.jingle_or_advertisement_chance:
                    delta = (100 - self.jingle_or_advertisement_chance)
                    
                    matched = False
                    if self.current_jingles and self.jingle_chance <= delta:
                        self.current_song = self.current_jingles.get_current_song();
                        self.stream_audio(self.current_jingles.get_current_song())
                        self.advertise_new_song()
                        self.current_jingles.next_song()
                        matched = True
                    
                    if self.current_advertisements and self.advertisement_chance <= delta and matched is False:
                        self.current_song = self.current_advertisements.get_current_song();
                        self.stream_audio(self.current_advertisements.get_current_song())
                        self.advertise_new_song()
                        self.current_advertisements.next_song()
                
                self.current_playlist.next_song()
    
    def stop(self):
        if self.current_playlist:
            self.current_playlist.stop_playing()
    
    def stream_audio(self, song: Song):
        # self.logger.info("Playing file %s" % str(audio_file))
        temp = open(song.get_filename(), "rb")
        self.shout.set_metadata({"song": song.get_song_name()})
        new_buffer = temp.read(4096)
        while len(new_buffer) != 0 and self.force_next is False:
            buffer = new_buffer
            new_buffer = temp.read(4096)
            self.shout.send(buffer)
            self.shout.sync()
        temp.close()
        self.force_next = False
