# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/Ari/src/callisto-core/callisto_core/wizard_builder/model_helpers.py
# Compiled at: 2019-08-07 16:42:06
# Size of source mod 2**32: 205 bytes


class ProxyQuestion:

    def __init__(self, *args, **kwargs):
        self._meta.get_field('type').default = self.proxy_name
        (super().__init__)(*args, **kwargs)

    class Meta:
        proxy = True