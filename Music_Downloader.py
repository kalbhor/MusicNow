#/Library/Frameworks/Python.framework/Versions/3.5/bin/python3


''' To do : Progress bar to show download status '''



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
import urllib.request



def get_url(name):	#Method to get URL of Music Video from YouTube
	array = list(str(name)) 
	for i in range(0,len(str(name))):
		if array[i]==' ':
			array[i] = '+'
	name = ''.join(array)
	name = 'https://www.youtube.com/results?search_query=' + str(name)

	YT_Class = 'yt-uix-sessionlink yt-uix-tile-link yt-ui-ellipsis yt-ui-ellipsis-2       spf-link '	#YouTube Class holding video

	driver = webdriver.PhantomJS() #Headless browser
	driver.set_window_size(1280, 1024) #For error free PhantomJS
	driver.get(name)					#Selenium object for search results
	search_results = driver.page_source	#Gets search result's page source
	search_results = str(search_results)
	driver.quit() #Closes PhantomJS

	soup = BeautifulSoup(search_results,"html.parser")	#Creates BeautifulSoup Object
	title = str(soup.find('a',{'class' : YT_Class}).get('title')) #Gets song name

	url = 'https://www.youtube.com/' + str(soup.find('a',{'class' : YT_Class}).get('href')) #Gets Music Video URL
	
	return (url,str(title)) #Returns Name of Song and URL of Music Video

def download_file(video_url,title):	#Method to download audio of Music Video
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
	url = str(url)
	soup = BeautifulSoup(url,"html.parser")	#Converts to BeautifulSoup Object

	for links in soup.findAll('a',{'id' : 'download'}):
		file = links.get('href')
		break	#Gets the download link href
	if file=='':
		print("ERROR")	#Checks whether download link is valid
		exit()
	urllib.request.urlretrieve(str(file),str(title)+'.mp3') #Downloads mp3 with the title as the name of file
	driver.quit() #Closes PhantomJS


def main(): #Main method 
	song_name = input('Enter Song Name : ') #Song Name as input or Keywords of Song
	song_YT_URL,title = get_url(song_name) #Calls method get_url
	download_file(song_YT_URL,title) #Downloads mp3



main() #Calls main method








