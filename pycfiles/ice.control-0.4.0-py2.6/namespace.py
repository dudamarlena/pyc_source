# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/ice/control/browser/namespace.py
# Compiled at: 2010-08-27 06:32:04
from zope.location import LocationProxy, locate
from zope.traversing.namespace import SimpleHandler
from control import Control

class ControlNamespace(SimpleHandler):

    def traverse(self, name, ignored):
        location = (
         self.context, '++control++')
        ob = Control()
        locate(ob, *location)
        return LocationProxy(ob, *location)