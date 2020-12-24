# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-jkXn_D/cherrypy/cherrypy/test/test_compat.py
# Compiled at: 2018-07-11 18:15:31
import unittest, nose
from cherrypy import _cpcompat as compat

class StringTester(unittest.TestCase):

    def test_ntob_non_native(self):
        """
        ntob should raise an Exception on unicode.
        (Python 2 only)

        See #1132 for discussion.
        """
        if compat.py3k:
            raise nose.SkipTest('Only useful on Python 2')
        self.assertRaises(Exception, compat.ntob, unicode('fight'))