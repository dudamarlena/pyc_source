# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/powellc/devel/cfm/beehve/beehve/apps/workers/forms.py
# Compiled at: 2016-08-07 13:07:33
# Size of source mod 2**32: 205 bytes
from django.core.urlresolvers import reverse
import floppyforms as forms
from .models import Worker

class WorkerForm(forms.ModelForm):

    class Meta:
        model = Worker
        exclude = ['user']