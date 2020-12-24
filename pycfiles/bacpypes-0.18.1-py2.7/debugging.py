# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bacpypes/debugging.py
# Compiled at: 2020-04-20 14:21:18
"""
Debugging
"""
import sys, re, logging, binascii
from cStringIO import StringIO
root_logger = logging.getLogger('bacpypes')

def btox(data, sep=''):
    """Return the hex encoding of a blob (string)."""
    hex_str = binascii.hexlify(data)
    if sep:
        hex_str = sep.join(hex_str[i:i + 2] for i in range(0, len(hex_str), 2))
    return hex_str


def xtob(data, sep=''):
    """Interpret the hex encoding of a blob (string)."""
    data = re.sub('[^0-9a-fA-F]', '', data)
    return binascii.unhexlify(data)


def ModuleLogger(globs):
    """Create a module level logger.

    To debug a module, create a _debug variable in the module, then use the
    ModuleLogger function to create a "module level" logger.  When a handler
    is added to this logger or a child of this logger, the _debug variable will
    be incremented.

    All of the calls within functions or class methods within the module should
    first check to see if _debug is set to prevent calls to formatter objects
    that aren't necessary.
    """
    if '_debug' not in globs:
        raise RuntimeError('define _debug before creating a module logger')
    logger_name = globs['__name__']
    logger = logging.getLogger(logger_name)
    logger.globs = globs
    if '.' not in logger_name:
        hdlr = logging.StreamHandler()
        hdlr.setLevel(logging.WARNING)
        hdlr.setFormatter(logging.Formatter(logging.BASIC_FORMAT, None))
        logger.addHandler(hdlr)
    return logger


_debug = 0
_log = ModuleLogger(globals())

class DebugContents(object):

    def debug_contents(self, indent=1, file=sys.stdout, _ids=None):
        """Debug the contents of an object."""
        if _debug:
            _log.debug('debug_contents indent=%r file=%r _ids=%r', indent, file, _ids)
        klasses = list(self.__class__.__mro__)
        klasses.reverse()
        if _debug:
            _log.debug('    - klasses: %r', klasses)
        attrs = []
        cids = []
        ownFn = []
        for klass in klasses:
            if klass is DebugContents:
                continue
            if not issubclass(klass, DebugContents) and hasattr(klass, 'debug_contents'):
                for i, seenAlready in enumerate(ownFn):
                    if issubclass(klass, seenAlready):
                        del ownFn[i]
                        break

                ownFn.append(klass)
                continue
            if not hasattr(klass, '_debug_contents'):
                continue
            debugContents = klass._debug_contents
            if not isinstance(debugContents, tuple):
                raise RuntimeError('%s._debug_contents must be a tuple' % (klass.__name__,))
            if id(debugContents) in cids:
                continue
            cids.append(id(debugContents))
            for attr in debugContents:
                if attr not in attrs:
                    attrs.append(attr)

        if _debug:
            _log.debug('    - attrs: %r', attrs)
            _log.debug('    - ownFn: %r', ownFn)
        if _ids is None:
            _ids = []
        for attr in attrs:
            goDeep = True
            goListDict = False
            goHexed = False
            if attr.endswith('-'):
                goDeep = False
                attr = attr[:-1]
            elif attr.endswith('*'):
                goHexed = True
                attr = attr[:-1]
            elif attr.endswith('+'):
                goDeep = False
                goListDict = True
                attr = attr[:-1]
                if attr.endswith('+'):
                    goDeep = True
                    attr = attr[:-1]
            value = getattr(self, attr, None)
            if value is None:
                continue
            if goListDict and isinstance(value, list) and value:
                file.write('%s%s = [\n' % ('    ' * indent, attr))
                indent += 1
                for i, elem in enumerate(value):
                    file.write('%s[%d] %r\n' % ('    ' * indent, i, elem))
                    if goDeep and hasattr(elem, 'debug_contents'):
                        if id(elem) not in _ids:
                            _ids.append(id(elem))
                            elem.debug_contents(indent + 1, file, _ids)

                indent -= 1
                file.write('%s    ]\n' % ('    ' * indent,))
            elif goListDict and isinstance(value, dict) and value:
                file.write('%s%s = {\n' % ('    ' * indent, attr))
                indent += 1
                for key, elem in value.items():
                    file.write('%s%r : %r\n' % ('    ' * indent, key, elem))
                    if goDeep and hasattr(elem, 'debug_contents'):
                        if id(elem) not in _ids:
                            _ids.append(id(elem))
                            elem.debug_contents(indent + 1, file, _ids)

                indent -= 1
                file.write('%s    }\n' % ('    ' * indent,))
            elif goHexed and isinstance(value, str):
                if len(value) > 20:
                    hexed = btox(value[:20], '.') + '...'
                else:
                    hexed = btox(value, '.')
                file.write("%s%s = x'%s'\n" % ('    ' * indent, attr, hexed))
            else:
                file.write('%s%s = %r\n' % ('    ' * indent, attr, value))
                if goDeep and hasattr(value, 'debug_contents'):
                    if id(value) not in _ids:
                        _ids.append(id(value))
                        value.debug_contents(indent + 1, file, _ids)

        ownFn.reverse()
        for klass in ownFn:
            klass.debug_contents(self, indent, file, _ids)

        return


class LoggingFormatter(logging.Formatter):

    def __init__(self, color=None):
        logging.Formatter.__init__(self, logging.BASIC_FORMAT, None)
        if color is not None:
            if color not in range(8):
                raise ValueError('colors are 0 (black) through 7 (white)')
        self.color = color
        return

    def format(self, record):
        try:
            msg = logging.Formatter.format(self, record) + '\n'
            for arg in record.args:
                if isinstance(arg, DebugContents):
                    if msg:
                        sio = StringIO()
                        sio.write(msg)
                        msg = None
                    sio.write('    %r\n' % (arg,))
                    arg.debug_contents(indent=2, file=sio)

            if not msg:
                msg = sio.getvalue()
            msg = msg[:-1]
        except Exception as err:
            record_attrs = [ attr + ': ' + str(getattr(record, attr, 'N/A')) for attr in ('name',
                                                                                          'level',
                                                                                          'pathname',
                                                                                          'lineno',
                                                                                          'msg',
                                                                                          'args',
                                                                                          'exc_info',
                                                                                          'func') ]
            record_attrs[:0] = [
             'LoggingFormatter exception: ' + str(err)]
            msg = ('\n    ').join(record_attrs)

        if self.color is not None:
            msg = '\x1b[%dm' % (30 + self.color,) + msg + '\x1b[0m'
        return msg


def bacpypes_debugging(obj):
    """Function for attaching a debugging logger to a class or function."""
    logger = logging.getLogger(obj.__module__ + '.' + obj.__name__)
    obj._logger = logger
    obj._debug = logger.debug
    obj._info = logger.info
    obj._warning = logger.warning
    obj._error = logger.error
    obj._exception = logger.exception
    obj._fatal = logger.fatal
    return obj


class _LoggingMetaclass(type):

    def __init__(cls, *args):
        bacpypes_debugging(cls)


class Logging(object):
    __metaclass__ = _LoggingMetaclass


def class_debugging(cls):
    """Add the debugging logger to the class."""
    bacpypes_debugging(cls)
    return cls


def function_debugging(f):
    """Add the debugging logger to the function."""
    bacpypes_debugging(f)
    return f