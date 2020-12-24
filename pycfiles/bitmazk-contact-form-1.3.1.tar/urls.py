# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Tyrdall/projects/bitmazk-contact-form/src/contact_form/urls.py
# Compiled at: 2016-04-11 01:56:11
"""URLs for bitmazk-contact-form application."""
from django.conf.urls import url
from .views import ContactFormView
urlpatterns = [
 url('^', ContactFormView.as_view(), name='contact_form')]