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

import unittest

from DrawerWindow import DrawerWindow
# import pygtk, gtk
import gtk


class DrawerWindowTest(unittest.TestCase):
    def setUp(self):
        # Called before the first testfunction is executed
        pass

    def tearDown(self):
        # Called after the last testfunction was executed
        pass

    def xtest_displayJpg(self):
        window = DrawerWindow()
        url = "http://upload.wikimedia.org/wikipedia/commons/5/57/PT05_ubt.jpeg"
        window.openUrl(url)
        gtk.main()
    
    def xtest_displayAnimGiff(self):
        window = DrawerWindow(True)
        url = "https://articulate-heroes.s3.amazonaws.com/uploads/rte/kgrtehja_DancingBannana.gif"
        window.openUrl(url)
        gtk.main()


if __name__ == "__main__":
    unittest.main()
