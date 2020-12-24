# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-zr3xXj/pytest/_pytest/_code/_py2traceback.py
# Compiled at: 2019-02-14 00:35:47
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import types
from six import text_type

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
        return [
         _format_final_exc_line(etype, value)]
    else:
        stype = etype.__name__
        if not issubclass(etype, SyntaxError):
            return [_format_final_exc_line(stype, value)]
        lines = []
        try:
            msg, (filename, lineno, offset, badline) = value.args
        except Exception:
            pass
        else:
            filename = filename or b'<string>'
            lines.append((b'  File "{}", line {}\n').format(filename, lineno))
            if badline is not None:
                if isinstance(badline, bytes):
                    badline = badline.decode(b'utf-8', b'replace')
                lines.append((b'    {}\n').format(badline.strip()))
                if offset is not None:
                    caretspace = badline.rstrip(b'\n')[:offset].lstrip()
                    caretspace = (c.isspace() and c or b' ' for c in caretspace)
                    lines.append((b'   {}^\n').format((b'').join(caretspace)))
            value = msg

        lines.append(_format_final_exc_line(stype, value))
        return lines


def _format_final_exc_line(etype, value):
    """Return a list of a single line -- normal case for format_exception_only"""
    valuestr = _some_str(value)
    if value is None or not valuestr:
        line = (b'{}\n').format(etype)
    else:
        line = (b'{}: {}\n').format(etype, valuestr)
    return line


def _some_str(value):
    try:
        return text_type(value)
    except Exception:
        try:
            return bytes(value).decode(b'UTF-8', b'replace')
        except Exception:
            pass

    return (b'<unprintable {} object>').format(type(value).__name__)