# BizBashAPI
This API is meant to GET data from https://www.bizbash.com/venue-directory

## Installation:
```
git clone git@github.com:Bigimus/BizBashAPI.git
```
### Requirments:
BeautifulSoup 4: 
```
pip install beautifulsoup4
```

Selenium: 
```
pip install selenium
```

## Usage:
  getSiteData(url) --> Returns the source code for the given URL

  getVenue() --> Returns marketID dict with the format - {Market:  marketId} 
  - Market refers to the location of the venue.
  - marketID is the websites key for a specific Market
                       
  getCategory() --> Returns topicID dict with the format - {Topic: topicID}
  - Topic refers to the topic of the venue.
            - topicID is the websites key for a specific Topic
                          
  getLocation(path) --> Returns locations_dict the with format - {Venue: Address}
  - path refers to search parameter for the URL
                              
  searchLocation(marketID, topicID) --> Returns location_dict with the format - {Venue: Address}
  - Must use marketID and topicID, NOT Market and Topic
  
## DISCLAIMER: 
This API is not associated with bizbash or any entity related to it. This software was designed and purposed for educational purposes.

>Your use of this Website is governed by, and subject to, the legal notices and disclaimers located at https://www.bizbash.com/terms is subject at all times to all such >legal notices and disclaimers. Furthermore, your use and access of the Website constitutes your agreement to be bound by the provisions contained in the Terms of Use and >in this Privacy Policy.


