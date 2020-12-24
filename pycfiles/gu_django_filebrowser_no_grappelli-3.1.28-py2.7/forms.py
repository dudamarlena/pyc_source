# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-intel/egg/filebrowser/forms.py
# Compiled at: 2014-11-22 02:35:13
import re, os
from django import forms
from django.forms.formsets import BaseFormSet
from django.utils.translation import ugettext as _
from filebrowser.settings import MAX_UPLOAD_SIZE, FOLDER_REGEX
from filebrowser.functions import convert_filename
alnum_name_re = re.compile(FOLDER_REGEX)

class MakeDirForm(forms.Form):
    """
    Form for creating Folder.
    """

    def __init__(self, path, *args, **kwargs):
        self.path = path
        super(MakeDirForm, self).__init__(*args, **kwargs)

    dir_name = forms.CharField(widget=forms.TextInput(attrs=dict({'class': 'vTextField'}, max_length=50, min_length=3)), label=_('Name'), help_text=_('Only letters, numbers, underscores, spaces and hyphens are allowed.'), required=True)

    def clean_dir_name(self):
        if self.cleaned_data['dir_name']:
            if not alnum_name_re.search(self.cleaned_data['dir_name']):
                raise forms.ValidationError(_('Only letters, numbers, underscores, spaces and hyphens are allowed.'))
            if os.path.isdir(os.path.join(self.path, convert_filename(self.cleaned_data['dir_name']))):
                raise forms.ValidationError(_('The Folder already exists.'))
        return convert_filename(self.cleaned_data['dir_name'])


class RenameForm(forms.Form):
    """
    Form for renaming Folder/File.
    """

    def __init__(self, path, file_extension, *args, **kwargs):
        self.path = path
        self.file_extension = file_extension
        super(RenameForm, self).__init__(*args, **kwargs)

    name = forms.CharField(widget=forms.TextInput(attrs=dict({'class': 'vTextField'}, max_length=50, min_length=3)), label=_('New Name'), help_text=_('Only letters, numbers, underscores, spaces and hyphens are allowed.'), required=True)

    def clean_name(self):
        if self.cleaned_data['name']:
            if not alnum_name_re.search(self.cleaned_data['name']):
                raise forms.ValidationError(_('Only letters, numbers, underscores, spaces and hyphens are allowed.'))
            if os.path.isdir(os.path.join(self.path, convert_filename(self.cleaned_data['name']))):
                raise forms.ValidationError(_('The Folder already exists.'))
            elif os.path.isfile(os.path.join(self.path, convert_filename(self.cleaned_data['name']) + self.file_extension)):
                raise forms.ValidationError(_('The File already exists.'))
        return convert_filename(self.cleaned_data['name'])