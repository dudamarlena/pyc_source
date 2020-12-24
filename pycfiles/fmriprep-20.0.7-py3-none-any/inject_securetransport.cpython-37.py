# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-vxs8l7gu/pip/pip/_internal/utils/inject_securetransport.py
# Compiled at: 2020-05-05 12:41:36
# Size of source mod 2**32: 810 bytes
"""A helper module that injects SecureTransport, on import.

The import should be done as early as possible, to ensure all requests and
sessions (or whatever) are created after injecting SecureTransport.

Note that we only do the injection on macOS, when the linked OpenSSL is too
old to handle TLSv1.2.
"""
import sys

def inject_securetransport():
    if sys.platform != 'darwin':
        return
    try:
        import ssl
    except ImportError:
        return
    else:
        if ssl.OPENSSL_VERSION_NUMBER >= 268439567:
            return
        try:
            from pip._vendor.urllib3.contrib import securetransport
        except (ImportError, OSError):
            return
        else:
            securetransport.inject_into_urllib3()


inject_securetransport()