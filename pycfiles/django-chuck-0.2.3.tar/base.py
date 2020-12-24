# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /data/django-chuck/django_chuck/template/base.py
# Compiled at: 2012-06-01 04:12:37
from django_chuck.utils import find_chuck_module_path

class BaseEngine(object):
    module_basedir = find_chuck_module_path()
    site_dir = ''
    project_dir = ''

    def __init__(self, site_dir, project_dir):
        self.site_dir = site_dir
        self.project_dir = project_dir

    def handle(self, input_file, output_file, placeholder):
        raise NotImplementedError()