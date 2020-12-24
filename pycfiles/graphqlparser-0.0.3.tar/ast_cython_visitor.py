# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/marco/devel/elastic-coders/pygraphql-parser/ast/ast_cython_visitor.py
# Compiled at: 2015-09-18 18:08:54
from casing import snake
import ast_cython_c

class Printer(object):
    """Printer for a visitor in cython
  """

    def __init__(self):
        self._types = []

    def start_file(self):
        print ast_cython_c.license_comment() + '\n\ncdef extern from "GraphQLAstVisitor.h":\n\n    struct GraphQLAstNode:\n        pass\n\n\n'

    def start_type(self, name):
        self._types.append(name)
        _map = {'snake': snake(name), 'name': name}
        print '    struct %s:' % ast_cython_c.struct_name(name)
        print '        pass'
        print '    ctypedef int (*visit_%(snake)s_func)(GraphQLAst%(name)s*, void*)' % _map
        print '    ctypedef void (*end_visit_%(snake)s_func)(GraphQLAst%(name)s*, void*)' % _map

    def field(self, type, name, nullable, plural):
        pass

    def end_type(self, name):
        pass

    def end_file(self):
        print '    struct GraphQLAstVisitorCallbacks:'
        for name in self._types:
            _map = {'snake': snake(name)}
            print '        visit_%(snake)s_func visit_%(snake)s' % _map
            print '        end_visit_%(snake)s_func end_visit_%(snake)s' % _map

        print '\n    void graphql_node_visit(GraphQLAstNode *node,\n                            GraphQLAstVisitorCallbacks *callbacks,\n                            void *userData)\n'

    def start_union(self, name):
        pass

    def union_option(self, option):
        pass

    def end_union(self, name):
        pass