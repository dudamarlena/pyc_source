# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mongotree.py
# Compiled at: 2016-04-25 10:23:15
"""
MongoTree
---------

This is something.
"""
__author__ = 'Joel Bender'
__email__ = 'joel@carrickbender.com'
__version__ = '0.1.3'
import bson

class NodeNotFound(Exception):
    """Node not found."""
    pass


class NodeNotBound(Exception):
    """Node not bound."""
    pass


class MismatchedNodeIdentifier(Exception):
    """Node identifier mismatch from an update."""
    pass


class MongoTreeNode(object):
    """
    A node in a tree.
    """

    def __init__(self, *contents, **attrs):
        """Initialize a new node.

        :param contents: optional children
        :param attrs: optional additional attributes
        """
        super(MongoTreeNode, self).__init__()
        object.__setattr__(self, '_id', None)
        object.__setattr__(self, '_attrs', {})
        object.__setattr__(self, '_contents', [])
        object.__setattr__(self, '_tree', None)
        object.__setattr__(self, '_parent', None)
        object.__setattr__(self, '_proxy', False)
        object.__setattr__(self, '_modified', False)
        if '_id' in attrs:
            self._id = attrs['_id']
            del attrs['_id']
            self._proxy = True
        for k, v in attrs.items():
            self.__setattr__(k, v)

        for v in contents:
            self.append(v)

        return

    def _load(self):
        """This function is called after the node has been loaded."""
        pass

    def _merge(self, node):
        """This function is called by the tree to incorporate database
        content into a proxy."""
        self._attrs = node._attrs
        self._contents = node._contents

    def _save(self):
        """This function is called by the tree before the node is
        about to be saved."""
        pass

    def _bind(self, tree):
        pass

    def _unbind(self):
        pass

    def __getattr__(self, k):
        if not isinstance(k, str):
            raise TypeError('attribute must be a string')
        if k.startswith('_'):
            raise AttributeError
        if self._tree and self._proxy:
            self._tree.load_node(self)
        return self._attrs[k]

    def __setattr__(self, k, v):
        if not isinstance(k, str):
            raise TypeError('attribute must be a string')
        if k.startswith('_'):
            return object.__setattr__(self, k, v)
        if self._tree and self._proxy:
            self._tree.load_node(self)
        self._attrs[k] = v
        self._modified = True

    def __delattr__(self, k):
        if not isinstance(k, str):
            raise TypeError('attribute must be a string')
        if k.startswith('_'):
            raise AttributeError
        if self._tree and self._proxy:
            self._tree.load_node(self)
        del self._attrs[k]
        self._modified = True

    def __hasattr__(self, k):
        if not isinstance(k, str):
            raise TypeError('attribute must be a string')
        if k.startswith('_'):
            raise AttributeError
        if self._tree and self._proxy:
            self._tree.load_node(self)
        return hasattr(self._attrs, k)

    def keys(self):
        if self._tree and self._proxy:
            self._tree.load_node(self)
        return self._attrs.keys()

    def items(self):
        if self._tree and self._proxy:
            self._tree.load_node(self)
        return self._attrs.items()

    def __getitem__(self, i):
        if self._tree and self._proxy:
            self._tree.load_node(self)
        if isinstance(i, int) or isinstance(i, slice):
            pass
        elif self._tree and isinstance(i, self._tree.marshal.node_id_class):
            i = self.index(i)
        else:
            raise TypeError('unknown kind of item to get')
        return self._contents[i]

    def __setitem__(self, i, node):
        if self._tree and not isinstance(node, self._tree.marshal.node_class):
            raise TypeError('node must be an instance of ' + self._tree.marshal.node_class.__name__)
        if node._tree and node._tree != self._tree:
            raise RuntimeError('node bound to the wrong tree')
        if self._tree and self._proxy:
            self._tree.load_node(self)
        self._contents[i] = node
        if not node._tree and self._tree:
            self._tree.bind(node)
        self._modified = True

    def __delitem__(self, i):
        if self._tree and self._proxy:
            self._tree.load_node(self)
        if isinstance(i, int):
            node = self._contents[i]
            if node._tree:
                node._tree.unbind(node)
        elif isinstance(i, slice):
            for node in self._contents[i]:
                if node._tree:
                    node._tree.unbind(node)

        elif self._tree and isinstance(i, self._tree.marshal.node_id_class):
            i = self.index(i)
            node = self._contents[i]
            if node._tree:
                node._tree.unbind(node)
        elif self._tree and isinstance(i, self._tree.marshal.node_class):
            i = self._contents.index(i)
            node = self._contents[i]
            if node._tree:
                node._tree.unbind(node)
        else:
            raise TypeError('unknown kind of thing to delete')
        del self._contents[i]
        self._modified = True

    def __contains__(self, kv):
        if self._tree and self._proxy:
            self._tree.load_node(self)
        if isinstance(kv, str):
            if kv in self._attrs:
                return True
            if not self._tree or not issubclass(self._tree.marshal.node_id_class, str):
                return False
        if self._tree and isinstance(kv, self._tree.marshal.node_class):
            try:
                self._contents.index(kv)
                return True
            except ValueError:
                return False

        if self._tree and isinstance(kv, self._tree.marshal.node_id_class):
            try:
                self.index(kv)
                return True
            except ValueError:
                return False

        raise TypeError('cannot check for something of type ' + str(type(kv)))

    def __len__(self):
        if self._tree and self._proxy:
            self._tree.load_node(self)
        return len(self._contents)

    def __iter__(self):
        if self._tree and self._proxy:
            self._tree.load_node(self)
        return iter(self._contents)

    def append(self, node):
        if self._tree and not isinstance(node, self._tree.marshal.node_class):
            raise TypeError('child must be a node')
        if self._tree and self._proxy:
            self._tree.load_node(self)
        self._contents.append(node)
        self._modified = True

    def extend(self, node_list):
        if self._tree and self._proxy:
            self._tree.load_node(self)
        for node in node_list:
            self.append(node)

    def index(self, node_id):
        for i, node in enumerate(self._contents):
            if node_id == node._id:
                return i

        raise ValueError(str(node_id) + ' not in contents')


class MongoTreeNodeMarshal(object):
    """
    Base class for marshaling nodes to/from the database.
    """

    def __init__(self, node_class=MongoTreeNode, node_id_class=bson.objectid.ObjectId, dict_class=dict):
        self.node_class = node_class
        self.node_id_class = node_id_class
        self.dict_class = dict_class

    def dict_to_node(self, some_dict, some_node=None):
        if some_node is None:
            some_node = self.node_class(_id=some_dict['_id'])
        if '_attrs' not in some_dict:
            raise RuntimeError('attrs expected')
        some_node._attrs = some_dict['_attrs']
        if '_contents' not in some_dict:
            raise RuntimeError('contents expected')
        contents = []
        for node_id in some_dict['_contents']:
            contents.append(self.node_class(_id=node_id))

        some_node._contents = contents
        return some_node

    def node_to_dict(self, some_node, some_dict=None):
        if some_dict is None:
            some_dict = self.dict_class()
        some_dict['_id'] = some_node._id
        some_dict['_attrs'] = some_node._attrs
        contents = []
        for node in some_node._contents:
            contents.append(node._id)

        some_dict['_contents'] = contents
        return some_dict


class MongoTree(object):

    def __init__(self, collection, marshal=None):
        self.collection = collection
        self.marshal = marshal or MongoTreeNodeMarshal()
        self.node_cache = {}

    def insert_node(self, node):
        if not isinstance(node, self.marshal.node_class):
            raise TypeError('must be an instance of ' + self.marshal.node_class.__name__)
        some_dict = self.marshal.node_to_dict(node)
        if node._id is None:
            if self.marshal.node_id_class is bson.objectid.ObjectId:
                if '_id' in some_dict:
                    del some_dict['_id']
            else:
                try:
                    some_dict['_id'] = self.marshal.node_id_class()
                except Exception as err:
                    raise RuntimeError('node identifier instance error: ' + str(err))

        elif not isinstance(node._id, self.marshal.node_id_class):
            raise TypeError('node identifier must be an instance of ' + self.marshal.node_id_class__name__)
        node._id = self.collection.insert(some_dict)
        node._modified = False
        node._proxy = False
        return

    def load_node(self, node):
        if not isinstance(node, self.marshal.node_class):
            raise TypeError('must be an instance of ' + self.marshal.node_class.__name__)
        if not node._id:
            raise RuntimeError('node has no identity')
        if node._tree and node._tree is not self:
            raise RuntimeError('node not bound to wrong tree ' + repr(node._tree))
        some_dict = self.collection.find_one({'_id': node._id})
        if not some_dict:
            raise NodeNotFound(str(node._id))
        some_node = self.marshal.dict_to_node(some_dict)
        node._merge(some_node)
        node._load()
        node._proxy = False
        if not node._tree:
            self._tree.bind(node)

    def save_node(self, node):
        if node._tree != self:
            raise NodeNotBound('node not bound')
        if not isinstance(node, self.marshal.node_class):
            raise TypeError('must be an instance of ' + self.marshal.node_class.__name__)
        node._save()
        some_dict = self.marshal.node_to_dict(node)
        stats = self.collection.find_and_modify(query={'_id': node._id}, update=some_dict, fields={'_id': 1})
        if not stats:
            raise NodeNotFound(str(node._id))
        if stats['_id'] != node._id:
            raise MismatchedNodeIdentifier(str(node._id))
        node._modified = False

    def bind(self, node):
        if node._tree:
            raise RuntimeError('already bound')
        if not isinstance(node, self.marshal.node_class):
            raise TypeError('must be an instance of ' + self.marshal.node_class.__name__)
        if node._id in self.node_cache:
            raise RuntimeError('node already in cache ' + repr(node))
        self.node_cache[node._id] = node
        node._tree = self
        node._bind(self)

    def unbind(self, node):
        if node._tree is not self:
            raise RuntimeError('node not bound, or not bound to this tree')
        if node._id not in self.node_cache:
            raise RuntimeError('node not in cache ' + repr(node))
        del self.node_cache[node._id]
        node._tree = None
        node._unbind()
        return

    def save_all_nodes(self):
        for node in self.node_cache.values():
            if node._modified:
                self.save_node(node)

    def flush_cache(self):
        node_list = list(self.node_cache.values())
        for node in node_list:
            if node._modified:
                self.save_node(node)
            self.unbind(node)

    def new_node(self, node_id=None):
        if node_id is not None:
            if node_id is not None and not isinstance(node_id, self.marshal.node_id_class):
                raise TypeError('node identifier must be a ' + str(self.marshal.node_id_class))
            if node_id in self.node_cache:
                raise RuntimeError('duplicate node identifier ' + repr(node_id))
            some_dict = self.collection.find_one({'_id': node_id}, {'_id': 1})
            if some_dict:
                raise RuntimeError('duplicate node identifier ' + repr(node_id))
        node = self.marshal.node_class(_id=node_id)
        self.insert_node(node)
        self.bind(node)
        return node

    def get_node(self, node_id):
        if node_id in self.node_cache:
            return self.node_cache[node_id]
        some_dict = self.collection.find_one({'_id': node_id})
        if not some_dict:
            raise NodeNotFound(str(node_id))
        some_node = self.marshal.dict_to_node(some_dict)
        self.bind(some_node)
        return some_node

    def del_node(self, node_id):
        for node in self.node_cache:
            if node._id == node_id:
                break
        else:
            node = None

        if node:
            self.unbind(node)
        stats = self.collection.remove(node_id)
        if not stats or stats['n'] != 1:
            raise NodeNotFound(str(node_id))
        return