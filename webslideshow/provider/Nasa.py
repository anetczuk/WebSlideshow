# MIT License
# 
# Copyright (c) 2017 Arkadiusz Netczuk <dev.arnet@gmail.com>
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
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
