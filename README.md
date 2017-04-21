<img src="https://s24.postimg.org/s14nonos5/Music_Repair_GIF.gif" width="700px" height="300px" />

# MusicNow

[![license](https://img.shields.io/github/license/mashape/apistatus.svg?style=flat-square)](LICENSE)
[![standard-readme compliant](https://img.shields.io/badge/readme%20style-standard-brightgreen.svg?style=flat-square)](https://github.com/RichardLitt/standard-readme)

> MusicNow is a python script that downloads music and albums with important tags such as : album name, artist name, lyrics and album art.

**You can now download songs online with metadata at [MusicSeize.com](https://musicseize.com)**

## Social:

[![GitHub stars](https://img.shields.io/github/stars/kalbhor/musicnow.svg?style=social&label=Star)](https://github.com/kalbhor/musicnow)
[![GitHub followers](https://img.shields.io/github/followers/kalbhor.svg?style=social&label=Follow)](https://github.com/kalbhor)  
[![Twitter Follow](https://img.shields.io/twitter/follow/lakshaykalbhor.svg?style=social)](https://twitter.com/lakshaykalbhor)


## Table of Contents

- [Features](#features)
- [Dependencies](#dependencies)
- [Installation](#installation)
  - [PyPI](#pypi)
  - [Source](#source)
- [Usage](#usage)
  - [Options](#options)
- [Disclaimer](#disclaimer)
- [Contribute](#contribute)
- [License](#license)

## Features

1. Downloads entire songs from youtube.
2. Fetches lyrics from [Genius](https://www.genius.com)
3. Fetches metadata from [Spotify](https://www.spotify.com)
4. Downloads entire albums.
5. Changes file name to "{artist} - {title}"


## Dependencies 

### Mac

```sh
$ brew install libav
```

### Ubuntu
```sh
$ sudo apt-get install libav-tools
```

### Windows
[Install libav](https://github.com/NixOS/nixpkgs/issues/5236)

[Check this for utf-8 errors](https://github.com/kalbhor/MusicRepair/issues/26)

### [Genius API](https://genius.com/api-clients)

1. Create an account and register an application 
2. Grab Access Token
3. Set access token in config file

### [Bing Search API](https://www.microsoft.com/cognitive-services/en-us/bing-image-search-api)

1. Create an account
2. Grab Access Token
3. Set access token in config file

```sh 
$ musicnow --config                                               
     
Enter Genius key : <enter genius key>                                 
Enter Bing key : <enter bing key>
```

## Installation

### PyPI
```sh
$ pip install musicnow
```

### Source
```sh
$ git clone https://github.com/kalbhor/MusicNow
$ cd MusicNow
$ python setup.py install
```

## Usage

```sh
$ musicnow
```

[![Usage](https://s30.postimg.org/6a34gq4m9/image.png)](https://www.youtube.com/watch?v=qtBTKUyWTgc "MusicNow - Usage")

### Options
```
$ musicnow --help
usage: musicnow [-h] [-c] [-m MULTIPLE_FILE] [-a] [--album]

Download songs with album art and metadata!

optional arguments:
  -h, --help            show this help message and exit
  -c, --config          Set your API keys
  -m MULTIPLE_FILE, --multiple MULTIPLE_FILE
                        Download multiple songs from a text file list
  -a, --auto            Automatically chooses top result
  --album               Downloads all songs from an album
```

## Disclaimer
Use at own risk.
Downloading music with copyrights might be illegal in your country.

## Contribute

Found an issue? Post it in the [issue tracker](https://github.com/kalbhor/MusicNow/issues). <br> 
Want to add another awesome feature? [Fork](https://github.com/kalbhor/MusicNow/fork) this repository and add your feature, then send a pull request.

## License
The MIT License (MIT)
Copyright (c) 2017 Lakshay Kalbhor
