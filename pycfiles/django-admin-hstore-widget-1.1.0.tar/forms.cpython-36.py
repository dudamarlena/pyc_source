# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/adufour/Projets/django-admin-hstore/django_admin_hstore_widget/forms.py
# Compiled at: 2018-03-05 07:50:48
# Size of source mod 2**32: 235 bytes
import json
from django.contrib.postgres.forms import HStoreField
from .widgets import HStoreFormWidget

class HStoreFormField(HStoreField):
    widget = HStoreFormWidget

    def clean(self, value):
        return json.loads(value)