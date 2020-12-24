# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/ice/control/browser/control.py
# Compiled at: 2010-08-27 06:32:04
from zope.location import Location
from zope.interface import implements
from interfaces import IControl

class Control(Location):
    implements(IControl)

    def get_content(self):

        def content(x):
            if IControl.providedBy(x):
                return content(x.__parent__)
            else:
                return x

        return content(self.__parent__)