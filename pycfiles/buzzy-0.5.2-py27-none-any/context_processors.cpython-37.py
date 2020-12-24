# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/accounts/context_processors.py
# Compiled at: 2020-05-05 16:46:09
# Size of source mod 2**32: 127 bytes
from django.contrib.auth.forms import AuthenticationForm

def forms(request):
    return {'login_form': AuthenticationForm()}