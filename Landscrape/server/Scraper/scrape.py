import urllib2
from bs4 import BeautifulSoup as BS


##
## search_params = [term, city, state]
##
def get_results(search_params):
    yelp_url = "https://www.yelp.com/search?find_desc=" + search_params[0] + "&find_loc=" + search_params[1] + "%2C+" + search_params[2] + "&ns=1"

    page = urllib2.urlopen(yelp_url)

    soup = BS(page,"html.parser")
    search_results = soup.find_all('li',class_='regular-search-result')

    info = {}

    for mini_soup in search_results:

        name = mini_soup.find("img",class_="photo-box-img").get('alt')
        stars = mini_soup.find("img",class_="offscreen").get('alt')[:3]
        tel = mini_soup.find("span",class_="biz-phone").text
        addr = mini_soup.find("address")

        info[str(name)] = {}
        sub_info = info[str(name)]
        sub_info['stars'] = str(stars)
        sub_info['tele'] = '(' + str(tel).split('(')[1].split('\n')[0]
        address = str(addr).split('<br/>')[0] + ', ' + str(addr).split('<br/>')[1]
        sub_info['addr'] = address[18:].split('\n')[0]

    #for i in info:
    #    print i, "    ", info[i]
    #print "\n\n",info
    return info


def print_stuff():
    print "stuff"

#yelp_info = get_results(["burgers","lawrence","KS"])
