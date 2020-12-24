# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hvelarde/collective/behavior.richpreview/src/collective/behavior/richpreview/browser/controlpanel.py
# Compiled at: 2018-04-05 17:11:04
from collective.behavior.richpreview import _
from collective.behavior.richpreview.interfaces import IRichPreviewSettings
from plone.app.registry.browser import controlpanel

class RichPreviewSettingsEditForm(controlpanel.RegistryEditForm):
    """Control panel edit form."""
    schema = IRichPreviewSettings
    label = _('Rich Link Preview')
    description = _('Settings for the collective.behavior.richpreview package')


class RichPreviewSettingsControlPanel(controlpanel.ControlPanelFormWrapper):
    """Control panel form wrapper."""
    form = RichPreviewSettingsEditForm