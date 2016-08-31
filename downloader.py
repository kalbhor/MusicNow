# -*- coding: utf-8 -*-
from os import system,rename
from sys import argv,stdin
from collections import OrderedDict
from select import select

from bs4 import BeautifulSoup
import requests
import urllib2
import json

import youtube_dl
from time import sleep

from mutagen.mp3 import MP3
from mutagen.id3 import ID3NoHeaderError
from mutagen.id3 import ID3, TIT2, TALB, TPE1, TPE2, COMM, USLT, TCOM, TCON, TDRC, APIC, error

script,mode = argv

''' To do : 
		1. Testing 
'''
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


def getURL(songInput):	
	print bcolors.YELLOW
	songInput = songInput.decode('utf-8')
	urls_list = OrderedDict()
	num = 0			   #List of songs index
	print '\n'
	array = list(songInput)
	for i in range(0,len(songInput)):
		if array[i] ==' ':
			array[i] = '+'
	songInput = ''.join(array)
	songInput = 'https://www.youtube.com/results?search_query=' + songInput
	html = requests.get(songInput)
	soup = BeautifulSoup(html.text,'html.parser')
		
	YT_Class = 'yt-uix-sessionlink yt-uix-tile-link yt-ui-ellipsis yt-ui-ellipsis-2       spf-link '	#YouTube Class holding video

	for i in soup.findAll('a',{'class' : YT_Class}): #In all Youtube Search Results
		link = 'https://www.youtube.com' + (i.get('href'))
		link_title = (i.get('title')).encode('utf-8')
		urls_list.update({link_title:link}) #Adds title and song url to dictionary

		if mode == 'S' or mode == 's': #Display list for single song mode
			print '#'+str(num+1)+' ', #Prints list
			print link_title


			num = num + 1

		elif mode == 'L' or mode == 'l': #For multiple song mode, return the first result
			return (urls_list.values()[0], urls_list.keys()[0])

	url,title = prompt(urls_list) #Gets the demanded song title and url (only for single song mode)

	print bcolors.ENDC

	return url,title #Returns Name of Song and URL of Music Video

def prompt(url): 
	x = int(raw_input('\nEnter song number > '))
	x = x - 1
	link = url.values()[x]
	title = url.keys()[x]
	system('clear')
	print 'Download Song: ',
	print title,
	print bcolors.UNDERLINE
	print 'Y/N?'
	print bcolors.ENDC
	x = raw_input('>')
	if x == 'Y' or x == 'y':
		pass
	elif x == 'N' or x == 'n':
		exit()
	else:
		print 'Invalid input'
		exit()

	return link,title


def downloadSong(song_YT_URL, title):
	title = title.decode('utf-8')
	initial_title = (title+'-'+song_YT_URL[32:]+'.mp3').encode('utf-8')
	title = (title + '.mp3').encode('utf-8')

	ydl_opts = {
		'format': 'bestaudio/best',
		'postprocessors': [{
			'key' : 'FFmpegExtractAudio',
			'preferredcodec': 'mp3',
			'preferredquality': '192',
		}],
	}

	with youtube_dl.YoutubeDL(ydl_opts) as ydl:
		ydl.download([song_YT_URL]) #Downloads audio using youtube-dl

	try:	
		rename(initial_title,title) #Renames file to song title
	except Exception:
		print bcolors.FAIL
		print "Could not rename the file."
		print bcolors.ENDC
		pass


def getDetails(songName):
	print bcolors.FAIL
	year =""
	timeout = 10
	title = songName

	array = list(title)
	for i in range(0,len(title)):
		if array[i] ==' ':
			array[i] = '+'
	title = ''.join(array)

	title = "http://search.letssingit.com/cgi-exe/am.cgi?a=search&artist_id=&l=archive&s=" + title
	title = requests.get(title)
	soup = BeautifulSoup(title.text,"html.parser")
	link = soup.find('a',{'class' : 'high_profile'})
	try:
		link = link.get('href')
		link = requests.get(link)

		soup = BeautifulSoup(link.text,"html.parser")

	
		divi_al = soup.find('div',{'id' : 'albums'})
		divi_title = soup.find('div',{'id':'content_artist'}).find('h1')

		try:
			title = divi_title.contents[0]
			title = title[1:-8]
			year = title[-8:]
		except Exception:
			print "I couldn't reset the song title, would you like to manually enter it? (Y/N) : ",
			rlist, _, _ = select([stdin], [], [], 10)
			if rlist:
				check = stdin.readline()
			else:
   				print "No input. I'll just move on"
   				check = 'N'

			if check == 'Y\n' or check =='y\n':
				title = raw_input("Enter song title : ")
				year =""
			else:
				title = songName
				year =""

			
	
		

		try:
			artist = divi_title.contents[1].getText()
		except Exception:
			print "I couldn't find artist name, would you like to manually enter it? (Y/N) : ",
			rlist, _, _ = select([stdin], [], [], 10)
			if rlist:
				check = stdin.readline()
			else:
   				print "No input. I'll just move on"
   				check = 'N'

			if check == 'Y\n' or check =='y\n':
				artist = raw_input("Enter artist name : ")
			else:
				artist = "Unknown"

		try:
			album = divi_al.find('a').contents[0]
			album = album[:-7]

		except Exception:
			print "I couldn't find the album name, would you like to manually enter it? (Y/N) : ",
			rlist, _, _ = select([stdin], [], [], 10)
			if rlist:
				check = stdin.readline()
			else:
   				print "No input. I'll just move on"
   				check = 'N'

			if check == 'Y\n' or check =='y\n':
				album = raw_input("Enter album name : ")
			else:
				album = songName


	except Exception:
		
		print "I couldn't find song details, would you like to manually enter them? (Y/N) : "

		rlist, _, _ = select([stdin], [], [], 10)
		if rlist:
			check = stdin.readline()
		else:
   			print "No input. I'll just move on"
   			check = "N"
   			

  

		if check == 'Y\n' or check =='y\n':
			
			album = raw_input("Enter album name : ")
			title = raw_input("Enter song title : ")
			artist = raw_input("Enter song artist : ")
		else:
			album = songName
			title = songName
			artist = "Unknown"

		print bcolors.ENDC


	

	return artist,album,title,year	



def getAlbumArt(Album_Name): 
	print bcolors.OKGREEN
	print "\nFetching Album Art.."
	print bcolors.ENDC

	Album_Name = Album_Name + " Album Art"
	Album_Name = Album_Name.split()
	Album_Name ='+'.join(Album_Name)
	Album_Name = Album_Name.encode('utf-8')
	
	url = ("https://www.google.co.in/search?q="+Album_Name+"&source=lnms&tbm=isch")
	

	header = {'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"
	}
	url = url.decode('ascii','ignore')

	soup = BeautifulSoup(urllib2.urlopen(urllib2.Request(url,headers=header)),"html.parser")
	

	a = soup.find("div",{"class":"rg_meta"})
	albumArt_url = json.loads(a.text)["ou"]

	return albumArt_url

def add_AlbumArt(albumArt_url, title): 
	img = urllib2.urlopen(albumArt_url) #Gets album art from url

	try:
		audio = MP3(title,ID3=ID3)
		try:
			audio.add_tags()
		except Exception:
			pass

		audio.tags.add(
			APIC(
				encoding=3, #UTF-8
				mime='image/png',
				type=3, # 3 is for album art
				desc=u'Cover',
				data=img.read() #Reads and adds album art
				)
			)
		audio.save()

	except Exception:
		print bcolors.FAIL
		print "An Error occured while adding the album art "
		print bcolors.ENDC
		pass

	

def add_Details(fname,new_title,artist,album,year = ""):

	print bcolors.OKGREEN
	print "Adding song details.."
	print bcolors.ENDC

	try:
		tags = ID3(fname)
	except ID3NoHeaderError:
		print "Adding ID3 header"
		tags = ID3()

	tags["TALB"] = TALB(encoding = 3,text  = album)
	tags["TIT2"] = TIT2(encoding = 3, text = new_title)
	tags["TPE1"] = TPE1(encoding = 3, text = artist)
	tags["TPE2"] = TPE2(encoding = 3, text = "Various Artists")
	tags["TDRC"] = TDRC(encoding = 3, text = year)
   

	tags.save(fname)


def singleMode():
	print bcolors.HEADER
	song_input = raw_input('Enter Song Name/Keywords : ')
	print bcolors.ENDC


	YT_URL,title = getURL(song_input) #Gets YT url

	print bcolors.GRAY
	downloadSong(YT_URL,title) #Saves as .mp3 file
	print bcolors.ENDC

	artist_name,album_name,new_title,year = getDetails(title)
	album_art_url = getAlbumArt(album_name) #Gets album art

	title = title.decode('utf-8')
	title = title + '.mp3'
	title = title.encode('utf-8')

	add_AlbumArt(album_art_url,title)
	add_Details(title,new_title,artist_name,album_name,year)

	

	print bcolors.OKBLUE
	print "Successfully downloaded : ",
	print new_title 
	print bcolors.ENDC	


def listMode():
	file = raw_input('Enter file location > ') 

	with open(file) as listOfSongs:
		content = listOfSongs.readlines() #Stores each song line by line
		
		
	
	for song_names in content: #iterates over each song name

		YT_URL,title = getURL(song_names) #Gets YT url
		downloadSong(YT_URL,title) #Downloads song

		artist,album_name,new_title = getDetails(title)
		album_art_url = getAlbumArt(title.decode('utf-8')) #Gets album art url

		title = title.decode('utf-8')
		title = title + '.mp3'
		title = title.encode('utf-8')

		add_AlbumArt(album_art_url,title)
		add_Details(title,new_title,artist,album_name)
	


'''Main Method'''

system('clear') 


if mode == 'S' or mode =='s':
	singleMode()


elif mode == 'L' or mode == 'l':
	listMode()

else:
	print('Error. Invalid mode.') #If mode is not 'S/s' or 'L/l'
