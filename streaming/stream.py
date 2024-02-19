import shout
import random
from .song import Song
from typing import Callable

class Stream:
    """

    Class: Stream

    Represents an audio stream that can be played on a Shoutcast server.

    Attributes:
    - shout (shout.Shout): The Shout instance used for streaming.
    - shout.audio_info (dict): Dictionary containing audio info (bitrate, samplerate, channels).
    - shout.format (str): The format of the audio stream ('mp3' or 'ogg vorbis').
    - shout.genre (str): The genre of the stream.
    - ogv (int): Flag indicating whether the format is ogg vorbis (0 or 1).
    - shout.host (str): The host of the stream.
    - shout.port (int): The port of the stream.
    - shout.password (str): The password for the stream.
    - shout.mount (str): The mount point for the stream.
    - shout.name (str): The name of the stream.
    - shout.url (str): The URL of the stream.
    - music_directory (str): The directory where the music is located.
    - shout.description (str): The description of the stream.
    - song_conter (int): The counter for the current song.

    Methods:
    - nextsong(self) -> Callable:
      Registers a callback function to be executed when the next song is played.

    - advertise_new_song(self) -> None:
      Advertises a new song by invoking the registered callbacks.

    - set_playlist(self, playlist) -> None:
      Set the current playlist.

    - set_advertisements(self, advertisements) -> None:
      Sets the list of advertisements for the current instance.

    - set_jingles(self, jingles) -> None:
      Set the jingles for the current object.

    - get_current_song(self) -> Song:
      Returns the current song.

    - next_song(self) -> None:
      Sets the `force_next` flag to True.

    - start(self) -> None:
      Starts playing the audio stream.

    - stop(self) -> None:
      Stops the current playing playlist.

    - stream_audio(self, song: Song) -> None:
      Streams audio from a given Song object to the Shoutcast server.

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
            "nextsong": [],
        }

    def nextsong(self) -> Callable:
        """
        Registers a callback function to be executed when the next song is played.

        :param self: The instance of the object.
        :return: The decorated function.
        """
        def inner(f):
            self.callbacks["nextsong"].append(f)
            return f

        return inner

    def advertise_new_song(self) -> None:
        """
        Advertises a new song by invoking the registered callbacks.

        Parameters:
        - self: The current instance of the class.

        Return Type:
        - None

        Example Usage:
        advertise_new_song(self)

        """
        for callback in self.callbacks["nextsong"]:
            callback(self.get_current_song())

    def set_playlist(self, playlist) -> None:
        """

        Set the current playlist.

        Parameters:
        - playlist (any): The playlist to be set.

        Returns:
        - None

        """
        self.stop()
        self.current_playlist = playlist

    def set_advertisements(self, advertisements) -> None:
        """
        Sets the list of advertisements for the current instance.

        :param advertisements: The list of advertisements.
        :type advertisements: list
        :return: None
        """
        self.current_advertisements = advertisements

    def set_jingles(self, jingles) -> None:
        """
        Set the jingles for the current object.

        :param jingles: A list of jingles to be set.
        :type jingles: list
        :return: None
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
        - self: Reference to the current instance of the class.

        Returns:
        - None
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
        - If a jingle should be played and there is a current jingle available, it plays the jingle and moves to the next jingle
        - If an advertisement should be played and there is a current advertisement available, it plays the advertisement and moves to the next advertisement
        - Moves to the next song in the playlist

        Parameters:
        - None

        Returns:
        - None
        """
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
                        self.current_jingles.next_song()
                        matched = True

                    if self.current_advertisements and self.advertisement_chance <= delta and matched is False:
                        self.current_song = self.current_advertisements.get_current_song();
                        self.stream_audio(self.current_advertisements.get_current_song())
                        self.current_advertisements.next_song()

                self.current_playlist.next_song()

    def stop(self) -> None:
        """
        Stops the current playing playlist.

        Parameters:
        - self: The instance of the class.

        Return Type:
        - None

        Example Usage:
            obj = ClassName()
            obj.stop()
        """
        if self.current_playlist:
            self.current_playlist.stop_playing()

    def stream_audio(self, song: Song) -> None:
        """

        Streams audio from a given Song object to the shoutcast server.

        Parameters:
        - `song` (Song): The Song object representing the audio to be streamed.

        Returns:
        None

        """
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
