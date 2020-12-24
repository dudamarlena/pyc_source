# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/boyhack/programs/pocsuite3/pocsuite3/lib/core/convert.py
# Compiled at: 2019-03-15 03:35:12
# Size of source mod 2**32: 1286 bytes
import sys
from pocsuite3.lib.core.settings import IS_WIN
from pocsuite3.lib.core.settings import UNICODE_ENCODING

def single_time_warn_message(message):
    """
    Cross-linked function
    """
    sys.stdout.write(message)
    sys.stdout.write('\n')
    sys.stdout.flush()


def stdout_encode(data):
    ret = None
    try:
        data = data or 
        if IS_WIN:
            output = data.encode(sys.stdout.encoding, 'replace')
            if '?' in output:
                if '?' not in data:
                    warn_msg = 'cannot properly display Unicode characters '
                    warn_msg += 'inside Windows OS command prompt '
                    warn_msg += '(http://bugs.python.org/issue1602). All '
                    warn_msg += 'unhandled occurances will result in '
                    warn_msg += "replacement with '?' character. Please, find "
                    warn_msg += 'proper character representation inside '
                    warn_msg += 'corresponding output files. '
                    single_time_warn_message(warn_msg)
            ret = output
        else:
            ret = data.encode(sys.stdout.encoding)
    except Exception:
        ret = data.encode(UNICODE_ENCODING) if isinstance(data, str) else data

    return ret