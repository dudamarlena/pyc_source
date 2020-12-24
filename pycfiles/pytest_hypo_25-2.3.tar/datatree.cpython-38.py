# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\User\AppData\Local\Temp\pip-install-oj_abz_z\hypothesis\hypothesis\internal\conjecture\datatree.py
# Compiled at: 2020-01-12 08:06:33
# Size of source mod 2**32: 16855 bytes
import attr
from hypothesis.errors import Flaky, HypothesisException
from hypothesis.internal.compat import int_to_bytes
from hypothesis.internal.conjecture.data import ConjectureData, DataObserver, Status, StopTest, bits_to_bytes
from hypothesis.internal.conjecture.junkdrawer import IntList

class PreviouslyUnseenBehaviour(HypothesisException):
    pass


def inconsistent_generation():
    raise Flaky('Inconsistent data generation! Data generation behaved differently between different runs. Is your data generation depending on external state?')


EMPTY = frozenset()

@attr.s(slots=True)
class Killed:
    __doc__ = 'Represents a transition to part of the tree which has been marked as\n    "killed", meaning we want to treat it as not worth exploring, so it will\n    be treated as if it were completely explored for the purposes of\n    exhaustion.'
    next_node = attr.ib()


@attr.s(slots=True)
class Branch:
    __doc__ = 'Represents a transition where multiple choices can be made as to what\n    to drawn.'
    bit_length = attr.ib()
    children = attr.ib(repr=False)

    @property
    def max_children(self):
        return 1 << self.bit_length


@attr.s(slots=True, frozen=True)
class Conclusion:
    __doc__ = 'Represents a transition to a finished state.'
    status = attr.ib()
    interesting_origin = attr.ib()


CONCLUSIONS = {}

def conclusion(status, interesting_origin):
    result = Conclusion(status, interesting_origin)
    return CONCLUSIONS.setdefault(result, result)


@attr.s(slots=True)
class TreeNode:
    __doc__ = 'Node in a tree that corresponds to previous interactions with\n    a ``ConjectureData`` object according to some fixed test function.\n\n    This is functionally a variant patricia trie.\n    See https://en.wikipedia.org/wiki/Radix_tree for the general idea,\n    but what this means in particular here is that we have a very deep\n    but very lightly branching tree and rather than store this as a fully\n    recursive structure we flatten prefixes and long branches into\n    lists. This significantly compacts the storage requirements.\n\n    A single ``TreeNode`` corresponds to a previously seen sequence\n    of calls to ``ConjectureData`` which we have never seen branch,\n    followed by a ``transition`` which describes what happens next.\n    '
    bit_lengths = attr.ib(default=(attr.Factory(IntList)))
    values = attr.ib(default=(attr.Factory(IntList)))
    _TreeNode__forced = attr.ib(default=None, init=False)
    transition = attr.ib(default=None)
    is_exhausted = attr.ib(default=False, init=False)

    @property
    def forced(self):
        if not self._TreeNode__forced:
            return EMPTY
        return self._TreeNode__forced

    def mark_forced(self, i):
        """Note that the value at index ``i`` was forced."""
        assert 0 <= i < len(self.values)
        if self._TreeNode__forced is None:
            self._TreeNode__forced = set()
        self._TreeNode__forced.add(i)

    def split_at--- This code section failed: ---

 L. 159         0  LOAD_DEREF               'i'
                2  LOAD_FAST                'self'
                4  LOAD_ATTR                forced
                6  COMPARE_OP               in
                8  POP_JUMP_IF_FALSE    16  'to 16'

 L. 160        10  LOAD_GLOBAL              inconsistent_generation
               12  CALL_FUNCTION_0       0  ''
               14  POP_TOP          
             16_0  COME_FROM             8  '8'

 L. 162        16  LOAD_FAST                'self'
               18  LOAD_ATTR                is_exhausted
               20  POP_JUMP_IF_FALSE    26  'to 26'
               22  LOAD_GLOBAL              AssertionError
               24  RAISE_VARARGS_1       1  'exception instance'
             26_0  COME_FROM            20  '20'

 L. 164        26  LOAD_FAST                'self'
               28  LOAD_ATTR                values
               30  LOAD_DEREF               'i'
               32  BINARY_SUBSCR    
               34  STORE_FAST               'key'

 L. 166        36  LOAD_GLOBAL              TreeNode

 L. 167        38  LOAD_FAST                'self'
               40  LOAD_ATTR                bit_lengths
               42  LOAD_DEREF               'i'
               44  LOAD_CONST               1
               46  BINARY_ADD       
               48  LOAD_CONST               None
               50  BUILD_SLICE_2         2 
               52  BINARY_SUBSCR    

 L. 168        54  LOAD_FAST                'self'
               56  LOAD_ATTR                values
               58  LOAD_DEREF               'i'
               60  LOAD_CONST               1
               62  BINARY_ADD       
               64  LOAD_CONST               None
               66  BUILD_SLICE_2         2 
               68  BINARY_SUBSCR    

 L. 169        70  LOAD_FAST                'self'
               72  LOAD_ATTR                transition

 L. 166        74  LOAD_CONST               ('bit_lengths', 'values', 'transition')
               76  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               78  STORE_FAST               'child'

 L. 171        80  LOAD_GLOBAL              Branch
               82  LOAD_FAST                'self'
               84  LOAD_ATTR                bit_lengths
               86  LOAD_DEREF               'i'
               88  BINARY_SUBSCR    
               90  LOAD_FAST                'key'
               92  LOAD_FAST                'child'
               94  BUILD_MAP_1           1 
               96  LOAD_CONST               ('bit_length', 'children')
               98  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              100  LOAD_FAST                'self'
              102  STORE_ATTR               transition

 L. 172       104  LOAD_FAST                'self'
              106  LOAD_ATTR                _TreeNode__forced
              108  LOAD_CONST               None
              110  COMPARE_OP               is-not
              112  POP_JUMP_IF_FALSE   158  'to 158'

 L. 173       114  LOAD_CLOSURE             'i'
              116  BUILD_TUPLE_1         1 
              118  LOAD_SETCOMP             '<code_object <setcomp>>'
              120  LOAD_STR                 'TreeNode.split_at.<locals>.<setcomp>'
              122  MAKE_FUNCTION_8          'closure'
              124  LOAD_FAST                'self'
              126  LOAD_ATTR                _TreeNode__forced
              128  GET_ITER         
              130  CALL_FUNCTION_1       1  ''
              132  LOAD_FAST                'child'
              134  STORE_ATTR               _TreeNode__forced

 L. 174       136  LOAD_CLOSURE             'i'
              138  BUILD_TUPLE_1         1 
              140  LOAD_SETCOMP             '<code_object <setcomp>>'
              142  LOAD_STR                 'TreeNode.split_at.<locals>.<setcomp>'
              144  MAKE_FUNCTION_8          'closure'
              146  LOAD_FAST                'self'
              148  LOAD_ATTR                _TreeNode__forced
              150  GET_ITER         
              152  CALL_FUNCTION_1       1  ''
              154  LOAD_FAST                'self'
              156  STORE_ATTR               _TreeNode__forced
            158_0  COME_FROM           112  '112'

 L. 175       158  LOAD_FAST                'child'
              160  LOAD_METHOD              check_exhausted
              162  CALL_METHOD_0         0  ''
              164  POP_TOP          

 L. 176       166  LOAD_FAST                'self'
              168  LOAD_ATTR                values
              170  LOAD_DEREF               'i'
              172  LOAD_CONST               None
              174  BUILD_SLICE_2         2 
              176  DELETE_SUBSCR    

 L. 177       178  LOAD_FAST                'self'
              180  LOAD_ATTR                bit_lengths
              182  LOAD_DEREF               'i'
              184  LOAD_CONST               None
              186  BUILD_SLICE_2         2 
              188  DELETE_SUBSCR    

 L. 178       190  LOAD_GLOBAL              len
              192  LOAD_FAST                'self'
              194  LOAD_ATTR                values
              196  CALL_FUNCTION_1       1  ''
              198  LOAD_GLOBAL              len
              200  LOAD_FAST                'self'
              202  LOAD_ATTR                bit_lengths
              204  CALL_FUNCTION_1       1  ''
              206  DUP_TOP          
              208  ROT_THREE        
              210  COMPARE_OP               ==
              212  POP_JUMP_IF_FALSE   222  'to 222'
              214  LOAD_DEREF               'i'
              216  COMPARE_OP               ==
              218  POP_JUMP_IF_TRUE    228  'to 228'
              220  JUMP_FORWARD        224  'to 224'
            222_0  COME_FROM           212  '212'
              222  POP_TOP          
            224_0  COME_FROM           220  '220'
              224  LOAD_GLOBAL              AssertionError
              226  RAISE_VARARGS_1       1  'exception instance'
            228_0  COME_FROM           218  '218'

Parse error at or near `LOAD_SETCOMP' instruction at offset 118

    def check_exhausted(self):
        """Recalculates ``self.is_exhausted`` if necessary then returns
        it."""
        if not self.is_exhausted:
            if len(self.forced) == len(self.values):
                if self.transition is not None:
                    if isinstance(self.transition, (Conclusion, Killed)):
                        self.is_exhausted = True
                    else:
                        if len(self.transition.children) == self.transition.max_children:
                            self.is_exhausted = all((v.is_exhausted for v in self.transition.children.values()))
        return self.is_exhausted


class DataTree:
    __doc__ = 'Tracks the tree structure of a collection of ConjectureData\n    objects, for use in ConjectureRunner.'

    def __init__(self):
        self.root = TreeNode()

    @property
    def is_exhausted(self):
        """Returns True if every possible node is dead and thus the language
        described must have been fully explored."""
        return self.root.is_exhausted

    def generate_novel_prefix(self, random):
        """Generate a short random string that (after rewriting) is not
        a prefix of any buffer previously added to the tree.

        The resulting prefix is essentially arbitrary - it would be nice
        for it to be uniform at random, but previous attempts to do that
        have proven too expensive.
        """
        assert not self.is_exhausted
        novel_prefix = bytearray()

        def append_int(n_bits, value):
            novel_prefix.extend(int_to_bytes(value, bits_to_bytes(n_bits)))

        current_node = self.root
        while True:
            assert not current_node.is_exhausted
            for i, (n_bits, value) in enumerate(zip(current_node.bit_lengths, current_node.values)):
                if i in current_node.forced:
                    append_int(n_bits, value)
                else:
                    while True:
                        k = random.getrandbits(n_bits)
                        if k != value:
                            append_int(n_bits, k)
                            break

                    return bytes(novel_prefix)
            else:
                if isinstance(current_node.transition, (Conclusion, Killed)):
                    raise AssertionError
                elif current_node.transition is None:
                    return bytes(novel_prefix)
                else:
                    branch = current_node.transition
                    if not isinstance(branch, Branch):
                        raise AssertionError
                    else:
                        n_bits = branch.bit_length
                        check_counter = 0
                k = random.getrandbits(n_bits)
                try:
                    child = branch.children[k]
                except KeyError:
                    append_int(n_bits, k)
                    return bytes(novel_prefix)
                else:
                    if not child.is_exhausted:
                        append_int(n_bits, k)
                        current_node = child
                    else:
                        check_counter += 1
                        if not (check_counter != 1000 or len(branch.children) < 2 ** n_bits):
                            if not any((not v.is_exhausted for v in branch.children.values())):
                                raise AssertionError

    def rewrite--- This code section failed: ---

 L. 276         0  LOAD_GLOBAL              bytes
                2  LOAD_FAST                'buffer'
                4  CALL_FUNCTION_1       1  ''
                6  STORE_FAST               'buffer'

 L. 278         8  LOAD_GLOBAL              ConjectureData
               10  LOAD_METHOD              for_buffer
               12  LOAD_FAST                'buffer'
               14  CALL_METHOD_1         1  ''
               16  STORE_FAST               'data'

 L. 279        18  SETUP_FINALLY        44  'to 44'

 L. 280        20  LOAD_FAST                'self'
               22  LOAD_METHOD              simulate_test_function
               24  LOAD_FAST                'data'
               26  CALL_METHOD_1         1  ''
               28  POP_TOP          

 L. 281        30  LOAD_FAST                'data'
               32  LOAD_ATTR                buffer
               34  LOAD_FAST                'data'
               36  LOAD_ATTR                status
               38  BUILD_TUPLE_2         2 
               40  POP_BLOCK        
               42  RETURN_VALUE     
             44_0  COME_FROM_FINALLY    18  '18'

 L. 282        44  DUP_TOP          
               46  LOAD_GLOBAL              PreviouslyUnseenBehaviour
               48  COMPARE_OP               exception-match
               50  POP_JUMP_IF_FALSE    70  'to 70'
               52  POP_TOP          
               54  POP_TOP          
               56  POP_TOP          

 L. 283        58  LOAD_FAST                'buffer'
               60  LOAD_CONST               None
               62  BUILD_TUPLE_2         2 
               64  ROT_FOUR         
               66  POP_EXCEPT       
               68  RETURN_VALUE     
             70_0  COME_FROM            50  '50'
               70  END_FINALLY      

Parse error at or near `POP_TOP' instruction at offset 54

    def simulate_test_function(self, data):
        """Run a simulated version of the test function recorded by
        this tree. Note that this does not currently call ``stop_example``
        or ``start_example`` as these are not currently recorded in the
        tree. This will likely change in future."""
        node = self.root
        try:
            for i, (n_bits, previous) in enumerate(zip(node.bit_lengths, node.values)):
                v = data.draw_bits(n_bits,
                  forced=(node.values[i] if i in node.forced else None))
                if v != previous:
                    raise PreviouslyUnseenBehaviour()
                if isinstance(node.transition, Conclusion):
                    t = node.transition
                    data.conclude_test(t.status, t.interesting_origin)
                elif node.transition is None:
                    raise PreviouslyUnseenBehaviour()
                elif isinstance(node.transition, Branch):
                    v = data.draw_bits(node.transition.bit_length)
                    try:
                        node = node.transition.children[v]
                    except KeyError:
                        raise PreviouslyUnseenBehaviour()

                else:
                    assert isinstance(node.transition, Killed)
                    data.observer.kill_branch()
                    node = node.transition.next_node

        except StopTest:
            pass

    def new_observer(self):
        return TreeRecordingObserver(self)


class TreeRecordingObserver(DataObserver):

    def __init__(self, tree):
        self._TreeRecordingObserver__current_node = tree.root
        self._TreeRecordingObserver__index_in_current_node = 0
        self._TreeRecordingObserver__trail = [self._TreeRecordingObserver__current_node]
        self.killed = False

    def draw_bits(self, n_bits, forced, value):
        i = self._TreeRecordingObserver__index_in_current_node
        self._TreeRecordingObserver__index_in_current_node += 1
        node = self._TreeRecordingObserver__current_node
        assert len(node.bit_lengths) == len(node.values)
        if i < len(node.bit_lengths):
            if n_bits != node.bit_lengths[i]:
                inconsistent_generation()
            if forced:
                if i not in node.forced:
                    inconsistent_generation()
            if value != node.values[i]:
                node.split_at(i)
                assert i == len(node.values)
                new_node = TreeNode()
                branch = node.transition
                branch.children[value] = new_node
                self._TreeRecordingObserver__current_node = new_node
                self._TreeRecordingObserver__index_in_current_node = 0
        else:
            trans = node.transition
            if trans is None:
                node.bit_lengths.append(n_bits)
                node.values.append(value)
                if forced:
                    node.mark_forced(i)
            else:
                if isinstance(trans, Conclusion):
                    assert trans.status != Status.OVERRUN
                    inconsistent_generation()
                else:
                    assert isinstance(trans, Branch), trans
                    if n_bits != trans.bit_length:
                        inconsistent_generation()
                    try:
                        self._TreeRecordingObserver__current_node = trans.children[value]
                    except KeyError:
                        self._TreeRecordingObserver__current_node = trans.children.setdefault(value, TreeNode())
                    else:
                        self._TreeRecordingObserver__index_in_current_node = 0
                    if self._TreeRecordingObserver__trail[(-1)] is not self._TreeRecordingObserver__current_node:
                        self._TreeRecordingObserver__trail.append(self._TreeRecordingObserver__current_node)

    def kill_branch(self):
        """Mark this part of the tree as not worth re-exploring."""
        if self.killed:
            return
        self.killed = True
        if (self._TreeRecordingObserver__index_in_current_node < len(self._TreeRecordingObserver__current_node.values) or self._TreeRecordingObserver__current_node.transition) is not None:
            if not isinstance(self._TreeRecordingObserver__current_node.transition, Killed):
                inconsistent_generation()
        if self._TreeRecordingObserver__current_node.transition is None:
            self._TreeRecordingObserver__current_node.transition = Killed(TreeNode())
            self._TreeRecordingObserver__update_exhausted()
        self._TreeRecordingObserver__current_node = self._TreeRecordingObserver__current_node.transition.next_node
        self._TreeRecordingObserver__index_in_current_node = 0
        self._TreeRecordingObserver__trail.append(self._TreeRecordingObserver__current_node)

    def conclude_test(self, status, interesting_origin):
        """Says that ``status`` occurred at node ``node``. This updates the
        node if necessary and checks for consistency."""
        if status == Status.OVERRUN:
            return
            i = self._TreeRecordingObserver__index_in_current_node
            node = self._TreeRecordingObserver__current_node
            if not i < len(node.values):
                if isinstance(node.transition, Branch):
                    inconsistent_generation()
                new_transition = conclusion(status, interesting_origin)
                if node.transition is not None:
                    if node.transition != new_transition:
                        if not isinstance(node.transition, Conclusion) or node.transition.status != Status.INTERESTING or new_transition.status != Status.VALID:
                            raise Flaky('Inconsistent test results! Test case was %r on first run but %r on second' % (
                             node.transition, new_transition))
            else:
                node.transition = new_transition
            if not node is self._TreeRecordingObserver__trail[(-1)]:
                raise AssertionError
        else:
            node.check_exhausted()
            if not len(node.values) > 0:
                assert node.check_exhausted()
            self.killed or self._TreeRecordingObserver__update_exhausted()

    def __update_exhausted(self):
        for t in reversed(self._TreeRecordingObserver__trail):
            if not t.check_exhausted():
                break