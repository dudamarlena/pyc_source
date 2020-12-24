# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/rhubarbtart/tart_template.py
# Compiled at: 2006-01-25 19:20:39
import os
from paste.script.templates import Template

class RhubarbTart(Template):
    __module__ = __name__
    _template_dir = 'paste_templates/rhubarbtart'
    summary = 'A RhubarbTart web application'
    egg_plugins = [
     'RhubarbTart']
    required_templates = [
     'PasteDeploy#paste_deploy']

    def post(self, command, output_dir, vars):
        fn = os.path.join(output_dir, 'docs', 'devel_config.ini')
        if os.path.exists(fn) and not command.simulate:
            try:
                os.chmod(fn, 73 | os.stat(fn).st_mode)
            except Exception, e:
                print 'Could not make %s executable: %s' % (fn, e)
            else:
                print 'Run %s to start a development server' % fn