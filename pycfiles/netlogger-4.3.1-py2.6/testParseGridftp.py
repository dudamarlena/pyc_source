# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/netlogger/tests/unit/testParseGridftp.py
# Compiled at: 2009-12-08 17:43:28
"""
Unittests for gridfp "info" event parser
"""
__author__ = 'Dan Gunter dkgunter@lbl.gov'
__rcsid__ = '$Id: testParseGridftp.py 23974 2009-10-20 12:57:44Z dang $'
import logging, os, sys, unittest
from netlogger.parsers.modules import gridftp
from netlogger.tests import shared
_opj = os.path.join

class TestCase(shared.BaseTestCase):

    def setUp(self):
        log = logging.getLogger('netlogger.parsers.modules.gridftp')
        if self.DEBUG > 0:
            log.addHandler(logging.StreamHandler())
        else:
            log.addHandler(logging.StreamHandler(file('/dev/null', 'w')))
        self.crazy_us = _opj(self.data_dir, 'gridftp.crazy_us')
        self.junky = _opj(self.data_dir, 'gridftp.junky')

    def testCrazyMicroseconds(self):
        """Non-zero-padded microseconds in date
        """
        infile = file(self.crazy_us)
        parser = gridftp.Parser(infile, one_event=True)
        for line in infile:
            line = line.strip()
            result = parser.process(line)
            self.failUnless(result, 'Could not parse: %s' % line)
            data = result[0]
            dur, nbytes = data['dur'], data['nbytes']
            self.failUnless(dur > 0, 'Non-positive duration: %s' % line)
            mbits = 8 * nbytes / 1000000.0 / dur
            self.failUnless(mbits < 10000, 'Duration too small (%lf): %s' % (
             dur, line))

    def testJunk(self):
        """Raise exceptions, don't die, on bad input
        """
        infile = file(self.junky)
        parser = gridftp.Parser(infile)
        for line in infile:
            line = line.strip()
            try:
                result = parser.process(line)
            except (ValueError, KeyError), E:
                self.debug_('Junk detected: %s' % line)


def suite():
    return shared.suite(TestCase)


if __name__ == '__main__':
    shared.main()