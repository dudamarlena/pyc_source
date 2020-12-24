# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/vsmclient/extension.py
# Compiled at: 2016-06-13 14:11:03
from vsmclient import base
from vsmclient import utils

class Extension(utils.HookableMixin):
    """Extension descriptor."""
    SUPPORTED_HOOKS = ('__pre_parse_args__', '__post_parse_args__')

    def __init__(self, name, module):
        self.name = name
        self.module = module
        self._parse_extension_module()

    def _parse_extension_module(self):
        self.manager_class = None
        for attr_name, attr_value in self.module.__dict__.items():
            if attr_name in self.SUPPORTED_HOOKS:
                self.add_hook(attr_name, attr_value)
            elif utils.safe_issubclass(attr_value, base.Manager):
                self.manager_class = attr_value

        return

    def __repr__(self):
        return "<Extension '%s'>" % self.name