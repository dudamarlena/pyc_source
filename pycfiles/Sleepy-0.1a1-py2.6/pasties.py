# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.4-i386/egg/sleepy/pasties.py
# Compiled at: 2011-05-12 00:09:06
from paste.script.templates import Template
from paste.deploy.converters import asbool
from tempita import paste_script_template_renderer

class SleepyTemplate(Template):
    _template_dir = 'templates/default_project'
    template_renderer = staticmethod(paste_script_template_renderer)
    summary = 'Sleepy Pylons project template'
    egg_plugins = ('PasteScript', 'Pylons')
    ensure_names = ('description', 'author', 'author_email', 'url')

    def pre(self, command, output_dir, vars):
        for name in self.ensure_names:
            vars.setdefault(name, '')

        vars['version'] = vars.get('version', '0.1')
        vars['zip_safe'] = asbool(vars.get('zip_safe', 'false'))