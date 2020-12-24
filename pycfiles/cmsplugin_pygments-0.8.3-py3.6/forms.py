# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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