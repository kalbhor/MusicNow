# MusicNow
[![PyPI](https://img.shields.io/pypi/pyversions/Django.svg)](https://pypi.python.org/pypi/musicnow)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
##### Download Music with album art and details.
* Adds Album Art, Artist, Album, lyrics.
* Fetches data from Spotify.
* Download entire albums by using '--album' argument.
* Multiple file mode to download multiple songs continously. 
* Changes file name to "{artist} - {title}".

<br>


<img src="https://s24.postimg.org/s14nonos5/Music_Repair_GIF.gif" width="800px" height="337px" />

<br>
----
### Dependencies

##### Mac

```sh
$ brew install libav
```


##### Ubuntu
```sh
$ sudo apt-get install libav-tools
```
##### Windows
[To install libav](https://github.com/NixOS/nixpkgs/issues/5236)

### Installation

##### Python 2.x
```sh
$ pip install musicnow
```

##### Python 3.x
```sh
$ pip3 install musicnow
```
<br>
----
### How to use
```sh
$ musicnow
```
(Added new feature not present in video that downloads entire albums, ```musicnow --album```)
[![Usage](https://s30.postimg.org/6a34gq4m9/image.png)](https://www.youtube.com/watch?v=qtBTKUyWTgc "MusicNow - Usage")

<br>
----
### Options 
```
$ musicnow --help

usage: musicnow [-h] [-m MULTIPLE_FILE] [-a] [--album]

Download songs with album art and metadata!

optional arguments:
  -h, --help            show this help message and exit
  -m                    Download multiple songs from a text file list
  -a, --auto            Automatically chooses top result
  --album               Downloads all songs from an album
```
<br>
----
### Disclaimer
Use at own risk.
Downloading music with copyrights might be illegal in your country.

License
----
The MIT License (MIT)
Copyright (c) 2016 Lakshay Kalbhor

