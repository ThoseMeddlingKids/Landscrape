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
    #                    CONSTRUCTOR                   #
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

        four_res = self.four_get_results(sub_term)

        return self.merge(yelp_res,four_res)

    ## @Function
    #
    # merge
    # @param self The object pointer
    # @param yelp_list A dictionary of scraped yelp values
    # @param four_list A dictionary of scraped foursquare values
    # @return info Ordered list
    def merge(self,yelp_list,four_list):

        sub_list = []
        output = []
        y = yelp_list
        f = four_list

        # for each yelp search result
        for sub_yelp in y:

            # flag if something has been added
            check = False

            # compare to each foursquare result
            for sub_four in f:

                # if the telephones match, they are the same place, do data analysis
                if sub_four["tele"] == sub_yelp["tele"]:

                    check = True  # set flag

                    # create new dictionary
                    new_rest = {}

                    # transfer data
                    for term in sub_yelp:
                        if sub_yelp[term] != "":
                            new_rest[term] = sub_yelp[term]
                        else:
                            new_rest[term] = sub_four[term]

                    # average the stars
                    s1 = float(sub_four["stars"])
                    s2 = float(sub_yelp["stars"])

                    new_rest['stars'] = str( (s1 + s2) / 2 )

                    # add directly to output
                    output.append(new_rest)

                    # remove this term from comparison
                    f.remove(sub_four)

                    break # break

            # if the term doesn't match one from the other list, add it
            if not check:

                sub_list.append(sub_yelp)

        # add the remaining values in the foursquare list
        for sub_four in f:

            sub_list.append(sub_four)

        # RANKING

        # sort the sub list byu stars
        sub_list = list(reversed(sorted(sub_list, key = lambda k: float(k['stars']))))

        for i in xrange(0,3-len(output)):
            output.append(sub_list[i])

        return output


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
        array = range(0,results)
        for n in array:

            try:
                mini_soup = search_results[n]

                # Set values to empty string, in case of overlap
                name = ""
                stars = ""
                tel = ""
                addr = ""

                # Get basic info
                name = mini_soup.find("img",class_="photo-box-img").get('alt')
                img = mini_soup.find("img",class_="photo-box-img").get('src')
                stars = str(float(mini_soup.find("img",class_="offscreen").get('alt')[:3])*2)
                tel = mini_soup.find("span",class_="biz-phone").text
                tel = ''.join( c for c in tel if c.isdigit() )

                # Set basic info
                sub_info = {}
                sub_info['name'] = str(name.encode("ascii","ignore"))
                sub_info['img'] = img
                sub_info['stars'] = str(stars)
                sub_info['tele'] = tel

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

            except AttributeError:
                array.append(array[len(array)-1]+1)

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
        hours = ""
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
        price = ""
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
                term += "%20" + split_terms[i]

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
            addr = ""

            # Get basic info
            name = mini_soup.find("a").text
            stars = mini_soup.find("div",class_="venueScore positive").text
            addr = mini_soup.find("div",class_="venueAddress").text
            sub_url = "https://foursquare.com" + mini_soup.find("h2").find("a").get("href")
            img = mini_soup.find("img",class_="photo").get("src")

            # Set basic info
            sub_info = {}
            sub_info['name'] = str(name.encode("ascii","ignore"))
            sub_info['sub_url'] = sub_url
            sub_info['stars'] = str(stars)
            sub_info['addr'] = addr
            sub_info['img'] = img

            # get the sub page information
            sub_info = self.four_get_sub_page_info(sub_info)

            # append the dictionary to the list
            info.append(sub_info)

        return info

    ## @Function
    #
    # four_get_sub_page_info
    # @param self The object pointer
    # @param sub_dict The dictionary for information to be added to
    # @return dictionary sub dict with new info website, hour info, price info
    def four_get_sub_page_info(self,sub_dict):

        # get sub page
        sub_page = urllib2.urlopen(sub_dict['sub_url'])
        sub_soup = BS(sub_page,"html.parser")

        # get telephone number
        try:
            tel = sub_soup.find_all("span",class_="tel")[0].text
            tel = ''.join( c for c in tel if c.isdigit() )
            sub_dict["tele"] = tel
        except (AttributeError,IndexError):
            sub_dict["tele"] = ""

        # Get/Set the restaurant URL
        try:
            web_addr = sub_soup.find_all("a",class_="url")[0].get("href")
            sub_dict["web_addr"] = web_addr
        except (AttributeError,IndexError):
            sub_dict["web_addr"] = ""

        return sub_dict
