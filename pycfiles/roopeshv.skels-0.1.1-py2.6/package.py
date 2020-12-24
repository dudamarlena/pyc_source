# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/roopeshv/skels/package.py
# Compiled at: 2010-06-14 19:48:43
from paste.script.templates import var
from paste.script.templates import Template

class Package(Template):
    """Package Template"""
    _template_dir = 'tmpl/package'
    summary = 'A namespaced package with a test environment'
    use_cheetah = True
    vars = [var('namespace_package', 'Namespace package', default='roopeshv'),
     var('package', 'The package contained', default='example'),
     var('version', 'Version', default='0.1.0'),
     var('description', 'One-line description of the package'),
     var('author', 'Author name'),
     var('author_email', 'Author email'),
     var('keywords', 'Space spereated keywords/tags'),
     var('url', 'URL of homepage'),
     var('license_name', 'License name', default='GPL')]

    def check_vars(self, vars, command):
        if not command.options.no_interactive and not hasattr(command, '_deleted_once'):
            del vars['package']
            command._deleted_once = True
        return Template.check_vars(self, vars, command)