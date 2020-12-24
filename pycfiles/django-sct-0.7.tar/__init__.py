# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/herbert/dev/python/sctdev/simpleproject/simpleproject/../../communitytools/sphenecoll/sphene/__init__.py
# Compiled at: 2012-03-17 12:42:14
from django.conf import settings
if hasattr(settings, 'SPH_SETTINGS') and settings.SPH_SETTINGS.get('django096compatibility', False):
    from django import forms
    if not hasattr(forms.Form, 'cleaned_data'):

        def get_cleaned_data(self):
            return self.clean_data


        def set_cleaned_data(self, v):
            self.__dict__['cleaned_data'] = v


        forms.Form.cleaned_data = property(get_cleaned_data, set_cleaned_data)