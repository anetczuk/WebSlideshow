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
    
    
    def test_parse001(self):
        body = """
        <article>
                <div class="demotivator pic "
                 id="demot4749008" data-tags="1">
                <input type="hidden" class="pic_id" name="pic_id" value="4749008" />
        <h2 style="display: none;">
                Tak wyglądała oprawa meczu pomiędzy Vive Kielce, a węgierskim Pick Szeged w ramach Ligi Mistrzów
                        </h2>
<div class="
         demot_pic
         image600                                "
>
                                        <a href="/4749008/Tak-wygladala-oprawa-meczu-pomiedzy-Vive-Kielce-a-wegierskim" class="picwrapper"
                                                           >
                
                                                                                        <img
                                                                                        src="http://img1.demotywatoryfb.pl//uploads/201703/1488375621_gdctxm_600.jpg"
                                                                                 alt="Tak wyglądała oprawa meczu pomiędzy Vive Kielce, a węgierskim Pick Szeged w ramach Ligi Mistrz&oacute;w &ndash;  "
                                         class="demot"
                                         width="600"
                                                                                        height="478"
                                                                                                                />
                                        </a>
                                                <script>
                $('.demotivator_inner_video_wrapper video.autoplay:not(.playing)').each(function () {
                $(this).addClass('playing');
                this.play();
        });
</script></div><!-- .demot_pic -->

        <div class="like_buttons_box">
                <section class="fb_like_button">
                        <div class="fb-like"
                                 data-href="http://demotywatory.pl/4749008/Tak-wygladala-oprawa-meczu-pomiedzy-Vive-Kielce-a-wegierskim"
                                 data-send="false"
                                 data-layout="box_count"
                                 data-width="100"
                                 data-show-faces="false"
                                 data-font="lucida grande"
                                 data-colorscheme="dark"
                        ></div>
                </section>
        </div>
<div class="true_demotivator"></div>

                                <div class="admin_menu">
                                                                                                </div>
        </div><!-- .demotivator -->
        </article>
""";
        provider = Demotywatory()
        links = provider.parsePage(body)        
        self.assertEqual(links, ['http://img1.demotywatoryfb.pl//uploads/201703/1488375621_gdctxm_600.jpg'])

    def test_parse002(self):
        body = """
<div id="submenu-wrapper">
<ul class="submenu">
<li>
<a href="https://instagram.com/demotywatorypl/" target="_blank" rel="nofollow">
<img src="/res/img/icons/instagram.png" alt="instagram demotywatory" class="instagram icon"/>
Instagram
</a>
</li>
<li class="hidden important ">
<a href="/demotivator/moje/obserwowani">Obserwowane</a>
</li>
<li><a href="/filmy">Filmy</a></li>
<li><a href="/gify">Gify</a></li>
<li><a href="/galerie">Galerie</a></li>
<li><a href="/wygraj" title="Konkursy">Konkursy</a></li>
<li>
<a href="/gadzety" title="Gadżety" class=" trackMenu">
Gadżety
</a>
</li>
<li>
<a href="/contact" title="Kontakt" class=" trackMenu">
Kontakt
</a>
</li>
<li><a href="/zasady">Zasady</a></li>
</ul>
</div>
""";
        provider = Demotywatory()
        links = provider.parsePage(body)        
        self.assertEqual(links, [])

    def test_parse003(self):
        body = """

<article>
<div class="demotivator pic" id="demot4555390" data-tags="1">
<input type="hidden" class="pic_id" name="pic_id" value="4555390"/>
<h2 style="display: none;">
Zakazać, zabronić, jakie to proste. Zapraszam do domów ludzi, których ledwo stać na węgiel. &#039;&#039;Kazać im&#039;&#039; ogrzewać gazem/prądem i wpaść do nich w środku zimy żeby &#039;&#039;odczuć&#039;&#039; efekt
</h2>
<div class="
         demot_pic
         image600                                ">
<span class="picwrapper">
<img src="http://img8.demotywatoryfb.pl//uploads/201509/1443340451_iqbq8x_600.jpg" alt="Zakazać, zabronić, jakie to proste. Zapraszam do dom&oacute;w ludzi, kt&oacute;rych ledwo stać na węgiel. &#039;&#039;Kazać im&#039;&#039; ogrzewać gazem/prądem i wpaść do nich w środku zimy żeby &#039;&#039;odczuć&#039;&#039; efekt &ndash;  " class="demot" width="600" height="621"/>
</span>
<script>
                $('.demotivator_inner_video_wrapper video.autoplay:not(.playing)').each(function () {
                $(this).addClass('playing');
                this.play();
        });
</script></div> 
<div class="source">
Źródło: <a href="http://www.bankier.pl/wiadomosc/NSA-nie-mozna-zabronic-palenia-weglem-3414214.html" target="_blank" rel="nofollow">http://www.bankier.pl/wiadomosc/NSA-nie-mozna&#8230;</a> </div>
<div class="like_buttons_box">
<section class="fb_like_button">
<div class="fb-like" data-href="http://demotywatory.pl/4555390/Zakazac-zabronic-jakie-to-proste-Zapraszam-do-domow-ludzi-ktorych-ledwo-stac-na-wegiel-039039Kazac-im039039-ogrzewac-gazem-pradem-i-wpasc-do-nich-w-srodku-zimy-zeby-039039odczuc039039-efekt" data-send="false" data-layout="box_count" data-width="100" data-show-faces="false" data-font="lucida grande" data-colorscheme="dark"></div>
</section>
</div>
<section class="tags">
<ul>
<li><a href="/tag/węgiel">#węgiel</a></li>
<li><a href="/tag/ogrzewanie">#ogrzewanie</a></li>
<li><a href="/tag/piec">#piec</a></li>
<li><a href="/tag/dom">#dom</a></li>
<li><a href="/tag/smog">#smog</a></li>
<li><a href="/tag/ekologia">#ekologia</a></li>
<li><a href="/tag/gaz">#gaz</a></li>
</ul>
</section>
<nav>
<div class="demot_info_stats">
 
<div class="demot_extra_area"></div>
 
<ul>
<li>
<time datetime="26 września 2015 o 14:38">26 września 2015 o 14:38</time>
przez
<a href="/user/MaciekMagik" class="demot-author super-account">
MaciekMagik </a>
</li>
<li>
<a href="http://demotywatory.pl/4555390#comments" class="comment" style="color: red;">Skomentuj (59)</a> </li>
<li>
<a href="/user/add_favorite/4555390" class="favorite">
Do ulubionych
</a>
</li>
</ul>
<br/>
</div> 
</nav>
<div class="true_demotivator"></div>
<div class="admin_menu">
</div> 
</div> 
</article>

""";
        provider = Demotywatory()
        links = provider.parsePage(body)        
        self.assertEqual(links, ['http://img8.demotywatoryfb.pl//uploads/201509/1443340451_iqbq8x_600.jpg'])

    def test_parsePage_short(self):
        body = """

<article>
<div class="demotivator pic" id="demot4555390" data-tags="1">
<input type="hidden" class="pic_id" name="pic_id" value="4555390"/>
<h2 style="display: none;">
Zakazać, zabronić, jakie to proste. Zapraszam do domów ludzi, których ledwo stać na węgiel. &#039;&#039;Kazać im&#039;&#039; ogrzewać gazem/prądem i wpaść do nich w środku zimy żeby &#039;&#039;odczuć&#039;&#039; efekt
</h2>
<div class="
         demot_pic
         image600                                ">
<span class="picwrapper">
<img src="/uploads/201509/1443340451_iqbq8x_600.jpg" alt="Zakazać, zabronić, jakie to proste. Zapraszam do dom&oacute;w ludzi, kt&oacute;rych ledwo stać na węgiel. &#039;&#039;Kazać im&#039;&#039; ogrzewać gazem/prądem i wpaść do nich w środku zimy żeby &#039;&#039;odczuć&#039;&#039; efekt &ndash;  " class="demot" width="600" height="621"/>
</span>
<script>
                $('.demotivator_inner_video_wrapper video.autoplay:not(.playing)').each(function () {
                $(this).addClass('playing');
                this.play();
        });
</script></div> 
<div class="source">
Źródło: <a href="http://www.bankier.pl/wiadomosc/NSA-nie-mozna-zabronic-palenia-weglem-3414214.html" target="_blank" rel="nofollow">http://www.bankier.pl/wiadomosc/NSA-nie-mozna&#8230;</a> </div>
<div class="like_buttons_box">
<section class="fb_like_button">
<div class="fb-like" data-href="http://demotywatory.pl/4555390/Zakazac-zabronic-jakie-to-proste-Zapraszam-do-domow-ludzi-ktorych-ledwo-stac-na-wegiel-039039Kazac-im039039-ogrzewac-gazem-pradem-i-wpasc-do-nich-w-srodku-zimy-zeby-039039odczuc039039-efekt" data-send="false" data-layout="box_count" data-width="100" data-show-faces="false" data-font="lucida grande" data-colorscheme="dark"></div>
</section>
</div>
<section class="tags">
<ul>
<li><a href="/tag/węgiel">#węgiel</a></li>
<li><a href="/tag/ogrzewanie">#ogrzewanie</a></li>
<li><a href="/tag/piec">#piec</a></li>
<li><a href="/tag/dom">#dom</a></li>
<li><a href="/tag/smog">#smog</a></li>
<li><a href="/tag/ekologia">#ekologia</a></li>
<li><a href="/tag/gaz">#gaz</a></li>
</ul>
</section>
<nav>
<div class="demot_info_stats">
 
<div class="demot_extra_area"></div>
 
<ul>
<li>
<time datetime="26 września 2015 o 14:38">26 września 2015 o 14:38</time>
przez
<a href="/user/MaciekMagik" class="demot-author super-account">
MaciekMagik </a>
</li>
<li>
<a href="http://demotywatory.pl/4555390#comments" class="comment" style="color: red;">Skomentuj (59)</a> </li>
<li>
<a href="/user/add_favorite/4555390" class="favorite">
Do ulubionych
</a>
</li>
</ul>
<br/>
</div> 
</nav>
<div class="true_demotivator"></div>
<div class="admin_menu">
</div> 
</div> 
</article>

""";
        provider = Demotywatory()
        links = provider.parsePage(body)        
        self.assertEqual(links, ['www.demotywatory.pl/uploads/201509/1443340451_iqbq8x_600.jpg'])

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
