# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-n_sfyb/Django/django/db/migrations/graph.py
# Compiled at: 2019-02-14 00:35:17
from __future__ import unicode_literals
import sys, warnings
from collections import deque
from functools import total_ordering
from django.db.migrations.state import ProjectState
from django.utils import six
from django.utils.datastructures import OrderedSet
from django.utils.encoding import python_2_unicode_compatible
from .exceptions import CircularDependencyError, NodeNotFoundError
RECURSION_DEPTH_WARNING = b"Maximum recursion depth exceeded while generating migration graph, falling back to iterative approach. If you're experiencing performance issues, consider squashing migrations as described at https://docs.djangoproject.com/en/dev/topics/migrations/#squashing-migrations."

@python_2_unicode_compatible
@total_ordering
class Node(object):
    """
    A single node in the migration graph. Contains direct links to adjacent
    nodes in either direction.
    """

    def __init__(self, key):
        self.key = key
        self.children = set()
        self.parents = set()

    def __eq__(self, other):
        return self.key == other

    def __lt__(self, other):
        return self.key < other

    def __hash__(self):
        return hash(self.key)

    def __getitem__(self, item):
        return self.key[item]

    def __str__(self):
        return str(self.key)

    def __repr__(self):
        return b'<Node: (%r, %r)>' % self.key

    def add_child(self, child):
        self.children.add(child)

    def add_parent(self, parent):
        self.parents.add(parent)

    def ancestors(self):
        if b'_ancestors' not in self.__dict__:
            ancestors = deque([self.key])
            for parent in sorted(self.parents):
                ancestors.extendleft(reversed(parent.ancestors()))

            self.__dict__[b'_ancestors'] = list(OrderedSet(ancestors))
        return self.__dict__[b'_ancestors']

    def descendants(self):
        if b'_descendants' not in self.__dict__:
            descendants = deque([self.key])
            for child in sorted(self.children):
                descendants.extendleft(reversed(child.descendants()))

            self.__dict__[b'_descendants'] = list(OrderedSet(descendants))
        return self.__dict__[b'_descendants']


class DummyNode(Node):

    def __init__(self, key, origin, error_message):
        super(DummyNode, self).__init__(key)
        self.origin = origin
        self.error_message = error_message

    def __repr__(self):
        return b'<DummyNode: (%r, %r)>' % self.key

    def promote(self):
        """
        Transition dummy to a normal node and clean off excess attribs.
        Creating a Node object from scratch would be too much of a
        hassle as many dependendies would need to be remapped.
        """
        del self.origin
        del self.error_message
        self.__class__ = Node

    def raise_error(self):
        raise NodeNotFoundError(self.error_message, self.key, origin=self.origin)


@python_2_unicode_compatible
class MigrationGraph(object):
    """
    Represents the digraph of all migrations in a project.

    Each migration is a node, and each dependency is an edge. There are
    no implicit dependencies between numbered migrations - the numbering is
    merely a convention to aid file listing. Every new numbered migration
    has a declared dependency to the previous number, meaning that VCS
    branch merges can be detected and resolved.

    Migrations files can be marked as replacing another set of migrations -
    this is to support the "squash" feature. The graph handler isn't responsible
    for these; instead, the code to load them in here should examine the
    migration files and if the replaced migrations are all either unapplied
    or not present, it should ignore the replaced ones, load in just the
    replacing migration, and repoint any dependencies that pointed to the
    replaced migrations to point to the replacing one.

    A node should be a tuple: (app_path, migration_name). The tree special-cases
    things within an app - namely, root nodes and leaf nodes ignore dependencies
    to other apps.
    """

    def __init__(self):
        self.node_map = {}
        self.nodes = {}
        self.cached = False

    def add_node(self, key, migration):
        dummy_node = self.node_map.get(key)
        if dummy_node:
            dummy_node.promote()
        else:
            node = Node(key)
            self.node_map[key] = node
        self.nodes[key] = migration
        self.clear_cache()

    def add_dummy_node(self, key, origin, error_message):
        node = DummyNode(key, origin, error_message)
        self.node_map[key] = node
        self.nodes[key] = None
        return

    def add_dependency(self, migration, child, parent, skip_validation=False):
        """
        This may create dummy nodes if they don't yet exist.
        If `skip_validation` is set, validate_consistency should be called afterwards.
        """
        if child not in self.nodes:
            error_message = b'Migration %s dependencies reference nonexistent child node %r' % (
             migration, child)
            self.add_dummy_node(child, migration, error_message)
        if parent not in self.nodes:
            error_message = b'Migration %s dependencies reference nonexistent parent node %r' % (
             migration, parent)
            self.add_dummy_node(parent, migration, error_message)
        self.node_map[child].add_parent(self.node_map[parent])
        self.node_map[parent].add_child(self.node_map[child])
        if not skip_validation:
            self.validate_consistency()
        self.clear_cache()

    def remove_replaced_nodes(self, replacement, replaced):
        """
        Removes each of the `replaced` nodes (when they exist). Any
        dependencies that were referencing them are changed to reference the
        `replacement` node instead.
        """
        replaced = set(replaced)
        try:
            replacement_node = self.node_map[replacement]
        except KeyError as exc:
            exc_value = NodeNotFoundError(b'Unable to find replacement node %r. It was either never added to the migration graph, or has been removed.' % (
             replacement,), replacement)
            exc_value.__cause__ = exc
            if not hasattr(exc, b'__traceback__'):
                exc.__traceback__ = sys.exc_info()[2]
            six.reraise(NodeNotFoundError, exc_value, sys.exc_info()[2])

        for replaced_key in replaced:
            self.nodes.pop(replaced_key, None)
            replaced_node = self.node_map.pop(replaced_key, None)
            if replaced_node:
                for child in replaced_node.children:
                    child.parents.remove(replaced_node)
                    if child.key not in replaced:
                        replacement_node.add_child(child)
                        child.add_parent(replacement_node)

                for parent in replaced_node.parents:
                    parent.children.remove(replaced_node)
                    if parent.key not in replaced:
                        replacement_node.add_parent(parent)
                        parent.add_child(replacement_node)

        self.clear_cache()
        return

    def remove_replacement_node(self, replacement, replaced):
        """
        The inverse operation to `remove_replaced_nodes`. Almost. Removes the
        replacement node `replacement` and remaps its child nodes to
        `replaced` - the list of nodes it would have replaced. Its parent
        nodes are not remapped as they are expected to be correct already.
        """
        self.nodes.pop(replacement, None)
        try:
            replacement_node = self.node_map.pop(replacement)
        except KeyError as exc:
            exc_value = NodeNotFoundError(b'Unable to remove replacement node %r. It was either never added to the migration graph, or has been removed already.' % (
             replacement,), replacement)
            exc_value.__cause__ = exc
            if not hasattr(exc, b'__traceback__'):
                exc.__traceback__ = sys.exc_info()[2]
            six.reraise(NodeNotFoundError, exc_value, sys.exc_info()[2])

        replaced_nodes = set()
        replaced_nodes_parents = set()
        for key in replaced:
            replaced_node = self.node_map.get(key)
            if replaced_node:
                replaced_nodes.add(replaced_node)
                replaced_nodes_parents |= replaced_node.parents

        replaced_nodes -= replaced_nodes_parents
        for child in replacement_node.children:
            child.parents.remove(replacement_node)
            for replaced_node in replaced_nodes:
                replaced_node.add_child(child)
                child.add_parent(replaced_node)

        for parent in replacement_node.parents:
            parent.children.remove(replacement_node)

        self.clear_cache()
        return

    def validate_consistency(self):
        """
        Ensure there are no dummy nodes remaining in the graph.
        """
        [ n.raise_error() for n in self.node_map.values() if isinstance(n, DummyNode) ]

    def clear_cache(self):
        if self.cached:
            for node in self.nodes:
                self.node_map[node].__dict__.pop(b'_ancestors', None)
                self.node_map[node].__dict__.pop(b'_descendants', None)

            self.cached = False
        return

    def forwards_plan(self, target):
        """
        Given a node, returns a list of which previous nodes (dependencies)
        must be applied, ending with the node itself.
        This is the list you would follow if applying the migrations to
        a database.
        """
        if target not in self.nodes:
            raise NodeNotFoundError(b'Node %r not a valid node' % (target,), target)
        self.ensure_not_cyclic(target, lambda x: (parent.key for parent in self.node_map[x].parents))
        self.cached = True
        node = self.node_map[target]
        try:
            return node.ancestors()
        except RuntimeError:
            warnings.warn(RECURSION_DEPTH_WARNING, RuntimeWarning)
            return self.iterative_dfs(node)

    def backwards_plan(self, target):
        """
        Given a node, returns a list of which dependent nodes (dependencies)
        must be unapplied, ending with the node itself.
        This is the list you would follow if removing the migrations from
        a database.
        """
        if target not in self.nodes:
            raise NodeNotFoundError(b'Node %r not a valid node' % (target,), target)
        self.ensure_not_cyclic(target, lambda x: (child.key for child in self.node_map[x].children))
        self.cached = True
        node = self.node_map[target]
        try:
            return node.descendants()
        except RuntimeError:
            warnings.warn(RECURSION_DEPTH_WARNING, RuntimeWarning)
            return self.iterative_dfs(node, forwards=False)

    def iterative_dfs(self, start, forwards=True):
        """
        Iterative depth first search, for finding dependencies.
        """
        visited = deque()
        visited.append(start)
        if forwards:
            stack = deque(sorted(start.parents))
        else:
            stack = deque(sorted(start.children))
        while stack:
            node = stack.popleft()
            visited.appendleft(node)
            if forwards:
                children = sorted(node.parents, reverse=True)
            else:
                children = sorted(node.children, reverse=True)
            stack.extendleft(children)

        return list(OrderedSet(visited))

    def root_nodes(self, app=None):
        """
        Returns all root nodes - that is, nodes with no dependencies inside
        their app. These are the starting point for an app.
        """
        roots = set()
        for node in self.nodes:
            if not any(key[0] == node[0] for key in self.node_map[node].parents) and (not app or app == node[0]):
                roots.add(node)

        return sorted(roots)

    def leaf_nodes(self, app=None):
        """
        Returns all leaf nodes - that is, nodes with no dependents in their app.
        These are the "most current" version of an app's schema.
        Having more than one per app is technically an error, but one that
        gets handled further up, in the interactive command - it's usually the
        result of a VCS merge and needs some user input.
        """
        leaves = set()
        for node in self.nodes:
            if not any(key[0] == node[0] for key in self.node_map[node].children) and (not app or app == node[0]):
                leaves.add(node)

        return sorted(leaves)

    def ensure_not_cyclic(self, start, get_children):
        todo = set(self.nodes)
        while todo:
            node = todo.pop()
            stack = [node]
            while stack:
                top = stack[(-1)]
                for node in get_children(top):
                    if node in stack:
                        cycle = stack[stack.index(node):]
                        raise CircularDependencyError((b', ').join(b'%s.%s' % n for n in cycle))
                    if node in todo:
                        stack.append(node)
                        todo.remove(node)
                        break
                else:
                    node = stack.pop()

    def __str__(self):
        return b'Graph: %s nodes, %s edges' % self._nodes_and_edges()

    def __repr__(self):
        nodes, edges = self._nodes_and_edges()
        return b'<%s: nodes=%s, edges=%s>' % (self.__class__.__name__, nodes, edges)

    def _nodes_and_edges(self):
        return (
         len(self.nodes), sum(len(node.parents) for node in self.node_map.values()))

    def make_state(self, nodes=None, at_end=True, real_apps=None):
        """
        Given a migration node or nodes, returns a complete ProjectState for it.
        If at_end is False, returns the state before the migration has run.
        If nodes is not provided, returns the overall most current project state.
        """
        if nodes is None:
            nodes = list(self.leaf_nodes())
        if len(nodes) == 0:
            return ProjectState()
        else:
            if not isinstance(nodes[0], tuple):
                nodes = [
                 nodes]
            plan = []
            for node in nodes:
                for migration in self.forwards_plan(node):
                    if migration not in plan:
                        if not at_end and migration in nodes:
                            continue
                        plan.append(migration)

            project_state = ProjectState(real_apps=real_apps)
            for node in plan:
                project_state = self.nodes[node].mutate_state(project_state, preserve=False)

            return project_state

    def __contains__(self, node):
        return node in self.nodes