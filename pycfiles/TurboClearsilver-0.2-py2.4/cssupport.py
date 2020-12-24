# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/turboclearsilver/cssupport.py
# Compiled at: 2006-03-22 15:06:21
__version__ = '0.1'
import os, sys
from urllib import urlopen
import neo_cgi
neo_cgi.update()
import neo_util
from turboclearsilver import HDFWrapper
try:
    import tidy
except ImportError:
    tidy = False

class TurboClearsilver:
    __module__ = __name__
    extension = 'cs'

    def __init__(self, extra_vars_func=None, options=None):
        self.get_extra_vars = extra_vars_func
        self.options = options
        self.compiledTemplates = {}
        try:
            self.loadpaths = options['loadpaths']
        except (KeyError, TypeError):
            self.loadpaths = None

        try:
            self.hdfdump = options['hdfdump']
        except (KeyError, TypeError):
            self.hdfdump = False

        try:
            self.normpath = options['normpath']
        except (KeyError, TypeError):
            self.normpath = False

        print 'normpath: %s' % str(self.normpath)
        return

    def render(self, info, format='html', fragment=False, template=None):
        """
        Renders the template to a string using the provided info.
        info: dict of variables to pass into template
        format: can only be "html" at this point
        template: path to template
        """
        if isinstance(info, dict):
            hdf = HDFWrapper(loadpaths=self.loadpaths)
            for (key, value) in info.items():
                hdf[key] = value

            info = hdf.hdf
        if isinstance(template, (str, unicode)):
            if self.normpath:
                filename = template
            else:
                filename = '%s.%s' % (os.path.join(*template.split('.')), self.extension)
            import neo_cs
            cs_template = neo_cs.CS(info)
            cs_template.parseFile(filename)
        elif isinstance(template, neo_cs.CS):
            cs_template = template
        if self.hdfdump:
            return str(hdf)
        return cs_template.render()

    def load_template(self, templatename):
        """ unused but required by tg """
        pass

    def transform(self, info, template):
        """ unused but required by tg """
        pass