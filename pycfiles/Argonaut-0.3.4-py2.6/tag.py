# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/argonaut/model/tag.py
# Compiled at: 2011-02-18 19:15:08
"""The tag model"""
from sqlalchemy import Column, ForeignKey
from sqlalchemy.types import Unicode, Integer
from argonaut.model.meta import Base, Session

class Tag(Base):
    __tablename__ = 'tag'
    id = Column(Integer, primary_key=True)
    name = Column(Unicode(50), unique=True, nullable=False)

    def __init__(self, id=None, name=None):
        self.id = id
        self.name = name

    def __unicode__(self):
        return self.name

    def __repr__(self):
        return "<Tag('%s','%s')>" % (self.id, self.name)

    __str__ = __unicode__


def get_tag(name):
    return Session.query(Tag).filter(Tag.name == name.lower().strip()).first()


def save_tag(name):
    tag = Tag(None, name.lower().strip())
    Session.add(tag)
    Session.commit()
    return


def get_number_of_tags():
    return Session.query(Tag).distinct().count()