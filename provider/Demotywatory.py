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
import logging



class SingleDemot(UrlProvider):
    def __init__(self, imageUrl):
        UrlProvider.__init__(self)
        self.image = imageUrl

    def provideUrl(self): 
        if (self.image is None):
            return ""
        url = self.image
        self.image = None
        return url

    def isEmpty(self):
        return (self.image is not None)


class DemotGalleryBrowser(UrlProvider):
    def __init__(self, galleryUrl):
        UrlProvider.__init__(self)
        self.article = galleryUrl
        self.images = None
        ## print "Starting article:", self.article

    def provideUrl(self): 
        if (self.images is None):
            body = self.getPageBody( self.article )
            self.images = self.parseArticle(body)
            
        if (len(self.images) < 1):
            ## end of images
            logging.warning("No more images in gallery")
            return ""
        
        url = self.images.pop(0)
        return url

    def isEmpty(self):
        if self.images is None:
            return False
        return (len(self.images) < 1)

    def parseArticle(self, body):
        inlineBody = body.replace("\r\n", " ")
        inlineBody = body.replace('\r', " ")
        inlineBody = body.replace('\n', " ")
        ## print "Body:\n", inlineBody
        
        lxmlSite = lxml.html.fromstring(inlineBody)
        players = lxmlSite.xpath("//article/div[contains(@class, 'demotivator')]/div[contains(@class, 'gallery')]")
        if (len(players) < 1):
            return ""
        
        ## print "Players:", players
        
        play = players[0]
        imgTags = play.xpath("//div[@class='rsSlideContent']//img[contains(@class, 'rsImg')]")
        ## print "Images:", imgTags

        retList = []
        for img in imgTags:
            url = img.get("src")
            if len(url) < 1:
                continue
            if url[0] == '/':
                retList.append( "http://demotywatory.pl/" + url )
            else:
                retList.append( url )
        
        return retList


class Demotywatory(UrlProvider):
    def __init__(self, random = False):
        UrlProvider.__init__(self)
        self.baseUrl = "http://www.demotywatory.pl"
        self.randomMode = random
        ##self.galleryProvider = DemotGalleryBrowser('http://demotywatory.pl/4750418/26-internautow-opowiada-o-najbardziej-zenujacych-wpadkach-i')
        self.providers = []

    def provideUrl(self): 
        ##url = self.galleryProvider.provideUrl()
        ##return url
        
        if (self.randomMode):
            return self.randomUrl()
        
        ## main page images
        if len(self.providers) < 1:
            self.extractUrls()
        
        while len(self.providers) > 0:
            provider = self.providers[0]
            if provider.isEmpty():
                self.providers.pop(0)
            return provider.provideUrl()
        logging.warning("Empty providers list")
        return ""
    
    def randomUrl(self):
        body = self.getPageBody( 'http://demotywatory.pl/losuj' )
        urlList = self.parseRandomPage(body)
        if (len(urlList) < 1):
            logging.warning("No url found")
            return ""
        return urlList[0]
    
    def extractUrls(self):
        body = self.getPageBody( self.baseUrl )
        self.providers = self.parseMainPage(body)

    def parseMainPage(self, body):
        inlineBody = body.replace("\r\n", " ")
        inlineBody = body.replace('\r', " ")
        inlineBody = body.replace('\n', " ")
        
        lxmlSite = lxml.html.fromstring(inlineBody)
        demotTags = lxmlSite.xpath("//article/div[contains(@class, 'demotivator')]/div[contains(@class, 'demot_pic')]")
        
        ##print "Found:", demotTags
        ##lxml.etree.tostring( imgTags[0] )
        
        retList = []
        for elem in demotTags:        
            classes = elem.get("class")
            ## print "Classes:", classes
            if "gallery" in classes:
                ## gallery case            
                aTags = elem.xpath("./a[contains(@class, 'picwrapper')]")
                if len(aTags)<1:
                    logging.error("Invalid 'a' tag")
                    continue
                aElem = aTags[0]
                url = aElem.get("href")
                if len(url) < 1:
                    continue
                galleryUrl = self.checkUrl(url)
                ## print "Found gallery:", galleryUrl
                retList.append( DemotGalleryBrowser(galleryUrl) )
                continue
            ## else standard picture
            
            imgTags = elem.xpath(".//img")
            if len(imgTags)<1:
                logging.error("Invalid 'img' tag")
                continue
            img = imgTags[0]
            url = img.get("src")
            if len(url) < 1:
                continue
            imgUrl = self.checkUrl(url)
            ## print "Found image:", imgUrl
            retList.append( SingleDemot(imgUrl) )
        
        return retList

    def checkUrl(self, anUrl):
        if anUrl[0] == '/':
            return self.baseUrl + anUrl
        return anUrl

    def parseRandomPage(self, body):
        inlineBody = body.replace("\r\n", " ")
        inlineBody = body.replace('\r', " ")
        inlineBody = body.replace('\n', " ")
        
        lxmlSite = lxml.html.fromstring(inlineBody)
        imgTags = lxmlSite.xpath("//article/div[contains(@class, 'demotivator')]/div[contains(@class, 'demot_pic')]//img")
        
        ##print "Found:", imgTags
        ##lxml.etree.tostring( imgTags[0] )
        
        retList = []
        for img in imgTags:
            url = img.get("src")
            if len(url) < 1:
                continue
            if url[0] == '/':
                retList.append( self.baseUrl + url )
            else:
                retList.append( url )
        
        return retList

