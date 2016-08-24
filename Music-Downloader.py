from __future__ import unicode_literals
import youtube_dl


from collections import OrderedDict
import os
from sys import argv


from bs4 import BeautifulSoup


import requests
import urllib2



from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC, error







'''To do : 
1. Use JSON for Album Art
2. Error testing
'''





script,mode = argv



def prompt(url): #Definition to prompt for song number from list of songs
	x = int(raw_input('Enter song number > '))
	link = url.values()[x]
	title = url.keys()[x]
	os.system('clear')
	print 'Download Song: %s  Y/N?' % title
	x = raw_input('>')
	if x == 'Y' or x == 'y':
		pass
	elif x == 'N' or x == 'n':
		exit()
	else:
		print 'Invalid input'
		exit()

	return title,link




def get_url(name):	#Method to get URL of Music Video from YouTube
	urls_list = OrderedDict() #Create ordered Dictionary
	num = 0			   #List of songs index
	print '\n'
	array = list(str(name)) 
	for i in range(0,len(str(name))):
		if array[i] ==' ':
			array[i] = '+'
	name = ''.join(array).encode('utf-8')
	name = 'https://www.youtube.com/results?search_query=' + str(name)
	html = requests.get(name)
	soup = BeautifulSoup(html.text,'html.parser')

	
	

	YT_Class = 'yt-uix-sessionlink yt-uix-tile-link yt-ui-ellipsis yt-ui-ellipsis-2       spf-link '	#YouTube Class holding video

	for i in soup.findAll('a',{'class' : YT_Class}): #In all Youtube Search Results
		link = 'https://www.youtube.com' + str(i.get('href')).encode('utf-8')
		link_title = (i.get('title')).encode('utf-8')
		urls_list.update({link_title:link}) #Adds title and song url to dictionary

		if mode == 'S': #Display list for single song mode
			try:
				print '['+str(num)+'] ' + link_title #Prints list
			except UnicodeDecodeError: 
				pas
			num = num + 1

		elif mode == 'M': #For multiple song mode, return the first result
			return (urls_list.values()[0], urls_list.keys()[0])

	title,url = prompt(urls_list) #Gets the demanded song title and url (only for single song mode)
	return (url,title) #Returns Name of Song and URL of Music Video



def download(url,title):
	initial_title = title+'-'+url[32:]+'.mp3'
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
		ydl.download([str(url)]) #Downloads audio using youtube-dl

	try:	
		os.rename(initial_title,title+'.mp3') #Renames file to song title
	except OSError:
		pass




	

'''Album Art Fetching and Adding '''


def get_albumart(title): #Gets album art
	print "\nFetching Album Art.."
	url = "http://www.bing.com/images/search?q=" + title #Opens bing image results for album art
	url = requests.get(url)
	url = url.text
	soup = BeautifulSoup(url,"html.parser")

	x = soup.find('img',{'height' : '170'}).get('src')
	mp3file = urllib2.urlopen(x)
	with open(title+'.png','wb') as output: #Saves album art
  		output.write(mp3file.read())

	return (title +'.png')
		
	

def add_albumart(image,title): #Adds album art using mutagen
	try:
		audio = MP3(title,ID3=ID3)
	except error:
		print "Could not add Album Art"
		pass

	try:
		audio.add_tags()
	except error:
		pass

	audio.tags.add(
		APIC(
			encoding=3, #UTF-8
			mime='image/png',
			type=3, # 3 is for album art
			desc=u'Cover',
			data=open(image).read()
			)
		)
	audio.save()
	os.remove(image) #Deletes image file once added as album art





'''Main Method'''

os.system('clear') #Clears terminal window


if mode == 'S' or mode =='s':
	song_name = raw_input('Enter Song Name/Keywords : ') #Song Name as input or Keywords of Song
	song_YT_URL,title = get_url(song_name) #Gets YT url


	download(song_YT_URL,title) #Saves as .mp3 file

	image = get_albumart(title) #Gets album art
	add_albumart(image,title+'.mp3') #Adds album art to song

elif mode == 'M' or mode == 'm':
	file = raw_input('Enter file location > ') 

	with open(str(file)) as f:
		content = f.readlines() #stores each song line by line
	
	for song_names in content: #iterates over each song name

		song_YT_URL,title = get_url(song_names) #Gets YT url
		title = unicode(title,"utf-8")

		download(song_YT_URL,title) #Downloads song

		image = get_albumart(title) #Gets album art
		add_albumart(image,title+'.mp3') #Adds album art

else:
	print('Error. Invalid mode.')











