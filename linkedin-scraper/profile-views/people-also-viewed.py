import cookielib
import os
import urllib
import urllib2
import re
import string
from BeautifulSoup import BeautifulSoup
from random import random
from time import sleep



cookie_filename = "parser.cookies.txt"

#The script will go through this persons 'also viewed' people. Change this to a profile of any person in the following format
PUT_ANY_LINK_HERE="https://www.linkedin.com/profile/view?id=205445&authType=OUT_OF_NETWORK&authToken=6pkw&locale=en_US&srchid=2007812921417601243298&srchindex=3&srchtotal=2982&trk=vsrp_people_res_name&trkInfo=VSRPsearchId%3A2007812921417601243298%2CVSRPtargetId%3A205445%2CVSRPcmpt%3Aprimary"

class LinkedInParser(object):

    def __init__(self, login, password):
        """ Start up... """
        self.login = login
        self.password = password

        # Simulate browser with cookies enabled
        self.cj = cookielib.MozillaCookieJar(cookie_filename)
        if os.access(cookie_filename, os.F_OK):
            self.cj.load()
        self.opener = urllib2.build_opener(
            urllib2.HTTPRedirectHandler(),
            urllib2.HTTPHandler(debuglevel=0),
            urllib2.HTTPSHandler(debuglevel=0),
            urllib2.HTTPCookieProcessor(self.cj)
        )
        self.opener.addheaders = [
            ('User-agent', ('Mozilla/4.0 (compatible; MSIE 6.0; '
                           'Windows NT 5.2; .NET CLR 1.1.4322)'))
        ]

        # Login
        self.loginPage()

        self.queue = []
        self.collectedPeople = []


        #collect from db
        f = open('db_looked.txt')
        lines = map(lambda x: x.strip('\n'), f.readlines())
        f.close()
        self.collectedPeople.extend(lines)

        currentPerson_url = PUT_ANY_LINK_HERE
        while True:
            while self.grabNewPerson(currentPerson_url)==False:
                currentPerson_url = self.queue.pop(0)
            self.collectedPeople.append(self.extractProfileId(currentPerson_url))            
            if not len(self.queue):
                break
            currentPerson_url = self.queue.pop(0)
            sleep(8+random()*2)

        self.cj.save()


    def loadPage(self, url, data=None):
        """
        Utility function to load HTML from URLs for us with hack to continue despite 404
        """
        # We'll print the url in case of infinite loop
        # print "Loading URL: %s" % url
        try:
            if data is not None:
                response = self.opener.open(url, data)
            else:
                response = self.opener.open(url)
            return ''.join(response.readlines())
        except:
            # If URL doesn't load for ANY reason, try again...
            # Quick and dirty solution for 404 returns because of network problems
            # However, this could infinite loop if there's an actual problem
            return self.loadPage(url, data)

    def loginPage(self):
        """
        Handle login. This should populate our cookie jar.
        """
        html = self.loadPage("https://www.linkedin.com/")
        soup = BeautifulSoup(html)
        csrf = soup.find(id="loginCsrfParam-login")['value']

        login_data = urllib.urlencode({
            'session_key': self.login,
            'session_password': self.password,
            'loginCsrfParam': csrf,
        })

        html = self.loadPage("https://www.linkedin.com/uas/login-submit", login_data)
        return

    def extractProfileId(self,s):
        return s[s.index("id=")+3:s.index("&")]

    def grabNewPerson(self, currentPerson_url):
        if self.extractProfileId(currentPerson_url) in self.collectedPeople:
            return False

        with open("visited.txt", "a") as visited:
            visited.write(currentPerson_url + "\n")

        raw_cards = self.grabSameExpirience(currentPerson_url)
        # print raw_cards
        cards = []
        for i in raw_cards:
            cards.append(i.find("a")["href"])
        self.queue.extend(cards)
        return True


    def grabAlsoViewed(self, currentPerson_url):
        html = self.loadPage(currentPerson_url)
        soup = BeautifulSoup(html)
        alsoViewedDiv = soup.find("div",{"class": "insights-browse-map"})
        print currentPerson_url

        if alsoViewedDiv:
            return alsoViewedDiv.findAll('li')

        return []

    def grabSameExpirience(self, currentPerson_url):
        html = self.loadPage(currentPerson_url)
        soup = BeautifulSoup(html)
        sameExpirience = soup.find("ol",{"class": "discovery-results"})
        print currentPerson_url

        if sameExpirience:
            return sameExpirience.findAll('li')

        return []


#For the scraper to work, you need to be loggedin to LinkedIn...
email = "ronisgraciegb@gmail.com"
password = "badboy123"
parser = LinkedInParser(email, password)