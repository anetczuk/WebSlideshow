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


import logging

# import shlex
from subprocess import Popen, PIPE
import re



##
## Cannot be set as global variable, because destructor will crash (calling Popen()).
##
class ScreenSaverDisabler:
    def __init__(self):
        self.properlyInit = False
        ## read state
        out = self.__call('xset q')
        ##print out
        ##if re.search('^F..m:', line) :
        ## find timeout
        timeoutList = re.findall('.*timeout:\W+(\w+)\W+.*', out)
        ## print "Found:", timeoutList
        if len(timeoutList) != 1:
            logging.warn("unable to get screensaver setting from %s", timeoutList)
            return
        self.timeout = int(timeoutList[0])
        
        dpmsList = re.findall('.*DPMS is Enabled.*', out)
        ##print "Found:", dpmsList
        if len(dpmsList) == 1:
            self.dpms = True
        else:
            self.dpms = False
        
        self.properlyInit = True
        logging.info("Disabling screensaver setings, current: timeout[%s] DPMS[%s]", self.timeout, self.dpms)
        
        ## disable blank screen
        ##if self.timeout > 0:
        self.__call("xset s off")
        ## disable dpms
        if self.dpms is True:
            self.__call("xset -dpms")
        
    def __del__(self):
        self.restore()
        
    def restore(self):
        if self.properlyInit is False:
            return
        ## call destructor part
        logging.info("Restoring screensaver setings: timeout[%s] DPMS[%s]", self.timeout, self.dpms)
        ## restoring blank screen
        if self.timeout > 0:
            timeoutCall = "xset s " + str(self.timeout)
            self.__call( timeoutCall )
        ## restore dpms
        if self.dpms is True:
            self.__call("xset dpms")
        self.properlyInit = False
        
    def __call(self, cmd):
        ##print "Calling:", cmd
        proc = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True)
        out = proc.communicate()
        ## out, err = proc.communicate()
        ## print "Output:", out, err
        ## exitcode = proc.returncode
        
        ## out[1] is error code
        return out[0]
