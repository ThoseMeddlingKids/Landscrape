## @file scrape.py
#
# File that contains all scraping functionality
import urllib2
from bs4 import BeautifulSoup as BS
#import pdb; pdb.set_trace()
#inport code; code.interact()


########################################################
#                       CLASSES
########################################################

## @Class Scraper
#
# Scraping class that takes the search parameters as an input_required
class Scraper:

    ####################################################
    #                   SUB-FUNCTIONS
    ####################################################

    ## @Function
    #
    # Constructor
    # @param self The object pointer
    # @param search_params The array of search parameters
    def __init__(self,search_params):
        self.search_term = search_params[0]
        self.city = search_params[1]
        self.state = search_params[2]

    ## @Function
    #
    # get_results
    # @param self The object pointer
    # @return info Nested dictionary, { result1 : { info }, ...}
    def get_results(self):

        # anticipate for multi word searches
        term = ""
        split_terms = self.search_term.split(' ')
        term = split_terms[0]
        for i in xrange(1,len(split_terms)):
            if split_terms[i] != "":
                term += "+" + split_terms[i]

        # anticipate for multi word cities
        city = ""
        split_city = self.city.split(' ')
        city = split_city[0]
        for i in xrange(1,len(split_city)):
            if split_city[i] != "":
                city += "+" + split_city[i]

        # set the search url and get the BeautifulSoup information
        yelp_url = "https://www.yelp.com/search?find_desc=" + term + "&find_loc=" + city + "%2C+" + self.state + "&ns=1"

        page = urllib2.urlopen(yelp_url)

        soup = BS(page,"html.parser")
        search_results = soup.find_all('li',class_='regular-search-result')

        # initialize the return type
        info = {}

        for mini_soup in search_results:

            # Set values to empty string, in case of overlap
            name = ""
            stars = ""
            tel = ""
            addr = ""
            web_addr = ""
            hours = ""
            price_range = ""

            # Get basic info
            name = mini_soup.find("img",class_="photo-box-img").get('alt')
            stars = mini_soup.find("img",class_="offscreen").get('alt')[:3]
            tel = mini_soup.find("span",class_="biz-phone").text

            # Set basic info
            info[name] = {}
            sub_info = info[name]
            sub_info['stars'] = str(stars)
            sub_info['tele'] = '(' + str(tel).split('(')[1].split('\n')[0]

            # Get/Set address
            addr = str(mini_soup.find("address"))[18:len(addr)-18]
            pos1 = addr.find('<')
            pos2 = addr.find('>')
            address = addr[:pos1] + ', ' + addr[pos2+1:]
            sub_info['addr'] = address

            # Get page-specific info, store in sub_soup
            sub_url = "https://www.yelp.com" + mini_soup.find("a",class_="biz-name js-analytics-click").get("href")
            sub_page = urllib2.urlopen(sub_url)
            sub_soup = BS(sub_page,"html.parser")

            # Get/Set the restaurant URL
            for i in sub_soup.find_all("span",class_="biz-website js-add-url-tagging"):
                web_addr = i.find('a').text
            if web_addr == "":
                web_addr = "No Website"
            sub_info['web_addr'] = web_addr.encode('utf-8')


            # Get/Set restaurant hours, if available
            hours = "No Hour Information"
            try:
                hour_start = sub_soup.find("strong", class_="u-space-r-half").find_all("span")[0].text
                hour_end = sub_soup.find("strong", class_="u-space-r-half").find_all("span")[1].text
                hours = hour_start + " - " + hour_end
            except TypeError:
                pass
            except AttributeError:
                pass
            except IndexError:
                pass
            sub_info['hours'] = str(hours)

            # Get/Set price range info if available
            price = "No Price Information"
            try:
                price_range = sub_soup.find("dd",class_="nowrap price-description").text
                price = str(price_range[25:].split("     ")[0].split("\n")[0])
            except AttributeError:
                pass
            sub_info["price"] = price

        # return type is a nested dictionary of a search
        #    result and a dictionary with its corresponding
        #    information
        return info

#yelp_info = Scraper(["ice cream    ","San Francisco    ","KS"])
#infor = yelp_info.get_results()
#for i in infor:
#    print i,infor[i]
