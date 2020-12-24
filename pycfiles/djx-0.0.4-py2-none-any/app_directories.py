# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-n_sfyb/Django/django/template/loaders/app_directories.py
# Compiled at: 2019-02-14 00:35:17
"""
Wrapper for loading templates from "templates" directories in INSTALLED_APPS
packages.
"""
from django.template.utils import get_app_template_dirs
from .filesystem import Loader as FilesystemLoader

class Loader(FilesystemLoader):

    def get_dirs(self):
        return get_app_template_dirs('templates')