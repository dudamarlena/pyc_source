# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/ndg/xacml/test/context/test_pdp_faam.py
# Compiled at: 2012-02-10 11:35:18
"""
Created on 31 Aug 2011

@author: rwilkinson
"""
import logging, os.path, time, unittest
from ndg.xacml.parsers.etree.factory import ReaderFactory
from ndg.xacml.core.context.pdp import PDP
from ndg.xacml.core.context.result import Decision
from ndg.xacml.test import THIS_DIR
from ndg.xacml.test.context import XacmlContextBaseTestCase
logging.basicConfig(level=logging.ERROR)

class Test(XacmlContextBaseTestCase):
    """Tests for FAAM policy.
    """
    RESOURCE_B555_ID = 'http://localhost/download/badc/faam/data/2010/b555-sep-15/core_raw/b555_raw_data.dat'
    XACML_FAAM_FILENAME = 'policy_faam.xml'
    XACML_FILEPATH = os.path.join(THIS_DIR, XACML_FAAM_FILENAME)

    def setUp(self):
        print 'Setting up'
        self.pdp = PDP.fromPolicySource(self.__class__.XACML_FILEPATH, ReaderFactory)
        print 'Setup complete'

    def test01(self):
        request = self._createRequestCtx(self.__class__.RESOURCE_B555_ID, subjectRoles=('faam_admin', ))
        print 'Starting request'
        start_time = time.time()
        response = self.pdp.evaluate(request)
        print 'Response received after %fs' % (time.time() - start_time)
        self.failIf(response is None, 'Null response')
        for result in response.results:
            self.failIf(result.decision != Decision.PERMIT, 'Expecting Permit decision')

        return

    def test02(self):
        request = self._createRequestCtx(self.__class__.RESOURCE_B555_ID, subjectRoles=('group1', ))
        print 'Starting request'
        start_time = time.time()
        response = self.pdp.evaluate(request)
        print 'Response received after %fs' % (time.time() - start_time)
        self.failIf(response is None, 'Null response')
        for result in response.results:
            self.failIf(result.decision != Decision.DENY, 'Expecting Deny decision')

        return

    def test03(self):
        request = self._createRequestCtx(self.__class__.RESOURCE_B555_ID, subjectRoles=('faam_admin', ))
        print 'Starting request'
        start_time = time.time()
        response = self.pdp.evaluate(request)
        print 'Response received after %fs' % (time.time() - start_time)
        self.failIf(response is None, 'Null response')
        for result in response.results:
            self.failIf(result.decision != Decision.PERMIT, 'Expecting Permit decision')

        return


if __name__ == '__main__':
    unittest.main()