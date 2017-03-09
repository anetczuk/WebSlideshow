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

import gtk, cairo, gobject
from threading import Lock


class PixbufDrawer(gtk.DrawingArea):
    def __init__(self):
        gtk.DrawingArea.__init__(self)
        self.connect('expose-event', self._do_expose)
        self.pixbuf = None
        self.currPixbuf = None

    def _do_expose(self, widget, event):
        self.preparePixbuf()
        if self.currPixbuf is None:
            return
        cr = self.window.cairo_create()
        cr.set_operator(cairo.OPERATOR_SOURCE)
        cr.set_source_rgb(1,1,1)
        cr.paint()
        
        rect = self.get_allocation()
        posX = (rect.width - self.currPixbuf.get_width()) / 2
        posY = (rect.height - self.currPixbuf.get_height()) / 2
        
        cr.set_source_pixbuf(self.currPixbuf, posX, posY)
        
        cr.paint()
            
    def set_from_pixbuf(self, newPixbuf):
        self.pixbuf = newPixbuf
        self.queue_resize()
        
    def preparePixbuf(self):
        # skip if no pixbuf set
        if self.pixbuf is None:
            return
        
        rect = self.get_allocation()
        if rect.width < 10 or rect.height < 10:
            return
        
        # calculate proportions for image widget and for image
        ##k_pixbuf = float(self.pixbuf.props.height) / self.pixbuf.props.width
        k_pixbuf = float(self.pixbuf.get_height()) / self.pixbuf.get_width()
        k_rect = float(rect.height) / rect.width

        # recalculate new height and width
        if k_pixbuf < k_rect:
            newWidth = rect.width
            newHeight = int(newWidth * k_pixbuf)
        else:
            newHeight = rect.height
            newWidth = int(newHeight / k_pixbuf)
        
        if hasattr(self.pixbuf, 'scale_simple'):
            ## scalable
            self.currPixbuf = self.pixbuf.scale_simple(newWidth, newHeight, gtk.gdk.INTERP_BILINEAR)
        else:
            self.currPixbuf = self.pixbuf


class ScopeLock:
    def __init__(self, aMutex):
        self.mutex = aMutex
        self.mutex.acquire()
        self.released = False
    
    def release(self):
        if (self.released is True):
            return
        self.released = True
        self.mutex.release()
    
    def __del__(self):
        self.release()


class AnimationPlayer(gobject.GObject):
    __gsignals__ = {
        'new-frame': (gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, (gtk.gdk.Pixbuf,) )
    }
    
    def __init__(self):
        gobject.GObject.__init__(self)
        self.animIter = None
        self.mutex = Lock()
        
    def play(self, pixbufAnim):
        self.stop()
        if pixbufAnim.is_static_image():
            buff = pixbufAnim.get_static_image()
            self.emit('new-frame', buff)
            return 
        scopeLock = ScopeLock(self.mutex)
        self.animIter = pixbufAnim.get_iter()
        scopeLock.release()
        self.show_frame()
    
    def stop(self):
        scopeLock = ScopeLock(self.mutex)
        ## if (self.animIter is not None):
        ##     print "Stopping"
        self.animIter = None
    
    def frame_timeout(self):
        scopeLock = ScopeLock(self.mutex)
        if (self.animIter is None):
            return False
        self.animIter.advance()
        scopeLock.release()
        self.show_frame()
        return False
    
    def show_frame(self): 
        scopeLock = ScopeLock(self.mutex)
        if (self.animIter is None):
            return 
        buff = self.animIter.get_pixbuf()
        gobject.timeout_add(self.animIter.get_delay_time(), self.frame_timeout)
        scopeLock.release()
        self.emit('new-frame', buff)

        
gobject.type_register(AnimationPlayer)


class PixbufAnimationDrawer(PixbufDrawer):
    def __init__(self):
        PixbufDrawer.__init__(self)
        self.player = AnimationPlayer()
        self.player.connect('new-frame', self.next_frame)
    
    def set_from_pixbuf(self, newPixbuf):
        self.player.stop()
        super(PixbufAnimationDrawer, self).set_from_pixbuf(newPixbuf)
        
    def set_from_animation(self, pixbufAnim):
        if (pixbufAnim is None):
            return
        self.player.play( pixbufAnim )

    def next_frame(self, window, newPixbuf):
        super(PixbufAnimationDrawer, self).set_from_pixbuf( newPixbuf )


