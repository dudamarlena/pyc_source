# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/camelot/admin/section.py
# Compiled at: 2013-04-11 17:47:52


class Section(object):
    """A Section as displayed in the left pane of the application.  Each Section
contains a list of SectionItems the user can click on.  Sections should be used
in the definition of the Application admin:

.. literalinclude:: ../../../../camelot_example/application_admin.py
   :start-after: begin section with action
   :end-before: end section with action

.. image:: /_static/controls/navigation_pane.png
    """

    def __init__(self, verbose_name, application_admin, icon=None, items=[]):
        self.verbose_name = verbose_name
        self.icon = icon
        self.items = structure_to_section_items(items, application_admin)
        self.admin = application_admin

    def get_verbose_name(self):
        return self.verbose_name

    def get_icon(self):
        from camelot.view.art import Icon
        return self.icon or Icon('tango/32x32/apps/system-users.png')

    def get_items(self):
        return self.items


class SectionItem(object):
    """An item inside a section, the user can click on and trigger an action."""

    def __init__(self, action, application_admin, verbose_name=None):
        from camelot.admin.action.application_action import structure_to_application_action
        self.verbose_name = verbose_name
        self.action = structure_to_application_action(action, application_admin)
        self.state = self.action.get_state(None)
        return

    def get_verbose_name(self):
        return self.verbose_name or self.state.verbose_name

    def get_action(self):
        return self.action

    def get_icon(self):
        return self.state.icon

    def get_tooltip(self):
        return self.state.tooltip

    def get_modes(self):
        return self.state.modes


def structure_to_section_items(structure, application_admin):

    def rule(element):
        if isinstance(element, (SectionItem, Section)):
            return element
        return SectionItem(element, application_admin)

    return [ rule(item) for item in structure ]