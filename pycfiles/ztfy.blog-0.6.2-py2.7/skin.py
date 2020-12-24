# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/blog/skin.py
# Compiled at: 2012-06-26 16:33:07
__docformat__ = 'restructuredtext'
from ztfy.blog.interfaces import ISkinnable
from zope.interface import implements
from zope.schema.fieldproperty import FieldProperty
from zope.traversing.api import getParent

class InheritedSkin(object):
    """Find content's skin locally or by inheriting via it's parents"""
    implements(ISkinnable)
    skin = FieldProperty(ISkinnable['skin'])

    def getSkin(self):
        if self.skin is not None:
            return self.skin
        else:
            parent = getParent(self)
            while parent is not None:
                adapted = ISkinnable(parent, None)
                if adapted is not None and adapted.skin is not None:
                    return adapted.skin
                parent = getParent(parent)

            return