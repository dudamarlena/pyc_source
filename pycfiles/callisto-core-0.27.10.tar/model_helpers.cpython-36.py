# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Ari/src/callisto-core/callisto_core/wizard_builder/model_helpers.py
# Compiled at: 2019-08-07 16:42:06
# Size of source mod 2**32: 205 bytes


class ProxyQuestion:

    def __init__(self, *args, **kwargs):
        self._meta.get_field('type').default = self.proxy_name
        (super().__init__)(*args, **kwargs)

    class Meta:
        proxy = True