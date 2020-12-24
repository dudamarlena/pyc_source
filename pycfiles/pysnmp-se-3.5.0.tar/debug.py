# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pysnmp/debug.py
# Compiled at: 2019-08-18 17:24:05
import logging
from pyasn1.compat.octets import octs2ints
from pysnmp import error
from pysnmp import __version__
flagNone = 0
flagIO = 1
flagDsp = 2
flagMP = 4
flagSM = 8
flagBld = 16
flagMIB = 32
flagIns = 64
flagACL = 128
flagPrx = 256
flagApp = 512
flagAll = 65535
flagMap = {'io': flagIO, 'dsp': flagDsp, 'msgproc': flagMP, 'secmod': flagSM, 'mibbuild': flagBld, 'mibview': flagMIB, 'mibinstrum': flagIns, 'acl': flagACL, 'proxy': flagPrx, 'app': flagApp, 'all': flagAll}

class Printer(object):
    __module__ = __name__

    def __init__(self, logger=None, handler=None, formatter=None):
        if logger is None:
            logger = logging.getLogger('pysnmp')
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
        self('running pysnmp version %s' % __version__)
        for f in flags:
            inverse = f and f[0] in ('!', '~')
            if inverse:
                f = f[1:]
            try:
                if inverse:
                    self._flags &= ~flagMap[f]
                else:
                    self._flags |= flagMap[f]
            except KeyError:
                raise error.PySnmpError('bad debug flag %s' % f)

            self("debug category '%s' %s" % (f, inverse and 'disabled' or 'enabled'))

        return

    def __str__(self):
        return 'logger %s, flags %x' % (self._printer, self._flags)

    def __call__(self, msg):
        self._printer(msg)

    def __and__(self, flag):
        return self._flags & flag

    def __rand__(self, flag):
        return flag & self._flags


logger = 0

def setLogger(l):
    global logger
    logger = l


def hexdump(octets):
    return (' ').join([ '%s%.2X' % (n % 16 == 0 and '\n%.5d: ' % n or '', x) for (n, x) in zip(range(len(octets)), octs2ints(octets)) ])