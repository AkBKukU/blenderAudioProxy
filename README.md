# blenderAudioProxy
Generate separate lower bitrate ogg proxy audio files for the Blender VSE.

## The Problem
My camera records audio as 16b PCM embedded inside the recorded MOV file. I am
using NFS & SFTP and editing videos over a network. Sometimes Wifi. While the proxy
video files work great, Blender still streams the full audio from the original
source.

## The Solution
So I decided it would be best to generate proxy audio sources. Using ffmpy I can
go through all audio clips in the scene and create smaller separate audio files.

By default, these are stored in the `BL_proxy` project proxy directory under a
new `audio` folder as an ogg. Both the path of the proxies and the output format
are configurable in the render panel.

## Usage
This plugin adds an option to the `Strip` menu in the VSE for "Audio Proxy".
After you have loaded all your sound clips into the scene you can go into the
menu and select "Create Audio Proxies". This will freeze Blender but in the
background ffmpy is creating the proxy files. After it is done the sound clips
in the scene will now have a custom property that stores the location of the
original source and the new proxy. You can use the options in the menu "Use
Proxy" or "Use Original" to switch between them. When a render begins it will
automatically switch back to the originals.


## Setup
You will need to install ffmpy with pip so blender can use FFMpeg. Blender is
uses Python 3 for plugins so you will need to specify that when installing.

 1. Install [FFMPEG](https://www.ffmpeg.org/) on your system
 2. Download [get-pip.py](https://bootstrap.pypa.io/get-pip.py)
 3. Run `get-pip.py` with the version of python blender is using. Likely
	`sudo python3 ./get-pip.py`
 4. Use that pip install to install `ffmpy`. Likely `sudo pip3 install ffmpy`

\*Note: Only tested on Ubuntu

