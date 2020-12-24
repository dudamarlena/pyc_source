# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/eggchecker/runflakes.py
# Compiled at: 2007-10-24 09:46:20
"""
script that runs pyflake
"""
import compiler, sys, os
from pyflakes import Checker as FlakeChecker

def check(code_string, filename):
    """checks a code string"""
    try:
        tree = compiler.parse(code_string)
    except (SyntaxError, IndentationError):
        value = sys.exc_info()[1]
        try:
            (lineno, offset, line) = value[1][1:]
        except IndexError:
            print >> sys.stderr, 'could not compile %r' % (filename,)
            return 1
        else:
            if line.endswith('\n'):
                line = line[:-1]
            print >> sys.stderr, '%s:%d: could not compile' % (filename, lineno)
            print >> sys.stderr, line
            print >> sys.stderr, ' ' * (offset - 2), '^'
            return 1
    else:
        w = FlakeChecker(tree, filename)
        w.messages.sort(lambda a, b: cmp(a.lineno, b.lineno))
        for warning in w.messages:
            print warning

        return len(w.messages)


def check_path(filename):
    """checks code in a path"""
    if os.path.exists(filename):
        return check(file(filename, 'U').read(), filename)


def run_flake():
    """run flake over the whole directory"""
    warnings = 0
    for (dirpath, dirnames, filenames) in os.walk(os.curdir):
        for filename in filenames:
            if filename.endswith('.py'):
                warnings += check_path(os.path.join(dirpath, filename))

    raise SystemExit(warnings > 0)