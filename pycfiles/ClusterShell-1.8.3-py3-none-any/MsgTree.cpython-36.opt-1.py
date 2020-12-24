# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /ClusterShell/MsgTree.py
# Compiled at: 2019-12-07 15:34:33
# Size of source mod 2**32: 12663 bytes
"""
MsgTree

ClusterShell message tree module. The purpose of MsgTree is to provide a
shared message tree for storing message lines received from ClusterShell
Workers (for example, from remote cluster commands). It should be
efficient, in term of algorithm and memory consumption, especially when
remote messages are the same.
"""
try:
    from itertools import filterfalse
except ImportError:
    from itertools import ifilterfalse as filterfalse

import sys
MODE_DEFER = 0
MODE_SHIFT = 1
MODE_TRACE = 2

class MsgTreeElem(object):
    __doc__ = '\n    Class representing an element of the MsgTree and its associated\n    message. Object of this class are returned by the various MsgTree\n    methods like messages() or walk(). The object can then be used as\n    an iterator over the message lines or casted into a bytes buffer.\n    '

    def __init__(self, msgline=None, parent=None, trace=False):
        """
        Initialize message tree element.
        """
        self.parent = parent
        self.children = {}
        if trace:
            self._shift = self._shift_trace
        else:
            self._shift = self._shift_notrace
        self.msgline = msgline
        self.keys = None

    def __len__(self):
        """Length of whole message buffer."""
        return len(bytes(self))

    def __eq__(self, other):
        """Comparison method compares whole message buffers."""
        return bytes(self) == bytes(other)

    def _add_key(self, key):
        """Add a key to this tree element."""
        if self.keys is None:
            self.keys = set([key])
        else:
            self.keys.add(key)

    def _shift_notrace(self, key, target_elem):
        """Shift one of our key to specified target element."""
        if self.keys:
            if len(self.keys) == 1:
                shifting = self.keys
                self.keys = None
            else:
                shifting = set([key])
                if self.keys:
                    self.keys.difference_update(shifting)
            target_elem.keys = target_elem.keys or shifting
        else:
            target_elem.keys.update(shifting)
        return target_elem

    def _shift_trace(self, key, target_elem):
        """Shift one of our key to specified target element (trace
        mode: keep backtrace of keys)."""
        if not target_elem.keys:
            target_elem.keys = set([key])
        else:
            target_elem.keys.add(key)
        return target_elem

    def __getitem__(self, i):
        return list(self.lines())[i]

    def __iter__(self):
        """Iterate over message lines up to this element."""
        bottomtop = []
        if self.msgline is not None:
            bottomtop.append(self.msgline)
            parent = self.parent
            while parent.msgline is not None:
                bottomtop.append(parent.msgline)
                parent = parent.parent

        return reversed(bottomtop)

    def lines(self):
        """Get an iterator over all message lines up to this element."""
        return iter(self)

    splitlines = lines

    def message(self):
        """
        Get the whole message buffer (from this tree element) as bytes.
        """
        return (b'\n').join(self.lines())

    __bytes__ = message

    def __str__(self):
        """
        Get the whole message buffer (from this tree element) as a string.

        DEPRECATED: use message() or cast to bytes instead.
        """
        if sys.version_info >= (3, 0):
            raise TypeError('cannot get string from %s, use bytes instead' % self.__class__.__name__)
        else:
            return self.message()

    def append(self, msgline, key=None):
        """
        A new message is coming, append it to the tree element with
        optional associated source key. Called by MsgTree.add().
        Return corresponding MsgTreeElem (possibly newly created).
        """
        elem = self.children.get(msgline)
        if elem is None:
            elem = self.__class__(msgline, self, self._shift == self._shift_trace)
            self.children[msgline] = elem
        if key is None:
            return elem
        else:
            return self._shift(key, elem)


class MsgTree(object):
    __doc__ = '\n    MsgTree maps key objects to multi-lines messages.\n\n    MsgTree is a mutable object. Keys are almost arbitrary values (must\n    be hashable). Message lines are organized as a tree internally.\n    MsgTree provides low memory consumption especially on a cluster when\n    all nodes return similar messages. Also, the gathering of messages is\n    done automatically.\n    '

    def __init__(self, mode=MODE_DEFER):
        """MsgTree initializer

        The `mode' parameter should be set to one of the following constant:

        MODE_DEFER: all messages are processed immediately, saving memory from
        duplicate message lines, but keys are associated to tree elements
        usually later when tree is first "walked", saving useless state
        updates and CPU time. Once the tree is "walked" for the first time, its
        mode changes to MODE_SHIFT to keep track of further tree updates.
        This is the default mode.

        MODE_SHIFT: all keys and messages are processed immediately, it is more
        CPU time consuming as MsgTree full state is updated at each add() call.

        MODE_TRACE: all keys and messages and processed immediately, and keys
        are kept for each message element of the tree. The special method
        walk_trace() is then available to walk all elements of the tree.
        """
        self.mode = mode
        self._root = MsgTreeElem(trace=(mode == MODE_TRACE))
        self._keys = {}

    def clear(self):
        """Remove all items from the MsgTree."""
        self._root = MsgTreeElem(trace=(self.mode == MODE_TRACE))
        self._keys.clear()

    def __len__(self):
        """Return the number of keys contained in the MsgTree."""
        return len(self._keys)

    def __getitem__(self, key):
        """Return the message of MsgTree with specified key. Raises a
        KeyError if key is not in the MsgTree."""
        return self._keys[key]

    def get(self, key, default=None):
        """
        Return the message for key if key is in the MsgTree, else default.
        If default is not given, it defaults to None, so that this method
        never raises a KeyError.
        """
        return self._keys.get(key, default)

    def add(self, key, msgline):
        """
        Add a message line (in bytes) associated with the given key to the
        MsgTree.
        """
        e_msg = self._keys.get(key, self._root)
        if self.mode >= MODE_SHIFT:
            key_shift = key
        else:
            key_shift = None
        self._keys[key] = e_msg.append(msgline, key_shift)

    def _update_keys(self):
        """Update keys associated to tree elements (MODE_DEFER)."""
        for key, e_msg in self._keys.items():
            assert key is not None and e_msg is not None
            e_msg._add_key(key)

        self.mode = MODE_SHIFT

    def keys(self):
        """Return an iterator over MsgTree's keys."""
        return iter(self._keys.keys())

    __iter__ = keys

    def messages(self, match=None):
        """Return an iterator over MsgTree's messages."""
        return (item[0] for item in self.walk(match))

    def items(self, match=None, mapper=None):
        """
        Return (key, message) for each key of the MsgTree.
        """
        if mapper is None:
            mapper = lambda k: k
        for key, elem in self._keys.items():
            if match is None or match(key):
                yield (
                 mapper(key), elem)

    def _depth(self):
        """
        Return the depth of the MsgTree, ie. the max number of lines
        per message. Added for debugging.
        """
        depth = 0
        estack = [
         (
          self._root, depth)]
        while estack:
            elem, edepth = estack.pop()
            if len(elem.children) > 0:
                estack += [(v, edepth + 1) for v in elem.children.values()]
            depth = max(depth, edepth)

        return depth

    def walk(self, match=None, mapper=None):
        """
        Walk the tree. Optionally filter keys on match parameter,
        and optionally map resulting keys with mapper function.
        Return an iterator over (message, keys) tuples for each
        different message in the tree.
        """
        if self.mode == MODE_DEFER:
            self._update_keys()
        estack = [self._root]
        while estack:
            elem = estack.pop()
            children = elem.children
            if len(children) > 0:
                estack += children.values()
            if elem.keys:
                mkeys = list(filter(match, elem.keys))
                if len(mkeys):
                    if mapper is not None:
                        keys = [mapper(key) for key in mkeys]
                    else:
                        keys = mkeys
                    yield (
                     elem, keys)

    def walk_trace(self, match=None, mapper=None):
        """
        Walk the tree in trace mode. Optionally filter keys on match
        parameter, and optionally map resulting keys with mapper
        function.
        Return an iterator over 4-length tuples (msgline, keys, depth,
        num_children).
        """
        assert self.mode == MODE_TRACE, 'walk_trace() is only callable in trace mode'
        estack = [
         (
          self._root, 0)]
        while estack:
            elem, edepth = estack.pop()
            children = elem.children
            nchildren = len(children)
            if nchildren > 0:
                estack += [(v, edepth + 1) for v in children.values()]
            if elem.keys:
                mkeys = list(filter(match, elem.keys))
                if len(mkeys):
                    if mapper is not None:
                        keys = [mapper(key) for key in mkeys]
                    else:
                        keys = mkeys
                    yield (
                     elem.msgline, keys, edepth, nchildren)

    def remove(self, match=None):
        """
        Modify the tree by removing any matching key references from the
        messages tree.

        Example of use:
            >>> msgtree.remove(lambda k: k > 3)
        """
        if self.mode != MODE_DEFER:
            estack = [
             self._root]
            while estack:
                elem = estack.pop()
                if len(elem.children) > 0:
                    estack += elem.children.values()
                if elem.keys:
                    elem.keys = set(filterfalse(match, elem.keys))

        for key in list(filter(match, self._keys.keys())):
            del self._keys[key]