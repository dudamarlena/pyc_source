# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/quintagroup/canonicalpath/interfaces.py
# Compiled at: 2010-06-01 09:56:52
from zope.interface import Interface, Attribute

class ICanonicalPath(Interface):
    """canonical_path provider interface
    """
    __module__ = __name__
    canonical_path = Attribute('canonical_path', 'canonical_path - for the object. Adapter must implement *setter* and *getter* for the attribute')


class ICanonicalLink(Interface):
    """canonical_link provider interface
    """
    __module__ = __name__
    canonical_link = Attribute('canonical_link', 'canonical_link - for the object. Adapter must implement *setter* and *getter* for the attribute')