# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/ndg/xacml/core/functions/v1/round.py
# Compiled at: 2012-02-23 07:35:19
"""NDG XACML one and only functions module

NERC DataGrid
"""
__author__ = 'P J Kershaw'
__date__ = '01/04/10'
__copyright__ = ''
__license__ = 'BSD - see LICENSE file in top-level directory'
__contact__ = 'Philip.Kershaw@stfc.ac.uk'
__revision__ = '$Id: round.py 8020 2012-02-23 12:35:19Z pjkersha $'
from ndg.xacml.core.functions import AbstractFunction, FunctionClassFactoryInterface
from ndg.xacml.core.context.exceptions import XacmlContextTypeError

class Round(AbstractFunction):
    """Base class for XACML <type>-round functions
    
    @cvar FUNCTION_NS: namespace for this function
    @type FUNCTION_NS: string
    """
    FUNCTION_NS = AbstractFunction.V1_0_FUNCTION_NS + 'round'

    def evaluate(self, num):
        """Execute mathematical round up of the input number
        
        @param num: number to round up
        @type num: int / long / float
        @rtype: float
        @raise TypeError: incorrect type for input
        """
        try:
            return round(num)
        except TypeError as e:
            raise XacmlContextTypeError('Round function: %s' % e)


class FunctionClassFactory(FunctionClassFactoryInterface):
    """Class Factory for round XACML function class
    """

    def __call__(self, identifier):
        """Create class for the Round XACML function identifier
        
        @param identifier: XACML round function identifier
        @type identifier: basestring
        @return: round function class or None if identifier doesn't match
        @rtype: ndg.xacml.core.functions.v1.round.Round / NoneType
        """
        if identifier == Round.FUNCTION_NS:
            return Round
        else:
            return
            return