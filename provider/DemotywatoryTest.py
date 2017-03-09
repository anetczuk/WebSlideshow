# -*- coding: utf-8 -*-

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

import unittest


from Demotywatory import Demotywatory


class DemotywatoryTest(unittest.TestCase):
    def setUp(self):
        # Called before the first testfunction is executed
        pass

    def tearDown(self):
        # Called after the last testfunction was executed
        pass
    
    def test_random(self):
        provider = Demotywatory()
        url = provider.randomUrl()
        self.assertGreater(len(url), 0)
        
    def test_provide(self):
        provider = Demotywatory()
        url = provider.provideUrl()
        ## print "Links:\n", provider.links
        self.assertGreater( len(url), 0 )


if __name__ == "__main__":
    unittest.main()
