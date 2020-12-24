# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/site-packages/django_files_library/forms.py
# Compiled at: 2018-02-10 07:51:58
# Size of source mod 2**32: 205 bytes
from django.forms import ModelForm
from django_files_library.models import File

class FileForm(ModelForm):

    class Meta:
        model = File
        fields = ['name', 'description', 'uploaded_file']