## @file scrape.py
#
# File that contains all scraping functionality
import urllib2
from bs4 import BeautifulSoup as BS

########################################################
#                       CLASSES                        #
########################################################

## @Class Scraper
#
# Scraping class that takes the search parameters as an input_required
class Scraper:

    ####################################################
    #                   SUB-FUNCTIONS                  #
    ####################################################

    ## @Function
    #
    # Constructor
    # @param self The object pointer
    # @param search_params The array of search parameters
    def __init__(self,search_params):
        self.search_term = search_params[0].split(',')
        self.city = search_params[1]
        self.state = search_params[2]


    ####################################################
    #               GENERAL GET FUNCTIONS              #
    ####################################################

    ## @Function
    #
    # get_results
    # @param self The object pointer
    # @return all_results Dictionary of search terms and info { term1 : [ info ], ...}
    def get_results(self):

        all_results = {}

        for i in self.search_term:
            all_results[i] = self.sub_get_results(i)

        return all_results

    ## @Function
    #
    # sub_get_results
    # @param self The object pointer
    # @param sub_term A string search value
    # @return info Ordered list of dictionaries
    def sub_get_results(self,sub_term):

        yelp_res = self.yelp_get_results(sub_term)

        self.four_get_results(sub_term)
        return yelp_res


    ####################################################
    #                  YELP SCRAPING                   #
    ####################################################

    ## @Function
    #
    # yelp_format_for_url
    # @param self The object pointer
    # @param format_term A string value
    # @return all_results Dictionary of search terms and info { term1 : [ info ], ...}
    def yelp_format_for_url(self,format_term):

        split_terms = format_term.split(' ')
        term = split_terms[0]
        for i in xrange(1,len(split_terms)):
            if split_terms[i] != "":
                term += "+" + split_terms[i]

        return term

    ## @Function
    #
    # yelp_get_results
    # @param self The object pointer
    # @param sub_term A string search value
    # @return info Ordered list of dictionaries
    def yelp_get_results(self,sub_term):

        # anticipate for multi word searches
        term = self.yelp_format_for_url(sub_term)

        # anticipate for multi word cities
        city = self.yelp_format_for_url(self.city)

        # set the search url and get the BeautifulSoup information
        yelp_url = "https://www.yelp.com/search?find_desc=" + term + "&find_loc=" + city + "%2C+" + self.state + "&ns=1"

        page = urllib2.urlopen(yelp_url)

        soup = BS(page,"html.parser")
        search_results = soup.find_all('li',class_='regular-search-result')

        # initialize the return type
        info = []

        # only scrape three results
        if len(search_results) > 3:
            results = 3
        else:
            results = len(search_results)

        # scrape the results and store them in a list
        for n in xrange(0,results):

            mini_soup = search_results[n]

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
            sub_info = {}
            sub_info['name'] = str(name)
            sub_info['stars'] = str(stars)
            sub_info['tele'] = '(' + str(tel).split('(')[1].split('\n')[0]

            # Get/Set address
            addr = str(mini_soup.find("address"))[18:len(addr)-15]
            pos1 = addr.find('<')
            pos2 = addr.find('>')
            address = addr[:pos1] + ', ' + addr[pos2+1:]
            sub_info['addr'] = address

            # Get page-specific info, store in sub_soup
            sub_info["sub_url"] = "https://www.yelp.com" + mini_soup.find("a",class_="biz-name js-analytics-click").get("href")

            # append the dictionary to the list
            info.append(sub_info)

        # return type is a list of dictionaries
        #    result and a dictionary with its corresponding
        #    information
        return info


    ## @Function
    #
    # yelp_get_sub_page_info
    # @param self The object pointer
    # @param sub_dict The dictionary for information to be added to
    # @return dictionary sub dict with new info website, hour info, price info
    def yelp_get_sub_page_info(self,sub_dict):

        # get sub page
        sub_page = urllib2.urlopen(sub_dict['sub_url'])
        sub_soup = BS(sub_page,"html.parser")

        # Get/Set the restaurant URL
        web_addr = ""
        for i in sub_soup.find_all("span",class_="biz-website js-add-url-tagging"):
            web_addr = i.find('a').text
        if web_addr == "":
            web_addr = "No Website"
        sub_dict['web_addr'] = web_addr.encode('utf-8')

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
        sub_dict['hours'] = str(hours)

        # Get/Set price range info if available
        price = "No Price Information"
        try:
            price_range = sub_soup.find("dd",class_="nowrap price-description").text
            price = str(price_range[25:].split("     ")[0].split("\n")[0])
        except AttributeError:
            pass
        sub_dict["price"] = price

        return sub_dict


    ####################################################
    #               FOURSQUARE SCRAPING                #
    ####################################################

    ## @Function
    #
    # four_format_for_url
    # @param self The object pointer
    # @param format_term A string value
    # @return all_results Dictionary of search terms and info { term1 : [ info ], ...}
    def four_format_for_url(self,format_term):

        split_terms = format_term.split(' ')
        term = split_terms[0]
        for i in xrange(1,len(split_terms)):
            if split_terms[i] != "":
                term += "+" + split_terms[i]

        return term

    ## @Function
    #
    # four_get_results
    # @param self The object pointer
    # @param sub_dict The dictionary for information to be added to
    # @return dictionary sub dict with new info website, hour info, price info
    def four_get_results(self,sub_term):

        # anticipate for multi word searches
        term = self.four_format_for_url(sub_term)

        # anticipate for multi word cities
        city = self.four_format_for_url(self.city)

        # set the search url and get the BeautifulSoup information
        foursquare_url = "https://foursquare.com/explore?mode=url&near=" + city + "%2C%20" + self.state + "&q=" + term

        page = urllib2.urlopen(foursquare_url)

        soup = BS(page,"html.parser")
        search_results = soup.find_all('div',class_='contentHolder')

        # initialize the return type
        info = []

        # only scrape three results
        if len(search_results) > 3:
            results = 3
        else:
            results = len(search_results)

        # scrape the results and store them in a list
        for n in xrange(0,results):

            mini_soup = search_results[n]

            # Set values to empty string, in case of overlap
            name = ""
            stars = ""
            tel = ""
            addr = ""
            web_addr = ""
            hours = ""
            price_range = ""

            # Get basic info
            name = mini_soup.find("a").text
            #stars = mini_soup.find("img",class_="offscreen").get('alt')[:3]
            #tel = mini_soup.find("span",class_="biz-phone").text
            addr = mini_soup.find("div",class_="venueAddress").text

            # Set basic info
            sub_info = {}
            sub_info['name'] = str(name)
            #sub_info['stars'] = str(stars)
            #sub_info['tele'] = '(' + str(tel).split('(')[1].split('\n')[0]

            # Get/Set address
            #addr = str(mini_soup.find("address"))[18:len(addr)-15]
            #pos1 = addr.find('<')
            #pos2 = addr.find('>')
            #address = addr[:pos1] + ', ' + addr[pos2+1:]
            #sub_info['addr'] = address

            # Get page-specific info, store in sub_soup
            #sub_info["sub_url"] = "https://www.yelp.com" + mini_soup.find("a",class_="biz-name js-analytics-click").get("href")

            # append the dictionary to the list
            info.append(sub_info)

            #print addr

        #print search_results[0]




#yelp_info = Scraper(["burgers","Lawrence","KS"])
#infor = yelp_info.get_results()
#for i in infor:
#    print i,infor[i]
