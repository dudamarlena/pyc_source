# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/eliotberriot/Seafile/kii/kii-blog/kii_blog/forms.py
# Compiled at: 2014-12-16 11:40:40
from kii.stream import forms
from . import models

class EntryForm(forms.StreamItemForm):

    class Meta(forms.StreamItemForm.Meta):
        model = models.Entry