# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-intel/egg/etk/docking/docksettings.py
# Compiled at: 2011-01-31 01:35:43
"""
Configuration settings for elements in a Etk.Docking configuration.

The configuration can be set for every element in the hierarchy. By default the class
name can be used.
"""
import gtk

class DockSettings(object):
    """
    Container for group specific settings.
    The following settings can be set:

    * auto_remove: group is removed if if empty.
    * can_float: Group can be a floating group.
    * expand: A group can expand/shrink on resize.
    * inherit_settings: new groups constructed from items dragged from a group should
    get the same group name.
    """
    __slots__ = [
     'auto_remove',
     'can_float',
     'float_retain_size',
     'expand',
     'inherit_settings']

    def __init__(self, auto_remove=True, can_float=True, float_retain_size=False, expand=True, inherit_settings=True):
        self.auto_remove = auto_remove
        self.can_float = can_float
        self.float_retain_size = float_retain_size
        self.expand = expand
        self.inherit_settings = inherit_settings


class DockSettingsDict(object):
    """
    Settings container. Adheres partly to the dict protocol, only get() and setitem are
    supported.

    Settings can deal with widget names as well as widgets itself (in which case the
    name is requested). By overriding ``widget_name()`` it is possible to customize
    the behaviour for settings.
    """

    def __init__(self):
        self._settings = {}

    def get(self, target):
        return self[target]

    def widget_name(self, target):
        if isinstance(target, gtk.Widget):
            return target.get_name()
        return str(target)

    def __getitem__(self, target):
        target = self.widget_name(target)
        settings = self._settings.get(target)
        if not settings:
            settings = self._settings[target] = DockSettings()
        return settings

    def __setitem__(self, target, settings):
        self._settings[self.widget_name(target)] = settings


settings = DockSettingsDict()