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
        self.animIter = None
        scopeLock.release()
    
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


