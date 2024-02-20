from streaming.playlist import Playlist
from streaming.song import Song
from streaming.stream import Stream
from dotenv import load_dotenv
import threading
import os

load_dotenv()

stream = Stream(
    mount_point=os.getenv("STREAM_MOUNT_POINT"),
    music_directory=os.getenv("STREAM_MUSIC_DIRECTORY"),
    station_url=os.getenv("STREAM_URL"),
    genre=os.getenv("STREAM_GENRE"),
    name=os.getenv("STREAM_NAME"),
    description=os.getenv("STREAM_DESCRIPTION"),
    stream_host=os.getenv("STREAM_HOST"),
    stream_port=os.getenv("STREAM_PORT"),
    stream_password=os.getenv("STREAM_PASSWORD"),
)

playlist = Playlist()
jingles = Playlist()
advertisements = Playlist()
requested_songs = []
remove_requests = True


@stream.nextsong()
def on_new_song(song: Song) -> None:
    """
    This function is called when a new song is starting.
    SparkleBeat uses this to send out notification of a new song to the game chat.
    """
    print("Playing", song.get_song_name())


@playlist.forced_song_ended()
def on_forced_song_ended(song: Song) -> None:
    """
    Callback from when a forced song has ended.
    SparkleBeat uses this ether queue up a next request.
    """

    print("Forced song ended:", song.get_song_name())

    if song.get_filename() in requested_songs:
        requested_songs.remove(song.get_filename())

        if len(requested_songs):
            file = requested_songs[0]
            playlist.add_song_and_play_next(file, remove_after=remove_requests)


def request_song(file: str, announce=False) -> None:
    if announce is True:
        requested_songs.append("music/announcement.mp3")

    requested_songs.append(file)
    playlist.add_song_and_play_next(file, remove_after=remove_requests)


playlist.from_directory(os.getenv("STREAM_MUSIC_DIRECTORY"))
jingles.from_directory(os.getenv("STREAM_JINGLE_DIRECTORY"))
advertisements.from_directory(os.getenv("STREAM_ADVERTISEMENT_DIRECTORY"))
playlist.set_loop(True)

stream.set_playlist(playlist)
stream.set_advertisements(advertisements)
stream.set_jingles(jingles)

bg_thread = threading.Thread(target=stream.start)
bg_thread.daemon = True  # Set the thread as a daemon
bg_thread.start()

"""
This is an optional feature. You dont have to use 
this and the playlist will just play the songs in order.

After playing a requested song the normal playlist will
resume.
"""
request_song("music/next.mp3")

try:
    while True:
        pass

except KeyboardInterrupt:
    for song in playlist.get_all_songs():
        print(song.get_song_name())
