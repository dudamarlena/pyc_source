# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/asc/contrib/music/importer.py
# Compiled at: 2011-02-15 01:26:38
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from asc.parser import Parser

class Importer(object):

    def __init__(self):
        try:
            self.url = settings.ASC_URL
        except AttributeError:
            raise ImproperlyConfigured('No ASC_URL setting found.')

    def run(self):
        return Parser(self.url).tracks