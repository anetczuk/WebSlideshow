'''
Documentation, License etc.

@package WebSlideshow
'''

import pygtk, gtk

from DrawerWindow import DrawerWindow
from ImageGrabber import ImageGrabberThread

import argparse
import importlib

##from provider.UrlProvider import ExampleProvider



def import_module( moduleName, className ):
    mod = importlib.import_module( moduleName )
    return getattr(mod, className)


#
#
#
class MainWin:
    def __init__(self, fullscreen):
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

    args = parser.parse_args()
    print "Args:", args
    
    randomMode = args.random
    
    print "Loading provider:", args.provider
    
    providerMod = "provider." + args.provider
    mod = import_module( providerMod, args.provider )
    
    provider = mod()
    
    mainW = MainWin(not args.nofs)
    mainW.setProvider( provider )
    mainW.setDisplayTime( args.dtime )
    mainW.main()
