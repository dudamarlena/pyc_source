# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: __init__.py
# Compiled at: 2016-03-24 02:01:02
from __future__ import unicode_literals, division, absolute_import, print_function
import transaction, decimal, json, datetime, uuid
from math import ceil
from functools import partial
from sqlalchemy import orm
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import engine_from_config
from zope.sqlalchemy import ZopeTransactionExtension
from pyramid.httpexceptions import HTTPNotFound
from pyramid.i18n import TranslationString as _
from pyramid.renderers import JSON

def __init__(self, objd={}):
    for k in objd:
        if hasattr(self, k):
            setattr(self, k, objd[k])


def __repr__(self):
    dd = self.__dict__.copy()
    try:
        dd.pop(b'_sa_instance_state')
    except KeyError as e:
        print(e)

    v = (b', ').join([ (b'{}={}').format(*i) for i in dd.items() ])
    return (b'<{0}({1})>').format(self.__class__.__name__, v)


def get_or_create(session, model, **kw):
    obj = session.query(model).filter_by(**kw).first()
    if obj:
        return obj
    else:
        obj = model(**kw)
        session.add(obj)
        session.flush()
        return obj


def get_object_or_404(session, model, **kw):
    obj = session.query(model).filter_by(**kw).first()
    if obj is None:
        raise HTTPNotFound(detail=_(b'在给定的查询中没有找到匹配的对象: <{}> .').format(model.__name__))
    return obj


def merge_session_with_post(session, post):
    for key, value in post:
        setattr(session, key, value)

    return session


class Pagination(object):

    def __init__(self, query, page, per_page, total_count, items):
        self.query = query
        self.page = page
        self.per_page = per_page
        self.total = total_count
        self.items = items

    def __json__(self, request):
        return {b'page': self.page, 
           b'per_page': self.per_page, 
           b'total': self.total, 
           b'items': [ {c.name:getattr(item, c.name) for c in item.__table__.columns}
                    for item in self.items
                   ], 
           b'pages': self.pages, 
           b'has_prev': self.has_prev, 
           b'has_next': self.has_next, 
           b'prev_num': self.prev_num, 
           b'next_num': self.next_num}

    @property
    def pages(self):
        if self.per_page == 0:
            pages = 0
        else:
            pages = int(ceil(self.total / float(self.per_page)))
        return pages

    def prev(self, error_out=False):
        assert self.query is not None, b'a query object is required for this method to work'
        return self.query.paginate(self.page - 1, self.per_page, error_out)

    @property
    def prev_num(self):
        return self.page - 1

    @property
    def has_prev(self):
        return self.page > 1

    def next(self, error_out=False):
        assert self.query is not None, b'a query object is required for this method to work'
        return self.query.paginate(self.page + 1, self.per_page, error_out)

    def __next__(self, error_out=False):
        return self.next(error_out)

    def __iter__(self):
        return self

    @property
    def has_next(self):
        return self.page < self.pages

    @property
    def next_num(self):
        return self.page + 1

    def iter_pages(self, left_edge=2, left_current=2, right_current=5, right_edge=2):
        last = 0
        for num in range(1, self.pages + 1):
            _mok = num > self.page - left_current - 1 and num < self.page + right_current
            if num <= left_edge or _mok or num > self.pages - right_edge:
                if last + 1 != num:
                    yield
                yield num
                last = num

        return


def paginate(query, page, per_page=20, error_out=False):
    if error_out and page < 1:
        raise HTTPNotFound(detail=b'无此页码-页码小于1')
    items = query.limit(per_page).offset((page - 1) * per_page).all()
    if not items and page != 1 and error_out:
        raise HTTPNotFound(detail=b'无此页码')
    if page == 1 and len(items) < per_page:
        total = len(items)
    else:
        total = query.order_by(None).count()
    return Pagination(query, page, per_page, total, items)


def db(request):

    def commit_callback(request):
        if request.exception is not None:
            transaction.abort()
        else:
            transaction.commit()
        return

    request.add_finished_callback(commit_callback)
    return DBSession


class Dict2Json(JSON):

    def __call__(self, info):

        def _render(value, system):
            request = system.get(b'request')
            if request is not None:
                response = request.response
                ct = response.content_type
            default = self._make_default(request)
            return self.serializer(value, default=default, **self.kw)

        return _render


def datetime_adapter(obj, request):
    return obj.strftime(b'%Y-%m-%d %H:%M:%S')


def timedelta_adapter(obj, request):
    return (b'{0:.6f}').format(obj.total_seconds())


def decimal_adapter(obj, request):
    return obj.to_eng_string()


def uuid_adapter(obj, request):
    return obj.hex


Base = declarative_base()
Base.__repr__ = __repr__
Base.__init__ = __init__
DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
DBSession.get_object_or_404 = partial(get_object_or_404, DBSession)
DBSession.get_or_create = partial(get_or_create, DBSession)
DBSession.merge_session_with_post = partial(merge_session_with_post, DBSession)
orm.Query.paginate = paginate
sql_json_renderer = Dict2Json(serializer=partial(json.dumps, ensure_ascii=False))
sql_json_renderer.add_adapter(datetime.date, datetime_adapter)
sql_json_renderer.add_adapter(datetime.datetime, datetime_adapter)
sql_json_renderer.add_adapter(datetime.timedelta, timedelta_adapter)
sql_json_renderer.add_adapter(decimal.Decimal, decimal_adapter)
sql_json_renderer.add_adapter(uuid.UUID, uuid_adapter)

def engine(settings):
    _engine = engine_from_config(settings, b'sqlalchemy.')
    DBSession.configure(bind=_engine)
    Base.metadata.bind = _engine