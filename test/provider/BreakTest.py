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

from Break import Break, BreakArticleBrowser



class BreakArticleBrowserTest(unittest.TestCase):
    def setUp(self):
        # Called before the first testfunction is executed
        pass

    def tearDown(self):
        # Called after the last testfunction was executed
        pass
   

    def test_provideUrl(self):
        provider = BreakArticleBrowser("http://www.break.com/pictures/30-examples-of-train-graffiti-3086924")
        url = provider.provideUrl()
        self.assertEqual(url, 'http://media1.break.com/dnet/media/890/086/3086890/7malmo-graffiti-steel-dsc-7844jpg.jpg')
        self.assertEqual(provider.nextElem, 'http://www.break.com/pictures/9jpg-3086891')
        
        url = provider.provideUrl()     ## provide next
        self.assertEqual(url, 'http://media1.break.com/dnet/media/891/086/3086891/9jpg.jpg')
        self.assertEqual(provider.nextElem, 'http://www.break.com/pictures/98e14ddaf9d16751f46d83d9f688ef16jpg-3086892')


class BreakTest(unittest.TestCase):
    def setUp(self):
        # Called before the first testfunction is executed
        pass

    def tearDown(self):
        # Called after the last testfunction was executed
        pass
   

    def test_articles(self):
        provider = Break()
        artList = provider.loadArticles()
        ##print "List:", artList
        self.assertGreater(len(artList), 0)
        
    def test_provide(self):
        provider = Break()
        url = provider.provideUrl()
        ## print "Links:\n", provider.links
        self.assertGreater( len(url), 0 )
        

if __name__ == "__main__":
    unittest.main()
