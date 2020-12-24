# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/niedbalski/src/vcs/vcs/extras.py
# Compiled at: 2016-04-08 09:25:43
import _ast, os, sys
from setuptools import Command

def check(filename):
    from pyflakes import reporter as mod_reporter
    from pyflakes.checker import Checker
    codeString = open(filename).read()
    reporter = mod_reporter._makeDefaultReporter()
    try:
        tree = compile(codeString, filename, 'exec', _ast.PyCF_ONLY_AST)
    except SyntaxError:
        value = sys.exc_info()[1]
        msg = value.args[0]
        lineno, offset, text = value.lineno, value.offset, value.text
        if text is None:
            reporter.unexpectedError(filename, 'problem decoding source')
        else:
            reporter.syntaxError(filename, msg, lineno, offset, text)
        return 1
    except Exception:
        reporter.unexpectedError(filename, 'problem decoding source')
        return 1

    lines = codeString.splitlines()
    warnings = Checker(tree, filename)
    warnings.messages.sort(key=lambda m: m.lineno)
    real_messages = []
    for m in warnings.messages:
        line = lines[(m.lineno - 1)]
        if 'pyflakes:ignore' in line.rsplit('#', 1)[(-1)]:
            pass
        else:
            real_messages.append(m)
            reporter.flake(m)

    return len(real_messages)
    return


class RunFlakesCommand(Command):
    """
    Runs pyflakes against guardian codebase.
    """
    description = 'Check sources with pyflakes'
    user_options = []
    ignore = ['__init__.py', '__main__.py', 'hgcompat.py']

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            import pyflakes
        except ImportError:
            sys.stderr.write('No pyflakes installed!\n')
            sys.exit(-1)

        thisdir = os.path.dirname(__file__)
        vcsdir = os.path.join(thisdir, 'vcs')
        warns = 0
        for topdir, dirnames, filenames in os.walk(vcsdir):
            filenames = (f for f in filenames if f not in self.ignore)
            paths = (os.path.join(topdir, f) for f in filenames if f.endswith('.py'))
            for path in paths:
                if path.endswith('tests/__init__.py'):
                    continue
                warns += check(path)

        if warns > 0:
            sys.stderr.write('ERROR: Finished with total %d warnings.\n' % warns)
            sys.exit(1)
        else:
            print 'No problems found in source codes.'