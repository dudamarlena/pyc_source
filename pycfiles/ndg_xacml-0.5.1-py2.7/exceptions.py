# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/ndg/xacml/core/context/exceptions.py
# Compiled at: 2011-02-11 08:34:12
"""NDG XACML exception types for the context package

NERC DataGrid
"""
__author__ = 'P J Kershaw'
__date__ = '01/04/10'
__copyright__ = '(C) 2010 Science and Technology Facilities Council'
__contact__ = 'Philip.Kershaw@stfc.ac.uk'
__license__ = 'BSD - see LICENSE file in top-level directory'
__contact__ = 'Philip.Kershaw@stfc.ac.uk'
__revision__ = '$Id: exceptions.py 7087 2010-06-25 11:23:09Z pjkersha $'
from ndg.xacml.core.context.response import Response
from ndg.xacml.core.context.result import Result, Decision, StatusCode

class XacmlContextError(Exception):
    """Base class for exceptions related XACML context handling
    
    @ivar __response: Context response object associated with this exception
    @type __response: ndg.xacml.core.context.response.Response
    """

    def __init__(self, *arg, **kw):
        """Override Exception base class so as to add the response object in
        the exception instance
        
        @param arg: base class arguments
        @type arg: tuple
        @param kw: base class keywords if any
        @type kw: dict
        """
        super(XacmlContextError, self).__init__(*arg, **kw)
        self.__response = Response()
        self.__response.results.append(Result.createInitialised())
        self.__response.results[0].decision = Decision.INDETERMINATE
        if len(arg) > 0:
            self.__response.results[0].status.statusMessage = arg[0]

    @property
    def response(self):
        """
        @return: Context response object associated with this exception
        @rtype: ndg.xacml.core.context.response.Response
        """
        return self.__response

    @response.setter
    def response(self, value):
        if not isinstance(value, Response):
            raise TypeError('Expecting %r type for "response" attribute; got %r instead' % (
             Response, type(Response)))
        self.__response = value


class XacmlContextTypeError(XacmlContextError):
    """Type errors within XACML context processing"""
    pass


class MissingAttributeError(XacmlContextError):
    """AttributeDesignator or AttributeSelector has specified MustBePresent
    but the request context contains no match for required attribute XPath
    respectively
    """
    pass