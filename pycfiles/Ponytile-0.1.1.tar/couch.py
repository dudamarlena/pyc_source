# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Library/Frameworks/Python.framework/Versions/2.6/lib/python2.6/site-packages/ponyexpress/couch.py
# Compiled at: 2011-02-06 21:16:14
__doc__ = '\nThe couchdbkit document models\n'
from couchdbkit import *
couch_db = None

def init(config, couch_db=couch_db):
    server = Server(config.get('COUCH_CONN', 'http://127.0.0.1:5984'))
    couch_db = server.get_or_create_db(config.get('COUCH_DB', 'ponyexpress'))
    PonyExpressTemplate.set_db(couch_db)
    PonyExpressError.set_db(couch_db)
    PonyExpressMessage.set_db(couch_db)
    return couch_db


class LocalTemplate(DocumentSchema):
    """
        Dict Schema for localized template content
        """
    lang = StringProperty()
    subject = StringProperty()
    body = StringProperty()


class PonyExpressTemplate(Document):
    """
        Couchdbkit document model for message template
        """
    name = StringProperty()
    format = StringProperty()
    contents = SchemaListProperty(LocalTemplate)


class PonyExpressError(Document):
    """
        For logging exceptions
        """
    date = DateTimeProperty()
    type = StringProperty()
    exception = StringProperty()
    template_id = StringProperty()
    pony_json = DictProperty()


class PonyExpressMessage(Document):
    """
        Full log of sent|queued messages
        """
    date = DateTimeProperty()
    status = StringProperty()
    template = StringProperty()
    lang = StringProperty()
    format = StringProperty()
    sender_address = StringProperty()
    recipient_address = StringProperty()
    sender_name = StringProperty()
    recipient_name = StringProperty()
    tags = ListProperty()
    replacements = DictProperty()
    subject = StringProperty()
    body = StringProperty()

    @classmethod
    def by_status(cls, status, **kwargs):
        """view by status (queued, sent, failed)"""
        return cls.view('ponyexpress/messages_by_status', key=status, **kwargs)