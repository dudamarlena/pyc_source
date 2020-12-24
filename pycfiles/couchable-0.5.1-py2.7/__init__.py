# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/couchable/__init__.py
# Compiled at: 2016-06-01 18:08:46
"""
The public API of couchable consists of:
    - L{CouchableDb}: The core DB wrapper/access object.
    - L{packer}: Extends the list of built-in or C types supported.
    - L{registerDocType}, L{CouchableDoc}: For adding new document classes.
    - L{registerAttachmentType}, L{CouchableAttachment}: For adding classes to store as attachments.
    - L{doGzip}, L{doGunzip}: Helper functions for compressing attachments.
    - L{newid}: Helper function to make document IDs readable.

For more information, please see:
    - API docs: U{http://packages.python.org/couchable}
    - Blog:     U{http://blog.nopinch.net/tag/couchable}
    - Package:  U{http://pypi.python.org/pypi/couchable}
    - Source:   U{http://github.com/wickedgrey/couchable}

Please use the github issue tracker for bugs:
    - U{http://github.com/wickedgrey/couchable/issues}

From the README.txt:

--README.txt--
"""
from core import CouchableDb
from core import registerDocType, CouchableDoc
from core import registerAttachmentType, CouchableAttachment
from core import registerPickleType, registerNoneType, registerUncouchableType
from core import custom_packer
from core import doGzip, doGunzip
from core import newid