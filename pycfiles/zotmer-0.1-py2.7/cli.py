# uncompyle6 version 3.7.4
# PyPy Python bytecode 2.7 (62218)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/zotmer/cli.py
# Compiled at: 2017-01-24 17:59:35
"""
Usage:
    zot [options] <command> [<args>...]

options:
    --help          print usage information
    -V, --version   print version information
"""
import importlib, os, pkgutil, sys, docopt
from pykmer.file import autoremove
import commands

def mainInner():
    args = docopt.docopt(__doc__, version='Zotmer k-mer toolkit 0.1', options_first=True)
    if args['<command>'] == 'help' and len(args['<args>']) != 1:
        print __doc__
        print 'Available commands:'
        for _, name, is_pkg in pkgutil.iter_modules([commands.__path__[0]]):
            print '\t' + name

        print '\nuse "zot help <command>" for command specific help.'
        return 0
    if args['<command>'] == 'help' and len(args['<args>']) == 1:
        modname = commands.__name__ + '.' + args['<args>'][0]
        try:
            argv = [
             args['<command>']] + args['<args>']
            m = importlib.import_module(modname)
            print m.__doc__
            return 0
        except ImportError:
            print >> sys.stderr, "unable to load command `%s', use `zot help` for help." % (args['<command>'],)
            return 1

    modname = commands.__name__ + '.' + args['<command>']
    try:
        argv = [
         args['<command>']] + args['<args>']
        m = importlib.import_module(modname)
        return m.main(argv)
    except ImportError:
        print >> sys.stderr, "unable to load command `%s', use `zot help` for help." % (args['<command>'],)
        return 1


def main():
    try:
        with autoremove():
            mainInner()
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()