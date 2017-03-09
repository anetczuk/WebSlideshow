'''
Documentation, License etc.

@package WebSlideshow
'''

import pygtk, gtk

from DrawerWindow import DrawerWindow
from ImageGrabber import ImageGrabberThread

import argparse

##from provider.UrlProvider import ExampleProvider
from provider.Demotywatory import Demotywatory
from provider.Ciastko import Ciastko
from provider.Gag9 import Gag9
from provider.Break import Break
from provider.Nasa import Nasa


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
    parser.add_argument('--Demoty', action='store_const', const=True, default=True, help='Use www.demotywatory.pl gallery (default)' )
    parser.add_argument('--Nasa', action='store_const', const=True, help='Use https://apod.nasa.gov/apod/random_apod.html gallery' )
    parser.add_argument('--Gag9', action='store_const', const=True, help='Use www.9gag.com gallery' )
    parser.add_argument('--Break', action='store_const', const=True, help='Use www.break.com/pictures gallery' )
    parser.add_argument('--Ciastka', action='store_const', const=True, help='Use gallery for cookie' )
    parser.add_argument('--random', action='store_const', const=True, default=False, help="Gallery random mode (if supporting)" )
    parser.add_argument('--dtime', action='store', default=10, help="Display time of single image [s]" )
    parser.add_argument('--nofs', action='store_const', const=True, default=False, help='No fullscreen at startup' )

    args = parser.parse_args()
    print "Args:", args
    
    randomMode = args.random
    
    provider = None
    if args.Demoty is True:
        provider = Demotywatory( randomMode )
    if args.Nasa is True:
        provider = Nasa()
    if args.Gag9 is True:
        provider = Gag9()
    if args.Break is True:
        provider = Break()
    if args.Ciastka is True:
        provider = Ciastko( randomMode )
    
    mainW = MainWin(not args.nofs)
    mainW.setProvider( provider )
    mainW.setDisplayTime( args.dtime )
    mainW.main()
