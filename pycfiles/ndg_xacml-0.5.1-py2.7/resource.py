# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/ndg/xacml/core/resource.py
# Compiled at: 2012-03-28 11:41:09
"""NDG Security Resource type definition

NERC DataGrid
"""
__author__ = 'P J Kershaw'
__date__ = '24/02/10'
__copyright__ = '(C) 2010 Science and Technology Facilities Council'
__contact__ = 'Philip.Kershaw@stfc.ac.uk'
__license__ = 'BSD - see LICENSE file in top-level directory'
__contact__ = 'Philip.Kershaw@stfc.ac.uk'
__revision__ = '$Id: resource.py 7955 2011-12-21 18:29:45Z rwilkinson $'
from ndg.xacml.core import TargetChildBase
from ndg.xacml.core.match import ResourceMatch

class Resource(TargetChildBase):
    """XACML Resource Target Policy element
    
    @cvar MATCH_TYPE: Sets the type for match attributes in this 
    TargetChildBase derived class
    @type MATCH_TYPE: ndg.xacml.core.match.ResourceMatch
    @cvar ELEMENT_LOCAL_NAME: XML element local name
    @type ELEMENT_LOCAL_NAME: string
    """
    MATCH_TYPE = ResourceMatch
    ELEMENT_LOCAL_NAME = 'Resource'
    ID = 'urn:oasis:names:tc:xacml:1.0:resource:resource-id'
    __slots__ = ()

    @property
    def resourceMatches(self):
        """Convenience wrapper to base class method
        @return: list of matches
        @rtype: ndg.xacml.utils.TypedList 
        """
        return self.matches