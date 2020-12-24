# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\User\AppData\Local\Temp\pip-install-oj_abz_z\hypothesis\hypothesis\internal\conjecture\shrinker.py
# Compiled at: 2020-01-12 08:06:33
# Size of source mod 2**32: 59173 bytes
from collections import defaultdict
import attr
from hypothesis.internal.compat import int_from_bytes, int_to_bytes
from hypothesis.internal.conjecture.choicetree import ChoiceTree
from hypothesis.internal.conjecture.data import ConjectureResult, Overrun, Status
from hypothesis.internal.conjecture.floats import DRAW_FLOAT_LABEL, float_to_lex, lex_to_float
from hypothesis.internal.conjecture.junkdrawer import binary_search, replace_all
from hypothesis.internal.conjecture.shrinking import Float, Integer, Lexical, Ordering
from hypothesis.internal.conjecture.shrinking.common import find_integer

def sort_key(buffer):
    """Returns a sort key such that "simpler" buffers are smaller than
    "more complicated" ones.

    We define sort_key so that x is simpler than y if x is shorter than y or if
    they have the same length and x < y lexicographically. This is called the
    shortlex order.

    The reason for using the shortlex order is:

    1. If x is shorter than y then that means we had to make fewer decisions
       in constructing the test case when we ran x than we did when we ran y.
    2. If x is the same length as y then replacing a byte with a lower byte
       corresponds to reducing the value of an integer we drew with draw_bits
       towards zero.
    3. We want a total order, and given (2) the natural choices for things of
       the same size are either the lexicographic or colexicographic orders
       (the latter being the lexicographic order of the reverse of the string).
       Because values drawn early in generation potentially get used in more
       places they potentially have a more significant impact on the final
       result, so it makes sense to prioritise reducing earlier values over
       later ones. This makes the lexicographic order the more natural choice.
    """
    return (
     len(buffer), buffer)


SHRINK_PASS_DEFINITIONS = {}

@attr.s()
class ShrinkPassDefinition:
    __doc__ = 'A shrink pass bundles together a large number of local changes to\n    the current shrink target.\n\n    Each shrink pass is defined by some function and some arguments to that\n    function. The ``generate_arguments`` function returns all arguments that\n    might be useful to run on the current shrink target.\n\n    The guarantee made by methods defined this way is that after they are\n    called then *either* the shrink target has changed *or* each of\n    ``fn(*args)`` has been called for every ``args`` in ``generate_arguments(self)``.\n    No guarantee is made that all of these will be called if the shrink target\n    changes.\n    '
    run_with_chooser = attr.ib()

    @property
    def name(self):
        return self.run_with_chooser.__name__

    def __attrs_post_init__(self):
        assert self.name not in SHRINK_PASS_DEFINITIONS, self.name
        SHRINK_PASS_DEFINITIONS[self.name] = self


def defines_shrink_pass():
    """A convenient decorator for defining shrink passes."""

    def accept(run_step):
        ShrinkPassDefinition(run_with_chooser=run_step)

        def run(self):
            raise AssertionError('Shrink passes should not be run directly')

        run.__name__ = run_step.__name__
        run.is_shrink_pass = True
        return run

    return accept


class Shrinker:
    __doc__ = "A shrinker is a child object of a ConjectureRunner which is designed to\n    manage the associated state of a particular shrink problem. That is, we\n    have some initial ConjectureData object and some property of interest\n    that it satisfies, and we want to find a ConjectureData object with a\n    shortlex (see sort_key above) smaller buffer that exhibits the same\n    property.\n\n    Currently the only property of interest we use is that the status is\n    INTERESTING and the interesting_origin takes on some fixed value, but we\n    may potentially be interested in other use cases later.\n    However we assume that data with a status < VALID never satisfies the predicate.\n\n    The shrinker keeps track of a value shrink_target which represents the\n    current best known ConjectureData object satisfying the predicate.\n    It refines this value by repeatedly running *shrink passes*, which are\n    methods that perform a series of transformations to the current shrink_target\n    and evaluate the underlying test function to find new ConjectureData\n    objects. If any of these satisfy the predicate, the shrink_target\n    is updated automatically. Shrinking runs until no shrink pass can\n    improve the shrink_target, at which point it stops. It may also be\n    terminated if the underlying engine throws RunIsComplete, but that\n    is handled by the calling code rather than the Shrinker.\n\n    =======================\n    Designing Shrink Passes\n    =======================\n\n    Generally a shrink pass is just any function that calls\n    cached_test_function and/or incorporate_new_buffer a number of times,\n    but there are a couple of useful things to bear in mind.\n\n    A shrink pass *makes progress* if running it changes self.shrink_target\n    (i.e. it tries a shortlex smaller ConjectureData object satisfying\n    the predicate). The desired end state of shrinking is to find a\n    value such that no shrink pass can make progress, i.e. that we\n    are at a local minimum for each shrink pass.\n\n    In aid of this goal, the main invariant that a shrink pass much\n    satisfy is that whether it makes progress must be deterministic.\n    It is fine (encouraged even) for the specific progress it makes\n    to be non-deterministic, but if you run a shrink pass, it makes\n    no progress, and then you immediately run it again, it should\n    never succeed on the second time. This allows us to stop as soon\n    as we have run each shrink pass and seen no progress on any of\n    them.\n\n    This means that e.g. it's fine to try each of N deletions\n    or replacements in a random order, but it's not OK to try N random\n    deletions (unless you have already shrunk at least once, though we\n    don't currently take advantage of this loophole).\n\n    Shrink passes need to be written so as to be robust against\n    change in the underlying shrink target. It is generally safe\n    to assume that the shrink target does not change prior to the\n    point of first modification - e.g. if you change no bytes at\n    index ``i``, all examples whose start is ``<= i`` still exist,\n    as do all blocks, and the data object is still of length\n    ``>= i + 1``. This can only be violated by bad user code which\n    relies on an external source of non-determinism.\n\n    When the underlying shrink_target changes, shrink\n    passes should not run substantially more test_function calls\n    on success than they do on failure. Say, no more than a constant\n    factor more. In particular shrink passes should not iterate to a\n    fixed point.\n\n    This means that shrink passes are often written with loops that\n    are carefully designed to do the right thing in the case that no\n    shrinks occurred and try to adapt to any changes to do a reasonable\n    job. e.g. say we wanted to write a shrink pass that tried deleting\n    each individual byte (this isn't an especially good choice,\n    but it leads to a simple illustrative example), we might do it\n    by iterating over the buffer like so:\n\n    .. code-block:: python\n\n        i = 0\n        while i < len(self.shrink_target.buffer):\n            if not self.incorporate_new_buffer(\n                self.shrink_target.buffer[: i] +\n                self.shrink_target.buffer[i + 1 :]\n            ):\n                i += 1\n\n    The reason for writing the loop this way is that i is always a\n    valid index into the current buffer, even if the current buffer\n    changes as a result of our actions. When the buffer changes,\n    we leave the index where it is rather than restarting from the\n    beginning, and carry on. This means that the number of steps we\n    run in this case is always bounded above by the number of steps\n    we would run if nothing works.\n\n    Another thing to bear in mind about shrink pass design is that\n    they should prioritise *progress*. If you have N operations that\n    you need to run, you should try to order them in such a way as\n    to avoid stalling, where you have long periods of test function\n    invocations where no shrinks happen. This is bad because whenever\n    we shrink we reduce the amount of work the shrinker has to do\n    in future, and often speed up the test function, so we ideally\n    wanted those shrinks to happen much earlier in the process.\n\n    Sometimes stalls are inevitable of course - e.g. if the pass\n    makes no progress, then the entire thing is just one long stall,\n    but it's helpful to design it so that stalls are less likely\n    in typical behaviour.\n\n    The two easiest ways to do this are:\n\n    * Just run the N steps in random order. As long as a\n      reasonably large proportion of the operations suceed, this\n      guarantees the expected stall length is quite short. The\n      book keeping for making sure this does the right thing when\n      it succeeds can be quite annoying.\n    * When you have any sort of nested loop, loop in such a way\n      that both loop variables change each time. This prevents\n      stalls which occur when one particular value for the outer\n      loop is impossible to make progress on, rendering the entire\n      inner loop into a stall.\n\n    However, although progress is good, too much progress can be\n    a bad sign! If you're *only* seeing successful reductions,\n    that's probably a sign that you are making changes that are\n    too timid. Two useful things to offset this:\n\n    * It's worth writing shrink passes which are *adaptive*, in\n      the sense that when operations seem to be working really\n      well we try to bundle multiple of them together. This can\n      often be used to turn what would be O(m) successful calls\n      into O(log(m)).\n    * It's often worth trying one or two special minimal values\n      before trying anything more fine grained (e.g. replacing\n      the whole thing with zero).\n\n    "

    def derived_value(fn):
        """It's useful during shrinking to have access to derived values of
        the current shrink target.

        This decorator allows you to define these as cached properties. They
        are calculated once, then cached until the shrink target changes, then
        recalculated the next time they are used."""

        def accept--- This code section failed: ---

 L. 253         0  SETUP_FINALLY        16  'to 16'

 L. 254         2  LOAD_FAST                'self'
                4  LOAD_ATTR                _Shrinker__derived_values
                6  LOAD_DEREF               'fn'
                8  LOAD_ATTR                __name__
               10  BINARY_SUBSCR    
               12  POP_BLOCK        
               14  RETURN_VALUE     
             16_0  COME_FROM_FINALLY     0  '0'

 L. 255        16  DUP_TOP          
               18  LOAD_GLOBAL              KeyError
               20  COMPARE_OP               exception-match
               22  POP_JUMP_IF_FALSE    54  'to 54'
               24  POP_TOP          
               26  POP_TOP          
               28  POP_TOP          

 L. 256        30  LOAD_FAST                'self'
               32  LOAD_ATTR                _Shrinker__derived_values
               34  LOAD_METHOD              setdefault
               36  LOAD_DEREF               'fn'
               38  LOAD_ATTR                __name__
               40  LOAD_DEREF               'fn'
               42  LOAD_FAST                'self'
               44  CALL_FUNCTION_1       1  ''
               46  CALL_METHOD_2         2  ''
               48  ROT_FOUR         
               50  POP_EXCEPT       
               52  RETURN_VALUE     
             54_0  COME_FROM            22  '22'
               54  END_FINALLY      

Parse error at or near `POP_TOP' instruction at offset 26

        accept.__name__ = fn.__name__
        return property(accept)

    def __init__(self, engine, initial, predicate):
        """Create a shrinker for a particular engine, with a given starting
        point and predicate. When shrink() is called it will attempt to find an
        example for which predicate is True and which is strictly smaller than
        initial.

        Note that initial is a ConjectureData object, and predicate
        takes ConjectureData objects.
        """
        self.engine = engine
        self._Shrinker__predicate = predicate
        self._Shrinker__derived_values = {}
        self._Shrinker__pending_shrink_explanation = None
        self.initial_size = len(initial.buffer)
        self.shrink_target = None
        self.update_shrink_target(initial)
        self.shrinks = 0
        self.initial_calls = self.engine.call_count
        self.passes_by_name = {}
        self.passes = []

    @derived_value
    def cached_calculations(self):
        return {}

    def cached(self, *keys):

        def accept--- This code section failed: ---

 L. 294         0  LOAD_FAST                'f'
                2  LOAD_ATTR                __name__
                4  BUILD_TUPLE_1         1 
                6  LOAD_DEREF               'keys'
                8  BINARY_ADD       
               10  STORE_FAST               'cache_key'

 L. 295        12  SETUP_FINALLY        26  'to 26'

 L. 296        14  LOAD_DEREF               'self'
               16  LOAD_ATTR                cached_calculations
               18  LOAD_FAST                'cache_key'
               20  BINARY_SUBSCR    
               22  POP_BLOCK        
               24  RETURN_VALUE     
             26_0  COME_FROM_FINALLY    12  '12'

 L. 297        26  DUP_TOP          
               28  LOAD_GLOBAL              KeyError
               30  COMPARE_OP               exception-match
               32  POP_JUMP_IF_FALSE    60  'to 60'
               34  POP_TOP          
               36  POP_TOP          
               38  POP_TOP          

 L. 298        40  LOAD_DEREF               'self'
               42  LOAD_ATTR                cached_calculations
               44  LOAD_METHOD              setdefault
               46  LOAD_FAST                'cache_key'
               48  LOAD_FAST                'f'
               50  CALL_FUNCTION_0       0  ''
               52  CALL_METHOD_2         2  ''
               54  ROT_FOUR         
               56  POP_EXCEPT       
               58  RETURN_VALUE     
             60_0  COME_FROM            32  '32'
               60  END_FINALLY      

Parse error at or near `POP_TOP' instruction at offset 36

        return accept

    def explain_next_call_as(self, explanation):
        self._Shrinker__pending_shrink_explanation = explanation

    def clear_call_explanation(self):
        self._Shrinker__pending_shrink_explanation = None

    def add_new_pass(self, run):
        """Creates a shrink pass corresponding to calling ``run(self)``"""
        definition = SHRINK_PASS_DEFINITIONS[run]
        p = ShrinkPass(run_with_chooser=(definition.run_with_chooser),
          shrinker=self,
          index=(len(self.passes)))
        self.passes.append(p)
        self.passes_by_name[p.name] = p
        return p

    def shrink_pass(self, name):
        """Return the ShrinkPass object for the pass with the given name."""
        if isinstance(name, ShrinkPass):
            return name
        if name not in self.passes_by_name:
            self.add_new_pass(name)
        return self.passes_by_name[name]

    @property
    def calls(self):
        """Return the number of calls that have been made to the underlying
        test function."""
        return self.engine.call_count

    def consider_new_buffer(self, buffer):
        """Returns True if after running this buffer the result would be
        the current shrink_target."""
        buffer = bytes(buffer)
        return buffer.startswith(self.buffer) or self.incorporate_new_buffer(buffer)

    def incorporate_new_buffer(self, buffer):
        """Either runs the test function on this buffer and returns True if
        that changed the shrink_target, or determines that doing so would
        be useless and returns False without running it."""
        buffer = bytes(buffer[:self.shrink_target.index])
        if sort_key(buffer) >= sort_key(self.shrink_target.buffer):
            return False
        if self.shrink_target.buffer.startswith(buffer):
            return False
        previous = self.shrink_target
        self.cached_test_function(buffer)
        return previous is not self.shrink_target

    def incorporate_test_data(self, data):
        """Takes a ConjectureData or Overrun object updates the current
        shrink_target if this data represents an improvement over it,
        returning True if it is."""
        if data is Overrun or data is self.shrink_target:
            return
        if self._Shrinker__predicate(data):
            if sort_key(data.buffer) < sort_key(self.shrink_target.buffer):
                self.update_shrink_target(data)
                return True
        return False

    def cached_test_function(self, buffer):
        """Returns a cached version of the underlying test function, so
        that the result is either an Overrun object (if the buffer is
        too short to be a valid test case) or a ConjectureData object
        with status >= INVALID that would result from running this buffer."""
        if self._Shrinker__pending_shrink_explanation is not None:
            self.debug(self._Shrinker__pending_shrink_explanation)
            self._Shrinker__pending_shrink_explanation = None
        buffer = bytes(buffer)
        result = self.engine.cached_test_function(buffer)
        self.incorporate_test_data(result)
        return result

    def debug(self, msg):
        self.engine.debug(msg)

    @property
    def random(self):
        return self.engine.random

    def shrink(self):
        """Run the full set of shrinks and update shrink_target.

        This method is "mostly idempotent" - calling it twice is unlikely to
        have any effect, though it has a non-zero probability of doing so.
        """
        if not any(self.shrink_target.buffer) or self.incorporate_new_buffer(bytes(len(self.shrink_target.buffer))):
            return
        try:
            self.greedy_shrink()
        finally:
            if self.engine.report_debug_info:

                def s(n):
                    if n != 1:
                        return 's'
                    return ''

                total_deleted = self.initial_size - len(self.shrink_target.buffer)
                self.debug('---------------------')
                self.debug('Shrink pass profiling')
                self.debug('---------------------')
                self.debug('')
                calls = self.engine.call_count - self.initial_calls
                self.debug('Shrinking made a total of %d call%s of which %d shrank. This deleted %d byte%s out of %d.' % (
                 calls,
                 s(calls),
                 self.shrinks,
                 total_deleted,
                 s(total_deleted),
                 self.initial_size))
                for useful in (True, False):
                    self.debug('')
                    if useful:
                        self.debug('Useful passes:')
                    else:
                        self.debug('Useless passes:')
                    self.debug('')
                    for p in sorted((self.passes),
                      key=(lambda t: (-t.calls, t.deletions, t.shrinks))):
                        if p.calls == 0:
                            pass
                        elif (p.shrinks != 0) != useful:
                            pass
                        else:
                            self.debug('  * %s made %d call%s of which %d shrank, deleting %d byte%s.' % (
                             p.name,
                             p.calls,
                             s(p.calls),
                             p.shrinks,
                             p.deletions,
                             s(p.deletions)))
                    else:
                        self.debug('')

    def greedy_shrink(self):
        """Run a full set of greedy shrinks (that is, ones that will only ever
        move to a better target) and update shrink_target appropriately.

        This method iterates to a fixed point and so is idempontent - calling
        it twice will have exactly the same effect as calling it once.
        """
        self.fixate_shrink_passes([
         block_program('XXXXX'),
         block_program('XXXX'),
         block_program('XXX'),
         block_program('XX'),
         block_program('X'),
         'pass_to_descendant',
         'adaptive_example_deletion',
         'alphabet_minimize',
         'zero_examples',
         'reorder_examples',
         'minimize_floats',
         'minimize_duplicated_blocks',
         block_program('-XX'),
         'minimize_individual_blocks',
         block_program('--X')])

    @derived_value
    def shrink_pass_choice_trees(self):
        return defaultdict(ChoiceTree)

    def fixate_shrink_passes(self, passes):
        """Run steps from each pass in ``passes`` until the current shrink target
        is a fixed point of all of them."""
        passes = list(map(self.shrink_pass, passes))
        any_ran = True
        while any_ran:
            any_ran = False
            can_discard = self.remove_discarded()
            successful_passes = set()
            for sp in passes:
                failures = 0
                successes = 0
                max_failures = 3
                while failures < max_failures:
                    prev_calls = self.calls
                    prev = self.shrink_target
                    if sp.step():
                        any_ran = True
                    else:
                        break
                    if prev_calls != self.calls:
                        if can_discard:
                            can_discard = self.remove_discarded()
                        if prev is self.shrink_target:
                            failures += 1
                    else:
                        successes += 1

                if successes > 0:
                    successful_passes.add(sp)
                if 0 < len(successful_passes) < len(passes):
                    self.fixate_shrink_passes(successful_passes)

        for sp in passes:
            sp.fixed_point_at = self.shrink_target

    @property
    def buffer(self):
        return self.shrink_target.buffer

    @property
    def blocks(self):
        return self.shrink_target.blocks

    @property
    def examples(self):
        return self.shrink_target.examples

    def all_block_bounds(self):
        return self.shrink_target.blocks.all_bounds()

    @derived_value
    def examples_by_label(self):
        """An index of all examples grouped by their label, with
        the examples stored in their normal index order."""
        examples_by_label = defaultdict(list)
        for ex in self.examples:
            examples_by_label[ex.label].append(ex)
        else:
            return dict(examples_by_label)

    @derived_value
    def distinct_labels(self):
        return sorted((self.examples_by_label), key=str)

    @defines_shrink_pass()
    def pass_to_descendant(self, chooser):
        """Attempt to replace each example with a descendant example.

        This is designed to deal with strategies that call themselves
        recursively. For example, suppose we had:

        binary_tree = st.deferred(
            lambda: st.one_of(
                st.integers(), st.tuples(binary_tree, binary_tree)))

        This pass guarantees that we can replace any binary tree with one of
        its subtrees - each of those will create an interval that the parent
        could validly be replaced with, and this pass will try doing that.

        This is pretty expensive - it takes O(len(intervals)^2) - so we run it
        late in the process when we've got the number of intervals as far down
        as possible.
        """
        label = chooser.chooseself.distinct_labels(lambda l: len(self.examples_by_label[l]) >= 2)
        ls = self.examples_by_label[label]
        i = chooser.choose(range(len(ls) - 1))
        ancestor = ls[i]
        if i + 1 == len(ls) or ls[(i + 1)].start >= ancestor.end:
            return

        @self.cachedlabeli
        def descendants():
            lo = i + 1
            hi = len(ls)
            while lo + 1 < hi:
                mid = (lo + hi) // 2
                if ls[mid].start >= ancestor.end:
                    hi = mid
                else:
                    lo = mid

            return [t for t in ls[i + 1:hi] if t.length < ancestor.length]

        descendant = chooser.choosedescendants(lambda ex: ex.length > 0)
        assert ancestor.start <= descendant.start
        assert ancestor.end >= descendant.end
        assert descendant.length < ancestor.length
        self.incorporate_new_buffer(self.buffer[:ancestor.start] + self.buffer[descendant.start:descendant.end] + self.buffer[ancestor.end:])

    def lower_common_block_offset(self):
        """Sometimes we find ourselves in a situation where changes to one part
        of the byte stream unlock changes to other parts. Sometimes this is
        good, but sometimes this can cause us to exhibit exponential slow
        downs!

        e.g. suppose we had the following:

        m = draw(integers(min_value=0))
        n = draw(integers(min_value=0))
        assert abs(m - n) > 1

        If this fails then we'll end up with a loop where on each iteration we
        reduce each of m and n by 2 - m can't go lower because of n, then n
        can't go lower because of m.

        This will take us O(m) iterations to complete, which is exponential in
        the data size, as we gradually zig zag our way towards zero.

        This can only happen if we're failing to reduce the size of the byte
        stream: The number of iterations that reduce the length of the byte
        stream is bounded by that length.

        So what we do is this: We keep track of which blocks are changing, and
        then if there's some non-zero common offset to them we try and minimize
        them all at once by lowering that offset.

        This may not work, and it definitely won't get us out of all possible
        exponential slow downs (an example of where it doesn't is where the
        shape of the blocks changes as a result of this bouncing behaviour),
        but it fails fast when it doesn't work and gets us out of a really
        nastily slow case when it does.
        """
        if len(self._Shrinker__changed_blocks) <= 1:
            return
        else:
            current = self.shrink_target
            blocked = [current.buffer[u:v] for u, v in self.all_block_bounds()]
            changed = [i for i in sorted(self._Shrinker__changed_blocks) if not self.shrink_target.blocks[i].trivial]
            return changed or None
        ints = [int_from_bytes(blocked[i]) for i in changed]
        offset = min(ints)
        assert offset > 0
        for i in range(len(ints)):
            ints[i] -= offset
        else:

            def reoffset(o):
                new_blocks = list(blocked)
                for i, v in zip(changed, ints):
                    new_blocks[i] = int_to_bytes(v + o, len(blocked[i]))
                else:
                    return self.incorporate_new_buffer(''.join(new_blocks))

            Integer.shrink(offset, reoffset, random=(self.random))
            self.clear_change_tracking()

    def clear_change_tracking(self):
        self._Shrinker__last_checked_changed_at = self.shrink_target
        self._Shrinker__all_changed_blocks = set()

    def mark_changed(self, i):
        self._Shrinker__changed_blocks.add(i)

    @property
    def __changed_blocks(self):
        if self._Shrinker__last_checked_changed_at is not self.shrink_target:
            prev_target = self._Shrinker__last_checked_changed_at
            new_target = self.shrink_target
            if not prev_target is not new_target:
                raise AssertionError
            else:
                prev = prev_target.buffer
                new = new_target.buffer
                assert sort_key(new) < sort_key(prev)
                if len(new_target.blocks) != len(prev_target.blocks) or new_target.blocks.endpoints != prev_target.blocks.endpoints:
                    self._Shrinker__all_changed_blocks = set()
            blocks = new_target.blocks
            last_changed = binary_search(0, len(blocks), lambda i: prev[blocks.start(i):] != new[blocks.start(i):])
            first_changed = binary_search(0, len(blocks), lambda i: prev[:blocks.start(i)] == new[:blocks.start(i)])
            for i in range(first_changed, last_changed + 1):
                u, v = blocks.bounds(i)

            if i not in self._Shrinker__all_changed_blocks:
                if prev[u:v] != new[u:v]:
                    self._Shrinker__all_changed_blocks.add(i)
                else:
                    self._Shrinker__last_checked_changed_at = new_target
        assert self._Shrinker__last_checked_changed_at is self.shrink_target
        return self._Shrinker__all_changed_blocks

    def update_shrink_target(self, new_target):
        if not isinstance(new_target, ConjectureResult):
            raise AssertionError
        elif self.shrink_target is not None:
            self.shrinks += 1
        else:
            self._Shrinker__all_changed_blocks = set()
            self._Shrinker__last_checked_changed_at = new_target
        self.shrink_target = new_target
        self._Shrinker__derived_values = {}

    def try_shrinking_blocks(self, blocks, b):
        """Attempts to replace each block in the blocks list with b. Returns
        True if it succeeded (which may include some additional modifications
        to shrink_target).

        In current usage it is expected that each of the blocks currently have
        the same value, although this is not essential. Note that b must be
        < the block at min(blocks) or this is not a valid shrink.

        This method will attempt to do some small amount of work to delete data
        that occurs after the end of the blocks. This is useful for cases where
        there is some size dependency on the value of a block.
        """
        initial_attempt = bytearray(self.shrink_target.buffer)
        for i, block in enumerate(blocks):
            if block >= len(self.blocks):
                blocks = blocks[:i]
                break
            u, v = self.blocks[block].bounds
            n = min(self.blocks[block].length, len(b))
            initial_attempt[v - n:v] = b[-n:]
        else:
            if not blocks:
                return False
            start = self.shrink_target.blocks[blocks[0]].start
            end = self.shrink_target.blocks[blocks[(-1)]].end
            initial_data = self.cached_test_function(initial_attempt)
            if initial_data is self.shrink_target:
                self.lower_common_block_offset()
                return True
            if initial_data.status < Status.VALID:
                return False
            if len(initial_data.buffer) < v:
                return False
            lost_data = len(self.shrink_target.buffer) - len(initial_data.buffer)
            if lost_data <= 0:
                return False
            regions_to_delete = {
             (
              end, end + lost_data)}
            for j in (
             blocks[(-1)] + 1, blocks[(-1)] + 2):
                if j >= min(len(initial_data.blocks), len(self.blocks)):
                    pass
                else:
                    r1, s1 = self.shrink_target.blocks[j].bounds
                    r2, s2 = initial_data.blocks[j].bounds
                    lost = s1 - r1 - (s2 - r2)
                    if not lost <= 0:
                        if r1 != r2:
                            pass
                        else:
                            regions_to_delete.add((r1, r1 + lost))

            for ex in self.shrink_target.examples:
                if ex.start > start:
                    pass
                elif ex.end <= end:
                    pass
                else:
                    replacement = initial_data.examples[ex.index]
                    in_original = [c for c in ex.children if c.start >= end]
                    in_replaced = [c for c in replacement.children if c.start >= end]
                    if not len(in_replaced) >= len(in_original):
                        if not in_replaced:
                            pass
                        else:
                            regions_to_delete.add((
                             in_original[0].start, in_original[(-len(in_replaced))].start))
                    for u, v in sorted(regions_to_delete, key=(lambda x: x[1] - x[0]), reverse=True):
                        try_with_deleted = bytearray(initial_attempt)
                        del try_with_deleted[u:v]
                        if self.incorporate_new_buffer(try_with_deleted):
                            return True
                        return False

    def remove_discarded(self):
        """Try removing all bytes marked as discarded.

        This is primarily to deal with data that has been ignored while
        doing rejection sampling - e.g. as a result of an integer range, or a
        filtered strategy.

        Such data will also be handled by the adaptive_example_deletion pass,
        but that pass is necessarily more conservative and will try deleting
        each interval individually. The common case is that all data drawn and
        rejected can just be thrown away immediately in one block, so this pass
        will be much faster than trying each one individually when it works.

        returns False if there is discarded data and removing it does not work,
        otherwise returns True.
        """
        while self.shrink_target.has_discards:
            discarded = []
            for ex in self.shrink_target.examples:
                if ex.length > 0:
                    if ex.discarded:
                        if discarded:
                            if ex.start >= discarded[(-1)][(-1)]:
                                discarded.append((ex.start, ex.end))
                            if not discarded:
                                break
                        attempt = bytearray(self.shrink_target.buffer)
                        for u, v in reversed(discarded):
                            del attempt[u:v]

                    if not self.incorporate_new_buffer(attempt):
                        return False

        return True

    @defines_shrink_pass()
    def adaptive_example_deletion(self, chooser):
        """Attempts to delete every example from the test case.

        That is, it is logically equivalent to trying ``self.buffer[:ex.start] +
        self.buffer[ex.end:]`` for every example ``ex``. The order in which
        examples are tried is randomized, and when deletion is successful it
        will attempt to adapt to delete more than one example at a time.
        """
        example = chooser.choose(self.examples)
        if not self.incorporate_new_buffer(self.buffer[:example.start] + self.buffer[example.end:]):
            return
        original = self.shrink_target
        endpoints = set()
        for ex in original.examples:
            if ex.depth <= example.depth:
                endpoints.add(ex.start)
                endpoints.add(ex.end)
            partition = sorted(endpoints)
            j = partition.index(example.start)

            def delete_region(a, b):
                assert a <= j <= b
                if a < 0 or b >= len(partition) - 1:
                    return False
                return self.consider_new_buffer(original.buffer[:partition[a]] + original.buffer[partition[b]:])

            to_right = find_integer(lambda n: delete_region(j, j + n))
            find_integer(lambda n: delete_region(j - n, j + to_right))

    def try_zero_example(self, ex):
        u = ex.start
        v = ex.end
        attempt = self.cached_test_function(self.buffer[:u] + bytes(v - u) + self.buffer[v:])
        if attempt is Overrun:
            return False
        in_replacement = attempt.examples[ex.index]
        used = in_replacement.length
        if attempt is not self.shrink_target:
            if in_replacement.end < len(attempt.buffer):
                if used < ex.length:
                    self.incorporate_new_buffer(self.buffer[:u] + bytes(used) + self.buffer[v:])
        return self.examples[ex.index].trivial

    @defines_shrink_pass()
    def zero_examples(self, chooser):
        """Attempt to replace each example with a minimal version of itself."""
        ex = chooser.chooseself.examples(lambda ex: not ex.trivial)
        if not self.try_zero_example(ex):
            return
        ex = self.examples[ex.index]
        original = self.shrink_target
        group = self.examples_by_label[ex.label]
        i = group.index(ex)
        replacement = self.buffer[ex.start:ex.end]

        def all_trivial(a, b):
            if a < 0 or b > len(group):
                return False
            return all((e.trivial for e in group[a:b]))

        start, end = expand_region(all_trivial, i, i + 1)
        if any((e.length != len(replacement) for e in group[start:end])):
            return

        def can_zero(a, b):
            if a < 0 or b > len(group):
                return False
            regions = []
            for e in group[a:b]:
                t = (
                 e.start, e.end, replacement)
                if not regions or t[0] >= regions[(-1)][1]:
                    regions.append(t)
                return self.consider_new_buffer(replace_all(original.buffer, regions))

        expand_region(can_zero, start, end)

    @derived_value
    def blocks_by_non_zero_suffix(self):
        """Returns a list of blocks grouped by their non-zero suffix,
        as a list of (suffix, indices) pairs, skipping all groupings
        where there is only one index.

        This is only used for the arguments of minimize_duplicated_blocks.
        """
        duplicates = defaultdict(list)
        for block in self.blocks:
            duplicates[non_zero_suffix(self.buffer[block.start:block.end])].append(block.index)
        else:
            return duplicates

    @derived_value
    def duplicated_block_suffixes(self):
        return sorted(self.blocks_by_non_zero_suffix)

    @defines_shrink_pass()
    def minimize_duplicated_blocks(self, chooser):
        """Find blocks that have been duplicated in multiple places and attempt
        to minimize all of the duplicates simultaneously.

        This lets us handle cases where two values can't be shrunk
        independently of each other but can easily be shrunk together.
        For example if we had something like:

        ls = data.draw(lists(integers()))
        y = data.draw(integers())
        assert y not in ls

        Suppose we drew y = 3 and after shrinking we have ls = [3]. If we were
        to replace both 3s with 0, this would be a valid shrink, but if we were
        to replace either 3 with 0 on its own the test would start passing.

        It is also useful for when that duplication is accidental and the value
        of the blocks doesn't matter very much because it allows us to replace
        more values at once.
        """
        block = chooser.choose(self.duplicated_block_suffixes)
        targets = self.blocks_by_non_zero_suffix[block]
        if len(targets) <= 1:
            return
        Lexical.shrink(block,
          (lambda b: self.try_shrinking_blockstargetsb),
          random=(self.random),
          full=False)

    @defines_shrink_pass()
    def minimize_floats(self, chooser):
        """Some shrinks that we employ that only really make sense for our
        specific floating point encoding that are hard to discover from any
        sort of reasonable general principle. This allows us to make
        transformations like replacing a NaN with an Infinity or replacing
        a float with its nearest integers that we would otherwise not be
        able to due to them requiring very specific transformations of
        the bit sequence.

        We only apply these transformations to blocks that "look like" our
        standard float encodings because they are only really meaningful
        there. The logic for detecting this is reasonably precise, but
        it doesn't matter if it's wrong. These are always valid
        transformations to make, they just don't necessarily correspond to
        anything particularly meaningful for non-float values.
        """
        ex = chooser.chooseself.examples(lambda ex: ex.label == DRAW_FLOAT_LABEL and len(ex.children) == 2 and ex.children[0].length == 8)
        u = ex.children[0].start
        v = ex.children[0].end
        buf = self.shrink_target.buffer
        b = buf[u:v]
        f = lex_to_float(int_from_bytes(b))
        b2 = int_to_bytes(float_to_lex(f), 8)
        if b == b2 or self.consider_new_buffer(buf[:u] + b2 + buf[v:]):
            Float.shrink(f,
              (lambda x: self.consider_new_buffer(self.shrink_target.buffer[:u] + int_to_bytes(float_to_lex(x), 8) + self.shrink_target.buffer[v:])),
              random=(self.random))

    @defines_shrink_pass()
    def minimize_individual_blocks(self, chooser):
        """Attempt to minimize each block in sequence.

        This is the pass that ensures that e.g. each integer we draw is a
        minimum value. So it's the part that guarantees that if we e.g. do

        x = data.draw(integers())
        assert x < 10

        then in our shrunk example, x = 10 rather than say 97.

        If we are unsuccessful at minimizing a block of interest we then
        check if that's because it's changing the size of the test case and,
        if so, we also make an attempt to delete parts of the test case to
        see if that fixes it.

        We handle most of the common cases in try_shrinking_blocks which is
        pretty good at clearing out large contiguous blocks of dead space,
        but it fails when there is data that has to stay in particular places
        in the list.
        """
        block = chooser.chooseself.blocks(lambda b: not b.trivial)
        initial = self.shrink_target
        u, v = block.bounds
        i = block.index
        Lexical.shrink((self.shrink_target.buffer[u:v]),
          (lambda b: self.try_shrinking_blocks(i,)b),
          random=(self.random),
          full=False)
        if self.shrink_target is not initial:
            return
        lowered = self.buffer[:block.start] + int_to_bytes(int_from_bytes(self.buffer[block.start:block.end]) - 1, block.length) + self.buffer[block.end:]
        attempt = self.cached_test_function(lowered)
        if attempt.status < Status.VALID or len(attempt.buffer) == len(self.buffer) or len(attempt.buffer) == block.end:
            return
        assert attempt is not self.shrink_target

        @self.cached(block.index)
        def first_example_after_block():
            lo = 0
            hi = len(self.examples)
            while lo + 1 < hi:
                mid = (lo + hi) // 2
                ex = self.examples[mid]
                if ex.start >= block.end:
                    hi = mid
                else:
                    lo = mid

            return hi

        ex = self.examples[chooser.chooserange(first_example_after_block, len(self.examples))(lambda i: self.examples[i].length > 0)]
        u, v = block.bounds
        buf = bytearray(lowered)
        del buf[ex.start:ex.end]
        self.incorporate_new_buffer(buf)

    @defines_shrink_pass()
    def reorder_examples(self, chooser):
        """This pass allows us to reorder the children of each example.

        For example, consider the following:

        .. code-block:: python

            import hypothesis.strategies as st
            from hypothesis import given

            @given(st.text(), st.text())
            def test_not_equal(x, y):
                assert x != y

        Without the ability to reorder x and y this could fail either with
        ``x=""``, ``y="0"``, or the other way around. With reordering it will
        reliably fail with ``x=""``, ``y="0"``.
        """
        ex = chooser.choose(self.examples)
        label = chooser.choose(ex.children).label
        group = [c for c in ex.children if c.label == label]
        if len(group) <= 1:
            return
        st = self.shrink_target
        pieces = [st.buffer[ex.start:ex.end] for ex in group]
        endpoints = [(ex.start, ex.end) for ex in group]
        Ordering.shrink(pieces,
          (lambda ls: self.consider_new_buffer(replace_all(st.buffer, [(u, v, r) for (u, v), r in zip(endpoints, ls)]))),
          random=(self.random))

    @derived_value
    def alphabet(self):
        return sorted(set(self.buffer))

    @defines_shrink_pass()
    def alphabet_minimize(self, chooser):
        """Attempts to minimize the "alphabet" - the set of bytes that
        are used in the representation of the current buffer. The main
        benefit of this is that it significantly increases our cache hit rate
        by making things that are equivalent more likely to have the same
        representation, but it's also generally a rather effective "fuzzing"
        step that gives us a lot of good opportunities to slip to a smaller
        representation of the same bug.
        """
        c = chooser.choose(self.alphabet)
        buf = self.buffer

        def can_replace_with(d):
            if d < 0:
                return False
            if self.consider_new_buffer(bytes([d if b == c else b for b in buf])):
                if d <= 1:

                    def replace_range(k):
                        if k > c:
                            return False

                        def should_replace_byte(b):
                            return c - k <= b <= c and d < b

                        return self.consider_new_buffer(bytes([d if should_replace_byte(b) else b for b in buf]))

                    find_integer(replace_range)
                return True

        if not (can_replace_with(c - 1) and can_replace_with(0) or can_replace_with(1) or can_replace_with(c - 2)):
            return
            lo = 1
            hi = c - 2
            while lo + 1 < hi:
                mid = (lo + hi) // 2
                if can_replace_with(mid):
                    hi = mid
                else:
                    lo = mid

    def run_block_program--- This code section failed: ---

 L.1363         0  LOAD_FAST                'i'
                2  LOAD_GLOBAL              len
                4  LOAD_FAST                'description'
                6  CALL_FUNCTION_1       1  ''
                8  BINARY_ADD       
               10  LOAD_GLOBAL              len
               12  LOAD_FAST                'original'
               14  LOAD_ATTR                blocks
               16  CALL_FUNCTION_1       1  ''
               18  COMPARE_OP               >
               20  POP_JUMP_IF_TRUE     30  'to 30'
               22  LOAD_FAST                'i'
               24  LOAD_CONST               0
               26  COMPARE_OP               <
               28  POP_JUMP_IF_FALSE    34  'to 34'
             30_0  COME_FROM            20  '20'

 L.1364        30  LOAD_CONST               False
               32  RETURN_VALUE     
             34_0  COME_FROM            28  '28'

 L.1365        34  LOAD_GLOBAL              bytearray
               36  LOAD_FAST                'original'
               38  LOAD_ATTR                buffer
               40  CALL_FUNCTION_1       1  ''
               42  STORE_FAST               'attempt'

 L.1366        44  LOAD_GLOBAL              range
               46  LOAD_FAST                'repeats'
               48  CALL_FUNCTION_1       1  ''
               50  GET_ITER         
               52  FOR_ITER            230  'to 230'
               54  STORE_FAST               '_'

 L.1367        56  LOAD_GLOBAL              reversed
               58  LOAD_GLOBAL              list
               60  LOAD_GLOBAL              enumerate
               62  LOAD_FAST                'description'
               64  CALL_FUNCTION_1       1  ''
               66  CALL_FUNCTION_1       1  ''
               68  CALL_FUNCTION_1       1  ''
               70  GET_ITER         
               72  FOR_ITER            228  'to 228'
               74  UNPACK_SEQUENCE_2     2 
               76  STORE_FAST               'k'
               78  STORE_FAST               'd'

 L.1368        80  LOAD_FAST                'i'
               82  LOAD_FAST                'k'
               84  BINARY_ADD       
               86  STORE_FAST               'j'

 L.1369        88  LOAD_FAST                'original'
               90  LOAD_ATTR                blocks
               92  LOAD_FAST                'j'
               94  BINARY_SUBSCR    
               96  LOAD_ATTR                bounds
               98  UNPACK_SEQUENCE_2     2 
              100  STORE_FAST               'u'
              102  STORE_FAST               'v'

 L.1370       104  LOAD_FAST                'v'
              106  LOAD_GLOBAL              len
              108  LOAD_FAST                'attempt'
              110  CALL_FUNCTION_1       1  ''
              112  COMPARE_OP               >
              114  POP_JUMP_IF_FALSE   124  'to 124'

 L.1371       116  POP_TOP          
              118  POP_TOP          
              120  LOAD_CONST               False
              122  RETURN_VALUE     
            124_0  COME_FROM           114  '114'

 L.1372       124  LOAD_FAST                'd'
              126  LOAD_STR                 '-'
              128  COMPARE_OP               ==
              130  POP_JUMP_IF_FALSE   192  'to 192'

 L.1373       132  LOAD_GLOBAL              int_from_bytes
              134  LOAD_FAST                'attempt'
              136  LOAD_FAST                'u'
              138  LOAD_FAST                'v'
              140  BUILD_SLICE_2         2 
              142  BINARY_SUBSCR    
              144  CALL_FUNCTION_1       1  ''
              146  STORE_FAST               'value'

 L.1374       148  LOAD_FAST                'value'
              150  LOAD_CONST               0
              152  COMPARE_OP               ==
              154  POP_JUMP_IF_FALSE   164  'to 164'

 L.1375       156  POP_TOP          
              158  POP_TOP          
              160  LOAD_CONST               False
              162  RETURN_VALUE     
            164_0  COME_FROM           154  '154'

 L.1377       164  LOAD_GLOBAL              int_to_bytes
              166  LOAD_FAST                'value'
              168  LOAD_CONST               1
              170  BINARY_SUBTRACT  
              172  LOAD_FAST                'v'
              174  LOAD_FAST                'u'
              176  BINARY_SUBTRACT  
              178  CALL_FUNCTION_2       2  ''
              180  LOAD_FAST                'attempt'
              182  LOAD_FAST                'u'
              184  LOAD_FAST                'v'
              186  BUILD_SLICE_2         2 
              188  STORE_SUBSCR     
              190  JUMP_BACK            72  'to 72'
            192_0  COME_FROM           130  '130'

 L.1378       192  LOAD_FAST                'd'
              194  LOAD_STR                 'X'
              196  COMPARE_OP               ==
              198  POP_JUMP_IF_FALSE   212  'to 212'

 L.1379       200  LOAD_FAST                'attempt'
              202  LOAD_FAST                'u'
              204  LOAD_FAST                'v'
              206  BUILD_SLICE_2         2 
              208  DELETE_SUBSCR    
              210  JUMP_BACK            72  'to 72'
            212_0  COME_FROM           198  '198'

 L.1381       212  LOAD_GLOBAL              AssertionError
              214  LOAD_STR                 'Unrecognised command %r'
              216  LOAD_FAST                'd'
              218  BUILD_TUPLE_1         1 
              220  BINARY_MODULO    
              222  CALL_FUNCTION_1       1  ''
              224  RAISE_VARARGS_1       1  'exception instance'
              226  JUMP_BACK            72  'to 72'
              228  JUMP_BACK            52  'to 52'

 L.1382       230  LOAD_FAST                'self'
              232  LOAD_METHOD              incorporate_new_buffer
              234  LOAD_FAST                'attempt'
              236  CALL_METHOD_1         1  ''
              238  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `COME_FROM' instruction at offset 192_0


def block_program(description):
    """Mini-DSL for block rewriting. A sequence of commands that will be run
    over all contiguous sequences of blocks of the description length in order.
    Commands are:

        * ".", keep this block unchanged
        * "-", subtract one from this block.
        * "0", replace this block with zero
        * "X", delete this block

    If a command does not apply (currently only because it's - on a zero
    block) the block will be silently skipped over. As a side effect of
    running a block program its score will be updated.
    """
    name = 'block_program(%r)' % (description,)
    if name not in SHRINK_PASS_DEFINITIONS:
        n = len(description)

        def run(self, chooser):
            i = chooser.choose(range(len(self.shrink_target.blocks) - n))
            if not self.run_block_program(i, description, original=(self.shrink_target)):
                return

            def offset_left(k):
                return i - k * n

            i = offset_left(find_integer(lambda k: self.run_block_program((offset_left(k)),
              description, original=(self.shrink_target))))
            original = self.shrink_target
            find_integer(lambda k: self.run_block_program(i,
              description, original=original, repeats=k))

        run.__name__ = name
        defines_shrink_pass()(run)
        assert name in SHRINK_PASS_DEFINITIONS
    return name


@attr.s(slots=True, eq=False)
class ShrinkPass:
    run_with_chooser = attr.ib()
    index = attr.ib()
    shrinker = attr.ib()
    next_prefix = attr.ib(default=())
    fixed_point_at = attr.ib(default=None)
    successes = attr.ib(default=0)
    calls = attr.ib(default=0)
    shrinks = attr.ib(default=0)
    deletions = attr.ib(default=0)

    def step(self):
        if self.fixed_point_at is self.shrinker.shrink_target:
            return False
        tree = self.shrinker.shrink_pass_choice_trees[self]
        if tree.exhausted:
            return False
        initial_shrinks = self.shrinker.shrinks
        initial_calls = self.shrinker.calls
        size = len(self.shrinker.shrink_target.buffer)
        self.shrinker.explain_next_call_as(self.name)
        try:
            self.next_prefix = tree.stepself.next_prefix(lambda chooser: self.run_with_chooserself.shrinkerchooser)
        finally:
            self.calls += self.shrinker.calls - initial_calls
            self.shrinks += self.shrinker.shrinks - initial_shrinks
            self.deletions += size - len(self.shrinker.shrink_target.buffer)
            self.shrinker.clear_call_explanation()

        return True

    @property
    def name(self):
        return self.run_with_chooser.__name__


def non_zero_suffix(b):
    """Returns the longest suffix of b that starts with a non-zero
    byte."""
    i = 0
    while i < len(b):
        if b[i] == 0:
            i += 1

    return b[i:]


def expand_region(f, a, b):
    """Attempts to find u, v with u <= a, v >= b such that f(u, v) is true.
    Assumes that f(a, b) is already true.
    """
    b += find_integer(lambda k: f(a, b + k))
    a -= find_integer(lambda k: f(a - k, b))
    return (a, b)