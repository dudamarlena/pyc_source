# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/gsquickstart/template.py
# Compiled at: 2007-11-27 16:10:30
import os
from glob import glob
from turbogears.command.quickstart import TGTemplate
import pkg_resources

class GenshiTemplate(TGTemplate):
    __module__ = __name__
    required_templates = [
     'turbogears']
    _template_dir = pkg_resources.resource_filename('gsquickstart.templates', 'quickstart')
    summary = 'web framework with genshi'
    use_cheetah = True

    def post(self, command, output_dir, vars):
        TGTemplate.post(self, command, output_dir, vars)
        for file in ['login.kid', 'master.kid', 'welcome.kid']:
            path = os.path.join(output_dir, vars['package'], 'templates', file)
            question = "Delete Kid template '%s'" % command.shorten(path)
            if os.path.exists(path) and command.command_name != 'update' or command.ask(question, default=False):
                try:
                    os.remove(path)
                    print 'Removing', path
                except OSError:
                    pass