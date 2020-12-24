# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/tests/test_suite.py
# Compiled at: 2012-03-24 03:53:24
from pywidl.pywidl import App
import unittest
from difflib import context_diff
import os, sys

class TestPyWIdl(unittest.TestCase):

    def _match(self, fromfile, tofile):
        diff = context_diff(open(fromfile).readlines(), open(tofile).readlines(), fromfile=fromfile, tofile=tofile)
        diff_clean = True
        for line in diff:
            if diff_clean:
                print
            diff_clean = False
            sys.stdout.write(line)

        if diff_clean:
            os.remove(tofile)
        return diff_clean

    def _buildDom(self, source):
        src = os.path.join('tests', 'data', source)
        eta = os.path.join('tests', 'data', '%s.eta' % source)
        rcv = os.path.join('tests', 'received.idl')
        app = App(src, rcv, 'tests.idl', App.NATIVE_TEMPLATE)
        app.run()
        self.assertTrue(self._match(eta, rcv))

    def test_data(self):
        for idl in os.listdir(os.path.join('tests', 'data')):
            if idl.endswith('.idl'):
                self._buildDom(idl)


if __name__ == '__main__':
    unittest.main()