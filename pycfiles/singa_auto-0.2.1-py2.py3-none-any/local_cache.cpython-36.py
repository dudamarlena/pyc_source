# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /root/singa_auto/utils/local_cache.py
# Compiled at: 2020-04-23 12:22:03
# Size of source mod 2**32: 3373 bytes


class _CacheNode:

    def __init__(self):
        self.key = None
        self.val = None
        self.prev = None
        self.next = None


class LocalCache:

    def __init__(self, size: int):
        assert size > 0
        self._size = size
        self._head = None
        self._tail = None
        self._key_to_node = {}

    def __len__(self):
        return len(self._key_to_node)

    def __contains__(self, item):
        return item in self._key_to_node

    @property
    def size(self) -> int:
        return self._size

    def put(self, key: str, value):
        if key in self._key_to_node:
            node = self._key_to_node[key]
            node.val = value
            self._move_to_front(node)
            return
        node = self._maybe_evict()
        node.key = key
        node.val = value
        self._key_to_node[key] = node
        self._insert_to_front(node)

    def get(self, key: str):
        if key in self._key_to_node:
            node = self._key_to_node[key]
            self._move_to_front(node)
            return node.val
        else:
            return

    def _maybe_evict(self):
        if len(self._key_to_node) < self._size:
            return _CacheNode()
        else:
            node = self._tail
            if node.prev is not None:
                node.prev.next = None
            self._tail = node.prev
            del self._key_to_node[node.key]
            return node

    def _insert_to_front(self, node):
        if self._head is None:
            self._head = node
            self._tail = node
            return
        node.next = self._head
        node.prev = None
        self._head.prev = node
        self._head = node

    def _move_to_front(self, node):
        if node is self._head:
            return
        else:
            if node is self._tail:
                self._tail = node.prev
            node.prev.next = node.next
            if node.next is not None:
                node.next.prev = node.prev
        node.next = self._head
        self._head.prev = node
        node.prev = None
        self._head = node

    def __str__(self):
        return 'Param cache has {} / {} items'.format(len(self), self.size)