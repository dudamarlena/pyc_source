# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\Development\django2-propeller\django2_propeller\views.py
# Compiled at: 2019-04-26 08:32:14
# Size of source mod 2**32: 363 bytes
from django.views.generic.base import ContextMixin

class NavBarMixin(ContextMixin):
    navbar_class = None
    navbar_name = 'navbar'

    def get_context_data(self, **kwargs):
        context = (super(NavBarMixin, self).get_context_data)(**kwargs)
        context[self.navbar_name] = self.navbar_class
        return context