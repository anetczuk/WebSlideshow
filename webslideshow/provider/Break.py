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
