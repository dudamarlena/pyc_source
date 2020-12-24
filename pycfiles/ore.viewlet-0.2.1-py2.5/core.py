# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-i386/egg/ore/viewlet/core.py
# Compiled at: 2008-05-19 13:01:22
"""
$Id: core.py 1965 2007-05-22 03:41:22Z hazmat $
"""
from zope.viewlet.viewlet import ViewletBase
import base

class EventViewlet(ViewletBase, base.BaseEventViewlet):
    pass


class FormViewlet(ViewletBase, base.BaseFormViewlet):

    def update(self):
        super(FormViewlet, self).update()
        super(base.BaseFormViewlet, self).update()


class ComponentViewlet(ViewletBase, base.ViewComponent):

    def update(self):
        super(ComponentViewlet, self).update()
        super(base.ViewComponent, self).update()