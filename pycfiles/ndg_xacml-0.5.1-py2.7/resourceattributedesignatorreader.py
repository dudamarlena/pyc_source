# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/ndg/xacml/parsers/etree/resourceattributedesignatorreader.py
# Compiled at: 2011-02-11 08:34:11
"""NDG XACML ElementTree based reader for ResourceAttributeDesignator type

NERC DataGrid
"""
__author__ = 'P J Kershaw'
__date__ = '19/03/10'
__copyright__ = '(C) 2010 Science and Technology Facilities Council'
__contact__ = 'Philip.Kershaw@stfc.ac.uk'
__license__ = 'BSD - see LICENSE file in top-level directory'
__contact__ = 'Philip.Kershaw@stfc.ac.uk'
__revision__ = '$Id: resourceattributedesignatorreader.py 7109 2010-06-28 12:54:57Z pjkersha $'
from ndg.xacml.core.attributedesignator import ResourceAttributeDesignator
from ndg.xacml.parsers.etree.attributedesignatorreader import AttributeDesignatorReaderBase

class ResourceAttributeDesignatorReader(AttributeDesignatorReaderBase):
    """ElementTree based XACML Resource Attribute Designator type parser
    
    @cvar TYPE: XACML class type that this reader will read values into
    @type TYPE: abc.ABCMeta
    """
    TYPE = ResourceAttributeDesignator