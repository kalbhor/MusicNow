#!/usr/bin/env python
from __future__ import print_function
from os import system, rename
from sys import version_info, stdin
from collections import OrderedDict
from select import select
from time import sleep

from bs4 import BeautifulSoup
import requests
import json
import youtube_dl

from mutagen.mp3 import MP3
from mutagen.id3 import ID3, TIT2, TALB, TPE1, TPE2, APIC


if version_info[0] < 3:
    input = raw_input
    from urllib2 import urlopen, Request
    from urllib2 import quote
else:
    from urllib.parse import quote
    from urllib.request import urlopen, Request


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[32m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    GRAY = '\033[30m'
    YELLOW = '\033[33m'

tick = u'\u2713'


def getURL(songInput):

    print(bcolors.YELLOW)
    print('\n')

    YoutubeList = OrderedDict()
    num = 0  # List of songs index
    songInput = songInput.replace(' ', '+')
    songInput = 'https://www.youtube.com/results?search_query=' + songInput
    html = requests.get(songInput)
    soup = BeautifulSoup(html.text, 'html.parser')

    YoutubeClass = 'spf-prefetch'  # YouTube Class holding video

    # In all Youtube Search Results
    for i in soup.findAll('a', {'rel': YoutubeClass}):
        songURL = 'https://www.youtube.com' + (i.get('href'))
        songTitle = (i.get('title'))
        # Adds title and song url to dictionary
        YoutubeList.update({songTitle: songURL})

        print('(%s) %s' % (str(num + 1), songTitle))  # Prints list

        num = num + 1

    # Gets the demanded song title and url
    songURL, songTitle = prompt(YoutubeList)

    print(bcolors.ENDC)

    return songURL, songTitle  # Returns Name of Song and URL of Music Video


def prompt(YoutubeList):

    x = int(input('\nEnter song number > '))
    x = x - 1
    songURL = list(YoutubeList.values())[x]
    songTitle = list(YoutubeList.keys())[x]
    system('clear')
    print('Download Song: ', end=' ')
    print(songTitle, end=' ')
    print(bcolors.UNDERLINE)
    print('Y/N?')
    print(bcolors.ENDC)
    x = input('>')
    if x == 'Y' or x == 'y':
        pass
    elif x == 'N' or x == 'n':
        exit()
    else:
        print('Invalid input')
        exit()

    return songURL, songTitle


def downloadSong(songURL, songTitle):

    print(bcolors.ENDC)
    FileName = (songTitle + '-' + songURL[32:] + '.mp3')
    songTitle = (songTitle + '.mp3')

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([songURL])  # Downloads audio using youtube-dl

    try:
        rename(FileName, songTitle)  # Renames file to song title
    except Exception as e:
        print(bcolors.FAIL)
        print("Could not rename the file : %s" % e)
        print(bcolors.ENDC)
        pass


def getDetails(songName):

    print(bcolors.FAIL)
    timeout = 10
    songName = songName.replace(' ', '+')
    url = "http://search.letssingit.com/cgi-exe/am.cgi?a=search&artist_id=&l=archive&s=" + songName
    html = requests.get(url)
    soup = BeautifulSoup(html.text, "html.parser")
    link = soup.find('a', {'class': 'high_profile'})
    try:
        link = link.get('href')
        link = requests.get(link)

        soup = BeautifulSoup(link.text, "html.parser")

        AlbumDiv = soup.find('div', {'id': 'albums'})
        TitleDiv = soup.find('div', {'id': 'content_artist'}).find('h1')

        try:
            songTitle = TitleDiv.contents[0]
            songTitle = songTitle[1:-8]
        except Exception as e:
            print("Couldn't reset song title : %s" % e, end=' ')
            songTitle = songName

        try:
            artist = TitleDiv.contents[1].getText()
        except Exception as e:
            print("Couldn't find artist name : %s" % e, end=' ')
            artist = "Unknown"

        try:
            album = AlbumDiv.find('a').contents[0]
            album = album[:-7]
        except Exception as e:
            print("Couldn't find the album name : %s" % e, end=' ')
            album = songName

    except Exception:

        print(
            "Couldn't find song details, would you like to manually enter them? (Y/N) : ")
        rlist, _, _ = select([stdin], [], [], 10)
        if rlist:
            check = stdin.readline()
        else:
            print("No input. Moving on.")
            album = songName
            songTitle = songName
            artist = "Unknown"

            print(bcolors.ENDC)

            return artist, album, songTitle

        if check == 'Y\n' or check == 'y\n':

            album = input("Enter album name : ")
            songTitle = input("Enter song title : ")
            artist = input("Enter song artist : ")

        print(bcolors.ENDC)

    return artist, album, songTitle


def getAlbumArt(album):

    print(bcolors.OKGREEN)
    print("\nFetching Album Art..")
    print(bcolors.ENDC)

    album = album + " Album Art"
    album = album.replace(' ', '+')

    url = ("https://www.google.co.in/search?q=" +
           quote(album.encode('utf-8')) + "&source=lnms&tbm=isch")
    header = {'User-Agent':
              "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"
              }

    soup = BeautifulSoup(urlopen(Request(url, headers=header)), "html.parser")

    a = soup.find("div", {"class": "rg_meta"})
    albumArt = json.loads(a.text)["ou"]

    return albumArt


def add_AlbumArt(albumArt, songTitle):

    img = urlopen(albumArt)  # Gets album art from url
    try:
        audio = MP3(songTitle, ID3=ID3)
        try:
            audio.add_tags()
        except Exception:
            pass

        audio.tags.add(
            APIC(
                encoding=3,  # UTF-8
                mime='image/png',
                type=3,  # 3 is for album art
                desc='Cover',
                data=img.read()  # Reads and adds album art
            )
        )
        audio.save()

    except Exception as e:
        print(bcolors.FAIL)
        print("An Error occured while adding the album art : %s " % e)
        print(bcolors.ENDC)
        pass


def add_Details(FileName, songTitle, artist, album):

    print(bcolors.OKGREEN)
    print("Adding song details..")
    print(bcolors.ENDC)

    try:
        tags = ID3(FileName)
        tags["TALB"] = TALB(encoding=3, text=album)
        tags["TIT2"] = TIT2(encoding=3, text=songTitle)
        tags["TPE1"] = TPE1(encoding=3, text=artist)
        tags["TPE2"] = TPE2(encoding=3, text="Various Artists")

        tags.save(FileName)

    except Exception as e:
        print(bcolors.FAIL)
        print("Couldn't add song details : %s" % e)
        print(bcolors.ENDC)
        pass


def singleMode():

    print(bcolors.HEADER)
    query = input('Enter Song Name : ')
    print(bcolors.ENDC)

    songURL, FileName = getURL(query)  # Gets YT url

    print(bcolors.GRAY)
    downloadSong(songURL, FileName)  # Saves as .mp3 file
    print(bcolors.ENDC)

    artist, album, songName = getDetails(FileName)
    albumArt = getAlbumArt(album)  # Gets album art

    FileName = FileName + '.mp3'

    add_AlbumArt(albumArt, FileName)
    add_Details(FileName, songName, artist, album)

    print(bcolors.OKBLUE)
    print("%s Successfully downloaded : %s " % (tick, songName))
    print(bcolors.ENDC)


system('clear')
