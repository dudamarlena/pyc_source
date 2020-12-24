# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/couchish/filestore.py
# Compiled at: 2009-06-02 10:20:20
from __future__ import with_statement
from cStringIO import StringIO
import couchish

class CouchDBAttachmentSource(object):
    """
    A file source for the FileResource to use to read attachments from
    documents in a CouchDB database.
    
    Note: the application would be responsible for uploading files.
    """

    def __init__(self, couchish_store):
        self.couchish = couchish_store

    def get(self, key, cache_tag=None):
        try:
            (doc_id, attachment_name) = key.split('/', 1)
        except ValueError:
            raise KeyError

        try:
            with self.couchish.session() as (S):
                doc = S.doc_by_id(doc_id)
        except couchish.NotFound:
            raise KeyError(key)

        attachment_stub = doc.get('_attachments', {}).get(attachment_name)
        if attachment_stub is None:
            raise KeyError(key)
        if cache_tag and doc['_rev'] == cache_tag:
            return (doc['_rev'], [('Content-Type', None)], None)
        else:
            with self.couchish.session() as (S):
                content = S.get_attachment(doc_id, attachment_name)
            return (
             doc['_rev'], [('Content-Type', attachment_stub['content_type'])], StringIO(content))