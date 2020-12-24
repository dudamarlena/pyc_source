# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/redomino/workgroup/browser/common.py
# Compiled at: 2008-06-25 09:09:13
from Products.Five.browser import BrowserView
from Products.Archetypes.interfaces._base import IBaseFolder
from redomino.workgroup.interfaces import IWorkgroup
from redomino.workgroup.interfaces import IMemberArea

class EnableWorkgroupCondition(BrowserView):
    """Returns True or False depending on whether the enable workgroup action is allowed
    on current context.
    """
    __module__ = __name__

    @property
    def _action_condition(self):
        return IBaseFolder.providedBy(self.context) and not IWorkgroup.providedBy(self.context) and not IMemberArea.providedBy(self.context)

    def __call__(self):
        return self._action_condition


class DisableWorkgroupCondition(BrowserView):
    """Returns True or False depending on whether the disable workgroup action is allowed
    on current context.
    """
    __module__ = __name__

    @property
    def _action_condition(self):
        return IWorkgroup.providedBy(self.context)

    def __call__(self):
        return self._action_condition