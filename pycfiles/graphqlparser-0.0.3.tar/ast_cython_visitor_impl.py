# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/marco/devel/elastic-coders/pygraphql-parser/ast/ast_cython_visitor_impl.py
# Compiled at: 2015-09-19 16:49:10
from casing import snake
import ast_cython_c
CMODULE_NAME = 'cGraphQLAstVisitor'

class Printer(object):
    """Printer for a visitor implementation in cython
  """

    def __init__(self):
        self._types = []

    def start_file(self):
        print ast_cython_c.license_comment() + '\n\nfrom libc.string cimport memset\ncimport %(cmodule)s\ncimport GraphQLAstNode\ncimport cGraphQLAstNode\ncimport cGraphQLAst\ncimport GraphQLAst\n\ncdef class GraphQLAstVisitor:\n\n    def visit_node(self, node):\n      cdef %(cmodule)s.GraphQLAstVisitorCallbacks callbacks_c\n      memset(&callbacks_c, 0, sizeof(callbacks_c))\n      set_callbacks(&callbacks_c)\n      cdef void* userData = <void *>self\n      cdef cGraphQLAstNode.GraphQLAstNode *node_c;\n      node_c = (<GraphQLAstNode.GraphQLAstNode?>node)._node\n      %(cmodule)s.graphql_node_visit(node_c, &callbacks_c, userData)\n\n' % {'cmodule': CMODULE_NAME}

    def start_type(self, name):
        self._types.append(name)

    def field(self, type, name, nullable, plural):
        pass

    def end_type(self, name):
        pass

    def end_file(self):
        for type in self._types:
            _map = {'snake': snake(type), 'name': type, 'cmodule': CMODULE_NAME}
            print "\n\ncdef int _visit_%(snake)s(%(cmodule)s.GraphQLAst%(name)s* node, void* userData, int end):\n    cdef GraphQLAstVisitor visitor\n    ast = GraphQLAst.GraphQLAst%(name)s.create(node)\n    if userData is not NULL:\n      visitor = <GraphQLAstVisitor>userData\n      attname = 'end_visit_%(snake)s' if end else 'visit_%(snake)s'\n      fun = getattr(visitor, attname, None)\n      if fun is not None:\n        retval = fun(ast)\n        return 0 if retval is None else retval\n\ncdef int visit_%(snake)s(%(cmodule)s.GraphQLAst%(name)s* node, void* userData):\n    return _visit_%(snake)s(node, userData, 0)\n\ncdef void end_visit_%(snake)s(%(cmodule)s.GraphQLAst%(name)s* node, void* userData):\n    _visit_%(snake)s(node, userData, 1)\n" % _map

        print '\n\ncdef set_callbacks(%(cmodule)s.GraphQLAstVisitorCallbacks *callbacks):\n' % {'cmodule': CMODULE_NAME}
        for type in self._types:
            _map = {'snake': snake(type), 'name': type, 'cmodule': CMODULE_NAME}
            print '\n    callbacks.visit_%(snake)s = &visit_%(snake)s\n    callbacks.end_visit_%(snake)s = &end_visit_%(snake)s\n' % _map

    def start_union(self, name):
        pass

    def union_option(self, option):
        pass

    def end_union(self, name):
        pass