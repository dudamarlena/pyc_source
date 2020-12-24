# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /private/var/folders/pb/598z8h910dvf2wrvwnbyl_2m0000gn/T/pip-install-65c3rg8f/requests/requests/certs.py
# Compiled at: 2019-11-10 08:27:46
# Size of source mod 2**32: 453 bytes
__doc__ = '\nrequests.certs\n~~~~~~~~~~~~~~\n\nThis module returns the preferred default CA certificate bundle. There is\nonly one — the one from the certifi package.\n\nIf you are packaging Requests, e.g., for a Linux distribution or a managed\nenvironment, you can change the definition of where() to return a separately\npackaged CA bundle.\n'
from certifi import where
if __name__ == '__main__':
    print(where())