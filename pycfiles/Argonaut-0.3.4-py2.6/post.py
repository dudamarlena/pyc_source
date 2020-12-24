# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/argonaut/model/post.py
# Compiled at: 2011-02-18 19:15:08
"""The post model"""
from sqlalchemy import Column, or_
from sqlalchemy.sql import join
from sqlalchemy.types import Integer, Unicode, UnicodeText, Date
from argonaut.model.meta import Base, Session

class Post(Base):
    __tablename__ = 'post'
    id = Column(Integer, primary_key=True)
    subject = Column(Unicode(300), nullable=False)
    body = Column(UnicodeText, nullable=False)
    posted = Column(Date, nullable=False)
    author = Column(Integer, nullable=True)
    viewed = Column(Integer, default=0)
    status = Column(Integer, default=1)

    def __init__(self, id=None, subject=None, body=None, posted=None, author=None, viewed=None, status=None):
        self.id = id
        self.subject = subject
        self.body = body
        self.posted = posted
        self.author = author
        self.viewed = viewed
        self.status = status

    def __unicode__(self):
        return self.subject

    def __repr__(self):
        return "<Post('%s','%s', '%s', '%s', '%s', '%s', '%s')>" % (self.id, self.subject, self.body, self.posted, self.author, self.viewed, self.status)

    __str__ = __unicode__


def get(id, active_only=True):
    try:
        if active_only:
            return Session.query(Post).filter(Post.status == 1).filter(Post.id == id).first()
        else:
            return Session.query(Post).get(id)
    except TypeError:
        return

    return


def get_many(amount=10, order='asc', active_only=True, count_only=False, filter=None):
    try:
        query = Session.query(Post)
        if active_only:
            query = query.filter(Post.status == 1)
        if filter:
            query = query.filter(or_(Post.subject.like('%' + filter + '%'), Post.body.like('%' + filter + '%')))
        if count_only:
            return query.limit(amount).count()
        if order == 'desc':
            return query.order_by(Post.id.desc()).limit(amount)
        return query.order_by(Post.id.asc()).limit(amount)
    except Exception:
        return

    return


def new():
    return Post()


def save(post):
    Session.add(post)
    Session.commit()


def get_by_tag_name(name):
    from argonaut.model.tag import Tag
    from argonaut.model.tag_post import Tag_Post
    return Session.query(Post).join(Tag_Post).join(Tag).filter(Post.status == 1).filter(Tag.name == name).order_by(Post.id.desc())