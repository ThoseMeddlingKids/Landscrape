import urllib2
from bs4 import BeautifulSoup as BS


##
## search_params = [term, city, state]
##

## Consider converting this to a class, one instance per search term. I dont think it will matter
def get_results(search_params):
    yelp_url = "https://www.yelp.com/search?find_desc=" + search_params[0] + "&find_loc=" + search_params[1] + "%2C+" + search_params[2] + "&ns=1"

    page = urllib2.urlopen(yelp_url)

    soup = BS(page,"html.parser")
    search_results = soup.find_all('li',class_='regular-search-result')

    info = {}

    for mini_soup in search_results:

        # Get basic info
        name = mini_soup.find("img",class_="photo-box-img").get('alt')
        stars = mini_soup.find("img",class_="offscreen").get('alt')[:3]
        tel = mini_soup.find("span",class_="biz-phone").text
        addr = mini_soup.find("address")

        # Set basic info
        info[str(name)] = {}
        sub_info = info[str(name)]
        sub_info['stars'] = str(stars)
        sub_info['tele'] = '(' + str(tel).split('(')[1].split('\n')[0]
        address = str(addr).split('<br/>')[0] + ', ' + str(addr).split('<br/>')[1]
        sub_info['addr'] = address[18:].split('\n')[0]

        # Get page-specific info
        sub_url = "https://www.yelp.com" + mini_soup.find("a",class_="biz-name js-analytics-click").get("href")
        sub_page = urllib2.urlopen(sub_url)
        sub_soup = BS(sub_page,"html.parser")

        # Get/Set the restaurant URL
        for i in sub_soup.find_all("span",class_="biz-website js-add-url-tagging"):
            web_addr = i.find('a').text
        if web_addr == "":
            web_addr = "No Website"
        sub_info['web_addr'] = str(web_addr)

        ##
        ## Room for hours and price range info
        ##

    return info

#yelp_info = get_results(["burgers","lawrence","KS"])
