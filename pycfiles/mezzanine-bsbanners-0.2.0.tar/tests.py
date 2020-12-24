# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/home/alan/projects/po/mezzanine_bsbanners/tests.py
# Compiled at: 2017-05-28 12:13:46
"""
Mezzanine BS Banners
Making it easier to manage attention grabbing and compelling banners
"""
from __future__ import unicode_literals
from django.test import TestCase
from django.template import Template, Context, TemplateSyntaxError
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from mezzanine_bsbanners.models import Banners, Slides

class BSBannersTestCase(TestCase):
    """
    Class to test mezzanine_bsbanners
    """

    def setUp(self):
        """
        Setup test
        """
        Banners.objects.create(title=b'Home')
        Banners.objects.create(title=b'Home Carousel', bannertype=1)
        jumbo = Banners.objects.create(title=b'Home Jumbotron', bannertype=2)
        Slides.objects.create(banner_id=jumbo.id, title=b'Jumbotrons are GREAT!', content=b'<p>Bootstrap Jumbotrons are great headline grabbers</p>', cta=b'Get one today', link_url=b'http://p-o.co.uk/', buttontype=b'default')

    def test_banner_has_good_slug(self):
        """Banners should have the correct slugs"""
        homebanner = Banners.objects.get(title=b'Home')
        homecarousel = Banners.objects.get(title=b'Home Carousel')
        homejumbo = Banners.objects.get(title=b'Home Jumbotron')
        self.assertEqual(homebanner.title, b'Home')
        self.assertEqual(homebanner.slug, b'home')
        self.assertEqual(homecarousel.title, b'Home Carousel')
        self.assertEqual(homecarousel.slug, b'home-carousel')
        self.assertEqual(homejumbo.title, b'Home Jumbotron')
        self.assertEqual(homejumbo.slug, b'home-jumbotron')

    def test_get_carousel_bsbanner(self):
        """
        Test carousel rendering
        """
        out = Template(b'{% load bsbanners_tags %}{% bsbanner "home" %}').render(Context())
        pagedat = b'\n\n\n<script type=\'text/javascript\'>\nwindow.setTimeout(function()\n{\n    // Prepare the carousel\n    var carousel7options = {\n        interval: 5000,\n        pause: "hover",\n        wrap: true,\n    }\n    jQuery(\'#home-carousel .carousel-caption\').hide();\n    jQuery(\'#home-carousel .active .carousel-caption\').show();\n    // Activate the carousel\n    jQuery(\'.carousel\').carousel(carousel7options);\n\n    // Set the carousel animations\n    jQuery(\'.carousel\').on(\'slide.bs.carousel\', function() {\n        jQuery(\'#home-carousel .active .carousel-caption\').slideUp(500);\n    });\n    jQuery(\'.carousel\').on(\'slid.bs.carousel\', function() {\n        jQuery(\'#home-carousel .active .carousel-caption\').slideDown(300);\n    });\n\n}, 5000);\n</script>\n\n\n<!-- Carousel\n================================================== -->\n<div id=\'home-carousel\' class="carousel slide">\n    <div class="carousel-inner">\n    \n    </div>\n    <a class="left carousel-control" href="#home-carousel" data-slide="prev">&lsaquo;</a>\n    <a class="right carousel-control" href="#home-carousel" data-slide="next">&rsaquo;</a>\n    \n    <ul class="carousel-indicators">\n    \n    </ul>\n    \n</div><!-- /.carousel -->\n\n\n'
        self.assertEqual(out, pagedat)

    def test_get_jumbotron_bsbanner(self):
        """
        Test jumbotron rendering
        """
        out = Template(b'{% load bsbanners_tags %}{% bsbanner "home-jumbotron" %}').render(Context())
        pagedat = b'\n\n\n<div id=\'home-jumbotron-jumbotron\' class="jumbotron">\n    <div class="container">\n    \n        <div>\n        \n            <h1>Jumbotrons are GREAT!</h1>\n        \n        <p>Bootstrap Jumbotrons are great headline grabbers</p>\n        \n            \n            <a class="btn btn-default"\n                href="http://p-o.co.uk/">\n            \n            \n            Get one today\n            \n            \n            </a>\n            \n        \n        </div>\n    \n    </div>\n</div>\n\n\n'
        self.assertEqual(out, pagedat)

    def test_banner_found_failures(self):
        """
        Non existent banners should barf as well as too many
        """
        self.assertRaises(MultipleObjectsReturned, Banners.objects.get)
        self.assertRaises(ObjectDoesNotExist, Banners.objects.get, title=b'zzz')
        self.assertRaisesMessage(ObjectDoesNotExist, b'Banners matching query does not exist.', Banners.objects.get, title=b'azerty')

    def test_parsing_errors(self):
        """Parsing variation on template"""
        render = lambda t: Template(t).render(Context())
        self.assertRaises(TemplateSyntaxError, render, b'{% load bsbanners_tags %}{% bsbanner %}')
        self.assertRaises(TemplateSyntaxError, render, b"{% load bsbanners_tags %}{% bsbanner 'one' 'two' 'three' %}")
        self.assertRaises(TemplateSyntaxError, render, b'{% load bsbanners_tags %}{% bsbanner one two three four five %}')