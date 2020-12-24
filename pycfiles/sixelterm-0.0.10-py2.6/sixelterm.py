# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-intel/egg/sixelterm/sixelterm.py
# Compiled at: 2012-11-26 08:25:13


def main():
    import sys, os, optparse, select
    usage = 'usage: %prog [options] command'
    parser = optparse.OptionParser(usage=usage)
    parser.add_option('--version', dest='version', action='store_true', default=False, help='show version')
    (options, args) = parser.parse_args()
    if options.version:
        import __init__
        print '\nsixelterm %s\nCopyright (C) 2012 Hayaki Saito <user@zuse.jp>. \n\nThis program is free software; you can redistribute it and/or modify\nit under the terms of the GNU General Public License as published by\nthe Free Software Foundation; either version 3 of the License, or\n(at your option) any later version.\n\nThis program is distributed in the hope that it will be useful,\nbut WITHOUT ANY WARRANTY; without even the implied warranty of\nMERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the\nGNU General Public License for more details.\n\nYou should have received a copy of the GNU General Public License\nalong with this program. If not, see http://www.gnu.org/licenses/.\n        ' % __init__.__version__
        return
    else:
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
        import termios, scanner, tff
        t = termios.tcgetattr(0)
        backup = termios.tcgetattr(0)
        t[1] &= ~termios.ONLCR
        termios.tcsetattr(0, termios.TCSANOW, t)
        tty = tff.DefaultPTY(term, lang, command, sys.stdin)
        t = termios.tcgetattr(0)
        t[1] |= termios.ONLCR
        termios.tcsetattr(0, termios.TCSANOW, t)
        tty.fitsize()
        session = tff.Session(tty)
        session.start(termenc=termenc, stdin=sys.stdin, stdout=sys.stdout, outputscanner=scanner.ImageAwareScanner())
        return


if __name__ == '__main__':
    main()