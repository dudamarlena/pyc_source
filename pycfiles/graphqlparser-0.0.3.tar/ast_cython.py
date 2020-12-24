# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/marco/devel/elastic-coders/pygraphql-parser/ast/ast_cython.py
# Compiled at: 2015-09-19 16:49:10
from casing import snake
import re, ast_cython_c
CMODULE_NAME = 'GraphQLAst'

class Printer(object):
    """Printer for the Ast Python Object level cython interface.

  """

    def start_file(self):
        print ast_cython_c.license_comment() + '\n\ncimport %s\n\n\ncdef class GraphQLAst:\n    """Base class for all Ast pieces"""\n    pass\n\n' % ast_cython_c.CMODULE_NAME

    def end_file(self):
        pass

    def start_type(self, name):
        st_name = ast_cython_c.struct_name(name)
        print '\ncdef class %(name)s(GraphQLAst):\n\n    cdef %(cmodule)s.%(name)s* _wrapped\n\n    @staticmethod\n    cdef create(cGraphQLAst.%(name)s *thing)\n\n' % {'name': st_name, 'cmodule': ast_cython_c.CMODULE_NAME}
        self._current_type = name

    def field(self, type, name, nullable, plural):
        pass

    def end_type(self, name):
        print
        print

    def start_union(self, name):
        pass

    def union_option(self, option):
        pass

    def end_union(self, name):
        print