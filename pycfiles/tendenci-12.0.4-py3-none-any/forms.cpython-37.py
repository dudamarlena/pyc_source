# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jennyq/.pyenv/versions/venv_t12/lib/python3.7/site-packages/tendenci/libs/uploader/fine_uploader/forms.py
# Compiled at: 2020-02-11 12:52:19
# Size of source mod 2**32: 698 bytes
from django import forms

class UploadFileForm(forms.Form):
    __doc__ = ' This form represents a basic request from Fine Uploader.\n    The required fields will **always** be sent, the other fields are optional\n    based on your setup.\n\n    Edit this if you want to add custom parameters in the body of the POST\n    request.\n    '
    qqfile = forms.FileField()
    qquuid = forms.CharField()
    qqfilename = forms.CharField()
    qqpartindex = forms.IntegerField(required=False)
    qqchunksize = forms.IntegerField(required=False)
    qqpartbyteoffset = forms.IntegerField(required=False)
    qqtotalfilesize = forms.IntegerField(required=False)
    qqtotalparts = forms.IntegerField(required=False)