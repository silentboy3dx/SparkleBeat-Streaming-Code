<h1 align="center"> DJ SparkleBeat Streaming Code</h1>

<p align="center">
    <img src="assets/sparklebeat.png" width="250"  height="250" alt="Alt Text" />
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
2. Navigate to the streaming_code directory.
3. pip install -r requirements.txt
4. Make sure you have some music on the music director
5. Copy .env.example to .env and make sure you configure it to your needs.
6Run the main.py script to start the streaming service.

   
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
