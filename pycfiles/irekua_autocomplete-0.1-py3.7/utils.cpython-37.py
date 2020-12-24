# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/irekua_autocomplete/utils.py
# Compiled at: 2019-10-28 01:37:58
# Size of source mod 2**32: 299 bytes
from django.urls import reverse
from dal import autocomplete

def get_autocomplete_widget(model):
    name = model._meta.verbose_name_plural.lower().replace(' ', '_')
    view_name = '{name}_autocomplete'.format(name=name)
    url = reverse(view_name)
    return autocomplete.ModelSelect2(url=url)