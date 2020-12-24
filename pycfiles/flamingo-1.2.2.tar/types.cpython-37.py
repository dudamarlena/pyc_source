# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/fsc/work/devel/flamingo/flamingo/core/types.py
# Compiled at: 2020-04-28 06:15:31
# Size of source mod 2**32: 2627 bytes


class OverlayList(list):

    def __getitem__(self, key):
        item = super().__getitem__(key)
        if isinstance(item, list):
            item = OverlayList(item.copy())
            super().__setitem__(key, item)
        if isinstance(item, dict):
            item = OverlayDict(item.copy())
            super().__setitem__(key, item)
        return item


class OverlayDict(dict):

    def __getitem__(self, key):
        item = super().__getitem__(key)
        if isinstance(item, list):
            item = OverlayList(item.copy())
            super().__setitem__(key, item)
        if isinstance(item, dict):
            item = OverlayDict(item.copy())
            super().__setitem__(key, item)
        return item


class OverlayObject:
    _OverlayObject__overlay_ignore_attributes = []

    def __init__(self, *args, **kwargs):
        self._overlay_enabled = False
        self._attrs = {}
        self.overlay_disable()
        self.overlay_reset()

    def __getattribute__(self, name):

        def convert(attr):
            if isinstance(attr, dict):
                if not isinstance(attr, OverlayDict):
                    attr = OverlayDict(attr.copy())
                    self._overlay_attrs[name] = attr
            if isinstance(attr, list):
                if not isinstance(attr, OverlayList):
                    attr = OverlayList(attr.copy())
                    self._overlay_attrs[name] = attr
            return attr

        if name.startswith('_') or name in self._OverlayObject__overlay_ignore_attributes:
            return super().__getattribute__(name)
        if self._overlay_enabled:
            if name in self._overlay_attrs:
                return convert(self._overlay_attrs[name])
            if name in self._attrs:
                return convert(self._attrs[name])
        if name in self._attrs:
            return self._attrs[name]
        attr = super().__getattribute__(name)
        if self._overlay_enabled:
            attr = convert(attr)
        return attr

    def __setattr__(self, name, value):
        if name.startswith('_') or name in self._OverlayObject__overlay_ignore_attributes:
            return super().__setattr__(name, value)
        if self._overlay_enabled:
            self._overlay_attrs[name] = value
            return
        self._attrs[name] = value

    def __dir__(self):
        return super().__dir__() + list(self._attrs.keys()) + list(self._overlay_attrs.keys())

    def overlay_enable(self):
        self._overlay_enabled = True

    def overlay_disable(self):
        self._overlay_enabled = False

    def overlay_reset(self):
        self._overlay_attrs = {}