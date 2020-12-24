# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/vellum/forms.py
# Compiled at: 2012-04-05 15:23:29
from django import forms
from vellum.models import Post
try:
    from wmd.widgets import WMDWidget

    class PostForm(forms.ModelForm):
        body = forms.CharField(widget=WMDWidget(large=True))

        class Meta:
            model = Post


except ImportError:
    pass