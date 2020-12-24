# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/hvelarde/collective/lazysizes/src/collective/lazysizes/controlpanel.py
# Compiled at: 2018-01-29 07:42:59
from collective.lazysizes import _
from collective.lazysizes.interfaces import ILazySizesSettings
from plone.app.registry.browser import controlpanel

class LazySizesSettingsEditForm(controlpanel.RegistryEditForm):
    schema = ILazySizesSettings
    label = _('title_controlpanel', 'lazysizes')
    description = _('description_controlpanel', default='Here you can modify the settings for collective.lazysizes.')


class LazySizesSettingsControlPanel(controlpanel.ControlPanelFormWrapper):
    form = LazySizesSettingsEditForm