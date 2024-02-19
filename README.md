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
