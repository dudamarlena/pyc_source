# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/ndg/xacml/finder/defaultfinder.py
# Compiled at: 2012-06-19 10:10:35
"""NDG XACML policy finder resolving within base policy document

NERC DataGrid
"""
__author__ = 'R B Wilkinson'
__date__ = '03/11/11'
__copyright__ = '(C) 2011 Science and Technology Facilities Council'
__contact__ = 'Philip.Kershaw@stfc.ac.uk'
__license__ = 'BSD - see LICENSE file in top-level directory'
__contact__ = 'Philip.Kershaw@stfc.ac.uk'
__revision__ = '$Id: defaultfinder.py 8078 2012-06-19 14:10:35Z pjkersha $'
import os
from ndg.xacml.finder.urlpolicyfinder import UrlPolicyFinder

def getDefaultPolicyFinder(source):
    """
    Constructs a default policy finder, using the location of root policy file
    if this can be determined. This implementation always returns a
    UrlPolicyFinder.
    @param: source
    @type: string, file, XML node type
    @return: default policy finder
    @rtype: subclass of ndg.xacml.finder.policyfinderbase.PolicyFinderBase
    """
    basePath = None
    if isinstance(source, str):
        if os.path.exists(source):
            basePath = os.path.dirname(source)
    elif isinstance(source, file):
        if hasattr(file, 'name') and file.name:
            basePath = os.path.dirname(file.name)
    finder = UrlPolicyFinder(basePath)
    return finder