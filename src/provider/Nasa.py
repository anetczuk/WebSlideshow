#
# <one line to give the library's name and an idea of what it does.>
# Copyright (C) 2017  Arkadiusz Netczuk <dev.arnet@gmail.com>
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
# 
#

from UrlProvider import UrlProvider

import lxml.html
import random
import datetime, time
import logging



class Nasa(UrlProvider):
    def __init__(self, random = False):
        UrlProvider.__init__(self)
        self.randomUrlBase = "https://apod.nasa.gov"

    def provideUrl(self): 
        return self.randomUrl()
    
    def randomUrl(self):
        url = self.generateUrl()
        body = self.getPageBody( url )
        urlList = self.parsePage(self.randomUrlBase, body)
        if (len(urlList) < 1):
            logging.warning("No url found")
            return ""
        return urlList[0]

    def generateUrl(self):
        ##return 'https://apod.nasa.gov/apod/random_apod.html'
        
        ## https://apod.nasa.gov/apod/ap121220.html
        ## https://apod.nasa.gov/apod/ap971101.html
        
        mindate = datetime.date(1995, 5, 16)
        mintimestamp = time.mktime(mindate.timetuple())
        ##print "Min:", mindate, mintimestamp
        
        maxdate = datetime.date.today()
        maxtimestamp = time.mktime(maxdate.timetuple())
        ##print "Max:", maxdate, maxtimestamp
        
        prop = random.random()
        
        rtimestamp = mintimestamp + prop * (maxtimestamp - mintimestamp)
        rdate = datetime.date.fromtimestamp(rtimestamp)
        ##print "R date:", rdate

        strdate = rdate.strftime("%y%m%d")
        return self.randomUrlBase + "/apod/ap" + strdate + ".html"

    def parsePage(self, urlBase, body):
        inlineBody = body.replace("\r\n", " ")
        inlineBody = inlineBody.replace('\r', " ")
        inlineBody = inlineBody.replace('\n', " ")
        ## print "Body:\n", inlineBody
        
        lxmlSite = lxml.html.fromstring(inlineBody)
        imgTags = lxmlSite.xpath("//center//a/img")
        ## print "Found:", lxml.etree.tostring( imgTags[0] )
        
        retList = []
        for img in imgTags:
            url = img.get("src")
            if len(url) < 1:
                continue
            retList.append( urlBase + "/" + url )
        
        return retList
