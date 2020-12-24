# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/foundation/alchemy/attachment.py
# Compiled at: 2012-10-12 07:02:39
from datetime import datetime
from sqlalchemy import *
import sqlalchemy.orm as orm
from base import Base, KVC

class Attachment(Base, KVC):
    __tablename__ = 'attachment'
    __entityName__ = 'Attachment'
    __internalName__ = 'Attachment'
    uuid = Column('attachment_id', String(255), primary_key=True)
    related_id = Column('related_id', Integer, ForeignKey('person.company_id'), ForeignKey('enterprise.company_id'), ForeignKey('date_x.date_id'), ForeignKey('job.job_id'), ForeignKey('project.project_id'), ForeignKey('doc.document_id'), ForeignKey('route.route_id'), ForeignKey('process.process_id'), nullable=True)
    kind = Column('kind', String(45), nullable=True)
    mimetype = Column('mimetype', String(128), nullable=False)
    created = Column('created', DateTime())
    size = Column('size', Integer)
    expiration = Column('expiration', Integer, nullable=True)
    context_id = Column('context_id', Integer, nullable=False)
    webdav_uid = Column('webdav_uid', String(128))
    checksum = Column('checksum', String(128))

    def __repr__(self):
        return ('<Attachment UUID="{0}" relatedId={1} kind={2} mimetype="{3}" size={4} name={5} checksum="{6}">').format(self.uuid, self.related_id if self.related_id else 'n/a', ('"{0}"').format(self.kind) if self.kind else 'n/a', self.mimetype, self.size, ('"{0}"').format(self.webdav_uid) if self.webdav_uid else 'n/a', self.checksum)