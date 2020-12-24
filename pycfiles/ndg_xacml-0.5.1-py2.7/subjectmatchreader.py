# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/ndg/xacml/parsers/etree/subjectmatchreader.py
# Compiled at: 2011-02-11 08:34:11
"""NDG XACML ElementTree based reader for subject match type

NERC DataGrid
"""
__author__ = 'P J Kershaw'
__date__ = '16/03/10'
__copyright__ = '(C) 2010 Science and Technology Facilities Council'
__contact__ = 'Philip.Kershaw@stfc.ac.uk'
__license__ = 'BSD - see LICENSE file in top-level directory'
__contact__ = 'Philip.Kershaw@stfc.ac.uk'
__revision__ = '$Id: subjectmatchreader.py 7109 2010-06-28 12:54:57Z pjkersha $'
from ndg.xacml.core.match import SubjectMatch
from ndg.xacml.core.attributedesignator import SubjectAttributeDesignator
from ndg.xacml.parsers.etree.matchreader import MatchReaderBase

class SubjectMatchReader(MatchReaderBase):
    """ElementTree based parser for XACML SubjectMatch
    
    @cvar TYPE: XACML class type that this reader will read values into
    @type TYPE: abc.ABCMeta
    
    @cvar ATTRIBUTE_DESIGNATOR_TYPE: type for attribute designator sub-elements
    @type ATTRIBUTE_DESIGNATOR_TYPE: abc.ABCMeta
    """
    TYPE = SubjectMatch
    ATTRIBUTE_DESIGNATOR_TYPE = SubjectAttributeDesignator