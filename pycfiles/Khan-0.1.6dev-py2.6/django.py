# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/khan/project/django.py
# Compiled at: 2010-05-16 12:13:08
import os, sys
from paste.script.templates import var
from core import ProjectTemplate

class DjangoTemplate(ProjectTemplate):
    _template_dir = 'templates/django'
    summary = 'Khan django project'
    vars = [
     var('django-admin', 'Path to your "django-admin.py" command', default='django-admin.py')]

    def pre(self, command, output_dir, vars):
        if not os.path.isdir(output_dir):
            os.makedirs(output_dir)
        cwd = os.getcwd()
        os.chdir(output_dir)
        sts = os.system(vars['django-admin'] + ' startproject ' + vars['package'])
        os.chdir(cwd)
        if sts != 0:
            sys.exit(sts)