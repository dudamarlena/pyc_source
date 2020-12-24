# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/tw/lymon/layout.py
# Compiled at: 2008-07-04 08:03:19
from lymon.core import Document
from lymon.tw import Site
from tw.api import CSSLink
__all__ = ['LymonSite', 'template']
style_template = CSSLink(modname=__name__, filename='static/css/layout/style.css')
template = Document()
template.div(slot='content', id=False, attrs={'class': 'content'})
template.div(slot='content.top', id=False, attrs={'class': 'header'})
template.div(slot='content.top.info', id=False, attrs={'class': 'top_info'})
template.div(slot='content.top.info.right', id=False, attrs={'class': 'top_info_right'})
html_text = '<p><b>Login slot at:</b> content.top.info.right<br/>\n<b>CSS Class:</b> top_info_right</p>'
template.div(slot='content.top.info.right.text', id=False, attrs={'class': 'top_info_right'}, html=html_text)
html_text = '<p><b>Header in:</b> content.top.info.left.text<br /><b>CSS Class:</b> top_info_left</p>'
template.div(slot='content.top.info.left.text', id=False, attrs={'class': 'top_info_left'}, html=html_text)
template.div(slot='content.top.logo', id=False, attrs={'class': 'logo'})
template.h1(slot='content.top.logo.title', id=False)
html_text = '<span class="dark">Ly</span>mon Project'
template.a(slot='content.top.logo.title.link', id=False, attrs={'href': 'http://code.google.com/p/lymon/'}, html=html_text)
html_text = '\n<ul>\n\t<li class="active">Menu item 1</li>\n\t<li><a href="#" accesskey="m">Menu item 2</a></li>\n\n</ul>\n'
template.div(slot='content.bar', id=False, attrs={'class': 'bar'}, html=html_text)
html_text = '\n\t\t\t<form method="post" action="?">\n\t\t\t\t<div class="search_form">\n\t\t\t\t<p>Search: <input type="text" name="search" class="search" /> <input type="submit" value="Search" class="submit" /> <a class="grey" href="#">Advanced</a></p>\n\t\t\t\t</div>\n\n\t\t\t</form>\n\t\t\t<p>Search at: content.search<br/>CSS Class: search_field</p>\n'
template.div(slot='content.search', id=False, attrs={'class': 'search_field'}, html=html_text)
template.div(slot='content.left', id=False, attrs={'class': 'left'})
html_text = 'Box at: content.left.box (h3)'
template.div(slot='content.right', id=False, attrs={'class': 'right'})
html_text = 'Right menu at: content.right (h3)'
template.h3(slot='content.right.title', id=False, html=html_text)
html_text = '<p>Cuadro de mensajes y alertas, en construccion por el momento</p>'
template.div(slot='content.right.right_articles_1', id=False, attrs={'class': 'right_articles'}, html=html_text)
html_text = '\n<p> &copy; Copyright 2008 Laureano Arcanio<br />\nPowered by <a href="http://code.google.com/p/lymon/">Lymon</a></p>\n'
template.div(slot='content.footer', id=False, attrs={'class': 'footer'}, html=html_text)

class LymonSite(Site):
    css = [
     style_template]