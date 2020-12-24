# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/argonaut/model/page_type.py
# Compiled at: 2011-02-18 19:15:08
"""The page_type model"""
from pylons import request, response, session, tmpl_context as c, url
from sqlalchemy import Column
from sqlalchemy.types import Unicode, Integer
from argonaut.model.meta import Base, Session

class Page_Type(Base):
    __tablename__ = 'page_type'
    id = Column(Integer, primary_key=True)
    name = Column(Unicode(30), nullable=False)
    controller = Column(Unicode(30), nullable=True)
    action = Column(Unicode(30), nullable=True)
    param = Column(Unicode(30), nullable=True)

    def __init__(self):
        self.id = None
        self.name = ''
        self.controller = None
        self.action = None
        self.param = None
        return

    def __unicode__(self):
        return self.name

    def __repr__(self):
        return "<Page_Type('%s','%s','%s','%s','%s')>" % (self.id, self.name, self.controller, self.action, self.param)

    __str__ = __unicode__


def get_url(id, url_param):
    route = Session.query(Page_Type).get(id)
    if url_param:
        target = url(controller=route.controller, action=route.action, id=url_param)
    elif len(route.param) > 0:
        target = url(controller=route.controller, action=route.action, id=route.param)
    else:
        target = url(controller=route.controller, action=route.action)
    return target