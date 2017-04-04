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
