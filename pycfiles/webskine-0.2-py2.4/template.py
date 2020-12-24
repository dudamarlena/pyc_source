# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/webskine/template.py
# Compiled at: 2008-05-28 15:16:57
import os
from paste.script import templates

class WebskineTemplate(templates.Template):
    __module__ = __name__
    summary = 'A Webskine blog deployed through paste.deploy'
    egg_plugins = [
     'webskine']
    _template_dir = 'paster_templates'
    use_cheetah = True

    def post(self, command, output_dir, vars):
        if command.verbose:
            print '*' * 72
            print '* Run "paster serve %s/server.ini" to run' % output_dir
            print '* the Webskine on http://localhost:8080'
            print '*' * 72