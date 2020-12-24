# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/buildutils/command/flakes.py
# Compiled at: 2007-08-08 19:58:56
"""
Uses the pyflakes library to find lint in all modules.

From the pyflakes_ project page:

    Pyflakes is a simple program which checks Python source files for
    errors. It is similar to PyChecker in scope, but differs in that it
    does not execute the modules to check them. This is both safer and
    faster, although it does not perform as many checks. Unlike PyLint,
    Pyflakes checks only for logical errors in programs; it does not
    perform any checks on style.

.. _pyflakes: http://divmod.org/projects/pyflakes

"""
from distutils import log
from buildutils.cmd import Command

class flakes(Command):
    __module__ = __name__
    description = 'check source files for errors and inefficiencies'
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def check(self, module, file):
        import compiler, sys, traceback, pyflakes
        log.debug('checking file %r', file)
        code = open(file, 'r').read()
        try:
            tree = compiler.parse(code)
        except (SyntaxError, IndentationError):
            print >> sys.stderr, 'could not compile %r. Traceback:' % (file,)
            traceback.print_exc(0, sys.stderr)
        else:
            w = pyflakes.Checker(tree, file)
            w.messages.sort(lambda a, b: cmp(a.lineno, b.lineno))
            for warning in w.messages:
                self.warn(warning)

    def run(self):
        self.require('pyflakes')
        base = self.get_finalized_command('build_py')
        for (package, module, file) in base.find_all_modules():
            self.check(module, file)