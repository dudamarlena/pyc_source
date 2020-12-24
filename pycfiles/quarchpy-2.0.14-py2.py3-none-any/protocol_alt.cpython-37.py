# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\sboon\AppData\Local\Temp\pip-install-ptdbtr91\quarchpy\quarchpy\connection_specific\serial\urlhandler\protocol_alt.py
# Compiled at: 2020-03-25 05:10:07
# Size of source mod 2**32: 1993 bytes
try:
    import urlparse
except ImportError:
    import urllib.parse as urlparse

import serial

def serial_class_for_url(url):
    """extract host and port from an URL string"""
    parts = urlparse.urlsplit(url)
    if parts.scheme != 'alt':
        raise serial.SerialException('expected a string in the form "alt://port[?option[=value][&option[=value]]]": not starting with alt:// ({!r})'.format(parts.scheme))
    class_name = 'Serial'
    try:
        for option, values in urlparse.parse_qs(parts.query, True).items():
            if option == 'class':
                class_name = values[0]
            else:
                raise ValueError('unknown option: {!r}'.format(option))

    except ValueError as e:
        try:
            raise serial.SerialException('expected a string in the form "alt://port[?option[=value][&option[=value]]]": {!r}'.format(e))
        finally:
            e = None
            del e

    if not hasattr(serial, class_name):
        raise ValueError('unknown class: {!r}'.format(class_name))
    cls = getattr(serial, class_name)
    if not issubclass(cls, serial.Serial):
        raise ValueError('class {!r} is not an instance of Serial'.format(class_name))
    return (
     ''.join([parts.netloc, parts.path]), cls)


if __name__ == '__main__':
    s = serial.serial_for_url('alt:///dev/ttyS0?class=PosixPollSerial')
    print(s)