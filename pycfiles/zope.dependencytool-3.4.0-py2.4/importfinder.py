# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/zope/dependencytool/importfinder.py
# Compiled at: 2007-09-21 15:26:02
"""Helper to locate all the imports from a single source file.

$Id: importfinder.py 27164 2004-08-17 11:16:39Z hdima $
"""
import sys, token, tokenize
from zope.dependencytool.dependency import Dependency
START = '<start>'
FROM = '<from>'
FROM_IMPORT = '<from-import>'
IMPORT = '<import>'
COLLECTING = '<collecting>'
SWALLOWING = '<swallowing>'
TOK_COMMA = (
 token.OP, ',')
TOK_IMPORT = (token.NAME, 'import')
TOK_FROM = (token.NAME, 'from')
TOK_NEWLINE = (token.NEWLINE, '\n')
TOK_ENDMARK = (token.ENDMARKER, '')
dotjoin = ('.').join

class ImportFinder(object):
    __module__ = __name__

    def __init__(self, packages=False):
        """Initialize the import finder.

        `packages` -- if true, reports package names rather than
          module names
        """
        self.packages = packages
        self.module_checks = {}
        self.deps = []
        self.imported_names = {}

    def get_imports(self):
        return self.deps

    def find_imports(self, f, path, package=None):
        """Find all the imported names in a source file.

        `f` -- open file
        `path` -- path of the source file
        `package` -- Python package the source file is contained in, or None
        """
        self.path = path
        self.package = package
        self.state = START
        self.post_name_state = None
        prevline = None
        try:
            for t in tokenize.generate_tokens(f.readline):
                (type, string, start, end, line) = t
                self.transition(type, string, start[0])

        except:
            print >> sys.stderr, 'error finding imports in', path
            raise

        return

    def add_import(self, name, lineno):
        """Record an import for `name`.

        `name` -- full dotted name as found in an import statement
          (may still be relative)

        `lineno` -- line number the import was found on
        """
        if self.package:
            fullname = '%s.%s' % (self.package, name)
            self.check_module_name(fullname)
            if not self.module_checks[fullname]:
                fullname = fullname[:fullname.rfind('.')]
                self.check_module_name(fullname)
            if self.module_checks[fullname]:
                name = fullname
        if name not in self.module_checks:
            self.check_module_name(name)
            if not self.module_checks[name] and '.' in name:
                name = dotjoin(name.split('.')[:-1])
                self.check_module_name(name)
        if self.module_checks[name] and name != '__main__':
            if self.packages:
                name = package_for_module(name)
                if name is None:
                    return
            self.deps.append(Dependency(name, self.path, lineno))
        return

    def check_module_name(self, name):
        """Check whether 'name' is a module name.  Update module_checks."""
        try:
            __import__(name)
        except ImportError:
            self.module_checks[name] = False
        else:
            self.module_checks[name] = name in sys.modules

    def transition(self, type, string, lineno):
        if type == tokenize.COMMENT:
            return
        entry = self.state_table.get((self.state, (type, string)))
        if entry is not None:
            self.state = entry[0]
            for action in entry[2:]:
                meth = getattr(self, 'action_' + action)
                meth(type, string, lineno)

            if entry[1] is not None:
                self.post_name_state = entry[1]
        elif self.state == COLLECTING:
            name = self.name
            if type == token.NAME and name and not name.endswith('.'):
                self.state = SWALLOWING
                if self.prefix:
                    self.name = '%s.%s' % (self.prefix, name)
            else:
                self.name += string
        elif self.state in (START, SWALLOWING):
            pass
        else:
            raise RuntimeError('invalid transition: %s %r' % (self.state, (type, string)))
        return

    state_table = {(START, TOK_IMPORT): (COLLECTING, IMPORT, 'reset'), (START, TOK_FROM): (COLLECTING, FROM, 'reset'), (FROM, TOK_IMPORT): (COLLECTING, FROM_IMPORT, 'setprefix'), (FROM_IMPORT, TOK_COMMA): (COLLECTING, FROM_IMPORT), (IMPORT, TOK_COMMA): (COLLECTING, IMPORT), (COLLECTING, TOK_COMMA): (COLLECTING, None, 'save', 'poststate'), (COLLECTING, TOK_IMPORT): (COLLECTING, FROM_IMPORT, 'setprefix'), (SWALLOWING, TOK_COMMA): (None, None, 'save', 'poststate'), (FROM_IMPORT, TOK_NEWLINE): (START, None, 'save', 'reset'), (COLLECTING, TOK_NEWLINE): (START, None, 'save', 'reset'), (SWALLOWING, TOK_NEWLINE): (START, None, 'save', 'reset'), (FROM_IMPORT, TOK_ENDMARK): (START, None, 'save', 'reset'), (COLLECTING, TOK_ENDMARK): (START, None, 'save', 'reset'), (SWALLOWING, TOK_ENDMARK): (START, None, 'save', 'reset')}

    def action_reset(self, type, string, lineno):
        self.name = ''
        self.prefix = None
        return

    def action_save(self, type, string, lineno):
        if self.name:
            assert not self.name.endswith('.'), repr(self.name)
            name = self.name
            if self.prefix:
                name = '%s.%s' % (self.prefix, name)
            self.add_import(name, lineno)
            self.name = ''

    def action_setprefix(self, type, string, lineno):
        assert self.name, repr(self.name)
        assert not self.name.endswith('.'), repr(self.name)
        self.prefix = self.name
        self.name = ''

    def action_collect(self, type, string, lineno):
        self.name += string

    def action_poststate(self, type, string, lineno):
        self.state = self.post_name_state
        self.post_name_state = None
        self.transition(type, string, lineno)
        return


def package_for_module(name):
    """Return the package name for the module named `name`."""
    __import__(name)
    module = sys.modules[name]
    if not hasattr(module, '__path__'):
        if '.' in name:
            name = name[:name.rfind('.')]
        else:
            name = None
    return name


def module_for_importable(name):
    """Return the module name for the importable object `name`."""
    try:
        __import__(name)
    except ImportError:
        while '.' in name:
            name = name[:name.rfind('.')]
            try:
                __import__(name)
            except ImportError:
                pass
            else:
                break

        return

    return name