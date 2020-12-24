# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-intel/egg/drcsterm/drcsterm.py
# Compiled at: 2014-02-11 00:51:00


def main():
    import sys, os, optparse, logging
    usage = 'usage: %prog [options] [command | - ]'
    parser = optparse.OptionParser(usage=usage)
    parser.add_option('--version', dest='version', action='store_true', default=False, help='show version')
    parser.add_option('-t', '--term', dest='term', help='override TERM environment variable')
    parser.add_option('-o', '--outenc', dest='enc', help='set output encoding')
    (options, args) = parser.parse_args()
    if options.version:
        import __init__
        print '\ndrcsterm %s\nCopyright (C) 2012 Hayaki Saito <user@zuse.jp>.\n\nThis program is free software; you can redistribute it and/or modify\nit under the terms of the GNU General Public License as published by\nthe Free Software Foundation; either version 3 of the License, or\n(at your option) any later version.\n\nThis program is distributed in the hope that it will be useful,\nbut WITHOUT ANY WARRANTY; without even the implied warranty of\nMERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the\nGNU General Public License for more details.\n\nYou should have received a copy of the GNU General Public License\nalong with this program. If not, see http://www.gnu.org/licenses/.\n        ' % __init__.__version__
        return
    else:
        import locale
        (language, encoding) = locale.getdefaultlocale()
        termenc = encoding
        if termenc.lower().startswith('utf_8_'):
            termenc = 'UTF-8'
        assert termenc.lower() == 'utf-8' or termenc.lower() == 'utf8'
        lang = '%s.%s' % (language, 'UTF-8')
        if len(args) > 0:
            command = args[0]
        elif os.getenv('SHELL') is not None:
            command = os.getenv('SHELL')
        else:
            command = '/bin/sh'
        if options.term:
            term = options.term
        elif os.getenv('TERM') is not None:
            term = os.getenv('TERM')
        else:
            term = 'xterm'
        rcdir = os.path.join(os.getenv('HOME'), '.drcsterm')
        logdir = os.path.join(rcdir, 'log')
        if not os.path.exists(logdir):
            os.makedirs(logdir)
        logfile = os.path.join(logdir, 'log.txt')
        logging.basicConfig(filename=logfile, filemode='w')
        import tff

        class UnicodeDRCSScanner(tff.Scanner):
            """ scan input stream and iterate characters """
            __data = None
            _enabled = False

            def assign(self, value, termenc):
                self.__data = value

            def setenabled(self, value):
                self._enabled = value

            def __iter__(self):
                if self._enabled:
                    for x in self.__data:
                        c = ord(x)
                        if c < 128:
                            self.__utf8_state = 0
                            self.__count = 0
                            yield c
                        elif c >> 6 == 2:
                            self.__utf8_state = self.__utf8_state << 6 | c & 63
                            self.__count -= 1
                            if self.__count == 0:
                                if self.__utf8_state < 128:
                                    yield 63
                                else:
                                    code = self.__utf8_state
                                    if code < 1064960:
                                        yield code
                                    else:
                                        xx = code >> 8 & 255
                                        if xx > 126:
                                            yield code
                                        else:
                                            yy = code & 255
                                            if yy < 32 or yy > 127:
                                                yield code
                                            else:
                                                yield 27
                                                yield 40
                                                yield 32
                                                yield xx
                                                yield yy
                                                yield 27
                                                yield 40
                                                yield 66
                                self.__count = 0
                                self.__utf8_state = 0
                        elif c >> 5 == 6:
                            if self.__count != 0:
                                self.__count = 0
                                yield 63
                            else:
                                self.__utf8_state = c & 31
                                self.__count = 1
                        elif c >> 4 == 14:
                            if self.__count != 0:
                                self.__count = 0
                                yield 63
                            else:
                                self.__utf8_state = c & 15
                                self.__count = 2
                        elif c >> 3 == 30:
                            if self.__count != 0:
                                self.__count = 0
                                yield 63
                            else:
                                self.__utf8_state = c & 7
                                self.__count = 3
                        elif c >> 2 == 62:
                            if self.__count != 0:
                                self.__count = 0
                                yield 63
                            else:
                                self.__utf8_state = c & 3
                                self.__count = 4
                        elif c >> 1 == 126:
                            if self.__count != 0:
                                self.__count = 0
                                yield 63
                            else:
                                self.__utf8_state = c & 1
                                self.__count = 5

                for x in unicode(self.__data, 'utf-8'):
                    yield ord(x)

        def parsedigits(parameter):
            it = parameter.__iter__()
            try:
                n = 0
                c = it.next()
                while True:
                    if c <= 59:
                        break
                    if c >= 64:
                        break
                    c = it.next()

                while True:
                    if c >= 48 and c < 58:
                        n = n * 10 + c - 48
                    elif c == 59:
                        if n >= 0:
                            yield n
                        n = 0
                    else:
                        n = -1
                    c = it.next()

            except StopIteration:
                if n >= 0:
                    yield n

        class OutputHandler(tff.DefaultHandler):
            _scanner = None

            def __init__(self, scanner):
                self._scanner = scanner

            def handle_csi(self, context, parameter, intermediate, final):
                if not intermediate and parameter and parameter[0] == 63:
                    if final == 104:
                        handled = False
                        params = []
                        for param in parsedigits(parameter):
                            if param == 8800:
                                self._scanner.setenabled(True)
                                handled = True
                            else:
                                params.append(param)

                        if handled:
                            context.puts('\x1b[?%sh' % (';').join([ str(p) for p in params ]))
                            return True
                    elif final == 108:
                        handled = False
                        params = []
                        for param in parsedigits(parameter):
                            if param == 8800:
                                handled = True
                                self._scanner.setenabled(False)
                            else:
                                params.append(param)

                        if handled:
                            context.puts('\x1b[?%sl' % (';').join([ str(p) for p in params ]))
                            return True
                return False

        tty = tff.DefaultPTY(term, lang, command, sys.stdin)
        try:
            try:
                tty.fitsize()
                session = tff.Session(tty)
                scanner = UnicodeDRCSScanner()
                session.start('UTF-8', outputscanner=scanner, outputhandler=OutputHandler(scanner))
            except IOError, e:
                logging.exception(e)
                logging.exception('Connection closed.')
                print 'Connection closed.'
            except Exception, e:
                logging.exception(e)
                logging.exception('Aborted by exception.')
                print 'drcsterm aborted by an uncaught exception. see $HOME/.drcsterm/log/log.txt.'

        finally:
            try:
                tty.restore_term()
            except Exception, e:
                logging.exception(e)

        return


if __name__ == '__main__':
    main()