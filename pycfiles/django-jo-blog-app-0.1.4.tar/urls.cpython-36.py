# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/maluki/blog/django_blog/blog_project/contact/urls.py
# Compiled at: 2019-07-25 09:24:04
# Size of source mod 2**32: 191 bytes
from django.urls import path
from contact.views import ContactView
app_name = 'contact'
urlpatterns = [
 path('contact/', (ContactView.as_view()), name='contact')]