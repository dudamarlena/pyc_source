# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/netlogger/tests/component/testParseSgeRpt.py
# Compiled at: 2009-12-08 17:43:28
"""
Unittests for sge_rpt.py
"""
__author__ = 'Dan Gunter dkgunter@lbl.gov'
__rcsid__ = '$Id: testParseSgeRpt.py 23798 2009-07-14 17:18:22Z dang $'
from netlogger.tests import shared
import unittest
from netlogger.parsers.modules import sge_rpt
from netlogger.parsers.base import NLFastParser

class TestCase(shared.BaseParserTestCase):
    basename = 'sge_rpt-'
    parser_class = sge_rpt.Parser

    def __init__(self, *args, **kw):
        shared.BaseParserTestCase.__init__(self, *args, **kw)
        self._p = NLFastParser()

    def testBasic(self):
        """Parse all events
        """
        self.checkGood('basic.log', num_expected=33, parser_kw={'host_consumable': True, 'hc_one': False})
        self.checkGood('basic.log', num_expected=6, parser_kw={'job_log': True})

    def testHostConsumable(self):
        """Correctly parsed host_consumable values.
        """

        def _check(e, num):
            self.debug_('event %d => %s' % (num, e['event']))
            self.failUnless(e['event'] == 'sge.rpt.hc')
            host = e['host']
            if host == 'global':
                for rsrc in ('snapidl', 'scpidl', 'dv13io', 'dv34io', 'dv37io', 'dv38io',
                             'dv39io', 'dv42io', 'dv43io', 'dv61io', 'dv71io', 'dv0302io',
                             'dv0308io', 'danteio', 'eliza1io', 'eliza2io', 'eliza3io',
                             'eliza5io', 'eliza6io', 'eliza11io', 'eliza12io', 'eliza13io',
                             'projectio', 'hpssio', 'eliza4io', 'eliza7io', 'eliza8io',
                             'eliza9io', 'snapidl', 'scpidl', 'dv13io', 'dv34io',
                             'dv37io', 'dv38io', 'dv39io', 'dv42io', 'dv43io', 'dv61io',
                             'dv71io', 'dv0302io', 'dv0308io', 'danteio', 'eliza1io',
                             'eliza2io', 'eliza3io', 'eliza5io', 'eliza6io', 'eliza11io',
                             'eliza12io', 'eliza13io', 'projectio', 'hpssio', 'eliza4io',
                             'eliza7io', 'eliza8io', 'eliza9io'):
                    self.failUnless(e.has_key(rsrc), 'Missing %s resource: %s' % (host, rsrc))
                    self.failUnless(e.has_key(rsrc + sge_rpt.MAX_SFX))

            else:
                self.failUnless(host.startswith('pc'), 'Bad host: %s' % host)
            for rsrc in ('jobslots', ):
                self.failUnless(e.has_key(rsrc), 'Missing %s resource: %s' % (host, rsrc))
                self.failUnless(e.has_key(rsrc + sge_rpt.MAX_SFX))

        self.checkGood('hc.log', num_expected=2, parser_kw={'host_consumable': True})
        self.checkGood('hc.log', num_expected=56, parser_kw={'host_consumable': True, 'hc_one': False})
        self.checkGood('hc.log', num_expected=29, parser_kw={'host_consumable': True, 'hc_one': False, 'hc_delta': True})
        self.checkGood('hc.log', num_expected=4, parser_kw={'host_consumable': True, 'hc_perhost': True}, test=_check)

    def testJobLog(self):
        """Correctly parsed job_log values.
        """

        def _check(e, num):
            self.debug_('event %d => %s' % (num, e['event']))
            if num == 0:
                self.failUnless(e['state'] == 'pending')
            elif num == 1:
                self.failUnless(e['state'] == 'sent')
            elif num == 2:
                self.failUnless(e['state'] == 'delivered')
            elif num == 3:
                self.failUnless(e['state'] == 'finished')
                self.failUnless(e['host'] == 'pc2211.nersc.gov')
            elif num == 4:
                self.failUnless(e['state'] == 'deleting')
            elif num == 5:
                self.failUnless(e['state'] == 'deleted')
            if num > 0 and num != 3:
                self.failUnless(e['host'] == 'pc2533.nersc.gov')
            self.failUnless(e['user'] == 'jmatykie')
            self.failUnless(e['group'] == 'rhstar')

        self.checkGood('basic.log', num_expected=6, parser_kw={'job_log': True}, test=_check)


def suite():
    return shared.suite(TestCase)


if __name__ == '__main__':
    shared.main()