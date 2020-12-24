# uncompyle6 version 3.6.7
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/canossa/canossa.py
# Compiled at: 2014-04-25 02:25:23
from stub import *

def _printver():
    import __init__
    print '\ncanossa %s\nCopyright (C) 2012 Hayaki Saito <user@zuse.jp>.\n\nThis program is free software; you can redistribute it and/or modify\nit under the terms of the GNU General Public License as published by\nthe Free Software Foundation; either version 3 of the License, or\n(at your option) any later version.\n\nThis program is distributed in the hope that it will be useful,\nbut WITHOUT ANY WARRANTY; without even the implied warranty of\nMERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the\nGNU General Public License for more details.\n\nYou should have received a copy of the GNU General Public License\nalong with this program. If not, see http://www.gnu.org/licenses/.\n        ' % __init__.__version__


def create(row, col, y, x, termenc, termprop, visibility=False):
    import output, screen
    screen = screen.Screen(row, col, y, x, termenc, termprop)
    return output.Canossa(screen, visibility=visibility)


def main():
    import sys, os, optparse, select
    usage = 'usage: %prog [options] command'
    parser = optparse.OptionParser(usage=usage)
    parser.add_option('-v', '--visible', dest='visibility', action='store_true', default=False, help='bring up the front of terminal (visible mode)')
    parser.add_option('--version', dest='version', action='store_true', default=False, help='show version')
    (options, args) = parser.parse_args()
    if options.version:
        _printver()
        return
    if len(args) > 0:
        command = args[0]
    elif os.getenv('SHELL') is not None:
        command = os.getenv('SHELL')
    else:
        command = '/bin/sh'
    if os.getenv('TERM') is not None:
        term = os.getenv('TERM')
    else:
        term = 'xterm'
    if os.getenv('LANG') is not None:
        lang = os.getenv('LANG')
    else:
        import locale
        lang = '%s.%s' % locale.getdefaultlocale()
    import locale
    (language, encoding) = locale.getdefaultlocale()
    termenc = encoding
    import output
    tty = tff.DefaultPTY(term, lang, command, sys.stdin)
    tty.fitsize()
    if options.visibility:
        outputhandler = output.Canossa(visibility=True, termenc=termenc)
    else:
        canossahandler = output.Canossa(visibility=False, termenc=termenc)
        outputhandler = tff.FilterMultiplexer(canossahandler, tff.DefaultHandler())
    session = tff.Session(tty)
    session.start(termenc=termenc, stdin=sys.stdin, stdout=sys.stdout, outputhandler=outputhandler, buffering=False)
    return


if __name__ == '__main__':
    main()