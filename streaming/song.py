import os


class Song:
    """
    A class representing a song.

    Attributes:
        is_playing (bool): Whether the song is currently playing.
        is_paused (bool): Whether the song is currently paused.
        is_stopped (bool): Whether the song is currently stopped.
        file (str): The path to the song file.
        basename (str): The filename of the song file.
    """

    def __init__(self, file: str,  song_name = "", song_artist: str = "", song_requested_by: str = ""):
        self.is_playing = False
        self.is_paused = False
        self.is_stopped = True
        self.requested_by = song_requested_by
        self.file = file
        self.basename = os.path.basename(self.file)
        self.song_name =  song_name
        self.artist = song_artist

        if len(song_name) == 0:
            name: str = self.basename.split("/")[-1].split(".")
            name = (".".join(name[:len(name) - 1]).replace("_", " ").replace("-", " - "))
            self.set_song_name(name)


    def is_request(self):
        """

        Check if the song was requested.

        Returns:
            bool: True if the object has requests, False otherwise.

        """
        return len(self.requested_by) > 0

    def get_requested_by(self):
        """
        Returns the name of the person requesting the song.

        :return: The value of the 'requested_by' parameter.
        :rtype: The data type of the 'requested_by' parameter.
        """
        return self.requested_by

    def play(self) -> None:
        """
        Start playing the audio.

        This method sets the `is_playing` flag to True, indicating that the audio is currently being played.
        It also sets the `is_paused` and `is_stopped` flags too False to indicate that the audio is not paused or
        stopped.

        Returns:
            None
            
        """
        self.is_playing = True
        self.is_paused = False
        self.is_stopped = False

    def pause(self) -> None:
        """
        This method pauses the playback of the audio.

        Parameters:
            self : object
                The instance of the class.

        Returns:
            None

        """
        self.is_playing = False
        self.is_paused = True
        self.is_stopped = False

    def stop(self) -> None:
        """
        Stops the playback.

        Sets the `is_playing` attribute to False, indicating that the playback has stopped.
        Sets the `is_paused` attribute to False, indicating that the playback is not paused.
        Sets the `is_stopped` attribute to True, indicating that the playback has fully stopped.

        This method does not return any value.

        Example usage:
            player = AudioPlayer()
            player.stop()
        """
        self.is_playing = False
        self.is_paused = False
        self.is_stopped = True

    def playing(self) -> bool:
        return self.is_playing

    def get_filename(self) -> str:
        """
        Get the filename of the current instance.

        Returns:
            str: The filename of the current instance.
        """
        return self.file

    def set_song_name(self, song_name: str) -> None:
        self.song_name = song_name

    def get_song_name(self) -> str:
        """
        Format song name from filename
        strips "mp3" and changes _ to " "
        Used for metadata
        """
        return self.song_name

    def get_artist(self) -> str:
        """
        Get the artist of the current instance.

        Returns:
            str: The artist of the current instance.
        """
        return self.artist