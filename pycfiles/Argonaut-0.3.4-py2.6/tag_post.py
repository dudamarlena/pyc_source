# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/argonaut/model/tag_post.py
# Compiled at: 2011-02-18 19:15:08
"""The tag_post model"""
from sqlalchemy import Column, ForeignKey, UniqueConstraint
from sqlalchemy.types import Integer
from sqlalchemy.sql import select, func
from argonaut.model.meta import Base, Session

class Tag_Post(Base):
    __tablename__ = 'tag_post'
    id = Column(Integer, primary_key=True)
    post_id = Column(Integer, ForeignKey('post.id'), nullable=False)
    tag_id = Column(Integer, ForeignKey('tag.id'), nullable=False)
    post_tag_c = UniqueConstraint('post_id', 'tag_id')

    def __init__(self, id=None, post_id=None, tag_id=None):
        self.id = id
        self.post_id = post_id
        self.tag_id = tag_id

    def __unicode__(self):
        return self.id

    def __repr__(self):
        return "<Tag_Post('%s','%s','%s')>" % (self.id, self.post_id, self.tag_id)

    __str__ = __unicode__


def add_to_post(tag_id, post_id):
    try:
        tag_post = Tag_Post(None, post_id, tag_id)
        Session.add(tag_post)
        Session.commit()
    except:
        pass

    return


def get_tags(id):
    from argonaut.model.post import Post
    from argonaut.model.tag import Tag
    return Session.query(Tag).filter(Post.id == id).filter(Post.id == Tag_Post.post_id).filter(Tag_Post.tag_id == Tag.id).all()


def get_tag_counts(order=False):
    from argonaut.model.tag import Tag
    if order:
        s = select([Tag.name, func.count(Tag_Post.tag_id)], Tag.id == Tag_Post.tag_id).group_by(Tag.name).order_by(func.count(Tag_Post.tag_id).desc())
    else:
        s = select([Tag.name, func.count(Tag_Post.tag_id)], Tag.id == Tag_Post.tag_id).group_by(Tag.name)
    tags = Session.execute(s)
    return tags