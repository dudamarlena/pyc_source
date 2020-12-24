# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\User\AppData\Local\Temp\pip-install-oj_abz_z\hypothesis\hypothesis\internal\conjecture\data.py
# Compiled at: 2020-01-12 08:06:33
# Size of source mod 2**32: 36044 bytes
from collections import defaultdict
from enum import IntEnum
import attr
from hypothesis.errors import Frozen, InvalidArgument, StopTest
from hypothesis.internal.compat import benchmark_time, bit_length, int_from_bytes, int_to_bytes
from hypothesis.internal.conjecture.junkdrawer import IntList, uniform
from hypothesis.internal.conjecture.utils import calc_label_from_name
from hypothesis.internal.escalation import mark_for_escalation
TOP_LABEL = calc_label_from_name('top')
DRAW_BYTES_LABEL = calc_label_from_name('draw_bytes() in ConjectureData')

class ExtraInformation:
    __doc__ = 'A class for holding shared state on a ``ConjectureData`` that should\n    be added to the final ``ConjectureResult``.'

    def __repr__(self):
        return 'ExtraInformation(%s)' % (
         ', '.join(['%s=%r' % (k, v) for k, v in self.__dict__.items()]),)

    def has_information(self):
        return bool(self.__dict__)


class Status(IntEnum):
    OVERRUN = 0
    INVALID = 1
    VALID = 2
    INTERESTING = 3

    def __repr__(self):
        return 'Status.%s' % (self.name,)


@attr.s(frozen=True, slots=True)
class StructuralCoverageTag:
    label = attr.ib()


STRUCTURAL_COVERAGE_CACHE = {}

def structural_coverage--- This code section failed: ---

 L.  68         0  SETUP_FINALLY        12  'to 12'

 L.  69         2  LOAD_GLOBAL              STRUCTURAL_COVERAGE_CACHE
                4  LOAD_FAST                'label'
                6  BINARY_SUBSCR    
                8  POP_BLOCK        
               10  RETURN_VALUE     
             12_0  COME_FROM_FINALLY     0  '0'

 L.  70        12  DUP_TOP          
               14  LOAD_GLOBAL              KeyError
               16  COMPARE_OP               exception-match
               18  POP_JUMP_IF_FALSE    46  'to 46'
               20  POP_TOP          
               22  POP_TOP          
               24  POP_TOP          

 L.  71        26  LOAD_GLOBAL              STRUCTURAL_COVERAGE_CACHE
               28  LOAD_METHOD              setdefault
               30  LOAD_FAST                'label'
               32  LOAD_GLOBAL              StructuralCoverageTag
               34  LOAD_FAST                'label'
               36  CALL_FUNCTION_1       1  ''
               38  CALL_METHOD_2         2  ''
               40  ROT_FOUR         
               42  POP_EXCEPT       
               44  RETURN_VALUE     
             46_0  COME_FROM            18  '18'
               46  END_FINALLY      

Parse error at or near `POP_TOP' instruction at offset 22


class Example:
    __doc__ = 'Examples track the hierarchical structure of draws from the byte stream,\n    within a single test run.\n\n    Examples are created to mark regions of the byte stream that might be\n    useful to the shrinker, such as:\n    - The bytes used by a single draw from a strategy.\n    - Useful groupings within a strategy, such as individual list elements.\n    - Strategy-like helper functions that aren\'t first-class strategies.\n    - Each lowest-level draw of bits or bytes from the byte stream.\n    - A single top-level example that spans the entire input.\n\n    Example-tracking allows the shrinker to try "high-level" transformations,\n    such as rearranging or deleting the elements of a list, without having\n    to understand their exact representation in the byte stream.\n\n    Rather than store each ``Example`` as a rich object, it is actually\n    just an index into the ``Examples`` class defined below. This has two\n    purposes: Firstly, for most properties of examples we will never need\n    to allocate storage at all, because most properties are not used on\n    most examples. Secondly, by storing the properties as compact lists\n    of integers, we save a considerable amount of space compared to\n    Python\'s normal object size.\n\n    This does have the downside that it increases the amount of allocation\n    we do, and slows things down as a result, in some usage patterns because\n    we repeatedly allocate the same Example or int objects, but it will\n    often dramatically reduce our memory usage, so is worth it.\n    '
    __slots__ = ('owner', 'index')

    def __init__(self, owner, index):
        self.owner = owner
        self.index = index

    def __eq__(self, other):
        if self is other:
            return True
        else:
            return isinstance(other, Example) or NotImplemented
        return self.owner is other.owner and self.index == other.index

    def __ne__(self, other):
        if self is other:
            return False
        else:
            return isinstance(other, Example) or NotImplemented
        return self.owner is not other.owner or self.index != other.index

    def __repr__(self):
        return 'examples[%d]' % (self.index,)

    @property
    def label(self):
        """A label is an opaque value that associates each example with its
        approximate origin, such as a particular strategy class or a particular
        kind of draw."""
        return self.owner.labels[self.owner.label_indices[self.index]]

    @property
    def parent(self):
        """The index of the example that this one is nested directly within."""
        if self.index == 0:
            return
        return self.owner.parentage[self.index]

    @property
    def start(self):
        """The position of the start of this example in the byte stream."""
        return self.owner.starts[self.index]

    @property
    def end(self):
        """The position directly after the last byte in this byte stream.
        i.e. the example corresponds to the half open region [start, end).
        """
        return self.owner.ends[self.index]

    @property
    def depth(self):
        """Depth of this example in the example tree. The top-level example has a
        depth of 0."""
        return self.owner.depths[self.index]

    @property
    def trivial(self):
        """An example is "trivial" if it only contains forced bytes and zero bytes.
        All examples start out as trivial, and then get marked non-trivial when
        we see a byte that is neither forced nor zero."""
        return self.index in self.owner.trivial

    @property
    def discarded(self):
        """True if this is example's ``stop_example`` call had ``discard`` set to
        ``True``. This means we believe that the shrinker should be able to delete
        this example completely, without affecting the value produced by its enclosing
        strategy. Typically set when a rejection sampler decides to reject a
        generated value and try again."""
        return self.index in self.owner.discarded

    @property
    def length(self):
        """The number of bytes in this example."""
        return self.end - self.start

    @property
    def children(self):
        """The list of all examples with this as a parent, in increasing index
        order."""
        return [self.owner[i] for i in self.owner.children[self.index]]


class ExampleProperty:
    __doc__ = 'There are many properties of examples that we calculate by\n    essentially rerunning the test case multiple times based on the\n    calls which we record in ExampleRecord.\n\n    This class defines a visitor, subclasses of which can be used\n    to calculate these properties.\n    '

    def __init__(self, examples):
        self.example_stack = []
        self.examples = examples
        self.bytes_read = 0
        self.example_count = 0
        self.block_count = 0

    def run(self):
        """Rerun the test case with this visitor and return the
        results of ``self.finish()``."""
        self.begin()
        blocks = self.examples.blocks
        for record in self.examples.trail:
            if record == DRAW_BITS_RECORD:
                self._ExampleProperty__push(0)
                self.bytes_read = blocks.endpoints[self.block_count]
                self.block(self.block_count)
                self.block_count += 1
                self._ExampleProperty__pop(False)
            elif record >= START_EXAMPLE_RECORD:
                self._ExampleProperty__push(record - START_EXAMPLE_RECORD)
            else:
                assert record in (
                 STOP_EXAMPLE_DISCARD_RECORD,
                 STOP_EXAMPLE_NO_DISCARD_RECORD)
                self._ExampleProperty__pop(record == STOP_EXAMPLE_DISCARD_RECORD)
        else:
            return self.finish()

    def __push(self, label_index):
        i = self.example_count
        assert i < len(self.examples)
        self.start_exampleilabel_index
        self.example_count += 1
        self.example_stack.append(i)

    def __pop(self, discarded):
        i = self.example_stack.pop()
        self.stop_exampleidiscarded

    def begin(self):
        """Called at the beginning of the run to initialise any
        relevant state."""
        self.result = IntList.of_length(len(self.examples))

    def start_example(self, i, label_index):
        """Called at the start of each example, with ``i`` the
        index of the example and ``label_index`` the index of
        its label in ``self.examples.labels``."""
        pass

    def block(self, i):
        """Called with each ``draw_bits`` call, with ``i`` the index of the
        corresponding block in ``self.examples.blocks``"""
        pass

    def stop_example(self, i, discarded):
        """Called at the end of each example, with ``i`` the
        index of the example and ``discarded`` being ``True`` if ``stop_example``
        was called with ``discard=True``."""
        pass

    def finish(self):
        return self.result


def calculated_example_property(cls):
    """Given an ``ExampleProperty`` as above we use this decorator
    to transform it into a lazy property on the ``Examples`` class,
    which has as its value the result of calling ``cls.run()``,
    computed the first time the property is accessed.

    This has the slightly weird result that we are defining nested
    classes which get turned into properties."""
    name = cls.__name__
    cache_name = '__' + name

    def lazy_calculate(self):
        result = getattr(self, cache_name, None)
        if result is None:
            result = cls(self).run()
            setattr(self, cache_name, result)
        return result

    lazy_calculate.__name__ = cls.__name__
    lazy_calculate.__qualname__ = getattr(cls, '__qualname__', cls.__name__)
    return property(lazy_calculate)


DRAW_BITS_RECORD = 0
STOP_EXAMPLE_DISCARD_RECORD = 1
STOP_EXAMPLE_NO_DISCARD_RECORD = 2
START_EXAMPLE_RECORD = 3

class ExampleRecord:
    __doc__ = 'Records the series of ``start_example``, ``stop_example``, and\n    ``draw_bits`` calls so that these may be stored in ``Examples`` and\n    replayed when we need to know about the structure of individual\n    ``Example`` objects.\n\n    Note that there is significant similarity between this class and\n    ``DataObserver``, and the plan is to eventually unify them, but\n    they currently have slightly different functions and implementations.\n    '

    def __init__(self):
        self.labels = [
         DRAW_BYTES_LABEL]
        self._ExampleRecord__index_of_labels = {DRAW_BYTES_LABEL: 0}
        self.trail = IntList()

    def freeze(self):
        self._ExampleRecord__index_of_labels = None

    def start_example(self, label):
        try:
            i = self._ExampleRecord__index_of_labels[label]
        except KeyError:
            i = self._ExampleRecord__index_of_labels.setdefaultlabellen(self.labels)
            self.labels.append(label)
        else:
            self.trail.append(START_EXAMPLE_RECORD + i)

    def stop_example(self, discard):
        if discard:
            self.trail.append(STOP_EXAMPLE_DISCARD_RECORD)
        else:
            self.trail.append(STOP_EXAMPLE_NO_DISCARD_RECORD)

    def draw_bits(self, n, forced):
        self.trail.append(DRAW_BITS_RECORD)


class Examples:
    __doc__ = 'A lazy collection of ``Example`` objects, derived from\n    the record of recorded behaviour in ``ExampleRecord``.\n\n    Behaves logically as if it were a list of ``Example`` objects,\n    but actually mostly exists as a compact store of information\n    for them to reference into. All properties on here are best\n    understood as the backing storage for ``Example`` and are\n    described there.\n    '

    def __init__(self, record, blocks):
        self.trail = record.trail
        self.labels = record.labels
        self._Examples__length = self.trail.count(STOP_EXAMPLE_DISCARD_RECORD) + record.trail.count(STOP_EXAMPLE_NO_DISCARD_RECORD) + record.trail.count(DRAW_BITS_RECORD)
        self._Examples__example_lengths = None
        self.blocks = blocks
        self._Examples__children = None

    @calculated_example_property
    class starts_and_ends(ExampleProperty):

        def begin(self):
            self.starts = IntList.of_length(len(self.examples))
            self.ends = IntList.of_length(len(self.examples))

        def start_example(self, i, label_index):
            self.starts[i] = self.bytes_read

        def stop_example(self, i, label_index):
            self.ends[i] = self.bytes_read

        def finish(self):
            return (
             self.starts, self.ends)

    @property
    def starts(self):
        return self.starts_and_ends[0]

    @property
    def ends(self):
        return self.starts_and_ends[1]

    @calculated_example_property
    class discarded(ExampleProperty):

        def begin(self):
            self.result = set()

        def finish(self):
            return frozenset(self.result)

        def stop_example(self, i, discarded):
            if discarded:
                self.result.add(i)

    @calculated_example_property
    class trivial(ExampleProperty):

        def begin(self):
            self.nontrivial = IntList.of_length(len(self.examples))
            self.result = set()

        def block(self, i):
            if not self.examples.blocks.trivial(i):
                self.nontrivial[self.example_stack[(-1)]] = 1

        def stop_example(self, i, discarded):
            if self.nontrivial[i]:
                if self.example_stack:
                    self.nontrivial[self.example_stack[(-1)]] = 1
            else:
                self.result.add(i)

        def finish(self):
            return frozenset(self.result)

    @calculated_example_property
    class parentage(ExampleProperty):

        def stop_example(self, i, discarded):
            if i > 0:
                self.result[i] = self.example_stack[(-1)]

    @calculated_example_property
    class depths(ExampleProperty):

        def begin(self):
            self.result = IntList.of_length(len(self.examples))

        def start_example(self, i, label_index):
            self.result[i] = len(self.example_stack)

    @calculated_example_property
    class label_indices(ExampleProperty):

        def start_example(self, i, label_index):
            self.result[i] = label_index

    @property
    def children(self):
        if self._Examples__children is None:
            self._Examples__children = [IntList() for _ in range(len(self))]
            for i, p in enumerate(self.parentage):
                if i > 0:
                    self._Examples__children[p].append(i)
            else:
                for i, c in enumerate(self._Examples__children):
                    if not c:
                        self._Examples__children[i] = ()

        return self._Examples__children

    def __len__(self):
        return self._Examples__length

    def __getitem__(self, i):
        assert isinstance(i, int)
        n = len(self)
        if i < -n or i >= n:
            raise IndexError('Index %d out of range [-%d, %d)' % (i, n, n))
        if i < 0:
            i += n
        return Example(self, i)


@attr.s(slots=True, frozen=True)
class Block:
    __doc__ = 'Blocks track the flat list of lowest-level draws from the byte stream,\n    within a single test run.\n\n    Block-tracking allows the shrinker to try "low-level"\n    transformations, such as minimizing the numeric value of an\n    individual call to ``draw_bits``.\n    '
    start = attr.ib()
    end = attr.ib()
    index = attr.ib()
    forced = attr.ib(repr=False)
    all_zero = attr.ib(repr=False)

    @property
    def bounds(self):
        return (self.start, self.end)

    @property
    def length(self):
        return self.end - self.start

    @property
    def trivial(self):
        return self.forced or self.all_zero


class Blocks:
    __doc__ = 'A lazily calculated list of blocks for a particular ``ConjectureResult``\n    or ``ConjectureData`` object.\n\n    Pretends to be a list containing ``Block`` objects but actually only\n    contains their endpoints right up until the point where you want to\n    access the actual block, at which point it is constructed.\n\n    This is designed to be as space efficient as possible, so will at\n    various points silently transform its representation into one\n    that is better suited for the current access pattern.\n\n    In addition, it has a number of convenience methods for accessing\n    properties of the block object at index ``i`` that should generally\n    be preferred to using the Block objects directly, as it will not\n    have to allocate the actual object.'
    __slots__ = ('endpoints', 'owner', '__blocks', '__count', '__sparse')

    def __init__(self, owner):
        self.owner = owner
        self.endpoints = IntList()
        self._Blocks__blocks = {}
        self._Blocks__count = 0
        self._Blocks__sparse = True

    def add_endpoint(self, n):
        """Add n to the list of endpoints."""
        assert isinstance(self.owner, ConjectureData)
        self.endpoints.append(n)

    def transfer_ownership(self, new_owner):
        """Used to move ``Blocks`` over to a ``ConjectureResult`` object
        when that is read to be used and we no longer want to keep the
        whole ``ConjectureData`` around."""
        assert isinstance(new_owner, ConjectureResult)
        self.owner = new_owner
        self._Blocks__check_completion()

    def start(self, i):
        """Equivalent to self[i].start."""
        i = self._check_index(i)
        if i == 0:
            return 0
        return self.end(i - 1)

    def end(self, i):
        """Equivalent to self[i].end."""
        return self.endpoints[i]

    def bounds(self, i):
        """Equivalent to self[i].bounds."""
        return (
         self.start(i), self.end(i))

    def all_bounds(self):
        """Equivalent to [(b.start, b.end) for b in self]."""
        prev = 0
        for e in self.endpoints:
            (yield (
             prev, e))
            prev = e

    @property
    def last_block_length(self):
        return self.end(-1) - self.start(-1)

    def __len__(self):
        return len(self.endpoints)

    def __known_block--- This code section failed: ---

 L. 559         0  SETUP_FINALLY        14  'to 14'

 L. 560         2  LOAD_FAST                'self'
                4  LOAD_ATTR                _Blocks__blocks
                6  LOAD_FAST                'i'
                8  BINARY_SUBSCR    
               10  POP_BLOCK        
               12  RETURN_VALUE     
             14_0  COME_FROM_FINALLY     0  '0'

 L. 561        14  DUP_TOP          
               16  LOAD_GLOBAL              KeyError
               18  LOAD_GLOBAL              IndexError
               20  BUILD_TUPLE_2         2 
               22  COMPARE_OP               exception-match
               24  POP_JUMP_IF_FALSE    38  'to 38'
               26  POP_TOP          
               28  POP_TOP          
               30  POP_TOP          

 L. 562        32  POP_EXCEPT       
               34  LOAD_CONST               None
               36  RETURN_VALUE     
             38_0  COME_FROM            24  '24'
               38  END_FINALLY      

Parse error at or near `POP_TOP' instruction at offset 28

    def trivial(self, i):
        """Equivalent to self.blocks[i].trivial."""
        if self.owner is not None:
            return self.start(i) in self.owner.forced_indices or not any(self.owner.buffer[self.start(i):self.end(i)])
        return self[i].trivial

    def _check_index(self, i):
        n = len(self)
        if i < -n or i >= n:
            raise IndexError('Index %d out of range [-%d, %d)' % (i, n, n))
        if i < 0:
            i += n
        return i

    def __getitem__(self, i):
        i = self._check_index(i)
        assert i >= 0
        result = self._Blocks__known_block(i)
        if result is not None:
            return result
        if self._Blocks__sparse:
            if len(self._Blocks__blocks) * 2 >= len(self):
                new_blocks = [
                 None] * len(self)
                for k, v in self._Blocks__blocks.items():
                    new_blocks[k] = v
                else:
                    self._Blocks__sparse = False
                    self._Blocks__blocks = new_blocks
                    assert self._Blocks__blocks[i] is None

        start = self.start(i)
        end = self.end(i)
        self._Blocks__count += 1
        assert self._Blocks__count <= len(self)
        result = Block(start=start,
          end=end,
          index=i,
          forced=(start in self.owner.forced_indices),
          all_zero=(not any(self.owner.buffer[start:end])))
        try:
            self._Blocks__blocks[i] = result
        except IndexError:
            assert isinstance(self._Blocks__blocks, list)
            assert len(self._Blocks__blocks) < len(self)
            self._Blocks__blocks.extend([None] * (len(self) - len(self._Blocks__blocks)))
            self._Blocks__blocks[i] = result
        else:
            self._Blocks__check_completion()
            return result

    def __check_completion(self):
        """The list of blocks is complete if we have created every ``Block``
        object that we currently good and know that no more will be created.

        If this happens then we don't need to keep the reference to the
        owner around, and delete it so that there is no circular reference.
        The main benefit of this is that the gc doesn't need to run to collect
        this because normal reference counting is enough.
        """
        if self._Blocks__count == len(self):
            if isinstance(self.owner, ConjectureResult):
                self.owner = None

    def __iter__(self):
        for i in range(len(self)):
            (yield self[i])

    def __repr__(self):
        parts = []
        for i in range(len(self)):
            b = self._Blocks__known_block(i)
            if b is None:
                parts.append('...')
            else:
                parts.append(repr(b))
        else:
            return 'Block([%s])' % (', '.join(parts),)


class _Overrun:
    status = Status.OVERRUN

    def __repr__(self):
        return 'Overrun'

    def as_result(self):
        return self


Overrun = _Overrun()
global_test_counter = 0
MAX_DEPTH = 100

class DataObserver:
    __doc__ = 'Observer class for recording the behaviour of a\n    ConjectureData object, primarily used for tracking\n    the behaviour in the tree cache.'

    def conclude_test(self, status, interesting_origin):
        """Called when ``conclude_test`` is called on the
        observed ``ConjectureData``, with the same arguments.

        Note that this is called after ``freeze`` has completed.
        """
        pass

    def draw_bits(self, n_bits, forced, value):
        """Called when ``draw_bits`` is called on on the
        observed ``ConjectureData``.
        * ``n_bits`` is the number of bits drawn.
        *  ``forced`` is True if the corresponding
           draw was forced or ``False`` otherwise.
        * ``value`` is the result that ``draw_bits`` returned.
        """
        pass

    def kill_branch(self):
        """Mark this part of the tree as not worth re-exploring."""
        pass


@attr.s(slots=True)
class ConjectureResult:
    __doc__ = 'Result class storing the parts of ConjectureData that we\n    will care about after the original ConjectureData has outlived its\n    usefulness.'
    status = attr.ib()
    interesting_origin = attr.ib()
    buffer = attr.ib()
    blocks = attr.ib()
    output = attr.ib()
    extra_information = attr.ib()
    has_discards = attr.ib()
    target_observations = attr.ib()
    tags = attr.ib()
    forced_indices = attr.ib(repr=False)
    examples = attr.ib(repr=False)
    index = attr.ib(init=False)

    def __attrs_post_init__(self):
        self.index = len(self.buffer)
        self.forced_indices = frozenset(self.forced_indices)

    def as_result(self):
        return self


BYTE_MASKS = [(1 << n) - 1 for n in range(8)]
BYTE_MASKS[0] = 255

class ConjectureData:

    @classmethod
    def for_buffer(self, buffer, observer=None):
        return ConjectureData(prefix=buffer,
          max_length=(len(buffer)),
          random=None,
          observer=observer)

    def __init__(self, max_length, prefix, random, observer=None):
        global global_test_counter
        if observer is None:
            observer = DataObserver()
        else:
            assert isinstance(observer, DataObserver)
            self._ConjectureData__bytes_drawn = 0
            self.observer = observer
            self.max_length = max_length
            self.is_find = False
            self.overdraw = 0
            self._ConjectureData__block_starts = defaultdict(list)
            self._ConjectureData__block_starts_calculated_to = 0
            self._ConjectureData__prefix = prefix
            self._ConjectureData__random = random
            if not random is not None:
                if not max_length <= len(prefix):
                    raise AssertionError
        self.blocks = Blocks(self)
        self.buffer = bytearray()
        self.index = 0
        self.output = ''
        self.status = Status.VALID
        self.frozen = False
        self.testcounter = global_test_counter
        global_test_counter += 1
        self.start_time = benchmark_time()
        self.events = set()
        self.forced_indices = set()
        self.interesting_origin = None
        self.draw_times = []
        self.max_depth = 0
        self.has_discards = False
        self._ConjectureData__result = None
        self.target_observations = {}
        self.tags = set()
        self.labels_for_structure_stack = []
        self._ConjectureData__examples = None
        self.depth = -1
        self._ConjectureData__example_record = ExampleRecord()
        self.extra_information = ExtraInformation()
        self.start_example(TOP_LABEL)

    def __repr__(self):
        return 'ConjectureData(%s, %d bytes%s)' % (
         self.status.name,
         len(self.buffer),
         ', frozen' if self.frozen else '')

    def as_result(self):
        """Convert the result of running this test into
        either an Overrun object or a ConjectureResult."""
        assert self.frozen
        if self.status == Status.OVERRUN:
            return Overrun
        if self._ConjectureData__result is None:
            self._ConjectureData__result = ConjectureResult(status=(self.status),
              interesting_origin=(self.interesting_origin),
              buffer=(self.buffer),
              examples=(self.examples),
              blocks=(self.blocks),
              output=(self.output),
              extra_information=(self.extra_information if self.extra_information.has_information() else None),
              has_discards=(self.has_discards),
              target_observations=(self.target_observations),
              tags=(frozenset(self.tags)),
              forced_indices=(self.forced_indices))
            self.blocks.transfer_ownership(self._ConjectureData__result)
        return self._ConjectureData__result

    def __assert_not_frozen(self, name):
        if self.frozen:
            raise Frozen('Cannot call %s on frozen ConjectureData' % (name,))

    def note(self, value):
        self._ConjectureData__assert_not_frozen('note')
        if not isinstance(value, str):
            value = repr(value)
        self.output += value

    def draw--- This code section failed: ---

 L. 844         0  LOAD_FAST                'self'
                2  LOAD_ATTR                is_find
                4  POP_JUMP_IF_FALSE    26  'to 26'
                6  LOAD_FAST                'strategy'
                8  LOAD_ATTR                supports_find
               10  POP_JUMP_IF_TRUE     26  'to 26'

 L. 845        12  LOAD_GLOBAL              InvalidArgument

 L. 847        14  LOAD_STR                 'Cannot use strategy %r within a call to find (presumably because it would be invalid after the call had ended).'

 L. 850        16  LOAD_FAST                'strategy'
               18  BUILD_TUPLE_1         1 

 L. 846        20  BINARY_MODULO    

 L. 845        22  CALL_FUNCTION_1       1  ''
               24  RAISE_VARARGS_1       1  'exception instance'
             26_0  COME_FROM            10  '10'
             26_1  COME_FROM             4  '4'

 L. 853        26  LOAD_FAST                'self'
               28  LOAD_ATTR                depth
               30  LOAD_CONST               0
               32  COMPARE_OP               ==
               34  STORE_FAST               'at_top_level'

 L. 854        36  LOAD_FAST                'at_top_level'
               38  POP_JUMP_IF_FALSE    46  'to 46'

 L. 859        40  LOAD_GLOBAL              benchmark_time
               42  CALL_FUNCTION_0       0  ''
               44  STORE_FAST               'start_time'
             46_0  COME_FROM            38  '38'

 L. 861        46  LOAD_FAST                'strategy'
               48  LOAD_METHOD              validate
               50  CALL_METHOD_0         0  ''
               52  POP_TOP          

 L. 863        54  LOAD_FAST                'strategy'
               56  LOAD_ATTR                is_empty
               58  POP_JUMP_IF_FALSE    68  'to 68'

 L. 864        60  LOAD_FAST                'self'
               62  LOAD_METHOD              mark_invalid
               64  CALL_METHOD_0         0  ''
               66  POP_TOP          
             68_0  COME_FROM            58  '58'

 L. 866        68  LOAD_FAST                'self'
               70  LOAD_ATTR                depth
               72  LOAD_GLOBAL              MAX_DEPTH
               74  COMPARE_OP               >=
               76  POP_JUMP_IF_FALSE    86  'to 86'

 L. 867        78  LOAD_FAST                'self'
               80  LOAD_METHOD              mark_invalid
               82  CALL_METHOD_0         0  ''
               84  POP_TOP          
             86_0  COME_FROM            76  '76'

 L. 869        86  LOAD_FAST                'label'
               88  LOAD_CONST               None
               90  COMPARE_OP               is
               92  POP_JUMP_IF_FALSE   100  'to 100'

 L. 870        94  LOAD_FAST                'strategy'
               96  LOAD_ATTR                label
               98  STORE_FAST               'label'
            100_0  COME_FROM            92  '92'

 L. 871       100  LOAD_FAST                'self'
              102  LOAD_ATTR                start_example
              104  LOAD_FAST                'label'
              106  LOAD_CONST               ('label',)
              108  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              110  POP_TOP          

 L. 872       112  SETUP_FINALLY       236  'to 236'

 L. 873       114  LOAD_FAST                'at_top_level'
              116  POP_JUMP_IF_TRUE    132  'to 132'

 L. 874       118  LOAD_FAST                'strategy'
              120  LOAD_METHOD              do_draw
              122  LOAD_FAST                'self'
              124  CALL_METHOD_1         1  ''
              126  POP_BLOCK        
              128  CALL_FINALLY        236  'to 236'
              130  RETURN_VALUE     
            132_0  COME_FROM           116  '116'

 L. 876       132  SETUP_FINALLY       188  'to 188'

 L. 877       134  LOAD_FAST                'strategy'
              136  LOAD_METHOD              validate
              138  CALL_METHOD_0         0  ''
              140  POP_TOP          

 L. 878       142  SETUP_FINALLY       164  'to 164'

 L. 879       144  LOAD_FAST                'strategy'
              146  LOAD_METHOD              do_draw
              148  LOAD_FAST                'self'
              150  CALL_METHOD_1         1  ''
              152  POP_BLOCK        
              154  CALL_FINALLY        164  'to 164'
              156  POP_BLOCK        
              158  POP_BLOCK        
              160  CALL_FINALLY        236  'to 236'
              162  RETURN_VALUE     
            164_0  COME_FROM           154  '154'
            164_1  COME_FROM_FINALLY   142  '142'

 L. 881       164  LOAD_FAST                'self'
              166  LOAD_ATTR                draw_times
              168  LOAD_METHOD              append
              170  LOAD_GLOBAL              benchmark_time
              172  CALL_FUNCTION_0       0  ''
              174  LOAD_FAST                'start_time'
              176  BINARY_SUBTRACT  
              178  CALL_METHOD_1         1  ''
              180  POP_TOP          
              182  END_FINALLY      
              184  POP_BLOCK        
              186  JUMP_FORWARD        232  'to 232'
            188_0  COME_FROM_FINALLY   132  '132'

 L. 882       188  DUP_TOP          
              190  LOAD_GLOBAL              BaseException
              192  COMPARE_OP               exception-match
              194  POP_JUMP_IF_FALSE   230  'to 230'
              196  POP_TOP          
              198  STORE_FAST               'e'
              200  POP_TOP          
              202  SETUP_FINALLY       218  'to 218'

 L. 883       204  LOAD_GLOBAL              mark_for_escalation
              206  LOAD_FAST                'e'
              208  CALL_FUNCTION_1       1  ''
              210  POP_TOP          

 L. 884       212  RAISE_VARARGS_0       0  'reraise'
              214  POP_BLOCK        
              216  BEGIN_FINALLY    
            218_0  COME_FROM_FINALLY   202  '202'
              218  LOAD_CONST               None
              220  STORE_FAST               'e'
              222  DELETE_FAST              'e'
              224  END_FINALLY      
              226  POP_EXCEPT       
              228  JUMP_FORWARD        232  'to 232'
            230_0  COME_FROM           194  '194'
              230  END_FINALLY      
            232_0  COME_FROM           228  '228'
            232_1  COME_FROM           186  '186'
              232  POP_BLOCK        
              234  BEGIN_FINALLY    
            236_0  COME_FROM           160  '160'
            236_1  COME_FROM           128  '128'
            236_2  COME_FROM_FINALLY   112  '112'

 L. 886       236  LOAD_FAST                'self'
              238  LOAD_METHOD              stop_example
              240  CALL_METHOD_0         0  ''
              242  POP_TOP          
              244  END_FINALLY      

Parse error at or near `SETUP_FINALLY' instruction at offset 132

    def start_example(self, label):
        self._ConjectureData__assert_not_frozen('start_example')
        self.depth += 1
        if self.depth > self.max_depth:
            self.max_depth = self.depth
        self._ConjectureData__example_record.start_example(label)
        self.labels_for_structure_stack.append({label})

    def stop_example(self, discard=False):
        if self.frozen:
            return
            if discard:
                self.has_discards = True
            self.depth -= 1
            assert self.depth >= -1
            self._ConjectureData__example_record.stop_example(discard)
            labels_for_structure = self.labels_for_structure_stack.pop()
            if not discard:
                if self.labels_for_structure_stack:
                    self.labels_for_structure_stack[(-1)].update(labels_for_structure)
        else:
            self.tags.update([structural_coverage(l) for l in labels_for_structure])
        if discard:
            self.observer.kill_branch()

    def note_event(self, event):
        self.events.add(event)

    @property
    def examples(self):
        assert self.frozen
        if self._ConjectureData__examples is None:
            self._ConjectureData__examples = Examples(record=(self._ConjectureData__example_record), blocks=(self.blocks))
        return self._ConjectureData__examples

    def freeze(self):
        if self.frozen:
            if not isinstance(self.buffer, bytes):
                raise AssertionError
        else:
            return
            self.finish_time = benchmark_time()
            assert len(self.buffer) == self.index
            while True:
                if self.depth >= 0:
                    self.stop_example()

        self._ConjectureData__example_record.freeze()
        self.frozen = True
        self.buffer = bytes(self.buffer)
        self.events = frozenset(self.events)
        self.observer.conclude_testself.statusself.interesting_origin

    def draw_bits(self, n, forced=None):
        """Return an ``n``-bit integer from the underlying source of
        bytes. If ``forced`` is set to an integer will instead
        ignore the underlying source and simulate a draw as if it had
        returned that integer."""
        self._ConjectureData__assert_not_frozen('draw_bits')
        if n == 0:
            return 0
        if not n > 0:
            raise AssertionError
        else:
            n_bytes = bits_to_bytes(n)
            self._ConjectureData__check_capacity(n_bytes)
            if forced is not None:
                buf = int_to_bytes(forced, n_bytes)
            else:
                if self._ConjectureData__bytes_drawn < len(self._ConjectureData__prefix):
                    index = self._ConjectureData__bytes_drawn
                    buf = self._ConjectureData__prefix[index:index + n_bytes]
                    if len(buf) < n_bytes:
                        buf += uniform(self._ConjectureData__random, n_bytes - len(buf))
                else:
                    buf = uniform(self._ConjectureData__random, n_bytes)
        buf = bytearray(buf)
        self._ConjectureData__bytes_drawn += n_bytes
        assert len(buf) == n_bytes
        buf[0] &= BYTE_MASKS[(n % 8)]
        buf = bytes(buf)
        result = int_from_bytes(buf)
        self.observer.draw_bits(n, forced is not None, result)
        self._ConjectureData__example_record.draw_bitsnforced
        initial = self.index
        self.buffer.extend(buf)
        self.index = len(self.buffer)
        if forced is not None:
            self.forced_indices.update(range(initial, self.index))
        self.blocks.add_endpoint(self.index)
        assert bit_length(result) <= n
        return result

    def draw_bytes(self, n):
        """Draw n bytes from the underlying source."""
        return int_to_bytes(self.draw_bits(8 * n), n)

    def write(self, string):
        """Write ``string`` to the output buffer."""
        self._ConjectureData__assert_not_frozen('write')
        string = bytes(string)
        if not string:
            return
        self.draw_bits((len(string) * 8), forced=(int_from_bytes(string)))
        return self.buffer[-len(string):]

    def __check_capacity(self, n):
        if self.index + n > self.max_length:
            self.mark_overrun()

    def conclude_test(self, status, interesting_origin=None):
        if not interesting_origin is None:
            assert status == Status.INTERESTING
        self._ConjectureData__assert_not_frozen('conclude_test')
        self.interesting_origin = interesting_origin
        self.status = status
        self.freeze()
        raise StopTest(self.testcounter)

    def mark_interesting(self, interesting_origin=None):
        self.conclude_testStatus.INTERESTINGinteresting_origin

    def mark_invalid(self):
        self.conclude_test(Status.INVALID)

    def mark_overrun(self):
        self.conclude_test(Status.OVERRUN)


def bits_to_bytes(n):
    """The number of bytes required to represent an n-bit number.
    Equivalent to (n + 7) // 8, but slightly faster. This really is
    called enough times that that matters."""
    return n + 7 >> 3