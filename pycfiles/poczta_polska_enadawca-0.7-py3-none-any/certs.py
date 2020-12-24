# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/hysia/Code/Pocsuite/pocsuite/thirdparty/requests/certs.py
# Compiled at: 2018-11-28 03:20:09
__doc__ = '\ncerts.py\n~~~~~~~~\n\nThis module returns the preferred default CA certificate bundle.\n\nIf you are packaging Requests, e.g., for a Linux distribution or a managed\nenvironment, you can change the definition of where() to return a separately\npackaged CA bundle.\n'
import os.path
try:
    from certifi import where
except ImportError:

    def where():
        """Return the preferred certificate bundle."""
        return os.path.join(os.path.dirname(__file__), 'cacert.pem')


if __name__ == '__main__':
    print where()