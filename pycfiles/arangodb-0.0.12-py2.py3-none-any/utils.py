# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/maxk/Projects/OpenSource/arango-python/arango/utils.py
# Compiled at: 2013-02-16 20:35:46
try:
    import simplejson as json
except ImportError:
    import json

__all__ = ('json', 'proxied_document_ref', 'parse_meta')

def proxied_document_ref(ref_or_document):
    """
    Utility to get reference from document **or** from
    proxied response or return string as is.
    """
    from .document import Document
    if issubclass(type(ref_or_document), Document):
        return ref_or_document.id
    return ref_or_document


def parse_meta(obj, response):
    """
    Get ``_id`` and ``_rev`` from response
    and update document with updated values
    """
    if '_id' in response.data:
        obj._id = str(response.data.get('_id'))
    obj._rev = str(response.data.get('_rev'))
    return response