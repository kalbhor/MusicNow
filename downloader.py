# -*- coding: utf-8 -*-
import os
from sys import argv
from collections import OrderedDict

from bs4 import BeautifulSoup
import requests
import urllib2
import json

import youtube_dl
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC, error

script,mode = argv

''' To do : 
		1. Testing 
'''

def prompt(url): 
	x = int(raw_input('\nEnter song number > '))
	x = x - 1
	link = url.values()[x]
	title = url.keys()[x]
	os.system('clear')
	print 'Download Song: ',
	print title,
	print 'Y/N?'
	x = raw_input('>')
	if x == 'Y' or x == 'y':
		pass
	elif x == 'N' or x == 'n':
		exit()
	else:
		print 'Invalid input'
		exit()

	return title,link

def get_url(name):	
	urls_list = OrderedDict()
	num = 0			   #List of songs index
	print '\n'
	array = list(name)
	for i in range(0,len(name)):
		if array[i] ==' ':
			array[i] = '+'
	name = ''.join(array)
	name = 'https://www.youtube.com/results?search_query=' + name
	html = requests.get(name)
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

		elif mode == 'M' or mode == 'm': #For multiple song mode, return the first result
			return (urls_list.values()[0], urls_list.keys()[0])

	title,url = prompt(urls_list) #Gets the demanded song title and url (only for single song mode)

	return (url,title) #Returns Name of Song and URL of Music Video

def download(url, title):
	title = title.decode('utf-8')
	initial_title = (title+'-'+url[32:]+'.mp3').encode('utf-8')
	print initial_title
	ydl_opts = {
		'format': 'bestaudio/best',
		'postprocessors': [{
			'key' : 'FFmpegExtractAudio',
			'preferredcodec': 'mp3',
			'preferredquality': '192',
		}],
	}

	with youtube_dl.YoutubeDL(ydl_opts) as ydl:
		ydl.download([(url)]) #Downloads audio using youtube-dl

	try:	
		os.rename(initial_title,title+'.mp3') #Renames file to song title
	except Exception:
		print "Could not rename the file."
		exit()

def get_albumart(query): 
	print "\nFetching Album Art.."
	query = query.decode('utf-8')
	query = query + " Album Art"
	query = query.split()
	query ='+'.join(query)
	
	url = ("https://www.google.co.in/search?q="+query+"&source=lnms&tbm=isch").encode('utf-8')
	

	header = {'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"
	}
	url = url.decode('ascii','ignore')

	soup = BeautifulSoup(urllib2.urlopen(urllib2.Request(url,headers=header)),"html.parser")
	

	a = soup.find("div",{"class":"rg_meta"})
	link = json.loads(a.text)["ou"]

	return link

def add_albumart(image, title): 
	response = urllib2.urlopen(image) #Gets album art from url
	try:
		audio = MP3(title,ID3=ID3)
	except Exception:
		print "An Error occured while adding the album art "
		exit()

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
			data=response.read() #Reads and adds album art
			)
		)
	audio.save()



'''Main Method'''

os.system('clear') 


if mode == 'S' or mode =='s':
	song_name = raw_input('Enter Song Name/Keywords : ')
	song_YT_URL,title = get_url(song_name) #Gets YT url

	download(song_YT_URL,title) #Saves as .mp3 file

	image = get_albumart(title) #Gets album art
	title = title.decode('utf-8')
	title = title + '.mp3'
	title = title.encode('utf-8')
	add_albumart(image,title) #Adds album art to song

elif mode == 'M' or mode == 'm':
	file = raw_input('Enter file location > ') 

	with open(file) as f:
		content = f.readlines() #Stores each song line by line
	
	for song_names in content: #iterates over each song name
		song_names = song_names.decode('utf-8')
		song_YT_URL,title = get_url(song_names) #Gets YT url
		

		download(song_YT_URL,title) #Downloads song

		image = get_albumart(title) #Gets album art url
		title = title.decode('utf-8')
		title = title + '.mp3'
		title = title.encode('utf-8')
		add_albumart(image,title) #Adds album art

else:
	print('Error. Invalid mode.') #If mode is not 'S/s' or 'M/m'
