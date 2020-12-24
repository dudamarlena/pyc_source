# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/site-packages/bootstrap3_wysihtml5x/tests/fields.py
# Compiled at: 2014-10-27 10:38:43
from __future__ import unicode_literals
from bs4 import BeautifulSoup
from django.forms.models import modelform_factory
from django.forms.widgets import Textarea
from django.test import TestCase as DjangoTestCase
from bootstrap3_wysihtml5x.tests.models import ModelTest
from bootstrap3_wysihtml5x.widgets import Wysihtml5xTextareaWidget

class Wysihtml5xTextFieldTestCase(DjangoTestCase):

    def test_widget_for_wysihtml5textfield_model_field(self):
        form = modelform_factory(ModelTest)()
        first_widget = form.fields.get(b'first_text').widget
        second_widget = form.fields.get(b'second_text').widget
        self.assertEqual(first_widget.__class__, Textarea)
        self.assertEqual(second_widget.__class__, Wysihtml5xTextareaWidget)


class KeepTagsTestCase(DjangoTestCase):

    def setUp(self):
        ModelTest.objects.create(first_text=b'Something not important here', second_text=b'A text with all the tags is coming here<h1>Header 1</h1><h2>Header 2</h2><h3>Header 3</h3><h4>Header 4</h4><h5>Header 5</h5><h6>Header 6</h6><h7>Header 7</h7><div>A DIV Element</div><p>A Paragraph</p><b>A B Element</b><i>An I Element</i><u>An U Element</u><ul>An UL Element<li>And a LI Element</li></ul><ol>An OL Element<li>And a LI Element</li></ol><span>A SPAN element</span><img src="http://blahblahbla.png"><a href="#">An Anchor Element</a><blockquote>Quoting a quote!</blockquote><script>alert("this should not stay!")</script><h7>A H7 header?</h7>')
        self.obj = ModelTest.objects.get(pk=1)

    def test_keeptags_keep_the_allowed_tags(self):
        soup = BeautifulSoup(self.obj.second_text)
        self.assert_(soup.find(b'h1') != None)
        self.assert_(soup.find(b'h2') != None)
        self.assert_(soup.find(b'h3') != None)
        self.assert_(soup.find(b'h4') != None)
        self.assert_(soup.find(b'h5') != None)
        self.assert_(soup.find(b'h6') != None)
        self.assert_(soup.find(b'div') != None)
        self.assert_(soup.find(b'p') != None)
        self.assert_(soup.find(b'b') != None)
        self.assert_(soup.find(b'i') != None)
        self.assert_(soup.find(b'u') != None)
        self.assert_(soup.find(b'ul') != None)
        self.assert_(soup.find(b'ol') != None)
        self.assert_(soup.find(b'span') != None)
        self.assert_(soup.find(b'img') != None)
        self.assert_(soup.find(b'a') != None)
        self.assert_(soup.find(b'blockquote') != None)
        return

    def test_keeptags_removes_not_specified_tags(self):
        soup = BeautifulSoup(self.obj.second_text)
        self.assert_(soup.find(b'script') == None)
        self.assert_(soup.find(b'h7') == None)
        return