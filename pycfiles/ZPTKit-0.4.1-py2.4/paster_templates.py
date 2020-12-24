# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/ZPTKit/paster_templates.py
# Compiled at: 2006-06-20 16:13:48
import os
from paste.script.templates import Template

class ZPT(Template):
    __module__ = __name__
    _template_dir = 'paster_templates/zpt'
    summary = 'A Zope Page Template project'

    def post(self, command, output_dir, vars):
        setup = os.path.join(output_dir, 'setup.py')
        command.insert_into_file(setup, 'package_data', "%r: ['templates/*.pt', 'templates/admin/*.pt'],\n" % vars['package'], indent=True)