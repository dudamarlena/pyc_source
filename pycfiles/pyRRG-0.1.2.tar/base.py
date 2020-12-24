# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\pyrrd\testing\base.py
# Compiled at: 2013-08-12 02:05:53
import tempfile
from unittest import TestCase
from pyrrd.backend.external import create

class RRDBaseTestCase(TestCase):

    def setUp(self):
        self.rrdfile = tempfile.NamedTemporaryFile()
        self.filename = self.rrdfile.name
        parameters = '--start 920804400 DS:speed:COUNTER:600:-10.1:10.3 RRA:AVERAGE:0.5:1:24 RRA:AVERAGE:0.5:6:10'
        create(self.filename, parameters)