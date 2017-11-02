import urllib2
from bs4 import BeautifulSoup as BS

#import sys


##
## search_params = [term, city, state]
##
def get_results(search_params):
    yelp_url = "https://www.yelp.com/search?find_desc=" + search_params[0] + "&find_loc=" + search_params[1] + "%2C+" + search_params[2] + "&ns=1"

    page = urllib2.urlopen(yelp_url)

    soup = BS(page,"html.parser")
    search_results = soup.find_all('li',class_='regular-search-result')

    mini_soup = search_results[0]

    name = mini_soup.find("img",class_="photo-box-img").get('alt')
    stars = mini_soup.find("img",class_="offscreen").get('alt')[:3]
    tel = mini_soup.find("span",class_="biz-phone").text

    info = {}
    info['name'] = str(name)
    info['stars'] = str(stars)
    info['tele'] = '(' + str(tel).split('(')[1].split('\n')[0]

    print info


#sys.argv[1]
get_results(["burgers","lawrence","KS"])
