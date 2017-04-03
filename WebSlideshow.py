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

# import pygtk, gtk
import gtk

from DrawerWindow import DrawerWindow
from ImageGrabber import ImageGrabberThread
from ScreenSaverDisabler import ScreenSaverDisabler

import argparse
import importlib
import logging

import ntpath

##from provider.UrlProvider import ExampleProvider



def import_module( path ):
    moduleName = path.replace("/", ".")
    className = ntpath.basename( path )
    
    logging.info("importing module: %s %s", moduleName, className)
    mod = importlib.import_module( moduleName )
    return getattr(mod, className)


#
#
#
class MainWin:
    def __init__(self, fullscreen):
        ## disable screen saver
        self.screensaver = ScreenSaverDisabler()
        
        self.imgWindow = DrawerWindow(fullscreen)
        self.thread = ImageGrabberThread( self.imgWindow )
        ##self.thread.urlProvider = ExampleProvider()
        
    def setProvider(self, provider):
        self.thread.urlProvider = provider
        
    def setDisplayTime(self, dTimeS):
        self.thread.setDisplayTime( dTimeS )
        
    def main(self):
        self.thread.start()
        gtk.gdk.threads_init()          ## run threads
        gtk.main()
        

if __name__ == "__main__":    
    parser = argparse.ArgumentParser(description='Display internet gallery.')
    parser.add_argument('--provider', action='store', default="Demotywatory", help='Load given image provider' )
    parser.add_argument('--random', action='store_const', const=True, default=False, help="Gallery random mode (if supporting)" )
    parser.add_argument('--dtime', action='store', default=10, help="Display time of single image [s]" )
    parser.add_argument('--nofs', action='store_const', const=True, default=False, help='No fullscreen at startup' )
    parser.add_argument('--loglevel', action='store', help='Set log level' )

    args = parser.parse_args()
        
    if args.loglevel:
        llevel = getattr(logging, args.loglevel)
        logging.basicConfig(level=llevel)
    
    logging.info("Args: %s", args)
    
    if args.loglevel:
        print "Log level:", args.loglevel
    
    randomMode = args.random
    
    logging.info("Loading provider: %s", args.provider)
    
    providerClass = import_module( "provider/" + args.provider )
    
    provider = providerClass( randomMode )              ## call constructor
    
    mainW = MainWin(not args.nofs)
    mainW.setProvider( provider )
    mainW.setDisplayTime( args.dtime )
    mainW.main()
