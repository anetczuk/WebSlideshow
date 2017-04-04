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



class BreakArticleBrowser(UrlProvider):
    def __init__(self, articleUrl):
        UrlProvider.__init__(self)
        self.article = articleUrl
        self.nextElem = articleUrl
        logging.info("Starting article: %s", self.article)

    def provideUrl(self): 
        if (self.nextElem is None) or (self.nextElem == ""):
            return ""
        body = self.getPageBody( self.nextElem )
        url = self.parseArticle(body)
        return url

    def isEmpty(self):
        return ((self.nextElem is None) or (self.nextElem == ""))

    def parseArticle(self, body):
        inlineBody = body.replace("\r\n", " ")
        inlineBody = inlineBody.replace('\r', " ")
        inlineBody = inlineBody.replace('\n', " ")
        ## print "Body:\n", inlineBody
        
        lxmlSite = lxml.html.fromstring(inlineBody)
        ##elems = lxmlSite.xpath("//article[contains(@id, 'js-brk-gallery-container')]//div[contains(@id, 'gallery-player')]/img")
        players = lxmlSite.xpath("//article[contains(@id, 'js-brk-gallery-container')]//div[contains(@id, 'gallery-player')]")
        if (len(players) < 1):
            return ""
        
        ## print "Players:", players
        
        play = players[0]
        imgs = play.xpath("//div[@id='gallery-player-cg']/img")
        if (len(imgs) < 1):
            return ""
        ##print "Images:", imgs
        ##print "Image:", lxml.etree.tostring( imgs[0] )
        imgUrl = imgs[0].get("src")
        
        nextPage = play.xpath("//a[contains(@class, 'next')]")
        if (len(nextPage) < 1):
            self.nextElem = None
            return imgUrl
        
        self.nextElem = nextPage[0].get("href")
        if (self.nextElem == self.article):
            logging.info("Returning article's last url")
            self.nextElem = None
            return imgUrl
        
        ##print "Next url:", self.nextElem
        return imgUrl

        

class Break(UrlProvider):
    #
    # random mode not supported
    #
    def __init__(self, randomMode = False):
        if (randomMode is True):
            logging.info("Random mode not supported")
        UrlProvider.__init__(self)
        self.baseUrl = "http://www.break.com/pictures/"
        self.articles = []
        self.artProvider = None

    def provideUrl(self):         
        self.initInnerProvider()

        if self.artProvider is None:
            return ""
        
        url = self.artProvider.provideUrl()
        if (url == ""):
            ## no more images for article
            logging.warning("No more images in article")
            self.artProvider = None
            
        return url
    
    def initInnerProvider(self):
        if (len(self.articles) < 1):
            self.loadArticles()
            ##print "Loaded articles:", self.articles
        if (len(self.articles) < 1):
            logging.warning("Could not load articles list")
            self.artProvider = None
            return
        if self.artProvider is None:
            artUrl = self.articles.pop(0)
            self.artProvider = BreakArticleBrowser(artUrl)
        if self.artProvider.isEmpty():
            artUrl = self.articles.pop(0)
            self.artProvider = BreakArticleBrowser(artUrl)
    
    def loadArticles(self):
        body = self.getPageBody( self.baseUrl )
        self.articles = self.parseArticles(body)
        return self.articles
    
    def parseArticles(self, body):
        inlineBody = body.replace("\r\n", " ")
        inlineBody = inlineBody.replace('\r', " ")
        inlineBody = inlineBody.replace('\n', " ")
        ## print "Body:\n", inlineBody
        
        lxmlSite = lxml.html.fromstring(inlineBody)
        elems = lxmlSite.xpath("//div[contains(@id, 'content-timestream')]//article/div//a")
        
        #print "Found:", elems
        #for e in elems:
        #    print "Found:", lxml.etree.tostring( e )
        
        retList = []
        for img in elems:
            url = img.get("href")
            if len(url) > 0:
                retList.append( url )
        
        return retList
