# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hedley/django/instances/mote/mote/loaders/app_directories.py
# Compiled at: 2016-12-01 10:32:24
# Size of source mod 2**32: 417 bytes
import os
from django.template.utils import get_app_template_dirs
from django.template.loaders.filesystem import Loader as FilesystemLoader

class Loader(FilesystemLoader):

    def get_dirs(self):
        return get_app_template_dirs(os.path.join('..', 'mote', 'projects')) + get_app_template_dirs(os.path.join('mote', 'projects'))