# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\index\proceed_default2\models.py
# Compiled at: 2013-09-26 17:01:52
from __future__ import division, absolute_import, print_function, unicode_literals
import sys, os
from datetime import datetime
from sqlalchemy import Column, Integer, Float, String, DateTime, PickleType, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import backref, relationship
Base = declarative_base()
if sys.version_info >= (3, ):

    class aStr:

        def __str__(self):
            return self.__unicode__()


else:

    class aStr:

        def __str__(self):
            return self.__unicode__().encode(b'utf-8')


class Dir(Base, aStr):
    __tablename__ = b'dirs'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    location = Column(String)
    status = Column(Integer)

    def __unicode__(self):
        return (b"<Директория '{0}' ({1})>").format(self.name, self.id)


class File(Base, aStr):
    __tablename__ = b'files'
    id = Column(Integer, primary_key=True)
    _dirs_id = Column(Integer, ForeignKey(b'dirs.id', onupdate=b'CASCADE', ondelete=b'CASCADE'))
    _dir = relationship(Dir, backref=backref(__tablename__, cascade=b'all, delete, delete-orphan'))
    name = Column(String)
    size = Column(Integer)
    mtime = Column(Integer)
    status = Column(Integer)

    def __unicode__(self):
        return (b"<Файл '{0}' ({1})>").format(self.name, self.id)


class Handler(Base, aStr):
    __tablename__ = b'handlers'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    rev = Column(Integer)
    disabled = Column(Integer)
    created = Column(Integer, default=datetime.utcnow)
    updated = Column(Integer, onupdate=datetime.utcnow)
    extras = Column(PickleType)

    def __unicode__(self):
        return (b"<Обработчик '{0}' ({1})>").format(self.name, self.id)


class FileProcessing(Base, aStr):
    __tablename__ = b'fileprocessings'
    id = Column(Integer, primary_key=True)
    _files_id = Column(Integer, ForeignKey(b'files.id', onupdate=b'CASCADE', ondelete=b'CASCADE'))
    _file = relationship(File, backref=backref(__tablename__, cascade=b'all, delete, delete-orphan'))
    _handlers_id = Column(Integer, ForeignKey(b'handlers.id', onupdate=b'CASCADE', ondelete=b'CASCADE'))
    _handler = relationship(Handler, backref=backref(__tablename__, cascade=b'all, delete, delete-orphan'))
    size = Column(Integer)
    mtime = Column(Integer)

    def __unicode__(self):
        return (b"<Обработка файла '{0}' обработчиком '{1}' ({2})>").format(self._file.name, self._handler.name, self.id)