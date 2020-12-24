# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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