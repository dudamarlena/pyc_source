# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/simpleweb/plugins/template.py
# Compiled at: 2007-01-10 11:06:24
import sys, os.path, simpleweb.settings, simpleweb.utils
plugins = {}
try:
    from Cheetah.Template import Template
    plugins['Cheetah'] = Template
except ImportError:
    pass

class Cheetah(object):
    __module__ = __name__

    def __init__(self, dir='templates'):
        if not plugins.has_key('Cheetah'):
            simpleweb.utils.optional_dependency_err('Cheetah Template Plugin', 'Cheetah')
        self.dir = dir

    def render(self, template, **kw):
        config = simpleweb.settings.Config('config')
        template_dir = os.path.join(config.working_directory, self.dir)
        os.chdir(template_dir)
        try:
            t = Template(file=template, searchList=[kw])
            t = str(t)
        finally:
            os.chdir(config.working_directory)
        return t