# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\django_synth\loaders.py
# Compiled at: 2014-09-09 11:26:43
from django.template.loaders import app_directories, filesystem
from django_synth.template import SynthTemplate

class AppDirectoriesLoader(app_directories.Loader):
    is_usable = True

    def load_template(self, template_name, template_dirs=None):
        source, origin = self.load_template_source(template_name, template_dirs)
        template = SynthTemplate(source, template_dirs, template_name)
        return (template, origin)


class FilesystemLoader(filesystem.Loader):
    is_usable = True

    def load_template(self, template_name, template_dirs=None):
        source, origin = self.load_template_source(template_name, template_dirs)
        template = SynthTemplate(source, template_dirs, template_name)
        return (template, origin)