# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/funkload/demo/simple/test_Simple.py
# Compiled at: 2015-05-06 05:03:08
"""Simple FunkLoad test

$Id$
"""
import unittest
from random import random
from funkload.FunkLoadTestCase import FunkLoadTestCase

class Simple(FunkLoadTestCase):
    """This test use a configuration file Simple.conf."""

    def setUp(self):
        """Setting up test."""
        self.server_url = self.conf_get('main', 'url')

    def test_simple(self):
        server_url = self.server_url
        nb_time = self.conf_getInt('test_simple', 'nb_time')
        for i in range(nb_time):
            self.get(server_url, description='Get URL')


if __name__ in ('main', '__main__'):
    unittest.main()