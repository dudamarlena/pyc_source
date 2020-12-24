# uncompyle6 version 3.6.7
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/pylonsgenshi/template.py
# Compiled at: 2008-01-03 15:16:00
from paste.script.templates import Template

class PylonsGenshiTemplate(Template):
    _template_dir = 'templates/default'
    summary = 'Pylons+Genshi template'
    egg_plugins = ['Pylons', 'Genshi']

    def pre(self, command, output_dir, vars):
        """Called before template is applied."""
        package_logger = vars['package']
        if package_logger == 'root':
            package_logger = 'app'
        vars['package_logger'] = package_logger