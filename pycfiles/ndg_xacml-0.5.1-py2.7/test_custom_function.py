# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/ndg/xacml/test/functions/test_custom_function.py
# Compiled at: 2012-06-19 10:10:37
"""NDG XACML tests for custom function

NERC DataGrid
"""
__author__ = 'R B Wilkinson'
__date__ = '14/03/12'
__copyright__ = ''
__license__ = 'BSD - see LICENSE file in top-level directory'
__contact__ = 'Philip.Kershaw@stfc.ac.uk'
__revision__ = '$Id: test_custom_function.py 8078 2012-06-19 14:10:35Z pjkersha $'
import logging
from os import path
import unittest, hashlib, urllib
from ndg.xacml.core.attributevalue import AttributeValueClassFactory
from ndg.xacml.core.context.exceptions import XacmlContextTypeError
from ndg.xacml.core.functions import AbstractFunction, FunctionClassFactoryBase, functionMap
from ndg.xacml.core.context.pdp import PDP
from ndg.xacml.core.context.result import Decision
from ndg.xacml.parsers.etree.factory import ReaderFactory
from ndg.xacml.test.context import XacmlContextBaseTestCase
logging.basicConfig(level=logging.DEBUG)
THIS_DIR = path.dirname(__file__)
XACML_CUSTOM_FUNCTION_TEST_FILEPATH = path.join(THIS_DIR, 'policy_custom_function.xml')
attributeValueClassFactory = AttributeValueClassFactory()

class Md5HexBase(AbstractFunction):
    FUNCTION_NS = None
    TYPE = attributeValueClassFactory('http://www.w3.org/2001/XMLSchema#string')
    RETURN_TYPE = attributeValueClassFactory('http://www.w3.org/2001/XMLSchema#string')

    def evaluate(self, arg):
        """URL encodes a value
        
        @param arg: 
        @type arg: str
        @return: URL encoded value
        @rtype: str
        @raise XacmlContextTypeError: incorrect type for input
        """
        if not isinstance(arg, self.__class__.TYPE):
            raise XacmlContextTypeError('Expecting type %r for argument; got %r' % (
             self.__class__.TYPE,
             type(arg)))
        result = hashlib.md5(arg.value).hexdigest()
        return self.__class__.RETURN_TYPE(result)


class Md5HexFunctionClassFactory(FunctionClassFactoryBase):
    """Class Factory for *-md5hex XACML custom function classes

    @cvar FUNCTION_NAMES: function URNs
    @type FUNCTION_NAMES: tuple

    @cvar FUNCTION_NS_SUFFIX: generic suffix for md5hex function URNs
    @type FUNCTION_NS_SUFFIX: string

    @cvar FUNCTION_BASE_CLASS: base class for all md5hex classes
    @type FUNCTION_BASE_CLASS: type
    """
    FUNCTION_NAMES = ('urn:ndg:xacml:2.0:function:string-md5hex', 'urn:ndg:xacml:2.0:function:anyURI-md5hex')
    FUNCTION_NS_SUFFIX = '-md5hex'
    FUNCTION_BASE_CLASS = Md5HexBase


class UrlencodeBase(AbstractFunction):
    FUNCTION_NS = None
    TYPE = attributeValueClassFactory('http://www.w3.org/2001/XMLSchema#string')
    RETURN_TYPE = attributeValueClassFactory('http://www.w3.org/2001/XMLSchema#string')

    def evaluate(self, arg):
        """URL encodes a value
        
        @param arg: 
        @type arg: str
        @return: URL encoded value
        @rtype: str
        @raise XacmlContextTypeError: incorrect type for input
        """
        if not isinstance(arg, self.__class__.TYPE):
            raise XacmlContextTypeError('Expecting type %r for argument; got %r' % (
             self.__class__.TYPE,
             type(arg)))
        result = urllib.quote_plus(arg.value)
        return self.__class__.RETURN_TYPE(result)


class UrlencodeFunctionClassFactory(FunctionClassFactoryBase):
    """Class Factory for *-urlencode XACML custom function classes

    @cvar FUNCTION_NAMES: function URNs
    @type FUNCTION_NAMES: tuple

    @cvar FUNCTION_NS_SUFFIX: generic suffix for urlencode function URNs
    @type FUNCTION_NS_SUFFIX: string

    @cvar FUNCTION_BASE_CLASS: base class for all urlencode classes
    @type FUNCTION_BASE_CLASS: type
    """
    FUNCTION_NAMES = ('urn:ndg:xacml:2.0:function:string-urlencode', 'urn:ndg:xacml:2.0:function:anyURI-urlencode')
    FUNCTION_NS_SUFFIX = '-urlencode'
    FUNCTION_BASE_CLASS = UrlencodeBase


def addXacmlEncodeFunctions():
    """Add functions to encode values for, e.g., constructing paths from
    subject IDs.
    """
    for name in Md5HexFunctionClassFactory.FUNCTION_NAMES:
        functionMap.load_custom_function(name, Md5HexFunctionClassFactory())

    for name in UrlencodeFunctionClassFactory.FUNCTION_NAMES:
        functionMap.load_custom_function(name, UrlencodeFunctionClassFactory())


class Test(XacmlContextBaseTestCase):
    RESOURCE1_ID = 'http://localhost/resource1'
    RESOURCE2_ID = 'http://localhost/resource2'
    RESOURCE3_ID = 'http://localhost/resource3'
    RESOURCE4_ID = 'http://localhost/resource4'
    RESOURCE5_ID = 'http://localhost/resource5'
    RESOURCE6_ID = 'http://localhost/resource6'
    RESOURCE7_ID = 'http://localhost/resource7'
    RESOURCE8_ID = 'http://localhost/resource8'

    def setUp(self):
        addXacmlEncodeFunctions()

    def test01_01StringUrlencode(self):
        """Test URL encoding of a string value resulting in a permit decision.
        """
        self.pdp = PDP.fromPolicySource(XACML_CUSTOM_FUNCTION_TEST_FILEPATH, ReaderFactory)
        request = self._createRequestCtx(self.__class__.RESOURCE1_ID, subjectRoles=('role1', ))
        response = self.pdp.evaluate(request)
        self.failIf(response is None, 'Null response')
        for result in response.results:
            self.failIf(result.decision != Decision.PERMIT, 'Expecting Permit decision')

        return

    def test01_02StringUrlencode(self):
        """Test URL encoding of a string value resulting in a deny decision.
        """
        self.pdp = PDP.fromPolicySource(XACML_CUSTOM_FUNCTION_TEST_FILEPATH, ReaderFactory)
        request = self._createRequestCtx(self.__class__.RESOURCE2_ID, subjectRoles=('role1', ))
        response = self.pdp.evaluate(request)
        self.failIf(response is None, 'Null response')
        for result in response.results:
            self.failIf(result.decision != Decision.DENY, 'Expecting Deny decision')

        return

    def test02_01AnyUriUrlencode(self):
        """Test URL encoding of a URI value resulting in a permit decision.
        """
        self.pdp = PDP.fromPolicySource(XACML_CUSTOM_FUNCTION_TEST_FILEPATH, ReaderFactory)
        request = self._createRequestCtx(self.__class__.RESOURCE3_ID, subjectRoles=('role1', ))
        response = self.pdp.evaluate(request)
        self.failIf(response is None, 'Null response')
        for result in response.results:
            self.failIf(result.decision != Decision.PERMIT, 'Expecting Permit decision')

        return

    def test02_02AnyUriUrlencode(self):
        """Test URL encoding of a URI value resulting in a deny decision.
        """
        self.pdp = PDP.fromPolicySource(XACML_CUSTOM_FUNCTION_TEST_FILEPATH, ReaderFactory)
        request = self._createRequestCtx(self.__class__.RESOURCE4_ID, subjectRoles=('role1', ))
        response = self.pdp.evaluate(request)
        self.failIf(response is None, 'Null response')
        for result in response.results:
            self.failIf(result.decision != Decision.DENY, 'Expecting Deny decision')

        return

    def test03_01StringMd5hex(self):
        """Test MD5 hex encoding of a string value resulting in a permit
        decision.
        """
        self.pdp = PDP.fromPolicySource(XACML_CUSTOM_FUNCTION_TEST_FILEPATH, ReaderFactory)
        request = self._createRequestCtx(self.__class__.RESOURCE5_ID, subjectRoles=('role1', ))
        response = self.pdp.evaluate(request)
        self.failIf(response is None, 'Null response')
        for result in response.results:
            self.failIf(result.decision != Decision.PERMIT, 'Expecting Permit decision')

        return

    def test03_02StringMd5hex(self):
        """Test MD5 hex encoding of a string value resulting in a deny
        decision.
        """
        self.pdp = PDP.fromPolicySource(XACML_CUSTOM_FUNCTION_TEST_FILEPATH, ReaderFactory)
        request = self._createRequestCtx(self.__class__.RESOURCE6_ID, subjectRoles=('role1', ))
        response = self.pdp.evaluate(request)
        self.failIf(response is None, 'Null response')
        for result in response.results:
            self.failIf(result.decision != Decision.DENY, 'Expecting Deny decision')

        return

    def test04_01AnyUriMd5hex(self):
        """Test MD5 hex encoding of a URI value resulting in a permit
        decision.
        """
        self.pdp = PDP.fromPolicySource(XACML_CUSTOM_FUNCTION_TEST_FILEPATH, ReaderFactory)
        request = self._createRequestCtx(self.__class__.RESOURCE7_ID, subjectRoles=('role1', ))
        response = self.pdp.evaluate(request)
        self.failIf(response is None, 'Null response')
        for result in response.results:
            self.failIf(result.decision != Decision.PERMIT, 'Expecting Permit decision')

        return

    def test04_02AnyUriMd5hex(self):
        """Test MD5 hex encoding of a URI value resulting in a deny
        decision.
        """
        self.pdp = PDP.fromPolicySource(XACML_CUSTOM_FUNCTION_TEST_FILEPATH, ReaderFactory)
        request = self._createRequestCtx(self.__class__.RESOURCE8_ID, subjectRoles=('role1', ))
        response = self.pdp.evaluate(request)
        self.failIf(response is None, 'Null response')
        for result in response.results:
            self.failIf(result.decision != Decision.DENY, 'Expecting Deny decision')

        return


if __name__ == '__main__':
    unittest.main()