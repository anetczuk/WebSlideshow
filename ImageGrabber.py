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

import threading, time
import logging



class Sleeper:
    def __init__(self):
        self.starttimemillis = time.time() * 1000
        
    def sleep(self, seconds):
        elapsed = time.time() * 1000 - self.starttimemillis
        waittime = (seconds * 1000 - elapsed) / 1000                    ## wait secs
        ## print "Waiting:", waittime
        if waittime <= 0:
            return
        time.sleep(waittime)
    

class ImageGrabberThread(threading.Thread):
    def __init__(self, imageWindow):
        threading.Thread.__init__(self)
        self.daemon = True                              ## automatically killed when needed
        
        self.playEvent = threading.Event()
        self.playEvent.set()                            ## play immediatelly
        
        self.display = imageWindow
        
        self.display.connect('play-pause', self.playPause)
        
        self.urlProvider = None
        self.waitTime = 7
        ##self.start()                                    # invoke the run method

    def playPause(self, window):
        if self.playEvent.is_set() is True:
            logging.info("pause")
            self.playEvent.clear();
        else:
            logging.info("resume")
            self.playEvent.set()

    def run(self):
        while True:
            self.iterateImages()
            ## iteration stopped due to exception -- wait some time to restore
            time.sleep(5)
        
    def iterateImages(self):
        try:
            newUrl = self.getNextUrl()
            while True:
                sleeper = Sleeper()
                
                loaded = self.display.openUrl( newUrl )
                
                newUrl = self.getNextUrl()

                if loaded == False:
                    ## could not load image
                    sleeper.sleep(1)
                    continue
                
                if self.playEvent.is_set() is False:
                    self.playEvent.wait()
                
                sleeper.sleep(self.waitTime)        
        except:
            logging.exception("Error while providing next image")
        
        
    def getNextUrl(self):
        while True:
            if self.urlProvider is None:
                logging.warning("No url provider")
                time.sleep(1)
                continue
            
            sleeper = Sleeper()
            newUrl = self.urlProvider.provideUrl()
            if newUrl == "":
                logging.warning("Url not provided")
                sleeper.sleep(1)
                continue
            
            return newUrl
        

    def setDisplayTime(self, dTimeS):
        self.waitTime = float(dTimeS)

#
#
