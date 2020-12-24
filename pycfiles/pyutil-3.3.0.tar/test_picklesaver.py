# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/user/code/pyutil/pyutil/test/deprecated/test_picklesaver.py
# Compiled at: 2018-01-06 14:43:43
import os
try:
    from twisted.trial import unittest
except ImportError as le:
    print 'Skipping %s since it requires Twisted and Twisted could not be imported: %s' % (__name__, le)
else:
    from pyutil import PickleSaver, fileutil

    class Thingie(PickleSaver.PickleSaver):

        def __init__(self, fname, delay=30):
            PickleSaver.PickleSaver.__init__(self, fname=fname, attrs={'tmp_store': 'False'}, DELAY=delay)


    class PickleSaverTest(unittest.TestCase):

        def _test_save_now(self, fname):
            thingie = Thingie(fname, delay=0)
            thingie.tmp_store = 'True'
            thingie.lazy_save()

        def test_save_now(self):
            """
            This test should create a lazy save object, save it with no delay and check if the file exists.
            """
            tempdir = fileutil.NamedTemporaryDirectory()
            fname = os.path.join(tempdir.name, 'picklesavertest')
            self._test_save_now(fname)
            self.failUnless(os.path.isfile(fname), 'The file [%s] does not exist.' % (fname,))
            tempdir.shutdown()