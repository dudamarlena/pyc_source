# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/syfilebrowser/forms.py
# Compiled at: 2016-04-18 13:43:03
from __future__ import unicode_literals
from future.builtins import super
import os, re
from django import forms
from django.utils.translation import ugettext as _
from syfilebrowser.settings import FOLDER_REGEX
alnum_name_re = re.compile(FOLDER_REGEX)

class MakeDirForm(forms.Form):
    """
    Form for creating Folder.
    """

    def __init__(self, path, *args, **kwargs):
        self.path = path
        super(MakeDirForm, self).__init__(*args, **kwargs)

    dir_name = forms.CharField(widget=forms.TextInput(attrs=dict({b'class': b'vTextField'}, max_length=50, min_length=3)), label=_(b'Name'), help_text=_(b'Only letters, numbers, underscores, spaces and hyphens are allowed.'), required=True)

    def clean_dir_name(self):
        if self.cleaned_data[b'dir_name']:
            if not alnum_name_re.search(self.cleaned_data[b'dir_name']):
                raise forms.ValidationError(_(b'Only letters, numbers, underscores, spaces and hyphens are allowed.'))
            if os.path.isdir(os.path.join(self.path, self.cleaned_data[b'dir_name'])):
                raise forms.ValidationError(_(b'The Folder already exists.'))
        return self.cleaned_data[b'dir_name']


class RenameForm(forms.Form):
    """
    Form for renaming Folder/File.
    """

    def __init__(self, path, file_extension, *args, **kwargs):
        self.path = path
        self.file_extension = file_extension
        super(RenameForm, self).__init__(*args, **kwargs)

    name = forms.CharField(widget=forms.TextInput(attrs=dict({b'class': b'vTextField'}, max_length=50, min_length=3)), label=_(b'New Name'), help_text=_(b'Only letters, numbers, underscores, spaces and hyphens are allowed.'), required=True)

    def clean_name(self):
        if self.cleaned_data[b'name']:
            if not alnum_name_re.search(self.cleaned_data[b'name']):
                raise forms.ValidationError(_(b'Only letters, numbers, underscores, spaces and hyphens are allowed.'))
            if os.path.isdir(os.path.join(self.path, self.cleaned_data[b'name'])):
                raise forms.ValidationError(_(b'The Folder already exists.'))
            elif os.path.isfile(os.path.join(self.path, self.cleaned_data[b'name'] + self.file_extension)):
                raise forms.ValidationError(_(b'The File already exists.'))
        return self.cleaned_data[b'name']