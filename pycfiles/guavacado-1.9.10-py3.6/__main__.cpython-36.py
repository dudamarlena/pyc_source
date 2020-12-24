# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/guavacado/__main__.py
# Compiled at: 2019-07-08 17:04:07
# Size of source mod 2**32: 1480 bytes
from .WebHost import WebHost
from .WebFileInterface import WebFileInterface
from .misc import wait_for_keyboardinterrupt
import os, argparse

def main():
    """
        serves a static folder in the local 'static' directory
        using https (self-signed certificate) on port 443, and redirecting traffic from port 80 to https
        """
    host = WebHost(loglevel='INFO')
    host.add_addr(port=80, disp_type=('redirect', 'https://localhost/'))
    host.add_addr(port=443, TLS=(os.path.join('TLS_keys', 'self_signed.crt'), os.path.join('TLS_keys', 'self_signed.key')))
    _ = WebFileInterface(host)
    host.start_service()
    wait_for_keyboardinterrupt()
    host.stop_service()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Serves a basic static folder on a HTTP server.')
    args = parser.parse_args()
    init_settings = args.__dict__
    main(**init_settings)