# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pysmi/debug.py
# Compiled at: 2018-12-29 12:21:47
import logging
from pysmi import error
from pysmi import __version__
flagNone = 0
flagSearcher = 1
flagReader = 2
flagLexer = 4
flagParser = 8
flagGrammar = 16
flagCodegen = 32
flagWriter = 64
flagCompiler = 128
flagBorrower = 256
flagAll = 65535
flagMap = {'searcher': flagSearcher, 'reader': flagReader, 'lexer': flagLexer, 'parser': flagParser, 'grammar': flagGrammar, 'codegen': flagCodegen, 'writer': flagWriter, 'compiler': flagCompiler, 'borrower': flagBorrower, 'all': flagAll}

class Printer(object):
    __module__ = __name__

    def __init__(self, logger=None, handler=None, formatter=None):
        if logger is None:
            logger = logging.getLogger('pysmi')
        logger.setLevel(logging.DEBUG)
        if handler is None:
            handler = logging.StreamHandler()
        if formatter is None:
            formatter = logging.Formatter('%(asctime)s %(name)s: %(message)s')
        handler.setFormatter(formatter)
        handler.setLevel(logging.DEBUG)
        logger.addHandler(handler)
        self.__logger = logger
        return

    def __call__(self, msg):
        self.__logger.debug(msg)

    def __str__(self):
        return '<python built-in logging>'

    def getCurrentLogger(self):
        return self.__logger


if hasattr(logging, 'NullHandler'):
    NullHandler = logging.NullHandler
else:

    class NullHandler(logging.Handler):
        __module__ = __name__

        def emit(self, record):
            pass


class Debug(object):
    __module__ = __name__
    defaultPrinter = None

    def __init__(self, *flags, **options):
        self._flags = flagNone
        if options.get('printer') is not None:
            self._printer = options.get('printer')
        elif self.defaultPrinter is not None:
            self._printer = self.defaultPrinter
        elif 'loggerName' in options:
            self._printer = Printer(logger=logging.getLogger(options['loggerName']), handler=NullHandler())
        else:
            self._printer = Printer()
        self('running pysmi version %s' % __version__)
        for flag in flags:
            inverse = flag and flag[0] in ('!', '~')
            if inverse:
                flag = flag[1:]
            try:
                if inverse:
                    self._flags &= ~flagMap[flag]
                else:
                    self._flags |= flagMap[flag]
            except KeyError:
                raise error.PySmiError('bad debug flag %s' % flag)

            self("debug category '%s' %s" % (flag, inverse and 'disabled' or 'enabled'))

        return

    def __str__(self):
        return 'logger %s, flags %x' % (self._printer, self._flags)

    def __call__(self, msg):
        self._printer(msg)

    def __and__(self, flag):
        return self._flags & flag

    def __rand__(self, flag):
        return flag & self._flags

    def getCurrentPrinter(self):
        return self._printer

    def getCurrentLogger(self):
        return self._printer and self._printer.getCurrentLogger() or None


logger = 0

def setLogger(l):
    global logger
    logger = l