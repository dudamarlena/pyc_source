# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-i386/egg/djangomako/template.py
# Compiled at: 2008-09-20 01:20:48
from mako.template import Template as MakoTemplate
import middleware
django_variables = [
 'lookup', 'template_dirs', 'output_encoding',
 'module_directory', 'encoding_errors']

class Template(MakoTemplate):

    def __init__(self, *args, **kwargs):
        """Overrides base __init__ to provide django variable overrides"""
        if not kwargs.get('no_django', False):
            overrides = dict([ (k, getattr(middleware, k, None)) for k in django_variables ])
            kwargs.update(overrides)
        super(Template, self).__init__(*args, **kwargs)
        return