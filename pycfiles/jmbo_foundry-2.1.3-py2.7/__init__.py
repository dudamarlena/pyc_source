# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/foundry/__init__.py
# Compiled at: 2015-01-27 08:59:34


def get_model():
    from foundry.models import FoundryComment
    return FoundryComment


def get_form():
    from foundry.forms import CommentForm
    return CommentForm


import os
from django.core.files.storage import FileSystemStorage

def FileSystemStorage_listdir(self, path):
    if not self.exists(path):
        return ([], [])
    path = self.path(path)
    directories, files = [], []
    for entry in os.listdir(path):
        if os.path.isdir(os.path.join(path, entry)):
            directories.append(entry)
        else:
            files.append(entry)

    return (
     directories, files)


FileSystemStorage.listdir = FileSystemStorage_listdir