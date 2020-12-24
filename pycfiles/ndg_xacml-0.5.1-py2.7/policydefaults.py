# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/ndg/xacml/core/policydefaults.py
# Compiled at: 2012-03-28 11:41:09
"""NDG Security Policy Defaults type definition

NERC DataGrid
"""
__author__ = 'P J Kershaw'
__date__ = '19/03/10'
__copyright__ = '(C) 2010 Science and Technology Facilities Council'
__contact__ = 'Philip.Kershaw@stfc.ac.uk'
__license__ = 'BSD - see LICENSE file in top-level directory'
__contact__ = 'Philip.Kershaw@stfc.ac.uk'
__revision__ = '$Id: policydefaults.py 7955 2011-12-21 18:29:45Z rwilkinson $'
from ndg.xacml.core import XacmlCoreBase

class PolicyDefaults(XacmlCoreBase):
    """XACML PolicyDefaults type
    
    @cvar ELEMENT_LOCAL_NAME: XML local name for this element
    @type ELEMENT_LOCAL_NAME: string
    @cvar XPATH_VERSION_ELEMENT_NAME: XML local name for XPath version element
    @type XPATH_VERSION_ELEMENT_NAME: string
   
    @ivar __xpathVersion: XPath version
    @type __xpathVersion: basestring / NoneType
    """
    ELEMENT_LOCAL_NAME = 'PolicyDefaults'
    XPATH_VERSION_ELEMENT_NAME = 'XPathVersion'
    __slots__ = ('__xpathVersion', )

    def __init__(self):
        """Initialise attributes"""
        super(PolicyDefaults, self).__init__()
        self.__xpathVersion = None
        return

    def _get_xpathVersion(self):
        """@return: XPath version
        @rtype: basestring / NoneType
        """
        return self.__xpathVersion

    def _set_xpathVersion(self, value):
        """@param value: XPath version
        @type value: basestring / NoneType
        @raise TypeError: incorrect input type
        """
        if not isinstance(value, basestring):
            raise TypeError('Expecting %r type for "xpathVersion" attribute; got %r' % (
             basestring, type(value)))
        self.__xpathVersion = value

    xpathVersion = property(_get_xpathVersion, _set_xpathVersion, None, 'PolicyDefaults type XPath version')