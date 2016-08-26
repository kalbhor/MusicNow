from __future__ import unicode_literals
import youtube_dl




from collections import OrderedDict
import os
from sys import argv


from bs4 import BeautifulSoup


import requests
import urllib2
import json



from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC, error






'''To do : 
1. Bug testing
'''





script,mode = argv




def prompt(url): #Definition to prompt for song number from list of songs
	x = int(raw_input('Enter song number > '))
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




def get_url(name):	#Method to get URL of Music Video from YouTube
	urls_list = OrderedDict() #Create ordered Dictionary
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

		if mode == 'S': #Display list for single song mode
			#try:
			print '['+str(num)+'] ', #Prints list
			print link_title
			#except UnicodeDecodeError: 
			#	pass
			num = num + 1

		elif mode == 'M': #For multiple song mode, return the first result
			return (urls_list.values()[0], urls_list.keys()[0])

	title,url = prompt(urls_list) #Gets the demanded song title and url (only for single song mode)

	return (url,title) #Returns Name of Song and URL of Music Video



def download(url,title):
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
	except OSError:
		pass




	

'''Album Art Fetching and Adding '''

def get_soup(url,header):
    return BeautifulSoup(urllib2.urlopen(urllib2.Request(url,headers=header)),"html.parser")

def get_albumart(query): 
	print "\nFetching Album Art.."
	query = query.decode('utf-8')
	query = query + " Album Art"
	query = query.split()
	query ='+'.join(query)
	
	url=("https://www.google.co.in/search?q="+query+"&source=lnms&tbm=isch").encode('utf-8')
	print url

	header={'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"
	}
	url = url.decode('ascii','ignore')
	soup = get_soup(url,header)



	a = soup.find("div",{"class":"rg_meta"})
	link =json.loads(a.text)["ou"]

	return (link)
		
	

def add_albumart(image,title): #Adds album art using mutagen
	response = urllib2.urlopen(image)
	try:
		audio = MP3(title,ID3=ID3)
	except error as e:
		print "Could not add Album Art : " + str(e)
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
			data=response.read()
			)
		)
	audio.save()






'''Main Method'''

os.system('clear') #Clears terminal window


if mode == 'S' or mode =='s':
	song_name = raw_input('Enter Song Name/Keywords : ') #Song Name as input or Keywords of Song
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
		content = f.readlines() #stores each song line by line
	
	for song_names in content: #iterates over each song name
		song_names = song_names.decode('utf-8')
		song_YT_URL,title = get_url(song_names) #Gets YT url
		

		download(song_YT_URL,title) #Downloads song

		image = get_albumart(title) #Gets album art
		title = title.decode('utf-8')
		title = title + '.mp3'
		title = title.encode('utf-8')
		add_albumart(image,title) #Adds album art

else:
	print('Error. Invalid mode.')
