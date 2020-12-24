# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/iw/sitestat/interfaces/layer.py
# Compiled at: 2008-10-10 10:13:59
"""
Interface for plone.browserlayer
"""
__author__ = 'Gilles Lenfant <gilles.lenfant@ingeniweb.com>'
__docformat__ = 'restructuredtext'
from zope.interface import Interface

class IIwSitestatLayer(Interface):
    """We just need this layer marker to prevent using browser
    resources from this component in Plone sites where it is not
    installed"""
    __module__ = __name__