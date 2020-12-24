# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\buffetmyghty\myghtysupport.py
# Compiled at: 2006-07-20 21:25:47
import os
try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

from myghty.interp import Interpreter

class MyghtyTemplatePlugin(object):
    __module__ = __name__
    extension = 'myt'

    def __init__(self, extra_vars_func=None, config=None):
        self.get_extra_vars = extra_vars_func
        self.config = config or {}
        if callable(self.get_extra_vars):
            extra_vars = self.get_extra_vars()
        else:
            extra_vars = dict()
        config['global_args'] = extra_vars
        config['allow_globals'] = extra_vars.keys()
        self.interpreter = Interpreter(**config)

    def _get_template_path(self, dotted_tmpl_path):
        parts = dotted_tmpl_path.split('.')
        template_file_path = os.path.join(*parts)
        return template_file_path

    def load_template(self, template_path):
        pass

    def render(self, info, format='html', fragment=False, template=None):
        vars = info
        template_path = '%s.%s' % (self._get_template_path(template), self.extension)
        buf = StringIO()
        if fragment:
            self.interpreter.execute(template_path, request_args=vars, out_buffer=buf, disable_wrapping=True)
        else:
            self.interpreter.execute(template_path, request_args=vars, out_buffer=buf)
        return buf.getvalue()