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

import logging

import shlex
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
        ##if re.search('^F..m:', line) :
        ##print out
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
        out, err = proc.communicate()
        ## print "Output:", out, err
        ## exitcode = proc.returncode
        return out
