# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/marco/devel/elastic-coders/pygraphql-parser/ast/ast_cython_impl.py
# Compiled at: 2015-09-18 18:08:54
from casing import snake
import ast_cython_c, ast_cython
SIMPLE_RETURN_CASTS = {'boolean': 'bool', 
   'int': '', 
   'string': '', 
   'OperationKind': ''}
SOURCE_TYPE_CASTS = {'IntValue': 'int', 
   'FloatValue': 'float', 
   'StringValue': '', 
   'BooleanValue': 'bool', 
   'EnumValue': ''}

def field_prototype(owning_type, type, name, nullable, plural):
    _map = {'cmodule': ast_cython_c.CMODULE_NAME, 'owning_st': ast_cython_c.struct_name(owning_type), 
       'snake': snake(name), 
       'return_st': ast_cython_c.struct_name(type)}
    if plural:
        return '\n    def get_%(snake)s_size(self):\n        return int(%(cmodule)s.%(owning_st)s_get_%(snake)s_size(self._wrapped))\n' % _map
    else:
        if type in SIMPLE_RETURN_CASTS:
            if owning_type in SOURCE_TYPE_CASTS:
                _map['cast'] = SOURCE_TYPE_CASTS[owning_type]
            else:
                _map['cast'] = SIMPLE_RETURN_CASTS[type]
            return '\n    def get_%(snake)s(self):\n        val = %(cmodule)s.%(owning_st)s_get_%(snake)s(self._wrapped)\n        if val is None:\n            return None\n        return %(cast)s(val)\n' % _map
        if type in ('Type', 'Value'):
            return '\n'
        return '\n    def get_%(snake)s(self):\n        cdef %(cmodule)s.%(return_st)s *next\n        next = %(cmodule)s.%(owning_st)s_get_%(snake)s(self._wrapped)\n        if next is NULL:\n           return None\n        return %(return_st)s.create(next)\n' % _map


class Printer(object):
    """Printer for a visitor in cython
  """

    def __init__(self):
        self._types = []

    def start_file(self):
        print ast_cython_c.license_comment() + '\n\ncimport %s\n\ncdef class GraphQLAst:\n    """Base class for all Ast pieces"""\n    pass\n\n' % ast_cython_c.CMODULE_NAME

    def start_type(self, name):
        self._current_type = name
        _map = {'snake': snake(name), 'name': name}
        print '\n\ncdef class %(name)s(GraphQLAst):\n\n    @staticmethod\n    cdef create(%(cmodule)s.%(name)s *thing):\n        node = %(name)s()\n        node._wrapped = thing\n        return node\n\n' % {'name': ast_cython_c.struct_name(name), 'cmodule': ast_cython_c.CMODULE_NAME}

    def field(self, type, name, nullable, plural):
        print field_prototype(self._current_type, type, name, nullable, plural)

    def end_type(self, name):
        print
        print

    def end_file(self):
        pass

    def start_union(self, name):
        pass

    def union_option(self, option):
        pass

    def end_union(self, name):
        pass