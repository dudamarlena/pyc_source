# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/ndg/xacml/core/variablereference.py
# Compiled at: 2011-02-11 08:34:12
"""NDG Security Variable Reference type definition

NERC DataGrid
"""
__author__ = 'P J Kershaw'
__date__ = '29/03/10'
__copyright__ = '(C) 2010 Science and Technology Facilities Council'
__contact__ = 'Philip.Kershaw@stfc.ac.uk'
__license__ = 'BSD - see LICENSE file in top-level directory'
__contact__ = 'Philip.Kershaw@stfc.ac.uk'
__revision__ = '$Id: variablereference.py 7108 2010-06-28 09:19:26Z pjkersha $'
from ndg.xacml.core import XacmlPolicyBase

class VariableReference(XacmlPolicyBase):
    """XACML Variable Reference Type - this class is a placeholder, it's not 
    currently implemented
    
    @cvar ELEMENT_LOCAL_NAME: XML element local name
    @type ELEMENT_LOCAL_NAME: string
    """
    ELEMENT_LOCAL_NAME = 'VariableReference'
    __slots__ = ()

    def __init__(self):
        """This class not needed yet"""
        raise NotImplementedError()