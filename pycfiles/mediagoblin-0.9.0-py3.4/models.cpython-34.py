# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mediagoblin/plugins/persona/models.py
# Compiled at: 2014-01-02 16:06:37
# Size of source mod 2**32: 1447 bytes
from sqlalchemy import Column, Integer, Unicode, ForeignKey
from sqlalchemy.orm import relationship, backref
from mediagoblin.db.models import User
from mediagoblin.db.base import Base

class PersonaUserEmails(Base):
    __tablename__ = 'persona__user_emails'
    id = Column(Integer, primary_key=True)
    persona_email = Column(Unicode, nullable=False)
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    user = relationship(User, backref=backref('persona_emails', cascade='all, delete-orphan'))


MODELS = [
 PersonaUserEmails]