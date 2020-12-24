# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./build/lib.linux-x86_64-2.7/serial/__init__.py
# Compiled at: 2015-09-22 16:25:15
import importlib, sys
from serial.serialutil import *
VERSION = '3.0a0'
if sys.platform == 'cli':
    from serial.serialcli import Serial
else:
    import os
    if os.name == 'nt':
        from serial.serialwin32 import Serial
    elif os.name == 'posix':
        from serial.serialposix import Serial, PosixPollSerial
    elif os.name == 'java':
        from serial.serialjava import Serial
    else:
        raise ImportError("Sorry: no implementation for your platform ('%s') available" % (os.name,))
protocol_handler_packages = [
 'serial.urlhandler']

def serial_for_url(url, *args, **kwargs):
    """    Get an instance of the Serial class, depending on port/url. The port is not
    opened when the keyword parameter 'do_not_open' is true, by default it
    is. All other parameters are directly passed to the __init__ method when
    the port is instantiated.

    The list of package names that is searched for protocol handlers is kept in
    ``protocol_handler_packages``.

    e.g. we want to support a URL ``foobar://``. A module
    ``my_handlers.protocol_foobar`` is provided by the user. Then
    ``protocol_handler_packages.append("my_handlers")`` would extend the search
    path so that ``serial_for_url("foobar://"))`` would work.
    """
    do_open = 'do_not_open' not in kwargs or not kwargs['do_not_open']
    if 'do_not_open' in kwargs:
        del kwargs['do_not_open']
    klass = Serial
    try:
        url_lowercase = url.lower()
    except AttributeError:
        pass

    if '://' in url_lowercase:
        protocol = url_lowercase.split('://', 1)[0]
        module_name = '.protocol_%s' % (protocol,)
        for package_name in protocol_handler_packages:
            package = importlib.import_module(package_name)
            try:
                handler_module = importlib.import_module(module_name, package_name)
            except ImportError:
                pass
            else:
                klass = handler_module.Serial
                break

        else:
            raise ValueError('invalid URL, protocol %r not known' % (protocol,))

    else:
        klass = Serial
    instance = klass(None, *args, **kwargs)
    instance.port = url
    if do_open:
        instance.open()
    return instance