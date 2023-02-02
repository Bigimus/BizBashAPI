import re
from bs4 import BeautifulSoup
from selenium import webdriver as wd
"""
    ||=============================||
    ||      BizBash Venues API     ||
    ||=============================||
    
    This API is meant to GET data from https://www.bizbash.com/venue-directory
    
    Methods:
        getSiteData(url) --> Returns the source code for the given URL
        
        getVenue() --> Returns marketID dict with format - {Market:  marketId} 
            - Market refers to the location of the venue.
            - marketID is the websites key for a specific Market
                       
        getCategory() --> Returns topicID dict with format - {Topic: topicID}
            - Topic refers to the topic of the venue.
            - topicID is the websites key for a specific Topic
                          
        getLocation(path) --> Returns locations_dict with format - {Venue: Address}
            - path refers to search parameter for the URL
                              
        searchLocation(marketID, topicID) --> Returns location_dict with format - {Venue: Address}
            - Must use marketID and topicID, NOT Market and Topic

"""
def getSiteData(url):
    driver = wd.Chrome()
    driver.get(url)
    soup = BeautifulSoup(driver.page_source,"lxml")
    return soup

def getVenue():
    marketID = {}
    soup = getSiteData('http://www.bizbash.com/venue-directory')
    temp_venues = soup.find_all('a',{"href" : re.compile("marketId")})
    for venue in temp_venues:
        marketID.update({venue.text.strip(): venue.get('href').split("=")[1]})
    return marketID

def getCategory():
    topicID = {}
    soup = getSiteData('http://www.bizbash.com/venue-directory')
    temp_categories = soup.find_all('a',{"href":re.compile("topicId")})
    for category in temp_categories:
        topicID.update({category.text.strip(): category.get('href').split("=")[1]})
    return topicID

def getLocation(path):
    locations_dict = {}
    x = y = 0
    while(y < 2):
        driver = wd.Chrome()
        y = (y % 26) + 1    
        if (y == 1):        
            x += 1
            url = f"https://www.bizbash.com/venue-directory?{path}page={x}"
            driver.get(url)
            soup = BeautifulSoup(driver.page_source,"lxml")
            temp_venues = soup.find_all('div',{"class":"node__body"})
    for venue in temp_venues: 
        VENUE, ADDRESS = splitVenueAddress(venue.text.strip())
        locations_dict.update({VENUE: ADDRESS})
    return locations_dict

def splitVenueAddress(venue):
    address = False
    temp_address = []
    temp_venue = []
    VENUE = ADDRESS = ""
    for idx, char in enumerate(venue):
        if address != False:
            temp_address.append(char)
        if not venue[idx-1].isdigit() and char.isdigit() and idx > 5:
            temp_address.append(char)
            address = True   
        elif address != True:
            temp_venue.append(char)
    return VENUE.join(temp_venue), ADDRESS.join(temp_address)

#Searching Link Example: https://www.bizbash.com/venue-directory?marketId=2000016&topicId=62492&page=2
#Searching Link Format: f"https://www.bizbash.com/venue-directory?marketId={marketID}&topicId=(topicID)&page={page}"
def searchLocations(marketID, topicID):
    path = f"marketId={marketID}&topicId={topicID}&"
    temp_data = getLocation(path)
    return temp_data

