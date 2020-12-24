# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/pylogo/script.py
# Compiled at: 2007-10-14 14:35:27
import os, sys, optparse
try:
    here = __file__
except NameError:
    here = sys.argv[0]

parser = optparse.OptionParser(usage='%prog [OPTIONS]')
parser.add_option('-c', '--console', help='Run the interpreter in the console (not the GUI)', action='store_true', dest='console')
parser.add_option('-q', '--quit', help='Quit after loading and running files', action='store_true', dest='quit_after')
parser.add_option('--doctest', help='Doctest the given (text) files', action='store_true', dest='doctest')
from pylogo import Logo

def main():
    doit(sys.argv[1:])


def doit(args):
    (options, filenames) = parser.parse_args(args)
    if options.doctest:
        from pylogo.logodoctest import testfile
        import doctest
        for fn in filenames:
            print '-- Testing %s %s' % (fn, '-' * (40 - len(fn)))
            testfile(fn, optionflags=doctest.ELLIPSIS, verbose_summary=True, interp=Logo)

    else:
        for fn in filenames:
            Logo.import_logo(filename)

        if options.quit_after:
            return
        if options.console:
            Logo.input_loop(sys.stdin, sys.stdout)
        else:
            from pylogo import ide
            ide.main()