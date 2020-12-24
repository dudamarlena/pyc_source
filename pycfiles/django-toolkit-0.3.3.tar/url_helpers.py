# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /media/ahayes/data/.workspaces/juno/django-toolkit/django_toolkit/tests/templatetags/url_helpers.py
# Compiled at: 2015-07-07 21:04:55
from django.utils import unittest
from django_toolkit.templatetags.url_helpers import shorten_url, netloc_no_www
from django_toolkit.tests.url.shorten import ShortenUrlTestCase, NetlocNoWwwTestCase

class ShortenUrlTemplateTagTestCases(ShortenUrlTestCase):

    @property
    def shorten_url(self):
        return shorten_url


class NetlocNoWwwTemplateTagTestCase(NetlocNoWwwTestCase):

    @property
    def netloc_no_www(self):
        return netloc_no_www