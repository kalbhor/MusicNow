# MusicNow
[![PyPI](https://img.shields.io/pypi/pyversions/Django.svg)](https://pypi.python.org/pypi/musicnow)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
##### Download Music with album art and details.
* Adds Album Art, Artist, Album, lyrics.
* Fetches data from Spotify.
* Multiple file mode to download multiple songs continously. 
* Changes file name to "{artist} - {title}".

<br>
___
<p align="center">
<img src="https://s27.postimg.org/bkz6sum2b/Final.png" width="702px" height="450px" />
</p>
<br>
___
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
___
### How to use
```sh
$ musicnow
```
(Outdated, will update soon)
![](https://media.giphy.com/media/3oriO2m4SAjRVKeWgE/source.gif)

<br>
___
### Options 
```
$ musicnow --help

usage: musicnow [-h] [-m MULTIPLE_FILE] [-a]

Download songs with album art and metadata!

optional arguments:
  -h, --help            show this help message and exit
  
  -m                    Download multiple songs from a text file list
                        
  -a, --auto            Automatically chooses top result
```
<br>
___
License
----
The MIT License (MIT)
Copyright (c) 2016 Lakshay Kalbhor

