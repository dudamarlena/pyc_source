# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-intel/egg/glyph/resource.py
# Compiled at: 2012-03-05 05:15:38
""" resource.py

contains Resource, Mapper and Router
"""
from urllib import quote_plus, unquote_plus
from uuid import uuid4
from werkzeug.wrappers import Request, Response
from werkzeug.exceptions import HTTPException, NotFound, BadRequest, NotImplemented, MethodNotAllowed
from .encoding import CONTENT_TYPE, dump, parse, get, form, link, node, embed, ismethod, methodargs

class SeeOther(HTTPException):
    """ A werkzeug http exception for redirects """
    code = 303
    description = ''

    def __init__(self, url):
        self.url = url
        HTTPException.__init__(self)

    def get_headers(self, environ):
        return [('Location', self.url)]


class BaseResource(object):
    """ An abstract resource to be served. Contains a mapper attribute __glyph__,
    which contains a mapper class to use for this resource,
    """
    __glyph__ = None

    def index(self):
        return dict((k, v) for k, v in self.__dict__.items() if not k.startswith('_'))


class BaseMapper(object):
    """ The base mapper - bound to a class and a prefix, handles requests
    from the router, and finds/creates a resource to handle it.

    This handles the verb mapping part of http, as well as the serializing/
    deserializing content. It also maps methods to urls, as well as object
    state representation.
    """

    def __init__(self, prefix, cls):
        self.prefix = prefix
        self.cls = cls

    @staticmethod
    def parse(data):
        return parse(data)

    @staticmethod
    def dump(data, resolver):
        return (CONTENT_TYPE, dump(data, resolver))

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
        """ handle a given request from a router:
            find the right resource:
                dispatch to a method 
            or
                create an index of the object,
                including forms for methods

        """
        path = request.path[1:].split('/')[1:]
        attr_name = 'index' if not path or not path[0] else path[0]
        verb = request.method
        if attr_name == 'index' and verb == 'POST':
            data = request.data
            try:
                args = ResourceMethod.parse(self.cls.__init__, data) if data else {}
                obj = self.create_resource(args)
            except StandardError:
                raise BadRequest()

            raise SeeOther(router.url(obj))
        else:
            try:
                args = self.parse_query(request.query_string)
                obj = self.find_resource(args)
                attr = getattr(obj, attr_name)
            except StandardError:
                raise BadRequest()

            if verb == 'GET' and attr_name == 'index':
                result = ResourceMethod.index(obj)
            elif verb == 'GET' and ResourceMethod.is_safe(attr):
                result = attr()
            elif verb == 'POST' and not ResourceMethod.is_safe(attr):
                try:
                    data = ResourceMethod.parse(attr, request.data) if request.data else {}
                except StandardError:
                    raise BadRequest()

                result = attr(**data)
            else:
                raise MethodNotAllowed()
            if ResourceMethod.is_redirect(attr) and isinstance(result, BaseResource):
                raise SeeOther(router.url(result))
            else:
                content_type, result = ResourceMethod.dump(attr, result, router.url)
                return Response(result, content_type=content_type)

    def url(self, r):
        """ return a url string that reflects this resource:
            can be a resource class, instance or method
        """
        if isinstance(r, self.cls):
            return '/%s/?%s' % (self.prefix, self.dump_query(self.get_repr(r)))
        if isinstance(r, type) and issubclass(r, self.cls):
            return '/%s/' % self.prefix
        if ismethod(r, self.cls):
            return '/%s/%s/?%s' % (self.prefix, r.im_func.__name__, self.dump_query(self.get_repr(r.im_self)))
        raise LookupError()

    def create_resource(self, representation):
        raise NotImplemented()

    def find_resource(self, representation):
        raise NotImplemented()

    def get_repr(self, resource):
        """ return the representation of the state of the resource as a dict """
        raise NotImplemented()


class TransientMapper(BaseMapper):

    def create_resource(self, args):
        return self.cls(**args)

    def find_resource(self, args):
        return self.cls(**args)

    def get_repr(self, resource):
        repr = {}
        args = methodargs(resource.__init__)
        for k, v in resource.__dict__.items():
            if k in args:
                repr[k] = v

        return repr


class Resource(BaseResource):
    __glyph__ = TransientMapper


class PersistentMapper(BaseMapper):

    def __init__(self, prefix, cls):
        BaseMapper.__init__(self, prefix, cls)
        self.instances = {}
        self.identifiers = {}

    def create_resource(self, args):
        instance = self.cls(**args)
        uuid = str(uuid4())
        self.instances[uuid] = instance
        self.identifiers[instance] = uuid
        return instance

    def find_resource(self, uuid):
        return self.instances[uuid]

    def get_repr(self, instance):
        if instance not in self.identifiers:
            uuid = str(uuid4())
            self.instances[uuid] = instance
            self.identifiers[instance] = uuid
        else:
            uuid = self.identifiers[instance]
        return uuid


class PersistentResource(BaseResource):
    __glyph__ = PersistentMapper


class ResourceMethod(object):
    """ Represents the capabilities of methods on resources, used by the mapper
        to determine how to handle requests
    """
    SAFE = False
    INLINE = False
    EXPIRES = False
    REDIRECT = False

    def __init__(self, resourcemethod=None):
        if resourcemethod:
            self.safe = resourcemethod.safe
            self.inline = resourcemethod.inline
            self.expires = resourcemethod.expires
        else:
            self.safe = self.SAFE
            self.inline = self.INLINE
            self.redirect = self.REDIRECT

    @staticmethod
    def index(obj):
        """ Generate a glyph-node that contains 
            the object attributes and methods
        """
        page = dict()
        page.update(make_controls(obj))
        page.update(obj.index())
        return node(obj.__class__.__name__, attributes=page)

    @staticmethod
    def parse(resource, data):
        return parse(data)

    @staticmethod
    def dump(resource, data, resolver):
        return (CONTENT_TYPE, dump(data, resolver))

    @classmethod
    def is_safe(cls, m):
        try:
            return m.__glyph_method__.safe
        except StandardError:
            return cls.SAFE

    @classmethod
    def is_inline(cls, m):
        try:
            return m.__glyph_method__.inline
        except StandardError:
            return cls.INLINE

    @classmethod
    def is_redirect(cls, m):
        try:
            return m.__glyph_method__.redirect
        except StandardError:
            return cls.REDIRECT


def get_mapper(obj, name):
    """ return the mapper for this object, with a given name"""
    if hasattr(obj, '__glyph__') and issubclass(obj.__glyph__, BaseMapper):
        return obj.__glyph__(name, obj)
    raise StandardError('no mapper for object')


class Router(object):

    def __init__(self):
        self.mappers = {}
        self.routes = {}
        self.default_path = ''

    def __call__(self, environ, start_response):
        request = Request(environ)
        try:
            if request.path == '/':
                raise SeeOther(self.default_path)
            try:
                mapper = self.find_mapper(request.path)
            except StandardError:
                raise NotFound()

            response = mapper.handle(request, self)
        except (StopIteration, GeneratorExit, SystemExit, KeyboardInterrupt):
            raise
        except HTTPException as r:
            response = r
        except Exception as e:
            import traceback
            traceback.print_exc()
            response = Response(traceback.format_exc(), status='500 not ok')

        return response(environ, start_response)

    def find_mapper(self, path):
        path = path[1:].split('/')
        return self.routes[path[0]]

    def register(self, obj, path=None, default=False):
        if path is None:
            path = obj.__name__
        mapper = get_mapper(obj, path)
        self.routes[path] = mapper
        self.mappers[obj] = mapper
        if default:
            self.default_path = path
        return obj

    def url(self, r):
        if isinstance(r, basestring):
            return r
        if isinstance(r, BaseResource):
            return self.mappers[r.__class__].url(r)
        if isinstance(r, type) and issubclass(r, BaseResource):
            return self.mappers[r].url(r)
        if ismethod(r, BaseResource):
            return self.mappers[r.im_class].url(r)
        raise LookupError('no url for', r)

    def add(self):
        return self.register

    def default(self):
        return lambda obj: self.register(obj, default=True)


def make_controls(resource):
    forms = {}
    for m in dir(resource.__class__):
        if not m.startswith('_') and m != 'index':
            cls_attr = getattr(resource.__class__, m)
            if isinstance(cls_attr, property):
                raise StandardError()
                page[m] = prop((resource, m))
            elif callable(cls_attr):
                ins_attr = getattr(resource, m)
                if hasattr(ins_attr, 'func_code'):
                    if ResourceMethod.is_safe(cls_attr):
                        if ResourceMethod.is_inline(cls_attr):
                            forms[m] = embed(ins_attr, content=ins_attr())
                        else:
                            forms[m] = link(ins_attr)
                    else:
                        forms[m] = form(ins_attr)

    return forms


def make_method_mapper(fn):
    if not hasattr(fn, '__glyph_method__'):
        fn.__glyph_method__ = ResourceMethod()
    return fn.__glyph_method__


def redirect(is_redirect=True):

    def _decorate(fn):
        m = make_method_mapper(fn)
        m.redirect = is_redirect
        return fn

    return _decorate


def safe(is_safe=True):

    def _decorate(fn):
        m = make_method_mapper(fn)
        m.safe = is_safe
        return fn

    return _decorate


def inline(is_inline=True):

    def _decorate(fn):
        m = make_method_mapper(fn)
        m.safe = is_inline
        m.inline = is_inline
        return fn

    return _decorate