# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.5-i386/egg/aodag/util/mkpkg.py
# Compiled at: 2010-06-25 05:31:43
import sys, os
from optparse import OptionParser
init_tmpl = "try:\n    __import__('pkg_resources').declare_namespace(__name__)\nexcept ImportError:\n    from pkgutil import extend_path\n    __path__ = extend_path(__path__, __name__)\n\n"

def main():
    parser = OptionParser()
    parser.add_option('-n', '--declare-namespace', dest='declare_namespace', help='add namespace statement to __init__.py', action='store_true', default=False)
    (options, args) = parser.parse_args()
    pkg = args[0]
    names = pkg.split('.')
    names = reduce(lambda x, y: x + [x[(-1)] + '/' + y], names, ['.'])
    for name in names:
        if not os.path.exists(name):
            os.mkdir(name)
            initpy = os.path.join(name, '__init__.py')
            f = open(initpy, 'w')
            if name != names[(-1)] and options.declare_namespace:
                f.write(init_tmpl)
            f.close()