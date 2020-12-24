# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/slab/core.py
# Compiled at: 2016-01-07 05:48:00
# Size of source mod 2**32: 2114 bytes
import functools, itertools
from .utils import get_node_name, get_node_qualname, listcontent, is_package, is_source, is_excluded
__all__ = ('build_tree', 'Node', 'Module', 'Directory')

def build_tree(root_path, excludes=None):
    return Directory(root_path, excludes=excludes)


@functools.total_ordering
class Node(object):

    def __init__(self, path, root=None):
        self.path = path
        self.root = root or self.path
        self.name = get_node_name(self.path)
        self.qualname = get_node_qualname(self.path, self.root)
        self.submodules = tuple()
        self.subdirs = tuple()
        self.subpackages = tuple()

    def docitems(self):
        yield self
        for node in itertools.chain(self.subpackages, self.submodules):
            yield from node.docitems()

    def __lt__(self, other):
        self.qualname.__lt__(other.qualname)

    def __eq__(self, other):
        return self.qualname.__eq__(other.qualname)


class Module(Node):
    pass


class Directory(Node):
    __default_excludes__ = frozenset([
     '__init__.py',
     '__pycache__'])

    def __init__(self, path, root=None, excludes=None):
        super().__init__(path, root)
        self.excludes = excludes or self.__default_excludes__
        files, subdirs = listcontent(self.path)
        self.is_package = is_package(self.path)
        self.submodules = sorted(Module(file, self.root) for file in sorted(files) if is_source(file) and not is_excluded(file, self.excludes))
        self.subdirs = sorted(Directory(subdir, self.root, excludes) for subdir in sorted(subdirs) if not is_excluded(subdir, self.excludes))
        self.subpackages = sorted(subdir for subdir in self.subdirs if subdir.is_package)
        self.is_empty = not self.submodules and not self.subdirs