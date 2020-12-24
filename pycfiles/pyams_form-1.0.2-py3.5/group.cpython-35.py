# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyams_form/group.py
# Compiled at: 2020-02-23 12:53:51
# Size of source mod 2**32: 3835 bytes
"""PyAMS_form.group module

This module handles groups of widgets within forms.
"""
from zope.interface import implementer
from pyams_form.events import DataExtractedEvent
from pyams_form.form import BaseForm, get_form_weight
from pyams_form.interfaces.form import IGroup, IGroupForm, IGroupManager
from pyams_form.interfaces.widget import IWidgets
__docformat__ = 'restructuredtext'

@implementer(IGroupManager)
class GroupManager:
    __doc__ = 'Base groups manager miixn class'
    groups = ()

    def update(self):
        """See interfaces.IForm"""
        self.update_widgets()
        groups = []
        for group_class in self.groups:
            if IGroup.providedBy(group_class):
                group = group_class
            else:
                group = group_class(self.context, self.request, self)
            groups.append(group)

        registry = self.request.registry
        for group in sorted((adapter for name, adapter in registry.getAdapters((self.context, self.request, self), IGroup)), key=get_form_weight):
            groups.append(group)

        [group.update() for group in groups]
        self.groups = tuple(groups)

    def extract_data(self, set_errors=True):
        """See interfaces.IForm"""
        data, errors = super(GroupManager, self).extract_data(set_errors=set_errors)
        for group in self.groups:
            group_data, group_errors = group.extract_data(set_errors=set_errors)
            data.update(group_data)
            if group_errors:
                if errors:
                    errors += group_errors
                else:
                    errors = group_errors

        registry = self.request.registry
        registry.notify(DataExtractedEvent(data, errors, self))
        return (data, errors)


@implementer(IGroup)
class Group(GroupManager, BaseForm):
    __doc__ = 'Group of field widgets within form'

    def __init__(self, context, request, parent_form):
        self.context = context
        self.request = request
        self.parent_form = self.__parent__ = parent_form

    def update_widgets(self, prefix=None):
        """See interfaces.IForm"""
        registry = self.request.registry
        self.widgets = registry.getMultiAdapter((self, self.request, self.get_content()), IWidgets)
        for attr_name in ('mode', 'ignore_request', 'ignore_context', 'ignore_readonly'):
            value = getattr(self.parent_form.widgets, attr_name)
            setattr(self.widgets, attr_name, value)

        if prefix is not None:
            self.widgets.prefix = prefix
        self.widgets.update()


@implementer(IGroupForm)
class GroupForm(GroupManager):
    __doc__ = 'A mix-in class for add and edit forms to support groups.'

    def update(self):
        """See interfaces.IForm"""
        GroupManager.update(self)
        self.update_actions()
        self.actions.execute()