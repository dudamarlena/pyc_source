# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/ndg/xacml/parsers/etree/conditionreader.py
# Compiled at: 2012-03-06 17:01:30
"""NDG XACML ElementTree based Target Element reader 

NERC DataGrid
"""
__author__ = 'P J Kershaw'
__date__ = '16/03/10'
__copyright__ = '(C) 2010 Science and Technology Facilities Council'
__contact__ = 'Philip.Kershaw@stfc.ac.uk'
__license__ = 'BSD - see LICENSE file in top-level directory'
__contact__ = 'Philip.Kershaw@stfc.ac.uk'
__revision__ = '$Id: conditionreader.py 8028 2012-02-27 14:38:01Z rwilkinson $'
from ndg.xacml.core.condition import Condition
from ndg.xacml.parsers import XMLParseError
from ndg.xacml.parsers.etree import QName, getElementChildren
from ndg.xacml.parsers.etree.reader import ETreeAbstractReader
from ndg.xacml.parsers.etree.applyreader import ApplyReader

class ConditionReader(ETreeAbstractReader):
    """ElementTree based XACML 2.0 Condition parser.  Note the difference to
    XACML 1.0: the Condition element is its own type and not an Apply type.
    It expects a single Expression derived type child element
    
    @cvar TYPE: XACML type to instantiate from parsed object
    @type TYPE: type
    """
    TYPE = Condition

    def __call__(self, obj, common):
        """Parse condition object
        
        @param obj: input object to parse
        @type obj: ElementTree Element, or stream object
        @return: new XACML condition instance
        @rtype: ndg.xacml.core.condition.Condition
        @raise XMLParseError: error reading sub-elements
        """
        elem = super(ConditionReader, self)._parse(obj)
        xacmlType = self.__class__.TYPE
        condition = xacmlType()
        localName = QName.getLocalPart(elem.tag)
        if localName != xacmlType.ELEMENT_LOCAL_NAME:
            raise XMLParseError('No "%s" element found' % xacmlType.ELEMENT_LOCAL_NAME)
        nSubElem = 0
        for childElem in getElementChildren(elem):
            nSubElem += 1
            subElem = childElem

        if nSubElem != 1:
            raise XMLParseError('XACML 2.0 policy schema expects only one expression sub-element in the Condition element; policy file has %d' % nSubElem)
        subElemlocalName = QName.getLocalPart(subElem.tag)
        if subElemlocalName == xacmlType.APPLY_ELEMENT_LOCAL_NAME:
            condition.expression = ApplyReader.parse(subElem, common)
        else:
            raise XMLParseError('Expecting %r Condition sub-element not recognised' % xacmlType.EXPRESSION_ELEMENT_LOCAL_NAME)
        return condition