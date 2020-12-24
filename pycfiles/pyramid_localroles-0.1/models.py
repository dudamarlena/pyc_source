# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyramid_localize/models.py
# Compiled at: 2014-05-04 12:45:31
__doc__ = 'Language model.'
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