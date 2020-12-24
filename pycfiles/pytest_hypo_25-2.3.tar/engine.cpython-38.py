# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\User\AppData\Local\Temp\pip-install-oj_abz_z\hypothesis\hypothesis\internal\conjecture\engine.py
# Compiled at: 2020-01-12 08:06:33
# Size of source mod 2**32: 40643 bytes
from collections import Counter, defaultdict
from enum import Enum
from random import Random, getrandbits
from weakref import WeakKeyDictionary
import attr
from hypothesis import HealthCheck, Phase, Verbosity, settings as Settings
from hypothesis._settings import local_settings
from hypothesis.internal.cache import LRUReusedCache
from hypothesis.internal.compat import ceil, int_from_bytes
from hypothesis.internal.conjecture.data import ConjectureData, ConjectureResult, DataObserver, Overrun, Status, StopTest
from hypothesis.internal.conjecture.datatree import DataTree, PreviouslyUnseenBehaviour, TreeRecordingObserver
from hypothesis.internal.conjecture.junkdrawer import clamp
from hypothesis.internal.conjecture.pareto import NO_SCORE, ParetoFront, ParetoOptimiser
from hypothesis.internal.conjecture.shrinker import Shrinker, sort_key
from hypothesis.internal.healthcheck import fail_health_check
from hypothesis.reporting import base_report
__tracebackhide__ = True
MAX_SHRINKS = 500
CACHE_SIZE = 10000
MUTATION_POOL_SIZE = 100
MIN_TEST_CALLS = 10
BUFFER_SIZE = 8192

@attr.s
class HealthCheckState:
    valid_examples = attr.ib(default=0)
    invalid_examples = attr.ib(default=0)
    overrun_examples = attr.ib(default=0)
    draw_times = attr.ib(default=(attr.Factory(list)))


class ExitReason(Enum):
    max_examples = 0
    max_iterations = 1
    max_shrinks = 3
    finished = 4
    flaky = 5


class RunIsComplete(Exception):
    pass


class ConjectureRunner:

    def __init__(self, test_function, settings=None, random=None, database_key=None):
        self._test_function = test_function
        self.settings = settings or Settings()
        self.shrinks = 0
        self.call_count = 0
        self.event_call_counts = Counter()
        self.valid_examples = 0
        self.random = random or Random(getrandbits(128))
        self.database_key = database_key
        self.status_runtimes = {}
        self.all_drawtimes = []
        self.all_runtimes = []
        self.events_to_strings = WeakKeyDictionary()
        self.interesting_examples = {}
        self.first_bug_found_at = None
        self.last_bug_found_at = None
        self.shrunk_examples = set()
        self.health_check_state = None
        self.tree = DataTree()
        self.best_observed_targets = defaultdict(lambda : NO_SCORE)
        self.best_examples_of_observed_targets = {}
        if self.database_key is not None and self.settings.database is not None:
            self.pareto_front = ParetoFront(self.random)
            self.pareto_front.on_evict(self.on_pareto_evict)
        else:
            self.pareto_front = None
        self._ConjectureRunner__data_cache = LRUReusedCache(CACHE_SIZE)

    @property
    def should_optimise(self):
        return Phase.target in self.settings.phases

    def __tree_is_exhausted(self):
        return self.tree.is_exhausted

    def __stoppable_test_function(self, data):
        """Run ``self._test_function``, but convert a ``StopTest`` exception
        into a normal return.
        """
        try:
            self._test_function(data)
        except StopTest as e:
            try:
                if e.testcounter == data.testcounter:
                    pass
                else:
                    raise
            finally:
                e = None
                del e

    def test_function(self, data):
        if not isinstance(data.observer, TreeRecordingObserver):
            raise AssertionError
        else:
            self.call_count += 1
            interrupted = False
            try:
                try:
                    self._ConjectureRunner__stoppable_test_function(data)
                except KeyboardInterrupt:
                    interrupted = True
                    raise
                except BaseException:
                    self.save_buffer(data.buffer)
                    raise

            finally:
                if not interrupted:
                    data.freeze()
                    self.note_details(data)

            self.debug_data(data)
            if self.pareto_front is not None:
                if self.pareto_front.add(data.as_result()):
                    self.save_buffer((data.buffer), sub_key=b'pareto')
            assert len(data.buffer) <= BUFFER_SIZE
            if data.status >= Status.VALID:
                for k, v in data.target_observations.items():
                    self.best_observed_targets[k] = max(self.best_observed_targets[k], v)
                    if k not in self.best_examples_of_observed_targets:
                        self.best_examples_of_observed_targets[k] = data.as_result()
                    else:
                        existing_example = self.best_examples_of_observed_targets[k]
                        existing_score = existing_example.target_observations[k]
                        if v < existing_score:
                            pass
                        elif v > existing_score or sort_key(data.buffer) < sort_key(existing_example.buffer):
                            self.best_examples_of_observed_targets[k] = data.as_result()

            if data.status == Status.VALID:
                self.valid_examples += 1
            if data.status == Status.INTERESTING:
                key = data.interesting_origin
                changed = False
                try:
                    existing = self.interesting_examples[key]
                except KeyError:
                    changed = True
                    self.last_bug_found_at = self.call_count
                    if self.first_bug_found_at is None:
                        self.first_bug_found_at = self.call_count
                else:
                    if sort_key(data.buffer) < sort_key(existing.buffer):
                        self.shrinks += 1
                        self.downgrade_buffer(existing.buffer)
                        self._ConjectureRunner__data_cache.unpin(existing.buffer)
                        changed = True
                    if changed:
                        self.save_buffer(data.buffer)
                        self.interesting_examples[key] = data.as_result()
                        self._ConjectureRunner__data_cache.pin(data.buffer)
                        self.shrunk_examples.discard(key)
                    if self.shrinks >= MAX_SHRINKS:
                        self.exit_with(ExitReason.max_shrinks)
            if not self.interesting_examples:
                if self.valid_examples >= self.settings.max_examples:
                    self.exit_with(ExitReason.max_examples)
                if self.call_count >= max(self.settings.max_examples * 10, 1000):
                    self.exit_with(ExitReason.max_iterations)
        if self._ConjectureRunner__tree_is_exhausted():
            self.exit_with(ExitReason.finished)
        self.record_for_health_check(data)

    def on_pareto_evict(self, data):
        self.settings.database.delete(self.pareto_key, data.buffer)

    def generate_novel_prefix(self):
        """Uses the tree to proactively generate a starting sequence of bytes
        that we haven't explored yet for this test.

        When this method is called, we assume that there must be at
        least one novel prefix left to find. If there were not, then the
        test run should have already stopped due to tree exhaustion.
        """
        return self.tree.generate_novel_prefix(self.random)

    def record_for_health_check(self, data):
        if data.status == Status.INTERESTING:
            self.health_check_state = None
        else:
            state = self.health_check_state
            if state is None:
                return
                state.draw_times.extend(data.draw_times)
                if data.status == Status.VALID:
                    state.valid_examples += 1
            elif data.status == Status.INVALID:
                state.invalid_examples += 1
            else:
                assert data.status == Status.OVERRUN
                state.overrun_examples += 1
        max_valid_draws = 10
        max_invalid_draws = 50
        max_overrun_draws = 20
        assert state.valid_examples <= max_valid_draws
        if state.valid_examples == max_valid_draws:
            self.health_check_state = None
            return
        if state.overrun_examples == max_overrun_draws:
            fail_health_check(self.settings, 'Examples routinely exceeded the max allowable size. (%d examples overran while generating %d valid ones). Generating examples this large will usually lead to bad results. You could try setting max_size parameters on your collections and turning max_leaves down on recursive() calls.' % (
             state.overrun_examples, state.valid_examples), HealthCheck.data_too_large)
        if state.invalid_examples == max_invalid_draws:
            fail_health_check(self.settings, 'It looks like your strategy is filtering out a lot of data. Health check found %d filtered examples but only %d good ones. This will make your tests much slower, and also will probably distort the data generation quite a lot. You should adapt your strategy to filter less. This can also be caused by a low max_leaves parameter in recursive() calls' % (
             state.invalid_examples, state.valid_examples), HealthCheck.filter_too_much)
        draw_time = sum(state.draw_times)
        if draw_time > 1.0:
            fail_health_check(self.settings, "Data generation is extremely slow: Only produced %d valid examples in %.2f seconds (%d invalid ones and %d exceeded maximum size). Try decreasing size of the data you're generating (with e.g.max_size or max_leaves parameters)." % (
             state.valid_examples,
             draw_time,
             state.invalid_examples,
             state.overrun_examples), HealthCheck.too_slow)

    def save_buffer(self, buffer, sub_key=None):
        if self.settings.database is not None:
            key = self.sub_key(sub_key)
            if key is None:
                return
            self.settings.database.save(key, bytes(buffer))

    def downgrade_buffer(self, buffer):
        if self.settings.database is not None:
            if self.database_key is not None:
                self.settings.database.move(self.database_key, self.secondary_key, buffer)

    def sub_key(self, sub_key):
        if self.database_key is None:
            return
        if sub_key is None:
            return self.database_key
        return (b'.').join((self.database_key, sub_key))

    @property
    def secondary_key(self):
        return self.sub_key(b'secondary')

    @property
    def pareto_key(self):
        return self.sub_key(b'pareto')

    def note_details(self, data):
        self._ConjectureRunner__data_cache[data.buffer] = data.as_result()
        runtime = max(data.finish_time - data.start_time, 0.0)
        self.all_runtimes.append(runtime)
        self.all_drawtimes.extend(data.draw_times)
        self.status_runtimes.setdefault(data.status, []).append(runtime)
        for event in set(map(self.event_to_string, data.events)):
            self.event_call_counts[event] += 1

    def debug(self, message):
        if self.settings.verbosity >= Verbosity.debug:
            base_report(message)

    @property
    def report_debug_info(self):
        return self.settings.verbosity >= Verbosity.debug

    def debug_data(self, data):
        if not self.report_debug_info:
            return
        stack = [[]]

        def go(ex):
            if ex.length == 0:
                return
            if len(ex.children) == 0:
                stack[(-1)].append(int_from_bytes(data.buffer[ex.start:ex.end]))
            else:
                node = []
                stack.append(node)
                for v in ex.children:
                    go(v)
                else:
                    stack.pop()
                    if len(node) == 1:
                        stack[(-1)].extend(node)
                    else:
                        stack[(-1)].append(node)

        go(data.examples[0])
        assert len(stack) == 1
        status = repr(data.status)
        if data.status == Status.INTERESTING:
            status = '%s (%r)' % (status, data.interesting_origin)
        self.debug('%d bytes %r -> %s, %s' % (data.index, stack[0], status, data.output))

    def run(self):
        with local_settings(self.settings):
            try:
                self._run()
            except RunIsComplete:
                pass
            else:
                for v in self.interesting_examples.values():
                    self.debug_data(v)
                else:
                    self.debug('Run complete after %d examples (%d valid) and %d shrinks' % (
                     self.call_count, self.valid_examples, self.shrinks))

    @property
    def database(self):
        if self.database_key is None:
            return
        return self.settings.database

    def has_existing_examples(self):
        return self.database is not None and Phase.reuse in self.settings.phases

    def reuse_existing_examples(self):
        """If appropriate (we have a database and have been told to use it),
        try to reload existing examples from the database.

        If there are a lot we don't try all of them. We always try the
        smallest example in the database (which is guaranteed to be the
        last failure) and the largest (which is usually the seed example
        which the last failure came from but we don't enforce that). We
        then take a random sampling of the remainder and try those. Any
        examples that are no longer interesting are cleared out.
        """
        if self.has_existing_examples():
            self.debug('Reusing examples from database')
            corpus = sorted((self.settings.database.fetch(self.database_key)),
              key=sort_key)
            desired_size = max(2, ceil(0.1 * self.settings.max_examples))
            if len(corpus) < desired_size:
                extra_corpus = list(self.settings.database.fetch(self.secondary_key))
                shortfall = desired_size - len(corpus)
                if len(extra_corpus) <= shortfall:
                    extra = extra_corpus
                else:
                    extra = self.random.sample(extra_corpus, shortfall)
                extra.sort(key=sort_key)
                corpus.extend(extra)
            for existing in corpus:
                data = self.cached_test_function(existing)
                if data.status != Status.INTERESTING:
                    self.settings.database.delete(self.database_key, existing)
                    self.settings.database.delete(self.secondary_key, existing)

            if len(corpus) < desired_size:
                if not self.interesting_examples:
                    desired_extra = desired_size - len(corpus)
                    pareto_corpus = list(self.settings.database.fetch(self.pareto_key))
                    if len(pareto_corpus) > desired_extra:
                        pareto_corpus = self.random.sample(pareto_corpus, desired_extra)
                    pareto_corpus.sort(key=sort_key)
                    for existing in pareto_corpus:
                        data = self.cached_test_function(existing)
                        if data not in self.pareto_front:
                            self.settings.database.delete(self.pareto_key, existing)
                        if data.status == Status.INTERESTING:
                            break

    def exit_with(self, reason):
        self.debug('exit_with(%s)' % (reason.name,))
        self.exit_reason = reason
        raise RunIsComplete()

    def generate_new_examples--- This code section failed: ---

 L. 509         0  LOAD_GLOBAL              Phase
                2  LOAD_ATTR                generate
                4  LOAD_DEREF               'self'
                6  LOAD_ATTR                settings
                8  LOAD_ATTR                phases
               10  COMPARE_OP               not-in
               12  POP_JUMP_IF_FALSE    18  'to 18'

 L. 510        14  LOAD_CONST               None
               16  RETURN_VALUE     
             18_0  COME_FROM            12  '12'

 L. 511        18  LOAD_DEREF               'self'
               20  LOAD_ATTR                interesting_examples
               22  POP_JUMP_IF_FALSE    28  'to 28'

 L. 515        24  LOAD_CONST               None
               26  RETURN_VALUE     
             28_0  COME_FROM            22  '22'

 L. 517        28  LOAD_DEREF               'self'
               30  LOAD_METHOD              debug
               32  LOAD_STR                 'Generating new examples'
               34  CALL_METHOD_1         1  ''
               36  POP_TOP          

 L. 519        38  LOAD_DEREF               'self'
               40  LOAD_METHOD              cached_test_function
               42  LOAD_GLOBAL              bytes
               44  LOAD_GLOBAL              BUFFER_SIZE
               46  CALL_FUNCTION_1       1  ''
               48  CALL_METHOD_1         1  ''
               50  STORE_FAST               'zero_data'

 L. 520        52  LOAD_FAST                'zero_data'
               54  LOAD_ATTR                status
               56  LOAD_GLOBAL              Status
               58  LOAD_ATTR                OVERRUN
               60  COMPARE_OP               >
               62  POP_JUMP_IF_FALSE    78  'to 78'

 L. 521        64  LOAD_DEREF               'self'
               66  LOAD_ATTR                _ConjectureRunner__data_cache
               68  LOAD_METHOD              pin
               70  LOAD_FAST                'zero_data'
               72  LOAD_ATTR                buffer
               74  CALL_METHOD_1         1  ''
               76  POP_TOP          
             78_0  COME_FROM            62  '62'

 L. 523        78  LOAD_FAST                'zero_data'
               80  LOAD_ATTR                status
               82  LOAD_GLOBAL              Status
               84  LOAD_ATTR                OVERRUN
               86  COMPARE_OP               ==
               88  POP_JUMP_IF_TRUE    120  'to 120'

 L. 524        90  LOAD_FAST                'zero_data'
               92  LOAD_ATTR                status
               94  LOAD_GLOBAL              Status
               96  LOAD_ATTR                VALID
               98  COMPARE_OP               ==

 L. 523       100  POP_JUMP_IF_FALSE   136  'to 136'

 L. 524       102  LOAD_GLOBAL              len
              104  LOAD_FAST                'zero_data'
              106  LOAD_ATTR                buffer
              108  CALL_FUNCTION_1       1  ''
              110  LOAD_CONST               2
              112  BINARY_MULTIPLY  
              114  LOAD_GLOBAL              BUFFER_SIZE
              116  COMPARE_OP               >

 L. 523       118  POP_JUMP_IF_FALSE   136  'to 136'
            120_0  COME_FROM            88  '88'

 L. 526       120  LOAD_GLOBAL              fail_health_check

 L. 527       122  LOAD_DEREF               'self'
              124  LOAD_ATTR                settings

 L. 528       126  LOAD_STR                 'The smallest natural example for your test is extremely large. This makes it difficult for Hypothesis to generate good examples, especially when trying to reduce failing ones at the end. Consider reducing the size of your data if it is of a fixed size. You could also fix this by improving how your data shrinks (see https://hypothesis.readthedocs.io/en/latest/data.html#shrinking for details), or by introducing default values inside your strategy. e.g. could you replace some arguments with their defaults by using one_of(none(), some_complex_strategy)?'

 L. 538       128  LOAD_GLOBAL              HealthCheck
              130  LOAD_ATTR                large_base_example

 L. 526       132  CALL_FUNCTION_3       3  ''
              134  POP_TOP          
            136_0  COME_FROM           118  '118'
            136_1  COME_FROM           100  '100'

 L. 541       136  LOAD_GLOBAL              HealthCheckState
              138  CALL_FUNCTION_0       0  ''
              140  LOAD_DEREF               'self'
              142  STORE_ATTR               health_check_state

 L. 543       144  LOAD_CLOSURE             'self'
              146  BUILD_TUPLE_1         1 
              148  LOAD_CODE                <code_object should_generate_more>
              150  LOAD_STR                 'ConjectureRunner.generate_new_examples.<locals>.should_generate_more'
              152  MAKE_FUNCTION_8          'closure'
              154  STORE_FAST               'should_generate_more'

 L. 586       156  LOAD_CONST               0
              158  STORE_FAST               'consecutive_zero_extend_is_invalid'

 L. 606       160  LOAD_GLOBAL              clamp
              162  LOAD_CONST               10
              164  LOAD_DEREF               'self'
              166  LOAD_ATTR                settings
              168  LOAD_ATTR                max_examples
              170  LOAD_CONST               10
              172  BINARY_FLOOR_DIVIDE
              174  LOAD_CONST               50
              176  CALL_FUNCTION_3       3  ''
              178  STORE_FAST               'small_example_cap'

 L. 608       180  LOAD_GLOBAL              max
              182  LOAD_DEREF               'self'
              184  LOAD_ATTR                settings
              186  LOAD_ATTR                max_examples
              188  LOAD_CONST               2
              190  BINARY_FLOOR_DIVIDE
              192  LOAD_FAST                'small_example_cap'
              194  LOAD_CONST               1
              196  BINARY_ADD       
              198  CALL_FUNCTION_2       2  ''
              200  STORE_FAST               'optimise_at'

 L. 609       202  LOAD_CONST               False
              204  STORE_FAST               'ran_optimisations'
            206_0  COME_FROM           942  '942'
            206_1  COME_FROM           938  '938'

 L. 611       206  LOAD_FAST                'should_generate_more'
              208  CALL_FUNCTION_0       0  ''
          210_212  POP_JUMP_IF_FALSE   958  'to 958'

 L. 612       214  LOAD_DEREF               'self'
              216  LOAD_METHOD              generate_novel_prefix
              218  CALL_METHOD_0         0  ''
              220  STORE_FAST               'prefix'

 L. 613       222  LOAD_GLOBAL              len
              224  LOAD_FAST                'prefix'
              226  CALL_FUNCTION_1       1  ''
              228  LOAD_GLOBAL              BUFFER_SIZE
              230  COMPARE_OP               <=
              232  POP_JUMP_IF_TRUE    238  'to 238'
              234  LOAD_ASSERT              AssertionError
              236  RAISE_VARARGS_1       1  'exception instance'
            238_0  COME_FROM           232  '232'

 L. 615       238  LOAD_DEREF               'self'
              240  LOAD_ATTR                valid_examples
              242  LOAD_FAST                'small_example_cap'
              244  COMPARE_OP               <=

 L. 614   246_248  POP_JUMP_IF_FALSE   468  'to 468'

 L. 616       250  LOAD_DEREF               'self'
              252  LOAD_ATTR                call_count
              254  LOAD_CONST               5
              256  LOAD_FAST                'small_example_cap'
              258  BINARY_MULTIPLY  
              260  COMPARE_OP               <=

 L. 614   262_264  POP_JUMP_IF_FALSE   468  'to 468'

 L. 617       266  LOAD_DEREF               'self'
              268  LOAD_ATTR                interesting_examples

 L. 614   270_272  POP_JUMP_IF_TRUE    468  'to 468'

 L. 618       274  LOAD_FAST                'consecutive_zero_extend_is_invalid'
              276  LOAD_CONST               5
              278  COMPARE_OP               <

 L. 614   280_282  POP_JUMP_IF_FALSE   468  'to 468'

 L. 620       284  LOAD_DEREF               'self'
              286  LOAD_METHOD              cached_test_function

 L. 621       288  LOAD_FAST                'prefix'
              290  LOAD_GLOBAL              bytes
              292  LOAD_GLOBAL              BUFFER_SIZE
              294  LOAD_GLOBAL              len
              296  LOAD_FAST                'prefix'
              298  CALL_FUNCTION_1       1  ''
              300  BINARY_SUBTRACT  
              302  CALL_FUNCTION_1       1  ''
              304  BINARY_ADD       

 L. 620       306  CALL_METHOD_1         1  ''
              308  STORE_FAST               'minimal_example'

 L. 624       310  LOAD_FAST                'minimal_example'
              312  LOAD_ATTR                status
              314  LOAD_GLOBAL              Status
              316  LOAD_ATTR                VALID
              318  COMPARE_OP               <
          320_322  POP_JUMP_IF_FALSE   334  'to 334'

 L. 625       324  LOAD_FAST                'consecutive_zero_extend_is_invalid'
              326  LOAD_CONST               1
              328  INPLACE_ADD      
              330  STORE_FAST               'consecutive_zero_extend_is_invalid'

 L. 626       332  JUMP_BACK           206  'to 206'
            334_0  COME_FROM           320  '320'

 L. 628       334  LOAD_CONST               0
              336  STORE_FAST               'consecutive_zero_extend_is_invalid'

 L. 630       338  LOAD_GLOBAL              len
              340  LOAD_FAST                'minimal_example'
              342  LOAD_ATTR                buffer
              344  CALL_FUNCTION_1       1  ''
              346  LOAD_GLOBAL              len
              348  LOAD_FAST                'prefix'
              350  CALL_FUNCTION_1       1  ''
              352  BINARY_SUBTRACT  
              354  STORE_FAST               'minimal_extension'

 L. 632       356  LOAD_GLOBAL              min
              358  LOAD_GLOBAL              len
              360  LOAD_FAST                'prefix'
              362  CALL_FUNCTION_1       1  ''
              364  LOAD_FAST                'minimal_extension'
              366  LOAD_CONST               10
              368  BINARY_MULTIPLY  
              370  BINARY_ADD       
              372  LOAD_GLOBAL              BUFFER_SIZE
              374  CALL_FUNCTION_2       2  ''
              376  STORE_FAST               'max_length'

 L. 642       378  SETUP_FINALLY       414  'to 414'

 L. 643       380  LOAD_DEREF               'self'
              382  LOAD_ATTR                new_conjecture_data

 L. 644       384  LOAD_FAST                'prefix'

 L. 644       386  LOAD_FAST                'max_length'

 L. 643       388  LOAD_CONST               ('prefix', 'max_length')
              390  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              392  STORE_FAST               'trial_data'

 L. 646       394  LOAD_DEREF               'self'
              396  LOAD_ATTR                tree
              398  LOAD_METHOD              simulate_test_function
              400  LOAD_FAST                'trial_data'
              402  CALL_METHOD_1         1  ''
              404  POP_TOP          

 L. 647       406  POP_BLOCK        
              408  JUMP_BACK           206  'to 206'
              410  POP_BLOCK        
              412  JUMP_FORWARD        436  'to 436'
            414_0  COME_FROM_FINALLY   378  '378'

 L. 648       414  DUP_TOP          
              416  LOAD_GLOBAL              PreviouslyUnseenBehaviour
              418  COMPARE_OP               exception-match
          420_422  POP_JUMP_IF_FALSE   434  'to 434'
              424  POP_TOP          
              426  POP_TOP          
              428  POP_TOP          

 L. 649       430  POP_EXCEPT       
              432  JUMP_FORWARD        436  'to 436'
            434_0  COME_FROM           420  '420'
              434  END_FINALLY      
            436_0  COME_FROM           432  '432'
            436_1  COME_FROM           412  '412'

 L. 653       436  LOAD_FAST                'trial_data'
              438  LOAD_ATTR                observer
              440  LOAD_ATTR                killed
          442_444  POP_JUMP_IF_FALSE   448  'to 448'

 L. 654       446  JUMP_BACK           206  'to 206'
            448_0  COME_FROM           442  '442'

 L. 658       448  LOAD_FAST                'should_generate_more'
              450  CALL_FUNCTION_0       0  ''
          452_454  POP_JUMP_IF_TRUE    460  'to 460'

 L. 659   456_458  BREAK_LOOP          958  'to 958'
            460_0  COME_FROM           452  '452'

 L. 661       460  LOAD_FAST                'trial_data'
              462  LOAD_ATTR                buffer
              464  STORE_FAST               'prefix'
              466  JUMP_FORWARD        472  'to 472'
            468_0  COME_FROM           280  '280'
            468_1  COME_FROM           270  '270'
            468_2  COME_FROM           262  '262'
            468_3  COME_FROM           246  '246'

 L. 663       468  LOAD_GLOBAL              BUFFER_SIZE
              470  STORE_FAST               'max_length'
            472_0  COME_FROM           466  '466'

 L. 665       472  LOAD_DEREF               'self'
              474  LOAD_ATTR                new_conjecture_data
              476  LOAD_FAST                'prefix'
              478  LOAD_FAST                'max_length'
              480  LOAD_CONST               ('prefix', 'max_length')
              482  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              484  STORE_DEREF              'data'

 L. 667       486  LOAD_DEREF               'self'
              488  LOAD_METHOD              test_function
              490  LOAD_DEREF               'data'
              492  CALL_METHOD_1         1  ''
              494  POP_TOP          

 L. 682       496  LOAD_DEREF               'data'
              498  LOAD_ATTR                status
              500  LOAD_GLOBAL              Status
              502  LOAD_ATTR                INVALID
              504  COMPARE_OP               >=

 L. 679   506_508  POP_JUMP_IF_FALSE   924  'to 924'

 L. 686       510  LOAD_DEREF               'self'
              512  LOAD_ATTR                health_check_state
              514  LOAD_CONST               None
              516  COMPARE_OP               is

 L. 679   518_520  POP_JUMP_IF_FALSE   924  'to 924'

 L. 688       522  LOAD_DEREF               'self'
              524  LOAD_ATTR                call_count
              526  STORE_FAST               'initial_calls'

 L. 689       528  LOAD_CONST               0
              530  STORE_FAST               'failed_mutations'

 L. 691       532  LOAD_FAST                'should_generate_more'
              534  CALL_FUNCTION_0       0  ''

 L. 690   536_538  POP_JUMP_IF_FALSE   924  'to 924'

 L. 695       540  LOAD_DEREF               'self'
              542  LOAD_ATTR                call_count
              544  LOAD_FAST                'initial_calls'
              546  LOAD_CONST               5
              548  BINARY_ADD       
              550  COMPARE_OP               <=

 L. 690   552_554  POP_JUMP_IF_FALSE   924  'to 924'

 L. 696       556  LOAD_FAST                'failed_mutations'
              558  LOAD_CONST               5
              560  COMPARE_OP               <=

 L. 690   562_564  POP_JUMP_IF_FALSE   924  'to 924'

 L. 698       566  LOAD_GLOBAL              defaultdict
              568  LOAD_GLOBAL              list
              570  CALL_FUNCTION_1       1  ''
              572  STORE_FAST               'groups'

 L. 699       574  LOAD_DEREF               'data'
              576  LOAD_ATTR                examples
              578  GET_ITER         
              580  FOR_ITER            610  'to 610'
              582  STORE_FAST               'ex'

 L. 700       584  LOAD_FAST                'groups'
              586  LOAD_FAST                'ex'
              588  LOAD_ATTR                label
              590  LOAD_FAST                'ex'
              592  LOAD_ATTR                depth
              594  BUILD_TUPLE_2         2 
              596  BINARY_SUBSCR    
              598  LOAD_METHOD              append
              600  LOAD_FAST                'ex'
              602  CALL_METHOD_1         1  ''
              604  POP_TOP          
          606_608  JUMP_BACK           580  'to 580'

 L. 702       610  LOAD_LISTCOMP            '<code_object <listcomp>>'
              612  LOAD_STR                 'ConjectureRunner.generate_new_examples.<locals>.<listcomp>'
              614  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              616  LOAD_FAST                'groups'
              618  LOAD_METHOD              values
              620  CALL_METHOD_0         0  ''
              622  GET_ITER         
              624  CALL_FUNCTION_1       1  ''
              626  STORE_FAST               'groups'

 L. 704       628  LOAD_FAST                'groups'
          630_632  POP_JUMP_IF_TRUE    638  'to 638'

 L. 705   634_636  BREAK_LOOP          924  'to 924'
            638_0  COME_FROM           630  '630'

 L. 707       638  LOAD_DEREF               'self'
              640  LOAD_ATTR                random
              642  LOAD_METHOD              choice
              644  LOAD_FAST                'groups'
              646  CALL_METHOD_1         1  ''
              648  STORE_FAST               'group'

 L. 709       650  LOAD_GLOBAL              sorted

 L. 710       652  LOAD_DEREF               'self'
              654  LOAD_ATTR                random
              656  LOAD_METHOD              sample
              658  LOAD_FAST                'group'
              660  LOAD_CONST               2
              662  CALL_METHOD_2         2  ''

 L. 710       664  LOAD_LAMBDA              '<code_object <lambda>>'
              666  LOAD_STR                 'ConjectureRunner.generate_new_examples.<locals>.<lambda>'
              668  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'

 L. 709       670  LOAD_CONST               ('key',)
              672  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              674  UNPACK_SEQUENCE_2     2 
              676  STORE_FAST               'ex1'
              678  STORE_FAST               'ex2'

 L. 712       680  LOAD_FAST                'ex1'
              682  LOAD_ATTR                end
              684  LOAD_FAST                'ex2'
              686  LOAD_ATTR                start
              688  COMPARE_OP               <=
          690_692  POP_JUMP_IF_TRUE    698  'to 698'
              694  LOAD_ASSERT              AssertionError
              696  RAISE_VARARGS_1       1  'exception instance'
            698_0  COME_FROM           690  '690'

 L. 714       698  LOAD_CLOSURE             'data'
              700  BUILD_TUPLE_1         1 
              702  LOAD_LISTCOMP            '<code_object <listcomp>>'
              704  LOAD_STR                 'ConjectureRunner.generate_new_examples.<locals>.<listcomp>'
              706  MAKE_FUNCTION_8          'closure'
              708  LOAD_FAST                'ex1'
              710  LOAD_FAST                'ex2'
              712  BUILD_TUPLE_2         2 
              714  GET_ITER         
              716  CALL_FUNCTION_1       1  ''
              718  STORE_FAST               'replacements'

 L. 716       720  LOAD_DEREF               'self'
              722  LOAD_ATTR                random
              724  LOAD_METHOD              choice
              726  LOAD_FAST                'replacements'
              728  CALL_METHOD_1         1  ''
              730  STORE_FAST               'replacement'

 L. 718       732  SETUP_FINALLY       808  'to 808'

 L. 727       734  LOAD_DEREF               'self'
              736  LOAD_ATTR                cached_test_function

 L. 728       738  LOAD_DEREF               'data'
              740  LOAD_ATTR                buffer
              742  LOAD_CONST               None
              744  LOAD_FAST                'ex1'
              746  LOAD_ATTR                start
              748  BUILD_SLICE_2         2 
              750  BINARY_SUBSCR    

 L. 729       752  LOAD_FAST                'replacement'

 L. 728       754  BINARY_ADD       

 L. 730       756  LOAD_DEREF               'data'
              758  LOAD_ATTR                buffer
              760  LOAD_FAST                'ex1'
              762  LOAD_ATTR                end
              764  LOAD_FAST                'ex2'
              766  LOAD_ATTR                start
              768  BUILD_SLICE_2         2 
              770  BINARY_SUBSCR    

 L. 728       772  BINARY_ADD       

 L. 731       774  LOAD_FAST                'replacement'

 L. 728       776  BINARY_ADD       

 L. 732       778  LOAD_DEREF               'data'
              780  LOAD_ATTR                buffer
              782  LOAD_FAST                'ex2'
              784  LOAD_ATTR                end
              786  LOAD_CONST               None
              788  BUILD_SLICE_2         2 
              790  BINARY_SUBSCR    

 L. 728       792  BINARY_ADD       

 L. 736       794  LOAD_CONST               True

 L. 737       796  LOAD_GLOBAL              BUFFER_SIZE

 L. 727       798  LOAD_CONST               ('error_on_discard', 'extend')
              800  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              802  STORE_DEREF              'new_data'
              804  POP_BLOCK        
              806  JUMP_FORWARD        844  'to 844'
            808_0  COME_FROM_FINALLY   732  '732'

 L. 739       808  DUP_TOP          
              810  LOAD_GLOBAL              ContainsDiscard
              812  COMPARE_OP               exception-match
          814_816  POP_JUMP_IF_FALSE   842  'to 842'
              818  POP_TOP          
              820  POP_TOP          
              822  POP_TOP          

 L. 740       824  LOAD_FAST                'failed_mutations'
              826  LOAD_CONST               1
              828  INPLACE_ADD      
              830  STORE_FAST               'failed_mutations'

 L. 741       832  POP_EXCEPT       
          834_836  JUMP_BACK           532  'to 532'
              838  POP_EXCEPT       
              840  JUMP_FORWARD        844  'to 844'
            842_0  COME_FROM           814  '814'
              842  END_FINALLY      
            844_0  COME_FROM           840  '840'
            844_1  COME_FROM           806  '806'

 L. 744       844  LOAD_DEREF               'new_data'
              846  LOAD_ATTR                status
              848  LOAD_DEREF               'data'
              850  LOAD_ATTR                status
              852  COMPARE_OP               >=

 L. 743   854_856  POP_JUMP_IF_FALSE   912  'to 912'

 L. 745       858  LOAD_DEREF               'data'
              860  LOAD_ATTR                buffer
              862  LOAD_DEREF               'new_data'
              864  LOAD_ATTR                buffer
              866  COMPARE_OP               !=

 L. 743   868_870  POP_JUMP_IF_FALSE   912  'to 912'

 L. 746       872  LOAD_GLOBAL              all
              874  LOAD_CLOSURE             'new_data'
              876  BUILD_TUPLE_1         1 
              878  LOAD_GENEXPR             '<code_object <genexpr>>'
              880  LOAD_STR                 'ConjectureRunner.generate_new_examples.<locals>.<genexpr>'
              882  MAKE_FUNCTION_8          'closure'

 L. 749       884  LOAD_DEREF               'data'
              886  LOAD_ATTR                target_observations
              888  LOAD_METHOD              items
              890  CALL_METHOD_0         0  ''

 L. 746       892  GET_ITER         
              894  CALL_FUNCTION_1       1  ''
              896  CALL_FUNCTION_1       1  ''

 L. 743   898_900  POP_JUMP_IF_FALSE   912  'to 912'

 L. 752       902  LOAD_DEREF               'new_data'
              904  STORE_DEREF              'data'

 L. 753       906  LOAD_CONST               0
              908  STORE_FAST               'failed_mutations'
              910  JUMP_BACK           532  'to 532'
            912_0  COME_FROM           898  '898'
            912_1  COME_FROM           868  '868'
            912_2  COME_FROM           854  '854'

 L. 755       912  LOAD_FAST                'failed_mutations'
              914  LOAD_CONST               1
              916  INPLACE_ADD      
              918  STORE_FAST               'failed_mutations'
          920_922  JUMP_BACK           532  'to 532'
            924_0  COME_FROM           562  '562'
            924_1  COME_FROM           552  '552'
            924_2  COME_FROM           536  '536'
            924_3  COME_FROM           518  '518'
            924_4  COME_FROM           506  '506'

 L. 764       924  LOAD_DEREF               'self'
              926  LOAD_ATTR                valid_examples
              928  LOAD_GLOBAL              max
              930  LOAD_FAST                'small_example_cap'
              932  LOAD_FAST                'optimise_at'
              934  CALL_FUNCTION_2       2  ''
              936  COMPARE_OP               >=

 L. 763       938  POP_JUMP_IF_FALSE   206  'to 206'

 L. 765       940  LOAD_FAST                'ran_optimisations'

 L. 763       942  POP_JUMP_IF_TRUE    206  'to 206'

 L. 767       944  LOAD_CONST               True
              946  STORE_FAST               'ran_optimisations'

 L. 768       948  LOAD_DEREF               'self'
              950  LOAD_METHOD              optimise_targets
              952  CALL_METHOD_0         0  ''
              954  POP_TOP          
              956  JUMP_BACK           206  'to 206'
            958_0  COME_FROM           210  '210'

Parse error at or near `POP_BLOCK' instruction at offset 410

    def optimise_targets(self):
        """If any target observations have been made, attempt to optimise them
        all."""
        if not self.should_optimise:
            return
        else:
            from hypothesis.internal.conjecture.optimiser import Optimiser
            max_improvements = 10
        prev_calls = self.call_count
        any_improvements = False
        for target, data in list(self.best_examples_of_observed_targets.items()):
            optimiser = Optimiser(self,
              data, target, max_improvements=max_improvements)
            optimiser.run()
            if optimiser.improvements > 0:
                any_improvements = True
            if self.interesting_examples:
                break
            max_improvements *= 2
            if any_improvements:
                pass
            else:
                self.pareto_optimise()
                if prev_calls == self.call_count:
                    break

    def pareto_optimise(self):
        if self.pareto_front is not None:
            ParetoOptimiser(self).run()

    def _run(self):
        self.reuse_existing_examples()
        self.generate_new_examples()
        if Phase.generate not in self.settings.phases:
            self.optimise_targets()
        self.shrink_interesting_examples()
        self.exit_with(ExitReason.finished)

    def new_conjecture_data(self, prefix, max_length=BUFFER_SIZE, observer=None):
        return ConjectureData(prefix=prefix,
          max_length=max_length,
          random=(self.random),
          observer=(observer or self.tree.new_observer()))

    def new_conjecture_data_for_buffer(self, buffer):
        return ConjectureData.for_buffer(buffer, observer=(self.tree.new_observer()))

    def shrink_interesting_examples(self):
        """If we've found interesting examples, try to replace each of them
        with a minimal interesting example with the same interesting_origin.

        We may find one or more examples with a new interesting_origin
        during the shrink process. If so we shrink these too.
        """
        if not Phase.shrink not in self.settings.phases:
            if not self.interesting_examples:
                return
            self.debug('Shrinking interesting examples')
            for prev_data in sorted((self.interesting_examples.values()),
              key=(lambda d: sort_key(d.buffer))):
                assert prev_data.status == Status.INTERESTING

        else:
            data = self.new_conjecture_data_for_buffer(prev_data.buffer)
            self.test_function(data)
            if data.status != Status.INTERESTING:
                self.exit_with(ExitReason.flaky)
            self.clear_secondary_key()
            while True:
                if len(self.shrunk_examples) < len(self.interesting_examples):
                    target, example = min(((
                     k, v) for k, v in self.interesting_examples.items() if k not in self.shrunk_examples),
                      key=(lambda kv: (
                     sort_key(kv[1].buffer), sort_key(repr(kv[0])))))
                    self.debug('Shrinking %r' % (target,))
                    if not self.settings.report_multiple_bugs:
                        self.shrink(example, lambda d: d.status == Status.INTERESTING)
                        return None

                    def predicate(d):
                        if d.status < Status.INTERESTING:
                            return False
                        return d.interesting_origin == target

                    self.shrink(example, predicate)
                    self.shrunk_examples.add(target)

    def clear_secondary_key(self):
        if self.has_existing_examples():
            corpus = sorted((self.settings.database.fetch(self.secondary_key)),
              key=sort_key)
            for c in corpus:
                primary = {v.buffer for v in self.interesting_examples.values()}
                cap = max(map(sort_key, primary))
                if sort_key(c) > cap:
                    break
                else:
                    self.cached_test_function(c)
                    self.settings.database.delete(self.secondary_key, c)

    def shrink(self, example, predicate):
        s = self.new_shrinker(example, predicate)
        s.shrink()
        return s.shrink_target

    def new_shrinker(self, example, predicate):
        return Shrinker(self, example, predicate)

    def cached_test_function--- This code section failed: ---

 L. 933         0  LOAD_GLOBAL              bytes
                2  LOAD_FAST                'buffer'
                4  CALL_FUNCTION_1       1  ''
                6  LOAD_CONST               None
                8  LOAD_GLOBAL              BUFFER_SIZE
               10  BUILD_SLICE_2         2 
               12  BINARY_SUBSCR    
               14  STORE_FAST               'buffer'

 L. 935        16  LOAD_GLOBAL              min
               18  LOAD_GLOBAL              BUFFER_SIZE
               20  LOAD_GLOBAL              len
               22  LOAD_FAST                'buffer'
               24  CALL_FUNCTION_1       1  ''
               26  LOAD_FAST                'extend'
               28  BINARY_ADD       
               30  CALL_FUNCTION_2       2  ''
               32  STORE_FAST               'max_length'

 L. 937        34  LOAD_CODE                <code_object check_result>
               36  LOAD_STR                 'ConjectureRunner.cached_test_function.<locals>.check_result'
               38  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
               40  STORE_FAST               'check_result'

 L. 943        42  SETUP_FINALLY        60  'to 60'

 L. 944        44  LOAD_FAST                'check_result'
               46  LOAD_FAST                'self'
               48  LOAD_ATTR                _ConjectureRunner__data_cache
               50  LOAD_FAST                'buffer'
               52  BINARY_SUBSCR    
               54  CALL_FUNCTION_1       1  ''
               56  POP_BLOCK        
               58  RETURN_VALUE     
             60_0  COME_FROM_FINALLY    42  '42'

 L. 945        60  DUP_TOP          
               62  LOAD_GLOBAL              KeyError
               64  COMPARE_OP               exception-match
               66  POP_JUMP_IF_FALSE    78  'to 78'
               68  POP_TOP          
               70  POP_TOP          
               72  POP_TOP          

 L. 946        74  POP_EXCEPT       
               76  JUMP_FORWARD         80  'to 80'
             78_0  COME_FROM            66  '66'
               78  END_FINALLY      
             80_0  COME_FROM            76  '76'

 L. 948        80  LOAD_FAST                'error_on_discard'
               82  POP_JUMP_IF_FALSE   108  'to 108'

 L. 950        84  LOAD_BUILD_CLASS 
               86  LOAD_CODE                <code_object DiscardObserver>
               88  LOAD_STR                 'DiscardObserver'
               90  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
               92  LOAD_STR                 'DiscardObserver'
               94  LOAD_GLOBAL              DataObserver
               96  CALL_FUNCTION_3       3  ''
               98  STORE_FAST               'DiscardObserver'

 L. 954       100  LOAD_FAST                'DiscardObserver'
              102  CALL_FUNCTION_0       0  ''
              104  STORE_FAST               'observer'
              106  JUMP_FORWARD        114  'to 114'
            108_0  COME_FROM            82  '82'

 L. 956       108  LOAD_GLOBAL              DataObserver
              110  CALL_FUNCTION_0       0  ''
              112  STORE_FAST               'observer'
            114_0  COME_FROM           106  '106'

 L. 958       114  LOAD_FAST                'self'
              116  LOAD_ATTR                new_conjecture_data

 L. 959       118  LOAD_FAST                'buffer'

 L. 959       120  LOAD_FAST                'max_length'

 L. 959       122  LOAD_FAST                'observer'

 L. 958       124  LOAD_CONST               ('prefix', 'max_length', 'observer')
              126  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              128  STORE_FAST               'dummy_data'

 L. 962       130  SETUP_FINALLY       148  'to 148'

 L. 963       132  LOAD_FAST                'self'
              134  LOAD_ATTR                tree
              136  LOAD_METHOD              simulate_test_function
              138  LOAD_FAST                'dummy_data'
              140  CALL_METHOD_1         1  ''
              142  POP_TOP          
              144  POP_BLOCK        
              146  JUMP_FORWARD        168  'to 168'
            148_0  COME_FROM_FINALLY   130  '130'

 L. 964       148  DUP_TOP          
              150  LOAD_GLOBAL              PreviouslyUnseenBehaviour
              152  COMPARE_OP               exception-match
              154  POP_JUMP_IF_FALSE   166  'to 166'
              156  POP_TOP          
              158  POP_TOP          
              160  POP_TOP          

 L. 965       162  POP_EXCEPT       
              164  JUMP_FORWARD        240  'to 240'
            166_0  COME_FROM           154  '154'
              166  END_FINALLY      
            168_0  COME_FROM           146  '146'

 L. 967       168  LOAD_FAST                'dummy_data'
              170  LOAD_ATTR                status
              172  LOAD_GLOBAL              Status
              174  LOAD_ATTR                OVERRUN
              176  COMPARE_OP               >
              178  POP_JUMP_IF_FALSE   226  'to 226'

 L. 968       180  LOAD_FAST                'dummy_data'
              182  LOAD_METHOD              freeze
              184  CALL_METHOD_0         0  ''
              186  POP_TOP          

 L. 969       188  SETUP_FINALLY       204  'to 204'

 L. 970       190  LOAD_FAST                'self'
              192  LOAD_ATTR                _ConjectureRunner__data_cache
              194  LOAD_FAST                'dummy_data'
              196  LOAD_ATTR                buffer
              198  BINARY_SUBSCR    
              200  POP_BLOCK        
              202  RETURN_VALUE     
            204_0  COME_FROM_FINALLY   188  '188'

 L. 971       204  DUP_TOP          
              206  LOAD_GLOBAL              KeyError
              208  COMPARE_OP               exception-match
              210  POP_JUMP_IF_FALSE   222  'to 222'
              212  POP_TOP          
              214  POP_TOP          
              216  POP_TOP          

 L. 972       218  POP_EXCEPT       
              220  JUMP_ABSOLUTE       240  'to 240'
            222_0  COME_FROM           210  '210'
              222  END_FINALLY      
              224  JUMP_FORWARD        240  'to 240'
            226_0  COME_FROM           178  '178'

 L. 974       226  LOAD_GLOBAL              Overrun
              228  LOAD_FAST                'self'
              230  LOAD_ATTR                _ConjectureRunner__data_cache
              232  LOAD_FAST                'buffer'
              234  STORE_SUBSCR     

 L. 975       236  LOAD_GLOBAL              Overrun
              238  RETURN_VALUE     
            240_0  COME_FROM           224  '224'
            240_1  COME_FROM           164  '164'

 L. 981       240  LOAD_CONST               None
              242  STORE_FAST               'result'

 L. 983       244  LOAD_FAST                'self'
              246  LOAD_ATTR                new_conjecture_data

 L. 984       248  LOAD_GLOBAL              max
              250  LOAD_FAST                'buffer'
              252  LOAD_FAST                'dummy_data'
              254  LOAD_ATTR                buffer
              256  BUILD_TUPLE_2         2 
              258  LOAD_GLOBAL              len
              260  LOAD_CONST               ('key',)
              262  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'

 L. 984       264  LOAD_FAST                'max_length'

 L. 983       266  LOAD_CONST               ('prefix', 'max_length')
              268  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              270  STORE_FAST               'data'

 L. 986       272  LOAD_FAST                'self'
              274  LOAD_METHOD              test_function
              276  LOAD_FAST                'data'
              278  CALL_METHOD_1         1  ''
              280  POP_TOP          

 L. 987       282  LOAD_FAST                'check_result'
              284  LOAD_FAST                'data'
              286  LOAD_METHOD              as_result
              288  CALL_METHOD_0         0  ''
              290  CALL_FUNCTION_1       1  ''
              292  STORE_FAST               'result'

 L. 988       294  LOAD_FAST                'result'
              296  LOAD_FAST                'self'
              298  LOAD_ATTR                _ConjectureRunner__data_cache
              300  LOAD_FAST                'buffer'
              302  STORE_SUBSCR     

 L. 989       304  LOAD_FAST                'result'
              306  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `POP_TOP' instruction at offset 70

    def event_to_string--- This code section failed: ---

 L. 992         0  LOAD_GLOBAL              isinstance
                2  LOAD_FAST                'event'
                4  LOAD_GLOBAL              str
                6  CALL_FUNCTION_2       2  ''
                8  POP_JUMP_IF_FALSE    14  'to 14'

 L. 993        10  LOAD_FAST                'event'
               12  RETURN_VALUE     
             14_0  COME_FROM             8  '8'

 L. 994        14  SETUP_FINALLY        28  'to 28'

 L. 995        16  LOAD_FAST                'self'
               18  LOAD_ATTR                events_to_strings
               20  LOAD_FAST                'event'
               22  BINARY_SUBSCR    
               24  POP_BLOCK        
               26  RETURN_VALUE     
             28_0  COME_FROM_FINALLY    14  '14'

 L. 996        28  DUP_TOP          
               30  LOAD_GLOBAL              KeyError
               32  COMPARE_OP               exception-match
               34  POP_JUMP_IF_FALSE    46  'to 46'
               36  POP_TOP          
               38  POP_TOP          
               40  POP_TOP          

 L. 997        42  POP_EXCEPT       
               44  JUMP_FORWARD         48  'to 48'
             46_0  COME_FROM            34  '34'
               46  END_FINALLY      
             48_0  COME_FROM            44  '44'

 L. 998        48  LOAD_GLOBAL              str
               50  LOAD_FAST                'event'
               52  CALL_FUNCTION_1       1  ''
               54  STORE_FAST               'result'

 L. 999        56  LOAD_FAST                'result'
               58  LOAD_FAST                'self'
               60  LOAD_ATTR                events_to_strings
               62  LOAD_FAST                'event'
               64  STORE_SUBSCR     

 L.1000        66  LOAD_FAST                'result'
               68  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `POP_TOP' instruction at offset 38


class ContainsDiscard(Exception):
    pass