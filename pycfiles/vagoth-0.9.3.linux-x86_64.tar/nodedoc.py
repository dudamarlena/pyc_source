# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/vagoth/registry/nodedoc.py
# Compiled at: 2013-12-29 05:01:04


class NodeDoc(object):
    """
    An encapsulation of the node dictionary, implementing INodeDoc
    """

    def __init__(self, registry, node_dict):
        self.registry = registry
        self.node_dict = node_dict
        assert 'type' in node_dict
        assert 'node_id' in node_dict
        assert 'name' in node_dict
        assert 'parent' in node_dict
        assert 'definition' in node_dict
        assert 'unique_keys' in node_dict
        if 'tenant' not in node_dict:
            node_dict['tenant'] = None
        if 'metadata' not in node_dict:
            node_dict['metadata'] = {}
        if 'tags' not in node_dict:
            node_dict['tags'] = {}
        elif type(node_dict['tags']) == list:
            node_dict['tags'] = dict([ (x, True) for x in node_dict['tags'] ])
        return

    @property
    def type(self):
        return self.node_dict['type']

    @property
    def id(self):
        return self.node_dict['node_id']

    @property
    def name(self):
        return self.node_dict['name']

    @property
    def definition(self):
        return self.node_dict['definition']

    @property
    def metadata(self):
        return self.node_dict['metadata']

    @property
    def parent(self):
        return self.node_dict['parent']

    @property
    def tags(self):
        return self.node_dict['tags']

    @property
    def unique_keys(self):
        return self.node_dict['unique_keys']

    @property
    def tenant(self):
        return self.node_dict['tenant']

    def get_blob(self, key):
        return self.registry.get_blob(self.id, key)

    def __getitem__(self, key):
        raise NotImplementedError

    def get(self, *args, **kwargs):
        raise NotImplementedError

    def __str__(self):
        return 'NodeDoc for %s' % (self.id,)

    def __repr__(self):
        return '<NodeDoc for %s at 0x%x>' % (self.id, id(self))