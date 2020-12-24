# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/ndg/xacml/core/functions/v2/regexp_match.py
# Compiled at: 2012-03-28 11:41:09
"""NDG XACML 2.0 regular expression matching function module

NERC DataGrid
"""
__author__ = 'P J Kershaw'
__date__ = '26/03/10'
__copyright__ = ''
__license__ = 'BSD - see LICENSE file in top-level directory'
__contact__ = 'Philip.Kershaw@stfc.ac.uk'
__revision__ = '$Id: regexp_match.py 7955 2011-12-21 18:29:45Z rwilkinson $'
from ndg.xacml.core.functions import FunctionClassFactoryBase
from ndg.xacml.core.functions.v1.regexp_match import RegexpMatchBase

class FunctionClassFactory(FunctionClassFactoryBase):
    """Class Factory for *-regexp-match XACML function classes
    
    @cvar FUNCTION_NAMES: regular expression match function URNs
    @type FUNCTION_NAMES: tuple
    
    @cvar FUNCTION_NS_SUFFIX: generic suffix for one and only function URNs
    @type FUNCTION_NS_SUFFIX: string
    
    @cvar FUNCTION_BASE_CLASS: base class for regular expression match function 
    classes 
    @type FUNCTION_BASE_CLASS: ndg.xacml.core.functions.v1.RegexMatchBase
    """
    FUNCTION_NS_SUFFIX = RegexpMatchBase.FUNCTION_NS_SUFFIX
    FUNCTION_BASE_CLASS = RegexpMatchBase
    FUNCTION_NAMES = ('urn:oasis:names:tc:xacml:2.0:function:anyURI-regexp-match',
                      'urn:oasis:names:tc:xacml:2.0:function:ipAddress-regexp-match',
                      'urn:oasis:names:tc:xacml:2.0:function:dnsName-regexp-match',
                      'urn:oasis:names:tc:xacml:2.0:function:rfc822Name-regexp-match',
                      'urn:oasis:names:tc:xacml:2.0:function:x500Name-regexp-match')