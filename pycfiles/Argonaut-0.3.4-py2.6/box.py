# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/argonaut/model/box.py
# Compiled at: 2011-02-18 19:15:08
"""The box model"""
from sqlalchemy import Column, ForeignKey
from sqlalchemy.types import Unicode, Integer
from argonaut.model.meta import Base, Session

class Box(Base):
    __tablename__ = 'box'
    id = Column(Integer, primary_key=True)
    name = Column(Unicode(50), unique=True, nullable=False)
    template = Column(Unicode(30), nullable=False)

    def __init__(self, id=None, name=None, template=None):
        self.id = id
        self.name = name
        self.template = template

    def __unicode__(self):
        return self.name

    def __repr__(self):
        return "<Box('%s','%s','%s')>" % (self.id, self.name, self.template)

    __str__ = __unicode__


def get(id):
    return Session.query(Box).filter(Box.id == id).one()