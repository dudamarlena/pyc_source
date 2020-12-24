# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/nowandnext_tests/caltestcase.py
# Compiled at: 2009-05-11 19:02:40
import unittest, ConfigParser
from nowandnext.calendar.calQuery import CalQuery
from nowandnext.applications.pinger import pinger

class caltestcase(unittest.TestCase):

    def setUp(self):
        configpath = pinger.getConfigFileLocation(pinger.CONFIG_FILE_NAME)
        self._config = pinger.loadConfig(configpath)
        self._calargs = (
         self._config.get('pinger', 'account'),
         self._config.get('pinger', 'password'),
         self._config.get('pinger', 'calendar_name'))
        self._cal = foo = CalQuery(*self._calargs)

    def tearDown(self):
        del self._cal