# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/ndg/xacml/parsers/etree/policybasereader.py
# Compiled at: 2012-06-19 10:10:35
"""NDG XACML ElementTree Policy Document Reader

NERC DataGrid
"""
__author__ = 'R B Wilkinson'
__date__ = '01/11/11'
__copyright__ = '(C) 2011 Science and Technology Facilities Council'
__contact__ = 'Philip.Kershaw@stfc.ac.uk'
__license__ = 'BSD - see LICENSE file in top-level directory'
__contact__ = 'Philip.Kershaw@stfc.ac.uk'
__revision__ = '$Id: policybasereader.py 8078 2012-06-19 14:10:35Z pjkersha $'
from ndg.xacml.parsers import XMLParseError
from ndg.xacml.core.policy import Policy
from ndg.xacml.core.policyset import PolicySet
from ndg.xacml.core.policybase import PolicyBase
from ndg.xacml.parsers.etree import QName
from ndg.xacml.parsers.etree.policyreader import PolicyReader
from ndg.xacml.parsers.etree.policysetreader import PolicySetReader
from ndg.xacml.parsers.etree.reader import ETreeAbstractReader

class PolicyBaseReader(ETreeAbstractReader):
    """Parse a Policy Document using ElementTree
    @cvar TYPE: XACML type to instantiate from parsed object
    @type TYPE: type"""
    TYPE = PolicyBase
    TYPE_MAP = {Policy.ELEMENT_LOCAL_NAME: (Policy, PolicyReader), PolicySet.ELEMENT_LOCAL_NAME: (
                                    PolicySet, PolicySetReader)}

    def __call__(self, obj, common):
        """Parse policy object

        @param obj: input object to parse
        @type obj: ElementTree Element, or stream object
        @return: new XACML expression instance
        @rtype: ndg.xacml.core.policybase.PolicyBase derived type
        @raise XMLParseError: error reading element
        @raise NotImplementedError: parsing is not implemented for rule
        combiner, combiner parameters and obligations elements.
        """
        elem = super(PolicyBaseReader, self)._parse(obj)
        localName = QName.getLocalPart(elem.tag)
        xacmlType, readerType = self.TYPE_MAP.get(localName, (None, None))
        if xacmlType is None:
            raise XMLParseError('Element %s is not valid as the root element of a XACML document', localName)
        rootElementReader = readerType()
        policy = rootElementReader.processElement(elem, common)
        return policy