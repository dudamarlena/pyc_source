# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/dlaxalde/src/cw/cubes/localperms/cubicweb_localperms/ccplugin.py
# Compiled at: 2019-03-13 06:52:19
# Size of source mod 2**32: 6505 bytes
"""cubicweb-ctl plugin providing the check-localperms command"""
from __future__ import print_function
__docformat__ = 'restructuredtext en'
import os
from cubicweb.toolsutils import Command
from cubicweb.cwctl import CWCTL
try:
    from cubicweb.devtools.instrument import PropagationAnalyzer, warn, get_color
    register_command = True
except ImportError:
    register_command = False
else:

    class PermissionPropagationAnalyzer(PropagationAnalyzer):
        prop_rel = 'require_permission'

        def is_root(self, eschema):
            return 'granted_permission' in eschema.subjrels

        def should_include(self, eschema):
            return super(PermissionPropagationAnalyzer, self).should_include(eschema) or any((self.prop_rel in rqlexpr.expression for rqlexpr in eschema.get_rqlexprs('read')))


def read_permission_edges(eschemas):
    """return a set of edges where <from node>'s read perms are referencing <to
    node>'s permissions.

    Each edge is defined by a 4-uple (from node, to node, rtype, package) where
    `rtype` is the relation type bringing from <from node> to <to node> and
    `package` is the cube defining the read permission rql expresssion.
    """
    perm_edges = set()
    for eschema in eschemas:
        for rqlexpr in eschema.get_rqlexprs('read'):
            triplets = [expr.split() for expr in rqlexpr.expression.split(',')]
            triplets = [triplet for triplet in triplets if len(triplet) == 3 if triplet[1] != 'has_group_permission']
            for triplet in triplets:
                subjvar, rel, objvar = triplet
                if rel == 'require_permission' and subjvar != 'X':
                    searchvar = subjvar
                    break
            else:
                continue

            for triplet in triplets:
                subjvar, rel, objvar = triplet
                if rel == 'require_permission':
                    continue
                if subjvar == searchvar:
                    if objvar != 'X':
                        print('Oops, unhandled 2 hops', eschema, triplet, searchvar, objvar)
                        continue
                    for target in eschema.objrels[rel].targets(eschema, 'object'):
                        if target in eschemas:
                            perm_edges.add((eschema.type, target.type, rel, rqlexpr.package))

                elif objvar == searchvar:
                    if subjvar != 'X':
                        print('Oops, unhandled 2 hops', eschema, triplet, searchvar, subjvar)
                        continue
                    for target in eschema.subjrels[rel].targets(eschema, 'subject'):
                        if target in eschemas:
                            perm_edges.add((eschema.type, target.type, rel, rqlexpr.package))

    return perm_edges


class CheckLocalPermsCommand(Command):
    __doc__ = 'Analyse local permissions configuration.\n\n    It will load the given cube schema and hooks, analyze local permissions in\n    read permission and propagation rules to print on the standart output\n    warnings about detected problems.\n    '
    name = 'check-localperms'
    arguments = '<cube>'
    min_args = max_args = 1
    options = (
     (
      'graph',
      {'short':'g', 
       'type':'string',  'metavar':'<file>',  'default':None, 
       'help':'draw propagation graph in the given file. Require pygraphviz installed'}),)

    def run(self, args):
        """run the command with its specific arguments"""
        cube = args[0]
        os.environ['LOCALPERMS_INSTRUMENTALIZE'] = '1'
        analyzer = PermissionPropagationAnalyzer()
        vreg, eschemas = analyzer.init(cube)
        if not eschemas:
            warn('nothing to analyze')
            return
        from cubicweb_localperms.hooks import S_RELS, O_RELS
        prop_edges = analyzer.prop_edges(S_RELS, O_RELS, eschemas)
        perm_edges = read_permission_edges(eschemas)
        problematic = analyzer.detect_problems(eschemas, prop_edges)
        for eschema in eschemas:
            if analyzer.is_root(eschema) or any((edge for edge in perm_edges if edge[1] == eschema)):
                any((edge for edge in prop_edges if edge[1] == eschema)) or warn("%s is used in a read permission but isn't reached by propagation", eschema)
                problematic.add(eschema)

        if self.config.graph:
            graph = analyzer.init_graph(eschemas, prop_edges, problematic)
            for subj, obj, rtype, package in perm_edges:
                graph.add_edge((str(subj)), (str(obj)), label=rtype, color=(get_color(package)),
                  arrowhead='normal',
                  style='dashed')

            analyzer.add_colors_legend(graph)
            graph.layout(prog='dot')
            graph.draw(self.config.graph)


if register_command:
    CWCTL.register(CheckLocalPermsCommand)