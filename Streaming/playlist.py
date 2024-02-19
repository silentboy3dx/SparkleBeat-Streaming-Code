from .song import Song
from glob import glob


class Playlist:
    def __init__(self):
        """
        Initialize the class instance.

        This method initializes the class instance and sets the initial values of
        various attributes and variables.

        Returns:
            None
        """
        self.files_array = []
        self.songs_array = []

        self.current_index = 0
        self.loop_playlist = False
        self.is_currently_stopped = True
        self.is_currently_playing = True
        self.loop = False

        self.stop_playing()

    def set_loop(self, value) -> None:
        """

        Set the loop option for the playlist.

        Parameters:
            value (bool): The loop option value to set.

        Returns:
            None

        """
        self.loop_playlist = value

    def is_playing(self) -> bool:
        """
        Check if the object is currently playing.

        Returns:
            bool: True if the object is currently playing, False otherwise.
        """
        return self.is_currently_playing

    def is_stopped(self) -> bool:
        return self.is_currently_stopped

    def from_directory(self, directory) -> None:
        """Loads songs from a directory.

        The method from_directory takes a directory path as input parameter and loads songs from that directory into the songs_array.

        Parameters:
        - directory (str): The path of the directory containing the songs to load.

        Return Type:
        None

        Example Usage:
        ```
        music_player.from_directory('/path/to/directory')
        ```
        """
        self.files_array = glob(directory + "/*.[mM][Pp]3")
        self.files_array.sort()

        for file in self.files_array:
            self.songs_array.append(Song(file))

    def get_all_songs(self) -> list[Song]:
        """

        Method Name: get_all_songs

        Description:
        This method returns a list of all songs in the songs_array.

        Parameters:
        - self (object): The instance of the class.

        Returns:
        - list[Song]: A list containing all the songs in the songs_array.

        """
        return self.songs_array

    def get_current_song(self) -> Song:
        """
        Returns the current song from the songs array.

        :return: Song
        """
        return self.songs_array[self.current_index]

    def start(self) -> None:
        self.stop_current_song()
        self.start_playing()

    def start_playing(self) -> None:
        """

        Starts playing the audio.

        This method sets the 'is_currently_playing' attribute of the object to True, indicating that the audio is currently being played. It also sets the 'is_currently_stopped' attribute to
        * False, indicating that the audio is not stopped. Finally, it sets the 'current_index' attribute to 0, indicating that the audio playback is starting from the beginning.

        Returns:
            None

        """
        self.is_currently_playing = True
        self.is_currently_stopped = False
        self.current_index = 0

    def stop_playing(self) -> None:
        """
        Stop playing.

        Resets the current index to 0, indicating the start of the playlist. Sets the 'is_currently_stopped' flag to True to indicate that the playback has stopped. Sets the 'is_currently_playing
        *' flag to False to indicate that no song is currently being played.

        Returns:
            None
        """
        self.current_index = 0
        self.is_currently_stopped = True
        self.is_currently_playing = False

    def previous_song(self) -> None:
        """
        Moves the current song to the previous song in the playlist.

        Returns:
            None

        Example usage:
            player = Player()
            player.previous_song()
        """
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

    def next_song(self) -> None:
        """
        Method: next_song

        Description:
        This method updates the current index of the playlist to select the next song. It also stops the currently playing song and starts playing the new current song.

        Return Type:
        - None

        Example Usage:
        next_song()

        """
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

    def play_current_song(self) -> None:
        """

        Plays the current song in the media player.

        :param self: The current instance of the media player.
        :type self: object

        :return: None
        :rtype: None

        """
        song = self.get_current_song()
        song.play()

    def pause_current_song(self) -> None:
        """
        Pause the current song.

        Parameters:
        self: The instance of the current object.

        Returns:
        None
        """
        song = self.get_current_song()
        song.pause()

    def stop_current_song(self) -> None:
        """Stop the current playing song.

        This method retrieves the current playing song and stops it.

        Parameters:
            self: The instance of the class.

        Returns:
            None.
        """
        song = self.get_current_song()
        song.stop()
