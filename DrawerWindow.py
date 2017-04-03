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

import pygtk
pygtk.require('2.0')

import gtk, gobject
# from gtk import Image

import urllib2
import logging

from PixbufDrawer import PixbufAnimationDrawer
from socket import error as SocketError



def loaderFromUrl( imageUrl ):
    print "Opening:", imageUrl
    logging.info("Opening: %s", imageUrl)
    
    try:
        response = urllib2.urlopen( imageUrl )
    except urllib2.HTTPError:
        logging.exception("Unable to open url: %s", imageUrl)
        return None
    except ValueError:
        logging.exception("Unable to open url: %s", imageUrl)
        return None
    except SocketError as sockerr:
        logging.exception("Error when opening url: %s, reason: %s", imageUrl, sockerr)
        return None


    loader=gtk.gdk.PixbufLoader()
    ##pixbufanim = gtk.gdk.PixbufAnimation("goalie.gif")
    try:
        resp = response.read()
        loader.write( resp )            ## raises GError
        loader.close()                  ## raises GError
    except gobject.GError:
        logging.exception("Error while writing response, received data type: %s", type(resp))
    except:
        logging.exception("Unexpected error while writing response")
        raise
    
    return loader


class DrawerWindow(gobject.GObject):
    __gsignals__ = {
        'play-pause': (gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, ()),
    }
    
    def __init__(self, fullscreen = False):
        gobject.GObject.__init__(self)
        
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        ### logging.info("screen instance: %s", self.window.get_screen())
        if self.window.get_screen() is None:
            logging.fatal("could not initialize window properly (no X server?)")
            quit(1)
        
        self.area = PixbufAnimationDrawer()
        
        bgcol = gtk.gdk.Color('#000')
        self.window.modify_bg(gtk.STATE_NORMAL, bgcol)
        self.window.connect("destroy", self.destroy)
        self.window.connect('key-press-event', self.on_key_press)
        
        self.window_is_fullscreen = False
        self.window.connect('window-state-event', self.on_window_state_change)
        
        self.window.add(self.area)
        
        self.window.set_border_width(0)
        if fullscreen is True:
            self.window.fullscreen()
        self.window.resize( 640, 480 )
        self.window.show_all()

    def destroy(self, widget, data=None):
        logging.info( "Destroy signal occurred" )
        gtk.main_quit()
        
    def on_key_press(self, widget, ev, data=None):
        keyname = gtk.gdk.keyval_name(ev.keyval)
        ##print "event key:", keyname
        if keyname == 'Escape':
            self.window.unfullscreen()
        elif keyname == 'F11':
            if self.window_is_fullscreen:
                self.window.unfullscreen()
            else:
                self.window.fullscreen()
        elif keyname == 'space':
            self.emit('play-pause')
    
    def on_window_state_change(self, window, event):
        ## print "Ev:", event, "W:", window
        self.window_is_fullscreen = bool(gtk.gdk.WINDOW_STATE_FULLSCREEN & event.new_window_state)
    
    def openUrl(self, imageUrl):
        loader = loaderFromUrl(imageUrl)
        if (loader is None):
            return False
        anim = loader.get_animation()        
        self.area.set_from_animation(anim)
        return True
        
        # This does the same thing, but by saving to a file
        # fname='/tmp/planet_x.jpg'
        # with open(fname,'w') as f:
        #     f.write(response.read())
        # self.image.set_from_file(fname)


gobject.type_register(DrawerWindow)


#
#
#
