# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/powellc/projects/planadversity/planadversity/apps/meditations/forms.py
# Compiled at: 2015-01-01 14:22:23
# Size of source mod 2**32: 305 bytes
from django.core.urlresolvers import reverse
import floppyforms as forms
from .models import Response, Meditation

class ResponseForm(forms.ModelForm):

    class Meta:
        model = Response
        exclude = ['user']