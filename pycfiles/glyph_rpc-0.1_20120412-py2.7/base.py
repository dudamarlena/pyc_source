# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-intel/egg/glyph/resource/base.py
# Compiled at: 2012-03-28 11:41:04
import types
from urllib import quote_plus, unquote_plus
from werkzeug.wrappers import Request, Response
from werkzeug.exceptions import HTTPException, NotFound, BadRequest, NotImplemented, MethodNotAllowed
from werkzeug.utils import redirect as Redirect
from ..data import CONTENT_TYPE, dump, parse, get, form, link, node, embed, ismethod, methodargs
from .handler import Handler, make_controls

class BaseResource(object):
    """ An abstract resource to be served. Contains a mapper attribute __glyph__,
    which contains a mapper class to use for this resource,
    """
    __glyph__ = None

    def GET(self):
        """ Generate a glyph-node that contains 
            the object attributes and methods
        """
        page = dict()
        page.update(make_controls(self))
        page.update(self.index())
        return node(self.__class__.__name__, attributes=page)

    def index(self):
        return dict((k, v) for k, v in self.__dict__.items() if not k.startswith('_'))


def get_mapper(obj, name):
    """ return the mapper for this object, with a given name"""
    if hasattr(obj, '__glyph__') and issubclass(obj.__glyph__, BaseMapper):
        return obj.__glyph__(name, obj)
    if isinstance(obj, types.FunctionType):
        return BaseMapper(name, obj)
    raise StandardError('no mapper for object')


class BaseMapper(object):
    """ The base mapper - bound to a class and a prefix, handles requests
    from the router, and finds/creates a resource to handle it.

    This handles the verb mapping part of http, as well as the serializing/
    deserializing content. It also maps methods to urls, as well as object
    state representation.
    """

    def __init__(self, prefix, res):
        self.prefix = prefix
        self.res = res

    @staticmethod
    def dump_query(d):
        """ transform a dict into a query string """
        if d:
            return quote_plus(dump(d))
        return ''

    @staticmethod
    def parse_query(query):
        """ turn a query string into a dict """
        if query:
            return parse(unquote_plus(query))
        return {}

    def handle(self, request, router):
        return Handler.call(self.res, request, router)

    def url(self, r):
        """ return a url string that reflects this resource:
            can be a resource class, instance or method
        """
        if isinstance(r, basestring):
            return r
        if r is self.res:
            return '/%s' % self.prefix
        raise LookupError()


class ClassMapper(BaseMapper):

    def handle(self, request, router):
        path = request.path.split(self.prefix)[1]
        verb = request.method.upper()
        try:
            if path:
                attr_name = path[1:] if path[1:] else verb
                args = self.parse_query(request.query_string)
                obj = self.get_instance(args)
                attr = getattr(obj, attr_name)
            else:
                attr = self.default_method(verb)
        except StandardError:
            raise BadRequest()

        return Handler.call(attr, request, router)

    def default_method(self, verb):
        try:
            return getattr(self, verb)
        except:
            raise MethodNotAllowed()

    def url(self, r):
        """ return a url string that reflects this resource:
            can be a resource class, instance or method
        """
        if isinstance(r, self.res):
            return '/%s/?%s' % (self.prefix, self.dump_query(self.get_repr(r)))
        else:
            if isinstance(r, type) and issubclass(r, self.res):
                return '/%s' % self.prefix
            if ismethod(r, self.res):
                return '/%s/%s?%s' % (self.prefix, r.im_func.__name__, self.dump_query(self.get_repr(r.im_self)))
            return BaseMapper.url(self, r)

    def get_instance(self, representation):
        raise NotImplemented()

    def get_repr(self, resource):
        """ return the representation of the state of the resource as a dict """
        raise NotImplemented()