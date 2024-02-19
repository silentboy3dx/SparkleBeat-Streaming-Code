from Streaming.playlist import Playlist
from Streaming.stream import Stream
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


@stream.nextsong()
def on_new_song(song):
    print("Playing", song.get_song_name())


playlist = Playlist()
jingles = Playlist()
advertisements = Playlist()

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

while True:
    input("Press enter for new next song\n")
    stream.next_song()
