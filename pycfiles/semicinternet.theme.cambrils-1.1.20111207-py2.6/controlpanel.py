# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/semicinternet/theme/cambrils/browser/controlpanel.py
# Compiled at: 2011-07-08 07:32:36
from plone.app.registry.browser import controlpanel
from semicinternet.theme.cambrils.browser.interfaces import ICambrilsSettings, _

class CambrilsSettingsEditForm(controlpanel.RegistryEditForm):
    schema = ICambrilsSettings
    label = _('Cambrils settings')
    description = _('')

    def updateFields(self):
        super(CambrilsSettingsEditForm, self).updateFields()

    def updateWidgets(self):
        super(CambrilsSettingsEditForm, self).updateWidgets()


class CambrilsSettingsControlPanel(controlpanel.ControlPanelFormWrapper):
    form = CambrilsSettingsEditForm