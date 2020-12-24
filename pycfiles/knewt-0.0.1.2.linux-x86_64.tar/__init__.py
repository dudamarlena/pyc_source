# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/sven/0/_sdks/python/sven-2.7/lib/python2.7/site-packages/knewt/__init__.py
# Compiled at: 2018-02-12 17:31:21
from debug import log, trace
from store import primitive_store

class Node:

    def __init__(self, g):
        self.__graph__ = g

    def in_degree(self, n):
        in_deg = lambda g, n: [ e for e in g.edges if e[1] == n ]
        return len(in_deg(self.__graph__, n))

    def out_degree(self, n):
        out_deg = lambda g, n: [ e for e in g.edges if e[0] == n ]
        return len(out_deg(self.__graph__, n))


class Graph:

    def __init__(self, label=None, density=3, storage=primitive_store):
        if label is None:
            label = '__UNDEF_'
        self.__edges__ = set([])
        self.__nodes__ = set([])
        self.__adjacency_list__ = {}
        self.__label__ = label
        let, get, hasher = storage()
        self.__properties_get__ = get
        self.__properties_let__ = let
        self.__properties_hasher__ = hasher
        return

    def __str__(self):
        return '<label=%s,nodes=%s,edges=%s>' % (self.__label__, len(self.__nodes__), len(self.__edges__))

    @property
    def edges(self):
        return self.__edges__

    @property
    def nodes(self):
        return self.__nodes__

    @staticmethod
    def values(edges):
        pass

    def extend_node(self, v):
        if v not in self.__nodes__:
            self.__nodes__.add(v)
        if v not in self.__adjacency_list__:
            self.__adjacency_list__[v] = set([])

    def add_node(self, v):
        v = self.__hasher__(v)
        self.extend_node(v)

    def extend_path(self, path):
        for i, el in enumerate(path):
            if i == 0:
                self.add_node(path[i])
                continue
            a = path[(i - 1)]
            b = path[i]
            self.extend_node(a, b)

    def add_path(self, path):
        for i, el in enumerate(path):
            if i == 0:
                self.add_node(path[i])
                continue
            a = path[(i - 1)]
            b = path[i]
            self.add_edge(a, b)

    def update(self, other_graph):
        self.__nodes__ = self.__nodes__.union(other_graph.__nodes__)
        for e in other_graph.__edges__:
            self.extend_edges(e[0], e[1])

    def union(self, other):
        g = Graph()
        edges = self.__edges__.union(other.__edges__)
        nodes = self.__nodes__.union(other.__nodes__)
        for e in edges:
            g.add_edge(e[0], e[1])

        for n in nodes:
            g.add_node(n)

        return g

    def extend_edges(self, a, b):
        [ self.__nodes__.add(v) for v in (a, b) if v not in self.__nodes__ ]
        self.__edges__.add((a, b))
        [ self.__nodes__.add(v) for v in (a, b) if v not in self.__nodes__ ]
        self.__edges__.add((a, b))
        new_entries = [ (v, set([])) for v in (a, b) if v not in self.__adjacency_list__ ]
        self.__adjacency_list__.update(dict(new_entries))
        if (
         a, b) not in self.__adjacency_list__[a]:
            self.__adjacency_list__[a].add(b)

    def add_edge(self, a, b):
        a_hash = self.__properties_hasher__(a)
        b_hash = self.__properties_hasher__(b)
        self.__properties_let__(a, a)
        self.__properties_let__(b, b)
        trace('* (add-edge): (%s,%s),hash(%s,%s)' % (a, b, a_hash, b_hash))
        self.extend_edges(a_hash, b_hash)

    @staticmethod
    def from_tuples(edges, storage=None):
        if storage is None:
            g = Graph()
        else:
            g = Graph(storage=storage)
        for e in edges:
            a = e[0]
            b = e[1]
            g.add_edge(a, b)

        return g

    def node_mapper(g1, fn):
        for k in g1.__nodes__:
            v = g1.__properties_get__(k)
            yield fn(k, v)

    def edge_mapper(g1, fn):
        for a, b in g1.__edges__:
            v_a = g1.__properties__get__(a)
            v_b = g1.__properties__get__(b)
            yield fn(a, b)


class Graph2:

    def __init__(self, label=None, store=None):
        if label is None:
            label = '__UNDEF_'
        self.__edges__ = set([])
        self.__nodes__ = set([])
        self.__adjacency_list__ = {}
        self.__label__ = label
        return

    def __str__(self):
        return '<label=%s,nodes=%s,edges=%s>' % (self.__label__, len(self.__nodes__), len(self.__edges__))

    @property
    def edges(self):
        return self.__edges__

    @property
    def nodes(self):
        return self.__nodes__

    def add_node(self, v):
        if v not in self.__nodes__:
            self.__nodes__.add(v)
        if v not in self.__adjacency_list__:
            self.__adjacency_list__[v] = set([])

    def add_path(self, path):
        for i, el in enumerate(path):
            if i == 0:
                self.add_node(path[i])
                continue
            a = path[(i - 1)]
            b = path[i]
            self.add_edge(a, b)

    def update(self, other_graph):
        self.__nodes__ = self.__nodes__.union(other_graph.__nodes__)
        for e in other_graph.__edges__:
            self.add_edge(e[0], e[1])

    def union(self, other):
        g = Graph()
        edges = self.__edges__.union(other.__edges__)
        nodes = self.__nodes__.union(other.__nodes__)
        for e in edges:
            g.add_edge(e[0], e[1])

        for n in nodes:
            g.add_node(n)

        return g

    def add_edge(self, a, b):
        [ self.__nodes__.add(v) for v in (a, b) if v not in self.__nodes__ ]
        self.__edges__.add((a, b))
        new_entries = [ (v, set([])) for v in (a, b) if v not in self.__adjacency_list__ ]
        self.__adjacency_list__.update(dict(new_entries))
        if (
         a, b) not in self.__adjacency_list__[a]:
            self.__adjacency_list__[a].add(b)

    @staticmethod
    def from_tuples(edges):
        g = Graph()
        for e in edges:
            a = e[0]
            b = e[1]
            g.add_edge(a, b)

        return g


class Traverser2:
    DEPTH = '__depth__'
    NEIGHBOURS = 'neighbours'
    PATH = '__path__'

    def __init__(self):
        self.__component_groupers__ = {}
        self.__partition_schemes__ = {}

    def grouper_add(self, name, fn):
        self.__component_groupers__[name] = fn

    def partition(self, name, fn):
        self.__partition_schemes__[name] = fn

    def update_components(self):
        self.component_start_depths = {}
        for name in self.__components__:
            self.__components__[name].append(None)
            c = Graph('%s_%s' % (name, len(self.__components__[name])))
            self.__components__[name][-1] = c

        return

    def bfs(self, g):
        self.__components__ = {}
        self.__visited__ = set([])
        for node in list(g.__nodes__):
            if node in self.__visited__:
                continue
            self.update_components()
            self.__traversal_visited__ = set([])
            self.alg_bfs(g, node)

    def dfs(self, g, ignore_cycles=False):
        self.__components__ = {}
        self.__partitions__ = {}
        self.__visited__ = set([])
        self.__iteration__ = 0
        for node in list(g.__nodes__):
            if node in self.__visited__:
                continue
            self.update_components()
            self.__traversal_visited__ = set([])
            self.alg_dfs(g, node, ignore_cycles=ignore_cycles)
            self.component_start_depths = {}
            self.__iteraton__ = self.__iteration__ + 1

    def alg_dfs(self, g, node=None, depth=0, context=None, ignore_cycles=False):
        self.__visited__.add(node)
        self.__traversal_visited__.add(node)
        neighbours = g.__adjacency_list__[node]
        if context is None:
            context = self.context({'graph': g, Traverser.DEPTH: depth, 'neighbours': neighbours, Traverser.PATH: [node]})
        else:
            ctxt = self.context({'graph': g, Traverser.DEPTH: depth, 'neighbours': neighbours})
            context.update(ctxt)
        for n in neighbours:
            self.apply_component_lambdas(g, node, (node, n), context=context)
            self.apply_partition_lambdas(g, node, (node, n), context=context)
            if n in self.__traversal_visited__:
                if ignore_cycles is False:
                    raise Exception('Cylce Detected  (%s,%s)' % (node, n))
                continue
            path = context[Traverser.PATH]
            new_context = {}
            new_context.update(context)
            new_path = []
            new_path.extend(path)
            new_path.append(n)
            new_context[Traverser.PATH] = new_path
            self.alg_dfs(g, node=n, depth=depth + 1, context=new_context, ignore_cycles=ignore_cycles)

        return

    def context(self, c):
        traversal_context = {'iteration': self.__iteration__}
        traversal_context.update(c)
        return traversal_context

    def groups(self):
        return self.__components__

    def partitions(self):
        return self.__partitions__

    def apply_partition_lambdas1(self, g, node, edge, context):
        for name in self.__partition_schemes__:
            fn = self.__partition_schemes__[name]
            n, e, hash_id = fn(node, edge, context)
            partition_name = '%s_%s' % (name, hash_id)
            if n is None and e is None:
                continue
            if hash_id is None:
                continue
            if partition_name not in self.__partitions__:
                self.__partitions__[partition_name] = []
                g = Graph(partition_name)
                self.__partitions__[partition_name].append(g)
            p = self.__partitions__[partition_name][0]
            if e is not None:
                p.add_edge(e[0], e[1])
            if n is not None:
                p.add_node(n)

        return

    def apply_partition_lambdas(self, g, node, edge, context):
        for name in self.__partition_schemes__:
            fn = self.__partition_schemes__[name]
            if type(fn(node, edge, context)) == tuple:
                result = [
                 fn(node, edge, context)]
            else:
                result = fn(node, edge, context)
            for r in result:
                print r
                n, e, hash_id = r[0], r[1], r[2]
                partition_name = '%s_%s' % (name, hash_id)
                if n is None and e is None:
                    continue
                if hash_id is None:
                    continue
                if partition_name not in self.__partitions__:
                    self.__partitions__[partition_name] = []
                    g = Graph(partition_name)
                    self.__partitions__[partition_name].append(g)
                p = self.__partitions__[partition_name][0]
                if e is not None:
                    p.add_edge(e[0], e[1])
                if n is not None:
                    p.add_node(n)

        return

    def apply_component_lambdas(self, g, node, edge, context):
        for name in self.__component_groupers__:
            if name not in self.component_start_depths:
                self.component_start_depths[name] = context[Traverser.DEPTH]
            fn = self.__component_groupers__[name]
            n, e = fn(node, edge, context)
            if e is None and n is None:
                return
            if (name in self.__components__) == False:
                self.__components__[name] = []
                c = Graph('%s_%s' % (name, 0))
                self.__components__[name].append(c)
            c = self.__components__[name][(-1)]
            if e is not None:
                c.add_edge(e[0], e[1])
            if n is not None:
                c.add_node(n)

        return


import copy

class Traverser:

    def __init__(self):
        pass

    @staticmethod
    def group(g, group_lambdas, start=None):
        context = {'seen': [], 'depth': 0, 'graphs': {}, 'lambdas': group_lambdas, 'graph': g}
        unvisited = g.__nodes__ - set(context['seen'])
        while True:
            unvisited = g.__nodes__ - set(context['seen'])
            if len(unvisited) > 0:
                start = list(unvisited)[0]
                Traverser.dfs(g, start, context)
            else:
                break

        return context['graphs']

    @staticmethod
    def dfs(g, a, context):
        context['depth'] = context['depth'] + 1
        context['current'] = a
        context['seen'].append(a)
        if a is None:
            a = g.__adjacency_list__.keys()[0]
        for b in g.__adjacency_list__[a]:
            generate(context, (a, b), context['graphs'], context['lambdas'])
            if b not in context['seen']:
                Traverser.dfs(g, b, context)

        return


def generate(context, e, graphs, lambdas):
    fns = dict(lambdas)
    for k in fns.keys():
        if type(k) == type(lambda x: x):
            graph_key = k(e[0], e, context)
        else:
            graph_key = k
        if graph_key not in graphs:
            graphs[graph_key] = Graph()
            graphs[graph_key].__label__ = graph_key
        fn = fns[k]
        new_edge = fn(e[0], e, context)
        if new_edge is not None:
            a = new_edge[0]
            b = new_edge[1]
            print graph_key
            print 'k:', graphs[graph_key].__edges__
            graphs[graph_key].add_edge(a, b)

    return