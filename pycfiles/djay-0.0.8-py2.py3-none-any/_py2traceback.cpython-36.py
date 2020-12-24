# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-m_4qh6p6/py/py/_code/_py2traceback.py
# Compiled at: 2019-07-30 18:47:10
# Size of source mod 2**32: 2765 bytes
import types

def format_exception_only(etype, value):
    """Format the exception part of a traceback.

    The arguments are the exception type and value such as given by
    sys.last_type and sys.last_value. The return value is a list of
    strings, each ending in a newline.

    Normally, the list contains a single string; however, for
    SyntaxError exceptions, it contains several lines that (when
    printed) display detailed information about where the syntax
    error occurred.

    The message indicating which exception occurred is always the last
    string in the list.

    """
    if isinstance(etype, BaseException) or isinstance(etype, types.InstanceType) or etype is None or type(etype) is str:
        return [_format_final_exc_line(etype, value)]
    else:
        stype = etype.__name__
        if not issubclass(etype, SyntaxError):
            return [
             _format_final_exc_line(stype, value)]
        lines = []
        try:
            msg, (filename, lineno, offset, badline) = value.args
        except Exception:
            pass
        else:
            filename = filename or '<string>'
            lines.append('  File "%s", line %d\n' % (filename, lineno))
            if badline is not None:
                lines.append('    %s\n' % badline.strip())
                if offset is not None:
                    caretspace = badline.rstrip('\n')[:offset].lstrip()
                    caretspace = (c.isspace() and c or ' ' for c in caretspace)
                    lines.append('   %s^\n' % ''.join(caretspace))
            value = msg
        lines.append(_format_final_exc_line(stype, value))
        return lines


def _format_final_exc_line(etype, value):
    """Return a list of a single line -- normal case for format_exception_only"""
    valuestr = _some_str(value)
    if value is None or not valuestr:
        line = '%s\n' % etype
    else:
        line = '%s: %s\n' % (etype, valuestr)
    return line


def _some_str(value):
    try:
        return unicode(value)
    except Exception:
        try:
            return str(value)
        except Exception:
            pass

    return '<unprintable %s object>' % type(value).__name__