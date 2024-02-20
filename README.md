<h1 align="center"> DJ SparkleBeat Streaming Code</h1>

<p align="center">
    <img src="assets/sparklebeat.png" width="250"  height="250" alt="Picture of DJ SparkleBeat" />
</p>
<p align="center">
<a href="https://github.com/silentboy3dx/SparkleBeat-Streaming-Code" title="Go to GitHub repo"><img src="https://img.shields.io/static/v1?label=silentboy3dx&message=SparkleBeat-Streaming-Code&color=blue&logo=github" alt="silentboy3dx - SparkleBeat-Streaming-Code"></a>
<a href="https://github.com/silentboy3dx/SparkleBeat-Streaming-Code"><img src="https://img.shields.io/github/stars/silentboy3dx/SparkleBeat-Streaming-Code?style=social" alt="stars - SparkleBeat-Streaming-Code"></a>
<a href="https://github.com/silentboy3dx/SparkleBeat-Streaming-Code"><img src="https://img.shields.io/github/forks/silentboy3dx/SparkleBeat-Streaming-Code?style=social" alt="forks - SparkleBeat-Streaming-Code"></a>

</p>


This repository contains the streaming code for DJ SparkleBeat, the AI DJ designed for 3DXChat. Whether you’re hosting virtual parties, creating playlists, or just vibing to the beats, DJ SparkleBeat’s streaming code powers the music experience in the game.
    
## Features
* Create playlists your own playlist by placing music in the music directory
* Random jingles by placing your jingles in the jingles folder.
* Random Advertisements by placing ads in the advertisements folder.

## Prerequisites 

You will need a few packages installed on your system in order for ***python-shout*** to compile on your system. First run 

```bash
sudo apt-get install python3-dev python3-pip libshout3-dev
```
Then continue to install the required libraries for python. 

```bash
pip install -r requirements.txt
```

## Getting Started


1. Clone this repository to your local machine.
2. Navigate to the created directory.
3. copy .env-example and fill all required information.
3. pip install -r requirements.txt
4. Make sure you have some music on the music director
5. Copy .env.example to .env and make sure you configure it to your needs.
6Run the main.py script to start the streaming service.


## Usage

```python
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

```

 
## License

MIT License

Copyright (c) 2024 Silentboy

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
