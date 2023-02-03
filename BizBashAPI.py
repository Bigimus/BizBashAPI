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
            - marketID > is the websites key for a specific market
                       
        getCategory() --> Returns topicID dict with format - {Topic: topicID}
            - Topic refers to the topic of the venue.
            - topicID > is the websites key for a specific topic
        
        getPageCount(path) --> Returns the amount of pages for a given URL path.
            - path refers to search parameters within the url.
            - An example path would be: f"marketId={marketID}&topicId=(topicID)&",
                          
        getLocation(marketID, topicID, limit) --> Returns locations_dict with format - {Venue: Address}
            - OPTIONAL: marketID
            - OPTIONAL: topicID
            - OPTIONAL: limit > The limit changes depending on what values are given. 
                                For example, if you input no values the default limit is 50 pages.
                                Otherwise, the limit will be equal to one less of the total amount of pages.
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

def getPageCount(path):
    url = f"https://www.bizbash.com/venue-directory?{path}"
    literal_soup = getSiteData(url).find('div',{"class":"document-container"})
    text_data = literal_soup.text.strip()
    text_list = text_data.split("PreviousShowing: 1 - 25 of ")
    venues = text_list[1].split("Next")[0]
    page_count = round((int(venues) / 25) - 1)
    return page_count

#Searching Link Format: f"https://www.bizbash.com/venue-directory?marketId={marketID}&topicId=(topicID)&page={page}"
def getLocation(marketID = None, topicID = None, limit = 0):
    
    if marketID is not None and topicID is not None:
        path = f"marketId={marketID}&topicId={topicID}&"

    elif marketID is not None and topicID is None:
        path = f"marketId={marketID}&"
        
    elif marketID is None and topicID is not None:
        path = f"topicId={topicID}&"
        
    else:
        path = ""
        
    if limit == 0 and path != "":
        limit = getPageCount(path)
        
    elif limit == 0 and path == "":
        limit = 50
    
    locations_dict = {}
    x = y = 0
    
    while(y < limit):
        y = (y % limit) + 1         
        x += 1
        url = f"https://www.bizbash.com/venue-directory?{path}page={x}"
        print(f"Getting page {x} of {limit}!")
        print(url)
        driver = wd.Chrome()
        driver.get(url)
        soup = BeautifulSoup(driver.page_source,"lxml")
        temp_venues = soup.find_all('div',{"class":"node__body"})
        
    for venue in temp_venues: 
        VENUE, ADDRESS = splitVenueAddress(venue.text.strip())
        locations_dict.update({VENUE: ADDRESS})
        
    return locations_dict



