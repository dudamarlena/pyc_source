# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/layers/loaders/app_directories.py
# Compiled at: 2018-03-27 03:51:51
from django.template.utils import get_app_template_dirs
from layers.loaders.filesystem import Loader as FilesystemLoader

class Loader(FilesystemLoader):

    def get_dirs(self):
        return get_app_template_dirs('templates')