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



class NasaTest(unittest.TestCase):
    def setUp(self):
        # Called before the first testfunction is executed
        pass

    def tearDown(self):
        # Called after the last testfunction was executed
        pass


    def test_parse001(self):
        body = """
                <div class="object">
                        <div class="podpis">
                                <span class="lewa">
                                        komentarze (<fb:comments-count href=http://pokazcyckidamciciastko.pl/cycki/2007/mmm-lt3/></fb:comments-count>)
                                        
                                </span>
                                <span class="prawa">
                                        <a href="#" class="thumb_up" onClick="vote_up(2007); return false;">dobre</a>
                                        <span style="color:#fff;" class="rate_2007">?%</span>
                                        <a href="#" class="thumb_down" onClick="vote_down(2007); return false;">słabe</a>
                                </span>
                        </div>
                        <a href="#"><img src="http://pokazcyckidamciciastko.pl/upload/20121112112157.png" title="mmm... &lt;3" alt="mmm... &lt;3" /></a>
                </div>
""";
        provider = Ciastko()
        links = provider.parsePage(body)        
        self.assertEqual(links, ['http://pokazcyckidamciciastko.pl/upload/20121112112157.png'])

    def test_random(self):
        provider = Ciastko()
        url = provider.randomUrl()
        self.assertGreater(len(url), 0)
        
    def test_provide(self):
        provider = Ciastko()
        url = provider.provideUrl()
        ## print "Links:\n", provider.links
        self.assertGreater( len(url), 0 )


if __name__ == "__main__":
    unittest.main()
