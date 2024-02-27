import shout
import random
from .song import Song
from typing import Callable


class Stream:
    """
    This class represents a live audio streaming object. It allows you to start and stop playing a playlist of songs
    or audio files and dynamically switch between songs, jingles, and advertisements.

    Attributes:
    - shout: An instance of the shoutcast library used for streaming audio.
    - shout.host: The host name or IP address of the shoutcast server.
    - shout.port: The port number of the shoutcast server.
    - shout.password: The password for accessing the shoutcast server.
    - shout.mount: The mount point for streaming the audio.
    - shout.name: The name of the streaming station.
    - shout.url: The URL associated with the streaming station.
    - shout.description: The description of the streaming station.
    - current_playlist: The current playlist being played.
    - current_jingles: The list of jingles for the current instance.
    - current_advertisements: The list of advertisements for the current instance.
    - current_song: The current song being played.
    - jingle_or_advertisement_chance: The chance for playing a jingle or advertisement during a song.
    - jingle_chance: The chance for playing a jingle instead of an advertisement.
    - advertisement_chance: The chance for playing an advertisement instead of a jingle.
    - force_next: A flag to force skipping to the next song.

    Methods:
    - nextsong(callback: Callable) -> Callable:
        Registers a callback function to be executed when the next song is played.

    - advertise_new_song() -> None:
        Advertises a new song by invoking the registered callbacks.

    - set_playlist(playlist: Any) -> None:
        Sets the current playlist.

    - set_advertisements(advertisements: List) -> None:
        Sets the list of advertisements for the current instance.

    - set_jingles(jingles: List) -> None:
        Sets the list of jingles for the current instance.

    - get_current_song() -> Song:
        Returns the current song being played.

    - next_song() -> None:
        Sets the 'force_next' flag to True.

    - start() -> None:
        Starts playing the audio stream.

    - stop() -> None:
        Stops the current playing playlist.

    - stream_audio(song: Song) -> None:
        Streams audio from a given Song object to the shoutcast server.
    """

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
        self.shout.host = stream_host
        self.shout.port = int(stream_port)
        self.shout.password = stream_password
        self.shout.mount = mount_point

        self.shout.name = name
        self.shout.url = station_url
        self.music_directory = music_directory
        self.shout.description = description

        self.current_playlist = None
        self.current_jingles = None
        self.current_advertisements = None
        self.current_song = None
        self.jingle_or_advertisement_chance = 40
        self.jingle_chance = 20
        self.advertisement_chance = 10
        self.force_next = False
        self.force_stop = False
        self.announce_songs = False

        self.callbacks = {
            "nextsong": [],
            "song_announcement": None,
            "song_announcement_played": None,
        }

    def __enter__(self):
        return self

    def __exit__(self, type, value, tb):
        pass

    def set_announce_songs(self, should_announce: bool):
        self.announce_songs = should_announce

    def nextsong(self) -> Callable:
        """
        Registers a callback function to be executed when the next song is played.

        Parameters:
            self: The current instance of the class.

        Return Type:
            None

        """

        def inner(f):
            self.callbacks["nextsong"].append(f)
            return f

        return inner

    def song_announcement(self) -> Callable:
        """
        Registers a callback function to be executed when the next song is played.

        Parameters:
            self: The current instance of the class.

        Return Type:
            None

        """

        def inner(f):
            self.callbacks["song_announcement"] = f
            return f

        return inner

    def song_announcement_played(self) -> Callable:
        """
        Registers a callback function to be executed when the next song is played.

        Parameters:
            self: The current instance of the class.

        Return Type:
            None

        """

        def inner(f):
            self.callbacks["song_announcement_played"] = f
            return f

        return inner

    def advertise_new_song(self) -> None:
        """
        Advertises a new song by invoking the registered callbacks.

        Parameters:
            self: The current instance of the class.

        Return Type:
            None

        Example Usage:
        advertise_new_song(self)

        """
        for callback in self.callbacks["nextsong"]:
            callback(self.get_current_song())

    def request_next_song_announcement(self) -> Song or None:
        """
        Advertises a new song by invoking the registered callbacks.

        Parameters:
            self: The current instance of the class.

        Return Type:
            None

        Example Usage:
        advertise_new_song(self)

        """

        callback = self.callbacks["song_announcement"]
        if callable(callback):
            return callback(self.get_current_song())

        return None

    def announcement_finished_playing(self, song: Song) -> None:
        """
        Performs callback when the announcement for a song has finished playing.

        Parameters:
            self (object): The instance of the class.
            song (Song): The song for which the announcement has finished playing.

        Returns:
            None: This method does not return any value.
        """
        callback = self.callbacks["song_announcement_played"]
        if callable(callback):
            return callback(song)

        return None


    def set_playlist(self, playlist) -> None:
        """
        Set the current playlist.

        Parameters:
            playlist (Playlist): The playlist to be set.

        Returns:
            None

        """
        self.stop()
        self.force_stop = False
        self.current_playlist = playlist

    def set_advertisements(self, advertisements) -> None:
        """
        Sets the list of advertisements for the current instance.

        Parameters:
            advertisements (Playlist): The advertisements playlist to be set.

        Returns:
            None

        """
        self.current_advertisements = advertisements

    def set_jingles(self, jingles) -> None:
        """
        Set the jingles for the current object.

        Parameters:
        - jingles (Playlist): The jingles playlist to be set.

        Returns:
            None

        """
        self.current_jingles = jingles

    def get_current_song(self) -> Song:
        """
        Returns the current song.

        Returns:
            Song: The current song.
        """
        return self.current_song

    def next_song(self) -> None:
        """
        Sets the `force_next` flag to True.

        Parameters:
            self: Reference to the current instance of the class.

        Returns:
            None

        """
        self.force_next = True

    def start(self) -> None:
        """
        Starts playing the audio stream.

        This method closes and reopens the audio stream.
        It then starts playing the current playlist.
        While the playlist is playing, it performs the following steps:
        - Gets the current song from the playlist
        - Advertises the new song (calls `advertise_new_song`)
        - Streams the audio of the current song
        - Determines if a jingle or advertisement should be played based on a random number generator
        - If a jingle should be played and there is a current jingle available, it plays the jingle and moves to the
          next jingle
        - If an advertisement should be played and there is a current advertisement available, it plays the
          advertisement and moves to the next advertisement
        - Moves to the next song in the playlist

        Returns:
            None

        """

        try:
            self.shout.close()
        except Exception:
            pass

        self.shout.open()

        if self.current_playlist:

            self.current_playlist.start_playing()

            while self.current_playlist.is_playing():
                self.current_song = self.current_playlist.get_current_song()

                if self.announce_songs:
                    announcement: Song or None = self.request_next_song_announcement()
                    if announcement:
                        self.stream_audio(announcement)
                        self.announcement_finished_playing(announcement)

                self.advertise_new_song()
                self.stream_audio(self.current_playlist.get_current_song())

                if self.force_stop:
                    self.force_stop = False
                    return

                rng = random.randrange(1, 100 - self.jingle_or_advertisement_chance, 1)

                if rng >= self.jingle_or_advertisement_chance:
                    delta = (100 - self.jingle_or_advertisement_chance)

                    matched = False
                    if self.current_jingles and self.jingle_chance <= delta and len(
                            self.current_jingles.get_all_songs()) > 0:
                        self.current_song = self.current_jingles.get_current_song()
                        self.stream_audio(self.current_jingles.get_current_song())
                        self.current_jingles.next_song()
                        matched = True

                    if (self.current_advertisements and self.advertisement_chance <= delta and matched is False
                            and len(self.current_advertisements.get_all_songs()) > 0):
                        self.current_song = self.current_advertisements.get_current_song()
                        self.stream_audio(self.current_advertisements.get_current_song())
                        self.current_advertisements.next_song()

                self.current_playlist.next_song()

    def stop(self) -> None:
        """
        Stops the current playing playlist.

        Parameters:
            self: The instance of the class.

        Return Type:
            None

        Example Usage:
            obj = ClassName()
            obj.stop()
        """
        if self.current_playlist:
            self.current_playlist.stop_playing()

        self.force_stop = True

    def stream_audio(self, song: Song) -> None:
        """
        Streams audio from a given Song object to the shoutcast server.

        Parameters:
            song` (Song): The Song object representing the audio to be streamed.

        Returns:
            None

        """
        temp = open(song.get_filename(), "rb")
        self.shout.set_metadata({"song": song.get_song_name()})
        new_buffer = temp.read(4096)
        while len(new_buffer) != 0 and self.force_next is False:
            if self.force_stop:
                break

            buffer = new_buffer
            new_buffer = temp.read(4096)
            self.shout.send(buffer)
            self.shout.sync()

        temp.close()

        self.force_next = False
