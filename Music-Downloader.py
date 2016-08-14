#!/usr/bin/python

#Trivial modules
from collections import OrderedDict
import os
from sys import argv

#Selenium module
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

#BeautifulSoup module
from bs4 import BeautifulSoup

#Requests and urllib
import requests
import urllib2

#Clint for download progress bar
from clint.textui import progress

#Album Art
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC, error

#Twilio Text message
from twilio.rest import TwilioRestClient




script , twilio = argv #Asks whether user wants twilio functions 




'''To do : 
1. Use JSON for Album Art
2. Handle exceptions,errors properly 
'''



'''Get song name and fetch Youtube URL'''


def prompt(url): #Definition to prompt for song song from list of songs
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
	url = OrderedDict() #Create ordered Dictionary
	num = 0			   #List of songs index
	print '\n'
	array = list(str(name)) 
	for i in range(0,len(str(name))):
		if array[i] ==' ':
			array[i] = '+'
	name = ''.join(array)
	name = 'https://www.youtube.com/results?search_query=' + str(name)

	YT_Class = 'yt-uix-sessionlink yt-uix-tile-link yt-ui-ellipsis yt-ui-ellipsis-2       spf-link '	#YouTube Class holding video

	driver = webdriver.PhantomJS() #Headless browser
	driver.set_window_size(1280, 1024) #For error free PhantomJS
	driver.get(name)					#Selenium object for search results
	search_results = driver.page_source	#Gets search result's page source
	driver.quit() #Closes PhantomJS

	soup = BeautifulSoup(search_results,"html.parser")	#Creates BeautifulSoup Object

	for i in soup.findAll('a',{'class' : YT_Class}): #In all Youtube Search Results
		link = 'https://www.youtube.com/' + str(i.get('href')).encode('utf-8')
		link_title = (i.get('title')).encode('utf-8')
		url.update({link_title:link}) #Adds title and song url to dictionary
		print '['+str(num)+'] ' + link_title #Prints list
		num = num + 1


	title,url_fin = prompt(url) #Gets the demanded song title and url
	return (url_fin,title) #Returns Name of Song and URL of Music Video





'''Parsing from Youtube2mp3.cc and get file and downloading file'''


def parse_Youtube(video_url):	#Method to download audio of Music Video

	driver = webdriver.PhantomJS()
	driver.set_window_size(1280, 1024)
	driver.get('https://www.youtube2mp3.cc/') #Third party website to convert to mp3

	vid_name = driver.find_element_by_id('input') 
	vid_name.send_keys(str(video_url))
	driver.find_element_by_id('button').click()


	
	element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, './/a[@id="download" and @href!=""]'))
	) 	#Waits till Download link href loads in the HTML of the page 

	url = driver.page_source	#Gets download page URL
	soup = BeautifulSoup(url,"html.parser")	#Converts to BeautifulSoup Object

	for links in soup.findAll('a',{'id' : 'download'}):
		file = links.get('href')
		break	#Gets the download link href
	if file=='':
		print("ERROR")	#Checks whether download link is valid
		exit()

	driver.quit() #Closes PhantomJS
	return(file)



def download(url,title): #Downloads song
	r = requests.get(url,stream = True) #Gets download url 
	title = title + '.mp3'
	with open(title, 'wb') as f: #Opens .mp3 file with title as name
		total_length = int(r.headers.get('content-length')) #Gets size of .mp3 file 
		for chunk in progress.bar(r.iter_content(chunk_size = 1024), expected_size = (total_length/1024)+1): #Prints status bar
			if chunk:
				f.write(chunk) #Creates .mp3 file
				f.flush()



	

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
	audio = MP3(title,ID3=ID3)

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


def text_message(url):
	txt = open("twilio_details.txt",'r') #Reads from twilio_details file
	x = txt.read().splitlines()
	



	print "Sending download url to mobile phone.."
	client  = TwilioRestClient(x[0], x[1]) 

	message = client.messages.create(to=x[2], from_=x[3], #Sends text message
                                 body=str(url))



'''Main Method'''

os.system('clear') #Clears terminal window

song_name = raw_input('Enter Song Name/Keywords : ') #Song Name as input or Keywords of Song
song_YT_URL,title = get_url(song_name) #Calls method to get YT url

url = parse_Youtube(song_YT_URL) #Gets download url and song title

if twilio == 'Y' or twilio =='y':
	text_message(url) #Sends text message to mobile phone

download(url,title) #Saves as .mp3 file

image = get_albumart(title) #Gets album art
add_albumart(image,title+'.mp3') #Adds album art to song

os.system('clear')








