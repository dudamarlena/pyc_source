# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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