# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.8-x86_64/egg/cmsplugin_phlog/forms/forms.py
# Compiled at: 2013-06-26 16:38:22
from django.forms import ModelForm, IntegerField, HiddenInput
from cmsplugin_phlog.forms.fields import ChildPluginsField
from cmsplugin_phlog.models import GalleryPlugin

class GalleryPluginForm(ModelForm):
    plugins = ChildPluginsField()

    def __init__(self, data=None, files=None, **kwargs):
        instance = kwargs.get('instance', None)
        if instance:
            kwargs.setdefault('initial', {})
            kwargs['initial']['plugins'] = instance
        super(GalleryPluginForm, self).__init__(data=data, files=files, **kwargs)
        return

    class Meta:
        model = GalleryPlugin