# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/ndg/xacml/core/context/action.py
# Compiled at: 2011-02-11 08:34:12
"""NDG XACML Context Action type

NERC DataGrid
"""
__author__ = 'P J Kershaw'
__date__ = '24/03/10'
__copyright__ = '(C) 2010 Science and Technology Facilities Council'
__contact__ = 'Philip.Kershaw@stfc.ac.uk'
__license__ = 'BSD - see LICENSE file in top-level directory'
__contact__ = 'Philip.Kershaw@stfc.ac.uk'
__revision__ = '$Id: action.py 7087 2010-06-25 11:23:09Z pjkersha $'
from ndg.xacml.core.context import RequestChildBase

class Action(RequestChildBase):
    """XACML Context Action type"""
    ELEMENT_LOCAL_NAME = 'Action'