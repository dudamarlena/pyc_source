# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyramid_localize/models.py
# Compiled at: 2014-05-04 12:45:31
"""Language model."""
from sqlalchemy import Column
from sqlalchemy import Sequence
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Unicode
from sqlalchemy import DateTime
from sqlalchemy import func
from pyramid_basemodel import Base

class Language(Base):
    """Language table model definition."""
    __tablename__ = 'languages'
    id = Column(Integer, Sequence(__tablename__ + '_sq'), primary_key=True)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)
    name = Column(Unicode(45), nullable=False)
    native_name = Column(Unicode(45), nullable=False)
    language_code = Column(String(2), unique=True, nullable=False)

    def __unicode__(self):
        """Language to unicode conversion."""
        return self.name

    def __str__(self):
        """Language to string conversion."""
        return self.name.encode('utf8')