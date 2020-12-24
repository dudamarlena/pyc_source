# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyasn1/debug.py
# Compiled at: 2019-10-17 01:00:19
import logging, sys
from pyasn1 import __version__
from pyasn1 import error
from pyasn1.compat.octets import octs2ints
__all__ = [
 'Debug', 'setLogger', 'hexdump']
DEBUG_NONE = 0
DEBUG_ENCODER = 1
DEBUG_DECODER = 2
DEBUG_ALL = 65535
FLAG_MAP = {'none': DEBUG_NONE, 'encoder': DEBUG_ENCODER, 'decoder': DEBUG_DECODER, 'all': DEBUG_ALL}
LOGGEE_MAP = {}

class Printer(object):
    __module__ = __name__

    def __init__(self, logger=None, handler=None, formatter=None):
        if logger is None:
            logger = logging.getLogger('pyasn1')
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
        return '<python logging>'


if hasattr(logging, 'NullHandler'):
    NullHandler = logging.NullHandler
else:

    class NullHandler(logging.Handler):
        __module__ = __name__

        def emit(self, record):
            pass


class Debug(object):
    __module__ = __name__
    defaultPrinter = Printer()

    def __init__(self, *flags, **options):
        self._flags = DEBUG_NONE
        if 'loggerName' in options:
            self._printer = Printer(logger=logging.getLogger(options['loggerName']), handler=NullHandler())
        elif 'printer' in options:
            self._printer = options.get('printer')
        else:
            self._printer = self.defaultPrinter
        self._printer('running pyasn1 %s, debug flags %s' % (__version__, (', ').join(flags)))
        for flag in flags:
            inverse = flag and flag[0] in ('!', '~')
            if inverse:
                flag = flag[1:]
            try:
                if inverse:
                    self._flags &= ~FLAG_MAP[flag]
                else:
                    self._flags |= FLAG_MAP[flag]
            except KeyError:
                raise error.PyAsn1Error('bad debug flag %s' % flag)

            self._printer("debug category '%s' %s" % (flag, inverse and 'disabled' or 'enabled'))

    def __str__(self):
        return 'logger %s, flags %x' % (self._printer, self._flags)

    def __call__(self, msg):
        self._printer(msg)

    def __and__(self, flag):
        return self._flags & flag

    def __rand__(self, flag):
        return flag & self._flags


_LOG = DEBUG_NONE

def setLogger(userLogger):
    global _LOG
    if userLogger:
        _LOG = userLogger
    else:
        _LOG = DEBUG_NONE
    for (module, (name, flags)) in LOGGEE_MAP.items():
        setattr(module, name, _LOG & flags and _LOG or DEBUG_NONE)


def registerLoggee(module, name='LOG', flags=DEBUG_NONE):
    LOGGEE_MAP[sys.modules[module]] = (name, flags)
    setLogger(_LOG)
    return _LOG


def hexdump(octets):
    return (' ').join([ '%s%.2X' % (n % 16 == 0 and '\n%.5d: ' % n or '', x) for (n, x) in zip(range(len(octets)), octs2ints(octets)) ])


class Scope(object):
    __module__ = __name__

    def __init__(self):
        self._list = []

    def __str__(self):
        return ('.').join(self._list)

    def push(self, token):
        self._list.append(token)

    def pop(self):
        return self._list.pop()


scope = Scope()