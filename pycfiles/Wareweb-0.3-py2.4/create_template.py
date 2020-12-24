# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/wareweb/create_template.py
# Compiled at: 2006-10-22 17:17:11
import os
from paste.script.templates import Template

class Wareweb(Template):
    __module__ = __name__
    _template_dir = 'paster_templates/wareweb'
    summary = 'A Wareweb web application'
    egg_plugins = [
     'Wareweb']
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