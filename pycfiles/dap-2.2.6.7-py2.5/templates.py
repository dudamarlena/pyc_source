# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/dap/wsgi/templates.py
# Compiled at: 2008-03-31 07:43:21
import os
from paste.script import templates

class DapServerTemplate(templates.Template):
    summary = 'A DAP server deployed through paste.deploy'
    egg_plugins = [
     'dap[server]']
    _template_dir = 'paster_templates'
    use_cheetah = True

    def post(self, command, output_dir, vars):
        if command.verbose:
            print '*' * 72
            print '* Run "paster serve %s/server.ini" to run' % output_dir
            print '* the DAP server on http://localhost:8080'
            print '*' * 72