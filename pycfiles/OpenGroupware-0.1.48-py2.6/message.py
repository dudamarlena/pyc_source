# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/foundation/alchemy/message.py
# Compiled at: 2012-10-12 07:02:39
from datetime import datetime
from uuid import uuid4
from sqlalchemy import *
from base import Base, KVC
from utcdatetime import UTCDateTime

class Message(Base, KVC):
    """ An OpenGroupare message object """
    __tablename__ = 'message'
    __entityName__ = 'Message'
    __internalName__ = 'Message'
    uuid = Column('uuid', String, primary_key=True)
    scope = Column('scope', String)
    process_id = Column('process_id', Integer)
    size = Column('size', Integer)
    status = Column('db_status', String)
    label = Column('label', String)
    mimetype = Column('mimetype', String)
    version = Column('object_version', Integer)
    created = Column('creation_timestamp', UTCDateTime)
    modified = Column('lastmodified', UTCDateTime)

    def __init__(self, process_id):
        self.process_id = process_id
        self.version = 0
        self.status = 'inserted'
        self.uuid = ('{{{0}}}').format(str(uuid4()))
        self.label = self.uuid
        self.mimetype = 'application/octet-stream'

    def get_payload(self):
        pass

    def store_payload(self, data):
        pass

    def __repr__(self):
        return ('<Message GUID={0} version={1} processId="{2}" label="{3}" size={4} mimeType="{5}">').format(self.uuid, self.version, self.process_id, self.label, self.size, self.mimetype)