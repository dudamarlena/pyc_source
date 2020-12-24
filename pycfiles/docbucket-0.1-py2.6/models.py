# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/docbucket/models.py
# Compiled at: 2010-12-14 14:28:02
import mongoengine as me
from datetime import datetime
from whoosh import fields, index
from django.conf import settings

class DocumentClass(me.Document):
    name = me.StringField(max_length=200, required=True)
    slug = me.StringField(max_length=20, required=True)

    def __unicode__(self):
        return self.name


class Thumbnail(me.EmbeddedDocument):
    size = me.StringField(max_length=30, required=True)
    image = me.FileField()


class Document(me.Document):
    name = me.StringField(max_length=200, required=True)
    attachment = me.FileField()
    thumbnails = me.ListField(me.EmbeddedDocumentField(Thumbnail))
    physical_location = me.StringField(max_length=50)
    page_number = me.IntField()
    created = me.DateTimeField(default=datetime.now)
    access = me.DateTimeField(default=None)
    document_class = me.ReferenceField(DocumentClass)
    content = me.DictField()

    def get_thumbnail(self, size):
        """ Get the thumbnail of specified size. """
        if not self.thumbnails:
            self.reload()
        found = [ t for t in self.thumbnails if t.size == size ]
        if found:
            return found[0].image
        else:
            return
            return

    def delete(self, *args, **kwargs):
        ix = index.open_dir(settings.WHOOSH_INDEX)
        ix.delete_by_term('doc_id', str(self.id))
        ix.commit()
        return super(Document, self).delete(*args, **kwargs)


WHOOSH_SCHEMA = fields.Schema(name=fields.TEXT(stored=True), content=fields.TEXT, doc_id=fields.ID(stored=True, unique=True))