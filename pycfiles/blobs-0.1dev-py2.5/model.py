# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/blobs/model.py
# Compiled at: 2008-02-19 12:19:12
from sqlalchemy import Column, MetaData, Table, types, ForeignKey
from sqlalchemy.orm import mapper, relation
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import and_
import blobs.helpers as h, os
meta = MetaData()
Session = scoped_session(sessionmaker(autoflush=True, transactional=True))
maxPathLen = 1024
filesTable = Table('files', meta, Column('id', types.Integer, primary_key=True), Column('hash', types.String(40), nullable=False, index=True), Column('size', types.Integer, nullable=False), Column('type', types.String(40), nullable=False), Column('ctime', types.DateTime, nullable=False, default=h.now), Column('dtime', types.DateTime), Column('atime', types.DateTime, nullable=False, default=h.now), Column('filename', types.Unicode(maxPathLen), nullable=False))

class File(object):

    def delete(self):
        if self.dtime is None:
            self.dtime = h.now()
        try:
            path = h.getBlobPath(self.hash)
            if os.path.exists(path):
                os.unlink(path)
        except OSError:
            pass

        return


Session.mapper(File, filesTable)