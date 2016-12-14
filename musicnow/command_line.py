#!/usr/bin/env python

from . import repair
from . import log

from os import system, rename, listdir, curdir, name
from collections import OrderedDict
import re

from bs4 import BeautifulSoup
import requests
import youtube_dl

import six

if six.PY2:
    from urllib2 import urlopen
    from urllib2 import quote
    input = raw_input
elif six.PY3:
    from urllib.parse import quote
    from urllib.request import urlopen

YOUTUBECLASS = 'spf-prefetch'


def get_url(song_input):

    print('\n')

    youtube_list = OrderedDict()
    num = 0  # List of songs index
    song_input = song_input.replace(' ', '+')
    song_input = 'https://www.youtube.com/results?search_query=' + song_input
    html = requests.get(song_input)
    soup = BeautifulSoup(html.text, 'html.parser')

    # In all Youtube Search Results
    for i in soup.findAll('a', {'rel': YOUTUBECLASS}):
        song_url = 'https://www.youtube.com' + (i.get('href'))
        song_title = (i.get('title'))
        # Adds title and song url to dictionary
        youtube_list.update({song_title: song_url})

        print('(%s) %s' % (str(num + 1), song_title))  # Prints list

        num = num + 1

    # Gets the demanded song title and url
    song_url, song_title = prompt(youtube_list)

    return song_url, song_title  # Returns Name of Song and URL of Music Video


def prompt(youtube_list):

    x = int(input('\nEnter song number > '))
    x = x - 1
    song_url = list(youtube_list.values())[x]
    song_title = list(youtube_list.keys())[x]
    system('clear')
    print('Download Song: ')
    print(song_title)
    print('Y/N?')
    x = input('>')
    if x == 'Y' or x == 'y':
        pass
    elif x == 'N' or x == 'n':
        exit()
    else:
        log.log_error('Invalid Input')
        exit()

    return song_url, song_title


def download_song(song_url, song_title):

    file_name = None

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([song_url])  # Downloads audio using youtube-dl

    try:

        files = listdir(curdir)
        for songs in files:
            re_found = re.match(re.escape(song_title) +
                                r'.*\.mp3$', songs, re.UNICODE)
            if re_found:
                file_name = re_found.group()
                break

        if file_name != None:
            # Renames file to song title
            rename(file_name, song_title + '.mp3')
        else:
            file_name = (song_title + '-' + song_url[32:] + '.mp3')
            rename(file_name, song_title + '.mp3')
    except Exception:
        log.log_error("Could not rename the file")
        pass


def main():

    system('clear')
    query = input('Enter Song Name : ')
    song_url, file_name = get_url(query)  # Gets YT url
    download_song(song_url, file_name)  # Saves as .mp3 file
    system('clear')
    repair.fix_music(file_name + '.mp3')


if __name__ == '__main__':
    main()
