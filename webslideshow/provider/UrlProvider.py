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


from StringIO import StringIO
import pycurl
# import exceptions
# import logging



class UrlProvider:
    def __init__(self): pass

    def provideUrl(self): 
        ## implement
        return ""
    
    ##
    ## Method should return valid page body or throw an exception.
    ##
    def getPageBody(self, target_url):
        dataBuffer = StringIO()
        try:
            c = pycurl.Curl()
            c.setopt(c.URL, target_url)
            c.setopt(c.WRITEDATA, dataBuffer)
            c.setopt(c.FOLLOWLOCATION, True)        ## follow redirects
            c.perform()
#         except Exception as err:
#             logging.exception("Unexpected exception")
#             return ""
        finally:
            c.close()
            
        bodyOutput = dataBuffer.getvalue()
        
        # Body is a string in some encoding.
        # In Python 2, we can print it without knowing what the encoding is.
        ##print "Body:\n", body
        
        return bodyOutput



class ExampleProvider(UrlProvider):
    def __init__(self, randomMode = False):
        UrlProvider.__init__(self)
        self.counter = 0
        self.list = [ 'http://www.dailygalaxy.com/photos/uncategorized/2007/05/05/planet_x.jpg', 
                      'https://www.w3schools.com/css/img_fjords.jpg' ]

    def provideUrl(self):
        ## implement
        lSize = len(self.list)
        elem = self.counter % lSize
        self.counter = self.counter + 1
        return self.list[ elem ]
    