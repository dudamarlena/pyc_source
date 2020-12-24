# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/Products/UpfrontContacts/utils.py
# Compiled at: 2010-03-10 13:47:45
import copy

def make_listing_from_schema(schema, columns):
    listing = schema.copy()
    field_names = copy.copy(listing.keys())
    for key in field_names:
        if key not in columns:
            del listing[key]

    return listing


import codecs
encoding = 'latin1'
try:
    (encodeLocal, decodeLocal, reader) = codecs.lookup(encoding)[:3]
    (encodeUTF8, decodeUTF8) = codecs.lookup('UTF-8')[:2]
    if getattr(reader, '__module__', '') == 'encodings.utf_8':
        to_utf8 = from_utf8 = str
    else:

        def from_utf8(s):
            return encodeLocal(decodeUTF8(s)[0])[0]


        def to_utf8(s):
            return encodeUTF8(decodeLocal(s)[0])[0]


except LookupError:
    raise LookupError, 'Unknown encoding "%s"' % encoding