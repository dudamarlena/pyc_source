# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-jkXn_D/cherrypy/cherrypy/test/test_httplib.py
# Compiled at: 2018-07-11 18:15:31
"""Tests for cherrypy/lib/httputil.py."""
import unittest
from cherrypy.lib import httputil

class UtilityTests(unittest.TestCase):

    def test_urljoin(self):
        self.assertEqual(httputil.urljoin('/sn/', '/pi/'), '/sn/pi/')
        self.assertEqual(httputil.urljoin('/sn/', '/pi'), '/sn/pi')
        self.assertEqual(httputil.urljoin('/sn/', '/'), '/sn/')
        self.assertEqual(httputil.urljoin('/sn/', ''), '/sn/')
        self.assertEqual(httputil.urljoin('/sn', '/pi/'), '/sn/pi/')
        self.assertEqual(httputil.urljoin('/sn', '/pi'), '/sn/pi')
        self.assertEqual(httputil.urljoin('/sn', '/'), '/sn/')
        self.assertEqual(httputil.urljoin('/sn', ''), '/sn')
        self.assertEqual(httputil.urljoin('/', '/pi/'), '/pi/')
        self.assertEqual(httputil.urljoin('/', '/pi'), '/pi')
        self.assertEqual(httputil.urljoin('/', '/'), '/')
        self.assertEqual(httputil.urljoin('/', ''), '/')
        self.assertEqual(httputil.urljoin('', '/pi/'), '/pi/')
        self.assertEqual(httputil.urljoin('', '/pi'), '/pi')
        self.assertEqual(httputil.urljoin('', '/'), '/')
        self.assertEqual(httputil.urljoin('', ''), '/')


if __name__ == '__main__':
    unittest.main()