# uncompyle6 version 3.7.4
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\turbocheetah\cheetahsupport.py
# Compiled at: 2007-11-18 05:39:48
"""Template support for Cheetah"""
import sys
from os import stat
from imp import new_module
from threading import RLock
from logging import getLogger
from pkg_resources import resource_filename
from Cheetah import Compiler
log = getLogger('turbokid.kidsupport')

def _compile_template(package, basename, tfile):
    code = str(Compiler.Compiler(file=tfile, mainClassName=basename))
    modname = '%s.%s' % (package, basename)
    mod = new_module(modname)
    ns = dict()
    exec code in ns
    mainclass = ns[basename]
    setattr(mod, basename, mainclass)
    sys.modules[modname] = mod
    return mod


class CheetahSupport(object):
    __module__ = __name__
    extension = '.tmpl'
    importhooks = False
    precompiled = False

    def __init__(self, extra_vars_func=None, options=None):
        if options is None:
            options = dict()
        self.get_extra_vars = extra_vars_func
        self.options = options
        self.compiledTemplates = {}
        self.precompiled = options.get('cheetah.precompiled', CheetahSupport.precompiled)
        if not self.precompiled:
            self.compile_lock = RLock()
        if not CheetahSupport.importhooks and options.get('cheetah.importhooks', False):
            from Cheetah import ImportHooks
            ImportHooks.install(templateFileExtensions=(self.extension,))
            CheetahSupport.importhooks = True
        return

    def load_template(self, template):
        """Search for a template along the Python path.

        Cheetah template files must end in ".tmpl" and
        must be contained in legitimate Python packages.

        """
        if not template:
            raise ValueError, 'You must pass a template as parameter'
        divider = template.rfind('.')
        if divider > -1:
            (package, basename) = (
             template[:divider], template[divider + 1:])
        else:
            raise ValueError, 'All Cheetah templates must be in a package'
        if self.precompiled:
            mod = __import__(template, dict(), dict(), [basename])
        else:
            tfile = resource_filename(package, basename + self.extension)
            ct = self.compiledTemplates
            self.compile_lock.acquire()
            try:
                try:
                    mtime = stat(tfile).st_mtime
                except OSError:
                    mtime = None

                if ct.has_key(template):
                    if ct[template] == mtime:
                        mod = __import__(template, dict(), dict(), [basename])
                    else:
                        del sys.modules[template]
                        mod = _compile_template(package, basename, tfile)
                        ct[template] = mtime
                else:
                    mod = _compile_template(package, basename, tfile)
                    ct[template] = mtime
            finally:
                self.compile_lock.release()
        mainclass = getattr(mod, basename)
        return mainclass
        return

    def render(self, info, format='html', fragment=False, template=None):
        """Renders data in the desired format.

        @param info: the data itself
        @type info: dict
        @param format: Cheetah output method (not used)
        @type format: string
        @param fragment: passed through to tell the template if only a
                         fragment of a page is desired
        @type fragment: bool
        @param template: the name of the Cheetah template to use
        @type template: string
        """
        tempclass = self.load_template(template)
        if self.get_extra_vars:
            extra = self.get_extra_vars()
        else:
            extra = {}
        tempobj = tempclass(searchList=[info, extra])
        if fragment:
            return tempobj.fragment()
        else:
            return tempobj.respond()