import os.path
from .parsers.m3u import M3U
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
        self.last_current_index = self.current_index
        self.loop_playlist = False
        self.is_currently_stopped = True
        self.is_currently_playing = True
        self.loop = False
        self.forced_next_song = None
        self.remove_forced_song = False
        self.start_playing_at = 0
        self.did_start_playing = False

        self.callbacks = {
            "forced_song_ended": []
        }

        self.stop_playing()

    def has_started_playing(self):
        """
        Checks whether the player has started playing.

        :return: True if the player has started playing, False otherwise
        :rtype: bool
        """
        return self.did_start_playing

    def forced_song_ended(self):
        """
        This method is used to add a callback function to the "forced_song_ended" event.

        Parameters:
            self: The instance of the class that invokes this method.

        Return Type:
            function: The callback function added to the "forced_song_ended" event.

        Example Usage:
        class MyClass:
            def __init__(self):
                self.callbacks = {"forced_song_ended": []}

            @forced_song_ended
            def my_callback(self):
                print("Song ended")

        my_class = MyClass()
        my_class.callbacks["forced_song_ended"][0]()  # Output: "Song ended"
        """

        def inner(f):
            self.callbacks["forced_song_ended"].append(f)
            return f

        return inner

    def advertise_forced_song_ended(self, song: Song) -> None:
        """
        This method advertises that a forced song has ended by calling all the registered callbacks for the
        "forced_song_ended" event.

        Parameters:
            - self: The current instance of the class.

        Return Type:
            - None

        """
        for callback in self.callbacks["forced_song_ended"]:
            callback(song)

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
        """
        Method: is_stopped

        Check if the object is currently stopped.

        Returns:
            bool: True if the object is currently stopped,
                  False otherwise.
        """
        return self.is_currently_stopped

    def from_directory(self, directory) -> None:
        """
        Loads songs from a directory.

        The method from_directory takes a directory path as input parameter and loads songs from that directory into
        the songs_array.

        Parameters:
            directory (str): The path of the directory containing the songs to load.

        Return Type:
            None

        Example Usage:
        ```
        music_player.from_directory('/path/to/directory')
        ```
        """
        if not os.path.isdir(directory):
            raise Exception("Directory not found.")

        self.files_array = glob(directory + "/*.[mM][Pp]3")
        self.files_array.sort()

        print("directory", directory)
        print("files_array", self.files_array)
        for file in self.files_array:
            if os.path.basename(file):
                self.songs_array.append(Song(file))

    def from_m3u_file(self, m3u_path: str) -> None:

        if not os.path.isfile(m3u_path):
            raise Exception("Playlist not found.")


        m3u: M3U = M3U(m3u_path)

        if len(m3u.data):
            for record in m3u.data:
                song: Song = Song(file=record['file'], song_name=record['name'], song_artist=record['artist'])
                self.songs_array.append(song)

    def get_all_songs(self) -> list[Song]:
        """
        This method returns a list of all songs in the songs_array.

        Parameters:
        - self (Playlist): The instance of the class.

        Returns:
        - list[Song]: A list containing all the songs in the songs_array.

        """
        return self.songs_array

    def get_current_song(self) -> Song or None:
        """
        Returns the current song from the songs array.

        :return: Song
        """
        print("current_index", self.current_index)
        print("songs_array", self.songs_array)

        if self.current_index in self.songs_array:
            return self.songs_array[self.current_index]

    def get_next_song(self) -> Song:
        _last_current_index = self.last_current_index
        _current_index = self.current_index

        self.next_song()
        song = self.get_current_song()

        self.last_current_index = _last_current_index
        self.current_index = _current_index
        return song

    def start_playing_at_position(self, position: int) -> None:
        """
        Start playing at the specified position.

        :param position: The position at which the playing should start.
        :type position: int

        Parameters:
            self (Playlist): The current instance of the class.
            position (int): The position at which the playing should start

        Return Type:
            None

        """
        self.start_playing_at = position
        self.start_playing()

    def start_playing(self) -> None:
        """
        Starts playing the audio.

        This method sets the 'is_currently_playing' attribute of the object to True, indicating that the audio is
        currently being played. It also sets the 'is_currently_stopped' attribute to * False, indicating that the
        audio is not stopped. Finally, it sets the 'current_index' attribute to 0, indicating that the audio playback
        is starting from the beginning.

        Returns:
            None

        """
        self.is_currently_playing = True
        self.is_currently_stopped = False
        self.did_start_playing = False

        self.current_index = self.start_playing_at
        self.last_current_index = 0

    def stop_playing(self) -> None:
        """
        Stop playing.

        Resets the current index to 0, indicating the start of the playlist. Sets the 'is_currently_stopped' flag to
        True to indicate that the playback has stopped. Sets the 'is_currently_playing *' flag too False to indicate
        that no song is currently being played.

        Returns:
            None
        """
        self.current_index = 0
        self.is_currently_stopped = True
        self.is_currently_playing = False

    def restore_current_index(self) -> None:
        """
        Restores the current index of the songs array.

        If a forced song was played, this method returns the current index of the songs array
        to the position it was before the forced song was played. If the remove_forced_song flag
        is True, the forced song will be removed from the songs array.

        Returns:
            None

        Example:
            player.restore_current_index()"""
        if self.forced_next_song and self.forced_next_song == self.current_index:
            """
            We are returning to the next_song song function after playing a forced song.
            """
            song = self.get_current_song()
            if self.remove_forced_song:
                self.songs_array.remove(self.get_current_song())

            self.forced_next_song = None
            self.current_index = self.last_current_index

            self.advertise_forced_song_ended(song)

    def previous_song(self) -> None:
        """
        Moves the current song to the previous song in the playlist.

        Returns:
            None

        Example usage:
            player = Player()
            player.previous_song()
        """
        self.restore_current_index()

        songs_length = len(self.songs_array) - 1
        self.last_current_index = self.current_index

        if self.current_index - 1 < 0:
            if self.loop_playlist:
                self.current_index = songs_length
            else:
                if self.current_index == 0 and self.is_currently_playing:
                    self.stop_playing()

                self.current_index = 0
        else:
            self.current_index -= 1

        if self.forced_next_song and self.current_index != self.forced_next_song:
            self.current_index = self.forced_next_song

        self.play_current_song()

    def next_song(self) -> None:
        """
        This method updates the current index of the playlist to select the next song. It also stops the
        currently playing song and starts playing the new current song.

        Return Type:
            None

        Example Usage:
            next_song()

        """
        self.restore_current_index()

        songs_length = len(self.songs_array) - 1
        self.last_current_index = self.current_index

        if self.current_index + 1 > songs_length:
            if self.loop_playlist:
                self.current_index = 0
            else:
                if self.current_index == songs_length and self.is_currently_playing:
                    self.stop_playing()

                self.current_index = songs_length
        else:
            self.current_index += 1

        if self.forced_next_song and self.current_index != self.forced_next_song:
            self.last_current_index = self.last_current_index
            self.current_index = self.forced_next_song

        self.play_current_song()

    def play_current_song(self) -> bool:
        """
        Plays the current song in the media player.

        Return Type:
            None

        """
        song = self.get_current_song()

        if song:
            song.play()
            return True

        return False

    def add_song_and_play_next(self, song: Song, remove_after=False) -> None:
        """
        Add the given song file to the songs_array and play it next.

        Parameters:
            self (Playlist: The instance of the current object.
            song (Song): The song to add
            remove_after (bool, optional): if set to True the forced song will be removed after playing.

        Returns:
            None

        """
        self.songs_array.append(song)
        self.forced_next_song = len(self.songs_array) - 1
        self.remove_forced_song = remove_after

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
        """
        Stop the current playing song.

        This method retrieves the current playing song and stops it.

        Parameters:
            self: The instance of the class.

        Returns:
            None.
        """
        song = self.get_current_song()
        song.stop()
