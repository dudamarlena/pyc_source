# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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