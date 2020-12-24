# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/plover_vcs/resources_rc.py
# Compiled at: 2020-04-03 22:11:21
# Size of source mod 2**32: 6593 bytes
from PyQt5 import QtCore
qt_resource_data = b'\x00\x00\x04\xd6<?xml version="1.0" encoding="UTF-8"?><svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 50 50" version="1.1"><path d="M46.793 22.09L27.91 3.207A4.093 4.093 0 0 0 25 2c-1.055 0-2.11.402-2.91 1.207l-3.735 3.734 4.622 4.622a3.994 3.994 0 0 1 4.851.609 3.988 3.988 0 0 1 .606 4.848l4.543 4.543a3.994 3.994 0 0 1 4.851 6.265 3.994 3.994 0 1 1-6.266-4.852l-4.542-4.542a3.855 3.855 0 0 1-1.02.421v12.286A3.99 3.99 0 0 1 29 35c0 2.21-1.79 4-4 4s-4-1.79-4-4a3.99 3.99 0 0 1 3-3.86V18.856a3.955 3.955 0 0 1-1.828-1.027 3.988 3.988 0 0 1-.606-4.848l-4.625-4.625L3.207 22.09a4.112 4.112 0 0 0 0 5.82L22.09 46.793A4.093 4.093 0 0 0 25 48c1.055 0 2.11-.402 2.91-1.207L46.793 27.91a4.112 4.112 0 0 0 0-5.82z" id="surface1"/><metadata><rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#" xmlns:rdfs="http://www.w3.org/2000/01/rdf-schema#" xmlns:dc="http://purl.org/dc/elements/1.1/"><rdf:Description about="https://iconscout.com/legal#licenses" dc:title="git,filled" dc:description="git,filled" dc:publisher="Iconscout" dc:date="2017-12-09" dc:format="image/svg+xml" dc:language="en"><dc:creator><rdf:Bag><rdf:li>Icons8</rdf:li></rdf:Bag></dc:creator></rdf:Description></rdf:RDF></metadata></svg>'
qt_resource_name = b"\x00\n\x0c\xca\x8ac\x00p\x00l\x00o\x00v\x00e\x00r\x00_\x00v\x00c\x00s\x00\x08\naW'\x00i\x00c\x00o\x00n\x00.\x00s\x00v\x00g"
qt_resource_struct_v1 = b'\x00\x00\x00\x00\x00\x02\x00\x00\x00\x01\x00\x00\x00\x01\x00\x00\x00\x00\x00\x02\x00\x00\x00\x01\x00\x00\x00\x02\x00\x00\x00\x1a\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00'
qt_resource_struct_v2 = b'\x00\x00\x00\x00\x00\x02\x00\x00\x00\x01\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02\x00\x00\x00\x01\x00\x00\x00\x02\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x1a\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x01q>l\xab\x8e'
qt_version = [int(v) for v in QtCore.qVersion().split('.')]
if qt_version < [5, 8, 0]:
    rcc_version = 1
    qt_resource_struct = qt_resource_struct_v1
else:
    rcc_version = 2
    qt_resource_struct = qt_resource_struct_v2

def qInitResources():
    QtCore.qRegisterResourceData(rcc_version, qt_resource_struct, qt_resource_name, qt_resource_data)


def qCleanupResources():
    QtCore.qUnregisterResourceData(rcc_version, qt_resource_struct, qt_resource_name, qt_resource_data)


qInitResources()