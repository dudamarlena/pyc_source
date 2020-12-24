# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/security/browser/roles.py
# Compiled at: 2013-03-01 06:59:28
__docformat__ = 'restructuredtext'
from ztfy.jqueryui import jquery_multiselect
from z3c.form import button, field
from z3c.formjs import jsaction
from zope.interface import Interface
from ztfy.skin.form import DialogEditForm
from ztfy.security import _

class IEditFormButtons(Interface):
    """Default edit form buttons"""
    submit = button.Button(title=_('Submit'))
    reset = jsaction.JSButton(title=_('Reset'))


class RolesEditForm(DialogEditForm):
    """Roles edit form"""
    legend = _('Define roles on current context')
    interfaces = ()
    resources = (jquery_multiselect,)

    @property
    def fields(self):
        return field.Fields(*self.interfaces)