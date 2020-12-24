# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/mvc/models/properties/action_mixins.py
# Compiled at: 2020-03-07 03:51:49
# Size of source mod 2**32: 3114 bytes
from mvc.support.utils import rec_getattr

class SetActionMixin(object):
    __doc__ = '\n    A descriptor mixin that will invoke a method on the instance\n    owning this property after setting it.\n    \n    Expects two more keyword arguments to be passed to the property constructor:\n        - set_action_name: a dotted string describing where to get the method\n          from the instance\n        - set_action_before: flag indicating whether this action should be \n          invoked before setting the property (default False) \n    '
    set_action_name = None
    set_action_before = False

    def __set__(self, instance, value):
        action = rec_getattr(instance, self.set_action_name, None)
        assert callable(action), 'The action in a SetActionMixin (%s) should be callable!' % self.label
        if self.set_action_before:
            action()
        super(SetActionMixin, self).__set__(instance, value)
        if not self.set_action_before:
            action()


class GetActionMixin(object):
    __doc__ = '\n    A descriptor mixin that will invoke a method on the instance\n    owning this property before getting it.\n    \n    Expects two more keyword arguments to be passed to the property constructor:\n        - get_action_name: a dotted string describing where to get the method\n          from the instance\n        - get_action_after: flag indicating whether this action should be \n          invoked after setting the property (default False) \n    '
    get_action_name = None
    get_action_after = False

    def __get__(self, instance, owner=None):
        if instance is None:
            return self
        else:
            action = rec_getattr(instance, self.get_action_name, None)
            assert callable(action), 'The action in a GetActionMixin (%s) should be callable!' % self.label
            if self.get_action_after:
                action()
            value = super(GetActionMixin, self).__get__(instance, owner=owner)
            if not self.get_action_after:
                action()
            return value