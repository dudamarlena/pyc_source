# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/kyle/git/flask-xxl/flask_xxl/apps/page/urls.py
# Compiled at: 2018-06-20 18:52:33
from . import page
from .views import ContactFormView, PageSlugView, PagesView, AddPageView
routes = [
 (
  page,
  (
   '/', 'page_list', PagesView),
  (
   '/<slug>', 'page', PageSlugView),
  (
   '/add_page', 'add_page', AddPageView),
  (
   '/contact-us', 'contact_us', ContactFormView))]