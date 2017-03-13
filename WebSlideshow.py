'''
Documentation, License etc.

@package WebSlideshow
'''

import pygtk, gtk

from DrawerWindow import DrawerWindow
from ImageGrabber import ImageGrabberThread
from ScreenSaverDisabler import ScreenSaverDisabler

import argparse
import importlib
import logging

##from provider.UrlProvider import ExampleProvider



def import_module( moduleName, className ):
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
    
    providerMod = "provider." + args.provider
    providerClass = import_module( providerMod, args.provider )
    
    provider = providerClass( randomMode )              ## call constructor
    
    mainW = MainWin(not args.nofs)
    mainW.setProvider( provider )
    mainW.setDisplayTime( args.dtime )
    mainW.main()
