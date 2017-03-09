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

import threading, time


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
            print "pause"
            self.playEvent.clear();
        else:
            print "resume"
            self.playEvent.set()

    def run(self):
        newUrl = self.getUrl()
        while True:
            sleeper = Sleeper()
            
            self.display.openUrl( newUrl )
            
            newUrl = self.getUrl()
            
            if self.playEvent.is_set() is False:
                self.playEvent.wait()
            
            sleeper.sleep(self.waitTime)
        
        
    def getUrl(self):
        while True:
            if self.urlProvider is None:
                print "No url provider"
                time.sleep(1)
                continue
            
            newUrl = self.urlProvider.provideUrl()
            if newUrl == "":
                print "Url not provided"
                time.sleep(1)
                continue
            
            return newUrl
        

    def setDisplayTime(self, dTimeS):
        self.waitTime = float(dTimeS)

#
#
