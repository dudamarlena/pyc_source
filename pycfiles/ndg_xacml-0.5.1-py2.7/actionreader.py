# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/ndg/xacml/parsers/etree/actionreader.py
# Compiled at: 2011-02-11 08:34:11
"""NDG XACML ElementTree based parser for Action type

NERC DataGrid
"""
__author__ = 'P J Kershaw'
__date__ = '16/03/10'
__copyright__ = '(C) 2010 Science and Technology Facilities Council'
__contact__ = 'Philip.Kershaw@stfc.ac.uk'
__license__ = 'BSD - see LICENSE file in top-level directory'
__contact__ = 'Philip.Kershaw@stfc.ac.uk'
__revision__ = '$Id: actionreader.py 7109 2010-06-28 12:54:57Z pjkersha $'
from ndg.xacml.core.action import Action
from ndg.xacml.parsers.etree.targetchildreader import TargetChildReader

class ActionReader(TargetChildReader):
    """ElementTree based parser for Action type
    @cvar TYPE: XACML type to instantiate from parsed object
    @type TYPE: type
    """
    TYPE = Action