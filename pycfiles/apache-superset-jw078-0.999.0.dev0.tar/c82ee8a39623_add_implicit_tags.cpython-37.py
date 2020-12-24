# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/bogdankyryliuk/src/oss/incubator-superset/superset/migrations/versions/c82ee8a39623_add_implicit_tags.py
# Compiled at: 2020-01-16 13:27:41
# Size of source mod 2**32: 2129 bytes
__doc__ = 'Add implicit tags\n\nRevision ID: c82ee8a39623\nRevises: c18bd4186f15\nCreate Date: 2018-07-26 11:10:23.653524\n\n'
revision = 'c82ee8a39623'
down_revision = 'c617da68de7d'
from alembic import op
from sqlalchemy import Column, Enum, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from superset.models.helpers import AuditMixinNullable
from superset.models.tags import ObjectTypes, TagTypes
Base = declarative_base()

class Tag(Base, AuditMixinNullable):
    """Tag"""
    __tablename__ = 'tag'
    id = Column(Integer, primary_key=True)
    name = Column((String(250)), unique=True)
    type = Column(Enum(TagTypes))


class TaggedObject(Base, AuditMixinNullable):
    __tablename__ = 'tagged_object'
    id = Column(Integer, primary_key=True)
    tag_id = Column(Integer, ForeignKey('tag.id'))
    object_id = Column(Integer)
    object_type = Column(Enum(ObjectTypes))


class User(Base):
    """User"""
    __tablename__ = 'ab_user'
    id = Column(Integer, primary_key=True)


def upgrade():
    bind = op.get_bind()
    Tag.__table__.create(bind)
    TaggedObject.__table__.create(bind)


def downgrade():
    op.drop_table('tagged_object')
    op.drop_table('tag')