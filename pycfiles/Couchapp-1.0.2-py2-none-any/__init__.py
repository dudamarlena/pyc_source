# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/couchable/__init__.py
# Compiled at: 2016-06-01 18:08:46
__doc__ = '\nThe public API of couchable consists of:\n    - L{CouchableDb}: The core DB wrapper/access object.\n    - L{packer}: Extends the list of built-in or C types supported.\n    - L{registerDocType}, L{CouchableDoc}: For adding new document classes.\n    - L{registerAttachmentType}, L{CouchableAttachment}: For adding classes to store as attachments.\n    - L{doGzip}, L{doGunzip}: Helper functions for compressing attachments.\n    - L{newid}: Helper function to make document IDs readable.\n\nFor more information, please see:\n    - API docs: U{http://packages.python.org/couchable}\n    - Blog:     U{http://blog.nopinch.net/tag/couchable}\n    - Package:  U{http://pypi.python.org/pypi/couchable}\n    - Source:   U{http://github.com/wickedgrey/couchable}\n\nPlease use the github issue tracker for bugs:\n    - U{http://github.com/wickedgrey/couchable/issues}\n\nFrom the README.txt:\n\n--README.txt--\n'
from core import CouchableDb
from core import registerDocType, CouchableDoc
from core import registerAttachmentType, CouchableAttachment
from core import registerPickleType, registerNoneType, registerUncouchableType
from core import custom_packer
from core import doGzip, doGunzip
from core import newid