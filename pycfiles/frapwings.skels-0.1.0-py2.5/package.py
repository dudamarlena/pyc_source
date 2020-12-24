# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-i386/egg/frapwings/skels/package.py
# Compiled at: 2010-10-11 10:04:59
from paste.script.templates import var
from paste.script.templates import Template
from datetime import date

class Package(Template):
    """Package Template"""
    _template_dir = 'tmpl/package'
    summary = 'A namespaced package with a enviroment'
    vars = [
     var('namespace_package', 'Namespace package', default='frapwings'),
     var('package', 'The package contained', default='example'),
     var('version', 'Version', default='0.1.0'),
     var('description', 'One-line description of the package'),
     var('author', 'Author name'),
     var('author_email', 'Author email'),
     var('keywords', 'Space-separeted keywords/tags'),
     var('url', 'URL of homepage'),
     var('license_name', 'License name', default='GPL')]

    def check_vars(self, vars, command):
        """check vars"""
        if not command.options.no_interactive and not hasattr(command, '_deleted_once'):
            del vars['package']
            command._deleted_once = True
        return Template.check_vars(self, vars, command)

    def pre(self, command, output_dir, vars):
        """ Called before template is applied.  """
        vars['date_now'] = date.today().isoformat()

    def post(self, command, output_dir, vars):
        """ Called after template is applied.  """
        pass