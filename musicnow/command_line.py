#!/usr/bin/env python

from . import repair
from . import log

import argparse
from os import system, rename, listdir, curdir, name
from os.path import basename
from collections import OrderedDict
import re

from bs4 import BeautifulSoup
import requests
import youtube_dl
import spotipy

import six

if six.PY2:
    from urllib2 import urlopen
    from urllib2 import quote
    input = raw_input
elif six.PY3:
    from urllib.parse import quote
    from urllib.request import urlopen

YOUTUBECLASS = 'spf-prefetch'


def get_tracks_from_album(album_name):
    '''
    Gets tracks from an album using Spotify's API
    '''

    spotify = spotipy.Spotify()

    album = spotify.search(q='album:' + album_name, limit=1)
    album_id = album['tracks']['items'][0]['album']['id']
    results = spotify.album_tracks(album_id=str(album_id))
    songs = []
    for items in results['items']:
        songs.append(items['name'])

    return songs


def get_url(song_input, auto):
    '''
    Provides user with a list of songs to choose from
    returns the url of chosen song.
    '''

    print('\n')

    youtube_list = OrderedDict()
    num = 0  # List of songs index

    html = requests.get("https://www.youtube.com/results",
                        params={'search_query': song_input})
    soup = BeautifulSoup(html.text, 'html.parser')

    # In all Youtube Search Results

    for i in soup.findAll('a', {'rel': YOUTUBECLASS}):
        song_url = 'https://www.youtube.com' + (i.get('href'))
        song_title = (i.get('title'))
        # Adds title and song url to dictionary
        youtube_list.update({song_title: song_url})

        if not auto:
            print('(%s) %s' % (str(num + 1), song_title))  # Prints list
            num = num + 1

        elif auto:
            print(song_title)
            return list(youtube_list.values())[0], list(youtube_list.keys())[0]

    # Checks if YouTube search return no results
    if youtube_list == {}:
        log.log_error('No match found!')
        exit()

    # Gets the demanded song title and url
    song_url, song_title = prompt(youtube_list)

    return song_url, song_title  # Returns Name of Song and URL of Music Video


def prompt(youtube_list):
    '''
    Prompts for song number from list of songs
    '''

    option = int(input('\nEnter song number > '))
    try:
        song_url = list(youtube_list.values())[option - 1]
        song_title = list(youtube_list.keys())[option - 1]
    except IndexError:
        log.log_error('Invalid Input')
        exit()

    system('clear')
    print('Download Song: ')
    print(song_title)
    print('Y/N?')
    confirm = input('>')
    if confirm.lower() == 'y':
        pass
    elif confirm.lower() == 'n':
        exit()
    else:
        log.log_error('Invalid Input')
        exit()

    return song_url, song_title


def download_song(song_url, song_title):
    '''
    Downloads song from youtube-dl
    '''
    outtmpl = song_title + '.%(ext)s'
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': outtmpl,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        },
            {'key': 'FFmpegMetadata'},
        ],

    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(song_url, download=True)


def main():
    '''
    Starts here, handles arguments
    '''

    system('clear')

    parser = argparse.ArgumentParser(
        description='Download songs with album art and metadata!')
    parser.add_argument('-m', '--multiple', action='store', dest='multiple_file',
                        help='Download multiple songs from a text file list')
    parser.add_argument('-a', '--auto', action='store_true',
                        help='Automatically chooses top result')
    parser.add_argument('--album', action='store_true',
                        help='Downloads all songs from an album')
    args = parser.parse_args()
    arg_multiple = args.multiple_file or None
    arg_auto = args.auto or None
    arg_album = args.album or None

    if arg_multiple and arg_album:
        log.log_error("Can't do both!")

    elif arg_album:
        album_name = input('Enter album name : ')
        try:
            tracks = get_tracks_from_album(album_name)
            [print(songs) for songs in tracks]
            confirm = input(
                '\nAre these the songs you want to download? (y/n)\n> ')

        except IndexError:
            log.log_error("Couldn't find album")
            exit()

        if confirm.lower() == ('y'):
            for track_name in tracks:
                track_name = track_name + ' song'
                song_url, file_name = get_url(track_name, arg_auto)
                download_song(song_url, file_name)
                system('clear')
                repair.fix_music(file_name + '.mp3')

        elif confirm.lower() == 'n':
            log.log_error("Sorry, if appropriate results weren't found")
            exit()
        else:
            log.log_error('Invalid Input')
            exit()

    elif arg_multiple:
        with open(arg_multiple, "r") as f:
            file_names = []
            for line in f:
                file_names.append(line.rstrip('\n'))

        for files in file_names:
            files = files + ' song'
            song_url, file_name = get_url(files, arg_auto)
            download_song(song_url, file_name)
            system('clear')
            repair.fix_music(file_name + '.mp3')

    else:
        query = input('Enter Song Name : ')
        song_url, file_name = get_url(query, arg_auto)  # Gets YT url
        download_song(song_url, file_name)  # Saves as .mp3 file
        system('clear')
        repair.fix_music(file_name + '.mp3')


if __name__ == '__main__':
    main()
