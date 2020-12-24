# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tornado_swirl/swagger.py
# Compiled at: 2019-12-17 19:27:20
# Size of source mod 2**32: 3084 bytes
"""Swagger decorators"""
import inspect, tornado.web
from tornado_swirl import docparser, settings
from tornado_swirl.handlers import swagger_handlers

class Ref(object):

    def __init__(self, value):
        self.link = value


def is_rest_api_method--- This code section failed: ---

 L.  15         0  LOAD_GLOBAL              inspect
                2  LOAD_METHOD              isfunction
                4  LOAD_FAST                'obj'
                6  CALL_METHOD_1         1  '1 positional argument'
                8  POP_JUMP_IF_TRUE     20  'to 20'
               10  LOAD_GLOBAL              inspect
               12  LOAD_METHOD              ismethod
               14  LOAD_FAST                'obj'
               16  CALL_METHOD_1         1  '1 positional argument'
               18  JUMP_IF_FALSE_OR_POP    42  'to 42'
             20_0  COME_FROM             8  '8'

 L.  16        20  LOAD_FAST                'obj'
               22  LOAD_ATTR                __name__
               24  LOAD_GLOBAL              list
               26  LOAD_GLOBAL              settings
               28  LOAD_ATTR                default_settings
               30  LOAD_METHOD              get
               32  LOAD_STR                 'enabled_methods'
               34  BUILD_LIST_0          0 
               36  CALL_METHOD_2         2  '2 positional arguments'
               38  CALL_FUNCTION_1       1  '1 positional argument'
               40  COMPARE_OP               in
             42_0  COME_FROM            18  '18'
               42  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `RETURN_VALUE' instruction at offset 42


def restapi(url, **kwargs):
    """REST API endpoint decorator."""

    def _real_decorator(cls):
        cls.rest_api = True
        cls.tagged_api_comps = []
        members = inspect.getmembersclsis_rest_api_method
        for name, member in members:
            doc = inspect.getdocmember
            if not doc:
                continue
            path_spec = docparser.parse_from_docstringstr(doc)
            if path_spec:
                setattr(member, 'path_spec', path_spec)
                cls.tagged_api_comps.appendname

        settings.add_api_handlercls
        (settings.add_route)(url, cls, **kwargs)
        return cls

    return _real_decorator


def schema(cls):
    """REST API schema decorator"""
    name = cls.__name__
    mro = inspect.getmrocls
    if not mro:
        mro = (
         cls,)
    mro = list(mro)
    mro.reverse()
    cls.schema_spec = []
    for item in mro:
        if item.__name__ == 'object':
            continue
        if item.__name__ == name:
            doc = inspect.getdocitem
            try:
                model_spec = docparser.parse_from_docstring(doc, spec='schema')
                if model_spec:
                    cls.schema_spec.appendmodel_spec
                    settings.add_schemanamecls
                    if hasattr(cls, 'Meta'):
                        if hasattr(cls.Meta, 'example'):
                            model_spec.example = cls.Meta.example
                        if hasattr(cls.Meta, 'examples'):
                            model_spec.examples = cls.Meta.examples
            except:
                pass

        else:
            cls.schema_spec.appendRef('#/components/schemas/{}'.formatitem.__name__)

    return cls


def describe(title='Your API', description='No description', **kwargs):
    """Describe API"""
    settings.default_settings.update{'title':title,  'description':description}
    if kwargs:
        settings.default_settings.updatekwargs


def add_global_tag(name, description=None, url=None):
    settings.add_global_tag(name, description, url)


def add_security_scheme(name, scheme):
    settings.add_security_schemenamescheme


class Application(tornado.web.Application):
    __doc__ = 'Swirl Application class'

    def __init__(self, handlers=None, default_host='', transforms=None, **kwargs):
        (super(Application, self).__init__)(
         (swagger_handlers() + handlers if handlers else swagger_handlers()), 
         default_host, transforms, **kwargs)