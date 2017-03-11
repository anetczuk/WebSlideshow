#
# <one line to give the library's name and an idea of what it does.>
# Copyright (C) 2017  Bob <email>
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

from StringIO import StringIO
import pycurl
import exceptions
import logging



class UrlProvider:
    def __init__(self): pass

    def provideUrl(self): 
        ## implement
        return ""
    
    def getPageBody(self, target_url):
        buffer = StringIO()
        try:
            c = pycurl.Curl()
            c.setopt(c.URL, target_url)
            c.setopt(c.WRITEDATA, buffer)
            c.setopt(c.FOLLOWLOCATION, True)        ## follow redirects
            c.perform()
        except Exception as err:
            logging.exception("Unexpected exception")
            return ""
        finally:
            c.close()
            
        bodyOutput = buffer.getvalue()
        
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
    