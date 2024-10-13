import threading
import shout
import random
from .song import Song
from typing import Callable


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
            shout.SHOUT_AI_CHANNELS: "2",
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
        self.has_started = False

        self.callbacks = {
            "nextsong": [],
            "song_announcement": None,
            "song_announcement_played": None,
            "should_announce_next_song": None,
            "prepare_next_announcement": None,
            "stream_started": None,
            "stream_ended": None
        }

    def __enter__(self):
        return self

    def __exit__(self, type, value, tb):
        pass

    def set_announce_songs(self, should_announce: bool) -> None:
        """
        Set the value for the announce_songs property.

        Parameters:
        - should_announce (bool): A boolean value indicating whether to announce the songs.

        """
        self.announce_songs = should_announce

    def is_announcing_songs(self) -> bool:
        """
        Determines whether the songs should be announced.

        :return: True if the songs should be announced, False otherwise
        """
        return self.announce_songs

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

    def should_announce_next_song(self) -> Callable:
        def inner(f):
            self.callbacks["should_announce_next_song"] = f
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

    def prepare_announcement(self):
        def inner(f):
            """

                Add a callback function to handle the preparation of the next announcement.

                Args:
                    f (function): The callback function to be added.

                Returns:
                    function: The same callback function.

            """
            self.callbacks["prepare_next_announcement"] = f
            return f

        return inner

    def stream_started(self):
        """
        Sets the callback function for when a stream has started.

        Parameters:
            f (function): The callback function to be set.

        Returns:
            The callback function.

        Example:
            >>> def my_callback():
            ...     print("Stream has started")
            ...
            >>> obj = MyClass()
            >>> obj.stream_started()(my_callback)
            Stream has started
        """
        def inner(f):
            self.callbacks["stream_started"] = f
            return f

        return inner

    def stream_ended(self):
        """
        Registers a callback function to be executed when the stream has ended.

        :param self: The instance of the class.
        :return: The callback function.
        """
        def inner(f):
            self.callbacks["stream_ended"] = f
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
            if callable(callback):
                if callback.__code__.co_argcount > 0:
                    callback(self.get_current_song())
                else:
                    callback()

    def _should_announce_next_song(self) -> None:
        """
        Check if the next song should be announced.

        Parameters:
            self: The instance of the class.

        Returns:
            None
        """
        callback = self.callbacks["should_announce_next_song"]
        if callable(callback):
            self.announce_songs = callback()

    def _prepare_next_announcement(self) -> None:
        """
        Prepare the next announcement by invoking all the callbacks registered for the "prepare_next_announcement" event.

        :return: None
        """
        if not self.announce_songs:
            return


        callback = self.callbacks["prepare_next_announcement"]
        if callable(callback):
            song = self.current_playlist.get_next_song()
            if song:
                thread = threading.Thread(target=callback, args=(song,))
                thread.start()

    def _stream_start(self) -> None:
        """
        Advertise the stream has started.
        """
        callback = self.callbacks["stream_started"]
        if callable(callback):
            callback()

    def _stream_ended(self) -> None:
        """
        Advertise the stream has ended.
        """
        callback = self.callbacks["stream_ended"]
        if callable(callback):
            callback()

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
            if callback.__code__.co_argcount > 0:
                return callback(self.get_current_song())
            else:
                return callback()

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
            if callback.__code__.co_argcount > 0:
                return callback(song)
            else:
                return callback()

        return None

    def set_playlist(self, playlist) -> None:
        """
        Set the current playlist.

        Parameters:
            playlist (Playlist): The playlist to be set.

        Returns:
            None

        """
        self.stop(False)
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


    def set_first_song(self):
        self.current_song = self.current_playlist.get_first_song()

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


        is_first_song: bool = True

        self.shout.open()
        self.set_first_song()
        self._should_announce_next_song()
        self._prepare_next_announcement()

        if self.current_playlist:

            self.current_playlist.start_playing()
            self._stream_start()
            self.has_started = True

            while self.current_playlist.is_playing():
                self.current_song = self.current_playlist.get_current_song()

                if self.announce_songs:
                    announcement: Song or None = self.request_next_song_announcement()
                    if announcement:
                        self.stream_audio(announcement)
                        self.announcement_finished_playing(announcement)

                self.advertise_new_song()
                self._should_announce_next_song()

                if not is_first_song:
                    self._prepare_next_announcement()

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
                is_first_song = False

    def stop(self, announce: bool = True) -> None:
        """
        Stops the current playing playlist.

        Parameters:
            self: The instance of the class.
            announce: If true the stream stopping will be announced.

        Return Type:
            None

        Example Usage:
            obj = ClassName()
            obj.stop()
        """
        if self.current_playlist:
            self.current_playlist.stop_playing()

        if announce and self.has_started:
            self._stream_ended()

        self.force_stop = True
        self.has_started = False

    def stream_audio(self, song: Song) -> None:
        """
        Streams audio from a given Song object to the shoutcast server.

        Parameters:
            song` (Song): The Song object representing the audio to be streamed.

        Returns:
            None

        """
        bsize: int = 8192
        temp = open(song.get_filename(), "rb")
        self.shout.set_metadata({"song": song.get_song_name()})

        print("Streaming ", song.get_song_name())
        while True:
            if self.force_next or self.force_stop:
                break

            self.shout.sync()
            buffer = temp.read(bsize)

            if len(buffer) == 0:
                break

            self.shout.send(buffer)
            self.shout.sync()

        temp.close()
        self.force_next = False
