# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/mrdon/dev/flask-async/venv/lib/python3.3/site-packages/flask/exthook.py
# Compiled at: 2014-01-20 12:41:11
# Size of source mod 2**32: 5087 bytes
"""
    flask.exthook
    ~~~~~~~~~~~~~

    Redirect imports for extensions.  This module basically makes it possible
    for us to transition from flaskext.foo to flask_foo without having to
    force all extensions to upgrade at the same time.

    When a user does ``from flask.ext.foo import bar`` it will attempt to
    import ``from flask_foo import bar`` first and when that fails it will
    try to import ``from flaskext.foo import bar``.

    We're switching from namespace packages because it was just too painful for
    everybody involved.

    This is used by `flask.ext`.

    :copyright: (c) 2014 by Armin Ronacher.
    :license: BSD, see LICENSE for more details.
"""
import sys, os
from ._compat import reraise

class ExtensionImporter(object):
    __doc__ = 'This importer redirects imports from this submodule to other locations.\n    This makes it possible to transition from the old flaskext.name to the\n    newer flask_name without people having a hard time.\n    '

    def __init__(self, module_choices, wrapper_module):
        self.module_choices = module_choices
        self.wrapper_module = wrapper_module
        self.prefix = wrapper_module + '.'
        self.prefix_cutoff = wrapper_module.count('.') + 1

    def __eq__(self, other):
        return self.__class__.__module__ == other.__class__.__module__ and self.__class__.__name__ == other.__class__.__name__ and self.wrapper_module == other.wrapper_module and self.module_choices == other.module_choices

    def __ne__(self, other):
        return not self.__eq__(other)

    def install(self):
        sys.meta_path[:] = [x for x in sys.meta_path if self != x] + [self]

    def find_module(self, fullname, path=None):
        if fullname.startswith(self.prefix):
            return self

    def load_module(self, fullname):
        if fullname in sys.modules:
            return sys.modules[fullname]
        else:
            modname = fullname.split('.', self.prefix_cutoff)[self.prefix_cutoff]
            for path in self.module_choices:
                realname = path % modname
                try:
                    __import__(realname)
                except ImportError:
                    exc_type, exc_value, tb = sys.exc_info()
                    sys.modules.pop(fullname, None)
                    if self.is_important_traceback(realname, tb):
                        reraise(exc_type, exc_value, tb.tb_next)
                    continue

                module = sys.modules[fullname] = sys.modules[realname]
                if '.' not in modname:
                    setattr(sys.modules[self.wrapper_module], modname, module)
                return module

            raise ImportError('No module named %s' % fullname)
            return

    def is_important_traceback(self, important_module, tb):
        """Walks a traceback's frames and checks if any of the frames
        originated in the given important module.  If that is the case then we
        were able to import the module itself but apparently something went
        wrong when the module was imported.  (Eg: import of an import failed).
        """
        while tb is not None:
            if self.is_important_frame(important_module, tb):
                return True
            tb = tb.tb_next

        return False

    def is_important_frame(self, important_module, tb):
        """Checks a single frame if it's important."""
        g = tb.tb_frame.f_globals
        if '__name__' not in g:
            return False
        module_name = g['__name__']
        if module_name == important_module:
            return True
        filename = os.path.abspath(tb.tb_frame.f_code.co_filename)
        test_string = os.path.sep + important_module.replace('.', os.path.sep)
        return test_string + '.py' in filename or test_string + os.path.sep + '__init__.py' in filename