# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nb/publish/btw/tingyun/tingyun/packages/requests/certs.py
# Compiled at: 2016-06-30 06:13:10
"""
certs.py
~~~~~~~~

This module returns the preferred default CA certificate bundle.

If you are packaging Requests, e.g., for a Linux distribution or a managed
environment, you can change the definition of where() to return a separately
packaged CA bundle.
"""
import os.path
try:
    from certifi import where
except ImportError:

    def where():
        """Return the preferred certificate bundle."""
        return os.path.join(os.path.dirname(__file__), 'cacert.pem')


if __name__ == '__main__':
    print where()