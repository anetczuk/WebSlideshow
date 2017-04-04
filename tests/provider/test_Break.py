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


import unittest

from webslideshow.provider.Break import Break, BreakArticleBrowser



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
