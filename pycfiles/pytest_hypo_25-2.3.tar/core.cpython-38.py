# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\User\AppData\Local\Temp\pip-install-oj_abz_z\hypothesis\hypothesis\core.py
# Compiled at: 2020-01-12 08:06:33
# Size of source mod 2**32: 45485 bytes
"""This module provides the core primitives of Hypothesis, such as given."""
import base64, contextlib, datetime, inspect, random as rnd_module, sys, traceback, warnings, zlib
from inspect import getfullargspec
from io import StringIO
from random import Random
from typing import Any, Callable, Hashable, List, TypeVar, Union
from unittest import TestCase
import attr
import hypothesis.strategies as st
from hypothesis._settings import HealthCheck, Phase, Verbosity, local_settings, settings as Settings
from hypothesis.control import BuildContext
from hypothesis.errors import DeadlineExceeded, DidNotReproduce, FailedHealthCheck, Flaky, Found, HypothesisDeprecationWarning, HypothesisWarning, InvalidArgument, MultipleFailures, NoSuchExample, Unsatisfiable, UnsatisfiedAssumption
from hypothesis.executors import new_style_executor
from hypothesis.internal.compat import bad_django_TestCase, benchmark_time, get_type_hints, int_from_bytes, qualname
from hypothesis.internal.conjecture.data import ConjectureData, StopTest
from hypothesis.internal.conjecture.engine import ConjectureRunner, sort_key
from hypothesis.internal.entropy import deterministic_PRNG
from hypothesis.internal.escalation import escalate_hypothesis_internal_error, get_trimmed_traceback
from hypothesis.internal.healthcheck import fail_health_check
from hypothesis.internal.reflection import arg_string, convert_positional_arguments, define_function_signature, function_digest, get_pretty_function_description, impersonate, is_mock, proxies
from hypothesis.reporting import current_verbosity, report, verbose_report, with_reporter
from hypothesis.statistics import note_engine_for_statistics
from hypothesis.strategies._internal.collections import TupleStrategy
from hypothesis.strategies._internal.strategies import Ex, MappedSearchStrategy, SearchStrategy
from hypothesis.utils.conventions import InferType, infer
from hypothesis.vendor.pretty import RepresentationPrinter
from hypothesis.version import __version__
TestFunc = TypeVar('TestFunc', bound=Callable)
running_under_pytest = False
global_force_seed = None

@attr.s()
class Example:
    args = attr.ib()
    kwargs = attr.ib()


def example(*args: Any, **kwargs: Any) -> Callable[([TestFunc], TestFunc)]:
    """A decorator which ensures a specific example is always tested."""
    if args:
        if kwargs:
            raise InvalidArgument('Cannot mix positional and keyword arguments for examples')
    if not args:
        if not kwargs:
            raise InvalidArgument('An example must provide at least one argument')

    def accept(test):
        if not hasattr(test, 'hypothesis_explicit_examples'):
            test.hypothesis_explicit_examples = []
        test.hypothesis_explicit_examples.append(Example(tuple(args), kwargs))
        return test

    return accept


def seed(seed: Hashable) -> Callable[([TestFunc], TestFunc)]:
    """seed: Start the test execution from a specific seed.

    May be any hashable object. No exact meaning for seed is provided
    other than that for a fixed seed value Hypothesis will try the same
    actions (insofar as it can given external sources of non-
    determinism. e.g. timing and hash randomization).

    Overrides the derandomize setting, which is designed to enable
    deterministic builds rather than reproducing observed failures.

    """

    def accept(test):
        test._hypothesis_internal_use_seed = seed
        current_settings = getattr(test, '_hypothesis_internal_use_settings', None)
        test._hypothesis_internal_use_settings = Settings(current_settings,
          database=None)
        return test

    return accept


def reproduce_failure(version, blob):
    """Run the example that corresponds to this data blob in order to reproduce
    a failure.

    A test with this decorator *always* runs only one example and always fails.
    If the provided example does not cause a failure, or is in some way invalid
    for this test, then this will fail with a DidNotReproduce error.

    This decorator is not intended to be a permanent addition to your test
    suite. It's simply some code you can add to ease reproduction of a problem
    in the event that you don't have access to the test database. Because of
    this, *no* compatibility guarantees are made between different versions of
    Hypothesis - its API may change arbitrarily from version to version.
    """

    def accept(test):
        test._hypothesis_internal_use_reproduce_failure = (
         version, blob)
        return test

    return accept


def encode_failure(buffer):
    buffer = bytes(buffer)
    compressed = zlib.compress(buffer)
    if len(compressed) < len(buffer):
        buffer = b'\x01' + compressed
    else:
        buffer = b'\x00' + buffer
    return base64.b64encode(buffer)


def decode_failure--- This code section failed: ---

 L. 189         0  SETUP_FINALLY        16  'to 16'

 L. 190         2  LOAD_GLOBAL              base64
                4  LOAD_METHOD              b64decode
                6  LOAD_FAST                'blob'
                8  CALL_METHOD_1         1  ''
               10  STORE_FAST               'buffer'
               12  POP_BLOCK        
               14  JUMP_FORWARD         50  'to 50'
             16_0  COME_FROM_FINALLY     0  '0'

 L. 191        16  DUP_TOP          
               18  LOAD_GLOBAL              Exception
               20  COMPARE_OP               exception-match
               22  POP_JUMP_IF_FALSE    48  'to 48'
               24  POP_TOP          
               26  POP_TOP          
               28  POP_TOP          

 L. 192        30  LOAD_GLOBAL              InvalidArgument
               32  LOAD_STR                 'Invalid base64 encoded string: %r'
               34  LOAD_FAST                'blob'
               36  BUILD_TUPLE_1         1 
               38  BINARY_MODULO    
               40  CALL_FUNCTION_1       1  ''
               42  RAISE_VARARGS_1       1  'exception instance'
               44  POP_EXCEPT       
               46  JUMP_FORWARD         50  'to 50'
             48_0  COME_FROM            22  '22'
               48  END_FINALLY      
             50_0  COME_FROM            46  '46'
             50_1  COME_FROM            14  '14'

 L. 193        50  LOAD_FAST                'buffer'
               52  LOAD_CONST               None
               54  LOAD_CONST               1
               56  BUILD_SLICE_2         2 
               58  BINARY_SUBSCR    
               60  STORE_FAST               'prefix'

 L. 194        62  LOAD_FAST                'prefix'
               64  LOAD_CONST               b'\x00'
               66  COMPARE_OP               ==
               68  POP_JUMP_IF_FALSE    82  'to 82'

 L. 195        70  LOAD_FAST                'buffer'
               72  LOAD_CONST               1
               74  LOAD_CONST               None
               76  BUILD_SLICE_2         2 
               78  BINARY_SUBSCR    
               80  RETURN_VALUE     
             82_0  COME_FROM            68  '68'

 L. 196        82  LOAD_FAST                'prefix'
               84  LOAD_CONST               b'\x01'
               86  COMPARE_OP               ==
               88  POP_JUMP_IF_FALSE   150  'to 150'

 L. 197        90  SETUP_FINALLY       112  'to 112'

 L. 198        92  LOAD_GLOBAL              zlib
               94  LOAD_METHOD              decompress
               96  LOAD_FAST                'buffer'
               98  LOAD_CONST               1
              100  LOAD_CONST               None
              102  BUILD_SLICE_2         2 
              104  BINARY_SUBSCR    
              106  CALL_METHOD_1         1  ''
              108  POP_BLOCK        
              110  RETURN_VALUE     
            112_0  COME_FROM_FINALLY    90  '90'

 L. 199       112  DUP_TOP          
              114  LOAD_GLOBAL              zlib
              116  LOAD_ATTR                error
              118  COMPARE_OP               exception-match
              120  POP_JUMP_IF_FALSE   146  'to 146'
              122  POP_TOP          
              124  POP_TOP          
              126  POP_TOP          

 L. 200       128  LOAD_GLOBAL              InvalidArgument
              130  LOAD_STR                 'Invalid zlib compression for blob %r'
              132  LOAD_FAST                'blob'
              134  BUILD_TUPLE_1         1 
              136  BINARY_MODULO    
              138  CALL_FUNCTION_1       1  ''
              140  RAISE_VARARGS_1       1  'exception instance'
              142  POP_EXCEPT       
              144  JUMP_ABSOLUTE       166  'to 166'
            146_0  COME_FROM           120  '120'
              146  END_FINALLY      
              148  JUMP_FORWARD        166  'to 166'
            150_0  COME_FROM            88  '88'

 L. 202       150  LOAD_GLOBAL              InvalidArgument

 L. 203       152  LOAD_STR                 'Could not decode blob %r: Invalid start byte %r'
              154  LOAD_FAST                'blob'
              156  LOAD_FAST                'prefix'
              158  BUILD_TUPLE_2         2 
              160  BINARY_MODULO    

 L. 202       162  CALL_FUNCTION_1       1  ''
              164  RAISE_VARARGS_1       1  'exception instance'
            166_0  COME_FROM           148  '148'

Parse error at or near `POP_TOP' instruction at offset 124


class WithRunner(MappedSearchStrategy):

    def __init__(self, base, runner):
        assert runner is not None
        MappedSearchStrategy.__init__(self, base)
        self.runner = runner

    def do_draw(self, data):
        data.hypothesis_runner = self.runner
        return self.mapped_strategy.do_draw(data)

    def __repr__(self):
        return 'WithRunner(%r, runner=%r)' % (self.mapped_strategy, self.runner)


def is_invalid_test(name, original_argspec, given_arguments, given_kwargs):
    """Check the arguments to ``@given`` for basic usage constraints.

    Most errors are not raised immediately; instead we return a dummy test
    function that will raise the appropriate error if it is actually called.
    When the user runs a subset of tests (e.g via ``pytest -k``), errors will
    only be reported for tests that actually ran.
    """

    def invalid(message):

        def wrapped_test(*arguments, **kwargs):
            raise InvalidArgument(message)

        wrapped_test.is_hypothesis_test = True
        return wrapped_test

    if not given_arguments:
        if not given_kwargs:
            return invalid('given must be called with at least one argument')
    if given_arguments:
        if any([
         original_argspec.varargs, original_argspec.varkw, original_argspec.kwonlyargs]):
            return invalid('positional arguments to @given are not supported with varargs, varkeywords, or keyword-only arguments')
    if len(given_arguments) > len(original_argspec.args):
        args = tuple(given_arguments)
        return invalid('Too many positional arguments for %s() were passed to @given - expected at most %d arguments, but got %d %r' % (
         name, len(original_argspec.args), len(args), args))
    if infer in given_arguments:
        return invalid('infer was passed as a positional argument to @given, but may only be passed as a keyword argument')
    if given_arguments:
        if given_kwargs:
            return invalid('cannot mix positional and keyword arguments to @given')
    extra_kwargs = [k for k in given_kwargs if k not in original_argspec.args + original_argspec.kwonlyargs]
    if extra_kwargs:
        if not original_argspec.varkw:
            arg = extra_kwargs[0]
            return invalid('%s() got an unexpected keyword argument %r, from `%s=%r` in @given' % (
             name, arg, arg, given_kwargs[arg]))
    if original_argspec.defaults or original_argspec.kwonlydefaults:
        return invalid('Cannot apply @given to a function with defaults.')
    missing = [repr(kw) for kw in original_argspec.kwonlyargs if kw not in given_kwargs]
    if missing:
        return invalid('Missing required kwarg{}: {}'.format('s' if len(missing) > 1 else '', ', '.join(missing)))


class ArtificialDataForExample(ConjectureData):
    __doc__ = "Dummy object that pretends to be a ConjectureData object for the purposes of\n    drawing arguments for @example. Provides just enough of the ConjectureData API\n    to allow the test to run. Does not support any sort of interactive drawing,\n    but that's fine because you can't access that when all of your arguments are\n    provided by @example.\n    "

    def __init__(self, kwargs):
        self._ArtificialDataForExample__draws = 0
        self._ArtificialDataForExample__kwargs = kwargs
        super().__init__(max_length=0, prefix=b'', random=None)

    def draw_bits(self, n):
        raise NotImplementedError()

    def draw(self, strategy):
        assert self._ArtificialDataForExample__draws == 0
        self._ArtificialDataForExample__draws += 1
        return (
         (), self._ArtificialDataForExample__kwargs)


def execute_explicit_examples(state, wrapped_test, arguments, kwargs):
    original_argspec = getfullargspec(state.test)
    for example in reversed(getattr(wrapped_test, 'hypothesis_explicit_examples', ())):
        example_kwargs = dict(original_argspec.kwonlydefaults or {})
        if example.args:
            if len(example.args) > len(original_argspec.args):
                raise InvalidArgument('example has too many arguments for test. Expected at most %d but got %d' % (
                 len(original_argspec.args), len(example.args)))
            example_kwargs.update(dict(zip(original_argspec.args[-len(example.args):], example.args)))
        else:
            example_kwargs.update(example.kwargs)
        if Phase.explicit not in state.settings.phases:
            pass
        else:
            example_kwargs.update(kwargs)
            with local_settings(state.settings):
                fragments_reported = []

                def report_buffered():
                    for f in fragments_reported:
                        report(f)
                    else:
                        del fragments_reported[:]

                try:
                    with with_reporter(fragments_reported.append):
                        state.execute_once((ArtificialDataForExample(example_kwargs)),
                          is_final=True,
                          print_example=True)
                except BaseException:
                    report_buffered()
                    raise
                else:
                    if current_verbosity() >= Verbosity.verbose:
                        prefix = 'Falsifying example'
                        assert fragments_reported[0].startswith(prefix)
                        fragments_reported[0] = 'Trying example' + fragments_reported[0][len(prefix):]
                        report_buffered()


def get_random_for_wrapped_test(test, wrapped_test):
    settings = wrapped_test._hypothesis_internal_use_settings
    wrapped_test._hypothesis_internal_use_generated_seed = None
    if wrapped_test._hypothesis_internal_use_seed is not None:
        return Random(wrapped_test._hypothesis_internal_use_seed)
    if settings.derandomize:
        return Random(int_from_bytes(function_digest(test)))
    if global_force_seed is not None:
        return Random(global_force_seed)
    seed = rnd_module.getrandbits(128)
    wrapped_test._hypothesis_internal_use_generated_seed = seed
    return Random(seed)


def process_arguments_to_given(wrapped_test, arguments, kwargs, given_kwargs, argspec, test, settings):
    selfy = None
    arguments, kwargs = convert_positional_arguments(wrapped_test, arguments, kwargs)
    if argspec.args:
        selfy = kwargs.get(argspec.args[0])
    else:
        if arguments:
            selfy = arguments[0]
    if is_mock(selfy):
        selfy = None
    test_runner = new_style_executor(selfy)
    arguments = tuple(arguments)
    search_strategy = TupleStrategy((
     st.just(arguments),
     st.fixed_dictionaries(given_kwargs).map(lambda args: dict(args, **kwargs))))
    if selfy is not None:
        search_strategy = WithRunner(search_strategy, selfy)
    search_strategy.validate()
    return (
     arguments, kwargs, test_runner, search_strategy)


def skip_exceptions_to_reraise():
    """Return a tuple of exceptions meaning 'skip this test', to re-raise.

    This is intended to cover most common test runners; if you would
    like another to be added please open an issue or pull request adding
    it to this function and to tests/cover/test_lazy_import.py
    """
    exceptions = set()
    if 'unittest' in sys.modules:
        exceptions.add(sys.modules['unittest'].SkipTest)
    if 'unittest2' in sys.modules:
        exceptions.add(sys.modules['unittest2'].SkipTest)
    if 'nose' in sys.modules:
        exceptions.add(sys.modules['nose'].SkipTest)
    if '_pytest' in sys.modules:
        exceptions.add(sys.modules['_pytest'].outcomes.Skipped)
    return tuple(sorted(exceptions, key=str))


def failure_exceptions_to_catch():
    """Return a tuple of exceptions meaning 'this test has failed', to catch.

    This is intended to cover most common test runners; if you would
    like another to be added please open an issue or pull request.
    """
    exceptions = [
     Exception]
    if '_pytest' in sys.modules:
        exceptions.append(sys.modules['_pytest'].outcomes.Failed)
    return tuple(exceptions)


def new_given_argspec--- This code section failed: ---

 L. 456         0  LOAD_CLOSURE             'given_kwargs'
                2  BUILD_TUPLE_1         1 
                4  LOAD_LISTCOMP            '<code_object <listcomp>>'
                6  LOAD_STR                 'new_given_argspec.<locals>.<listcomp>'
                8  MAKE_FUNCTION_8          'closure'
               10  LOAD_FAST                'original_argspec'
               12  LOAD_ATTR                args
               14  GET_ITER         
               16  CALL_FUNCTION_1       1  ''
               18  STORE_DEREF              'new_args'

 L. 457        20  LOAD_CLOSURE             'given_kwargs'
               22  BUILD_TUPLE_1         1 
               24  LOAD_LISTCOMP            '<code_object <listcomp>>'
               26  LOAD_STR                 'new_given_argspec.<locals>.<listcomp>'
               28  MAKE_FUNCTION_8          'closure'
               30  LOAD_FAST                'original_argspec'
               32  LOAD_ATTR                kwonlyargs
               34  GET_ITER         
               36  CALL_FUNCTION_1       1  ''
               38  STORE_DEREF              'new_kwonlyargs'

 L. 458        40  LOAD_CLOSURE             'new_args'
               42  LOAD_CLOSURE             'new_kwonlyargs'
               44  BUILD_TUPLE_2         2 
               46  LOAD_DICTCOMP            '<code_object <dictcomp>>'
               48  LOAD_STR                 'new_given_argspec.<locals>.<dictcomp>'
               50  MAKE_FUNCTION_8          'closure'

 L. 460        52  LOAD_FAST                'original_argspec'
               54  LOAD_ATTR                annotations
               56  LOAD_METHOD              items
               58  CALL_METHOD_0         0  ''

 L. 458        60  GET_ITER         
               62  CALL_FUNCTION_1       1  ''
               64  STORE_FAST               'annots'

 L. 463        66  LOAD_CONST               None
               68  LOAD_FAST                'annots'
               70  LOAD_STR                 'return'
               72  STORE_SUBSCR     

 L. 464        74  LOAD_FAST                'original_argspec'
               76  LOAD_ATTR                _replace

 L. 465        78  LOAD_DEREF               'new_args'

 L. 465        80  LOAD_DEREF               'new_kwonlyargs'

 L. 465        82  LOAD_FAST                'annots'

 L. 464        84  LOAD_CONST               ('args', 'kwonlyargs', 'annotations')
               86  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               88  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `LOAD_DICTCOMP' instruction at offset 46


class StateForActualGivenExecution:

    def __init__(self, test_runner, search_strategy, test, settings, random, wrapped_test):
        self.test_runner = test_runner
        self.search_strategy = search_strategy
        self.settings = settings
        self.last_exception = None
        self.falsifying_examples = ()
        self._StateForActualGivenExecution__was_flaky = False
        self.random = random
        self._StateForActualGivenExecution__warned_deadline = False
        self._StateForActualGivenExecution__test_runtime = None
        self._StateForActualGivenExecution__had_seed = wrapped_test._hypothesis_internal_use_seed
        self.is_find = getattr(wrapped_test, '_hypothesis_internal_is_find', False)
        self.wrapped_test = wrapped_test
        self.test = test
        self.print_given_args = getattr(wrapped_test, '_hypothesis_internal_print_given_args', True)
        self.files_to_propagate = set()
        self.failed_normally = False

    def execute_once(self, data, print_example=False, is_final=False, expected_failure=None):
        """Run the test function once, using ``data`` as input.

        If the test raises an exception, it will propagate through to the
        caller of this method. Depending on its type, this could represent
        an ordinary test failure, or a fatal error, or a control exception.

        If this method returns normally, the test might have passed, or
        it might have placed ``data`` in an unsuccessful state and then
        swallowed the corresponding control exception.
        """
        data.is_find = self.is_find
        text_repr = [
         None]
        if self.settings.deadline is None:
            test = self.test
        else:

            @proxies(self.test)
            def test(*args, **kwargs):
                self._StateForActualGivenExecution__test_runtime = None
                initial_draws = len(data.draw_times)
                start = benchmark_time()
                result = (self.test)(*args, **kwargs)
                finish = benchmark_time()
                internal_draw_time = sum(data.draw_times[initial_draws:])
                runtime = datetime.timedelta(seconds=(finish - start - internal_draw_time))
                self._StateForActualGivenExecution__test_runtime = runtime
                current_deadline = self.settings.deadline
                if not is_final:
                    current_deadline = current_deadline // 4 * 5
                if runtime >= current_deadline:
                    raise DeadlineExceeded(runtime, self.settings.deadline)
                return result

        def run--- This code section failed: ---

 L. 538         0  LOAD_GLOBAL              local_settings
                2  LOAD_DEREF               'self'
                4  LOAD_ATTR                settings
                6  CALL_FUNCTION_1       1  ''
             8_10  SETUP_WITH          482  'to 482'
               12  POP_TOP          

 L. 539        14  LOAD_GLOBAL              deterministic_PRNG
               16  CALL_FUNCTION_0       0  ''
            18_20  SETUP_WITH          472  'to 472'
               22  POP_TOP          

 L. 540        24  LOAD_GLOBAL              BuildContext
               26  LOAD_FAST                'data'
               28  LOAD_DEREF               'is_final'
               30  LOAD_CONST               ('is_final',)
               32  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
            34_36  SETUP_WITH          462  'to 462'
               38  POP_TOP          

 L. 543        40  LOAD_FAST                'data'
               42  LOAD_METHOD              draw
               44  LOAD_DEREF               'self'
               46  LOAD_ATTR                search_strategy
               48  CALL_METHOD_1         1  ''
               50  UNPACK_SEQUENCE_2     2 
               52  STORE_FAST               'args'
               54  STORE_FAST               'kwargs'

 L. 544        56  LOAD_DEREF               'expected_failure'
               58  LOAD_CONST               None
               60  COMPARE_OP               is-not
               62  POP_JUMP_IF_FALSE    80  'to 80'

 L. 545        64  LOAD_GLOBAL              arg_string
               66  LOAD_DEREF               'test'
               68  LOAD_FAST                'args'
               70  LOAD_FAST                'kwargs'
               72  CALL_FUNCTION_3       3  ''
               74  LOAD_DEREF               'text_repr'
               76  LOAD_CONST               0
               78  STORE_SUBSCR     
             80_0  COME_FROM            62  '62'

 L. 547        80  LOAD_DEREF               'print_example'
               82  POP_JUMP_IF_TRUE     98  'to 98'
               84  LOAD_GLOBAL              current_verbosity
               86  CALL_FUNCTION_0       0  ''
               88  LOAD_GLOBAL              Verbosity
               90  LOAD_ATTR                verbose
               92  COMPARE_OP               >=
            94_96  POP_JUMP_IF_FALSE   416  'to 416'
             98_0  COME_FROM            82  '82'

 L. 548        98  LOAD_GLOBAL              StringIO
              100  CALL_FUNCTION_0       0  ''
              102  STORE_FAST               'output'

 L. 550       104  LOAD_GLOBAL              RepresentationPrinter
              106  LOAD_FAST                'output'
              108  CALL_FUNCTION_1       1  ''
              110  STORE_FAST               'printer'

 L. 551       112  LOAD_DEREF               'print_example'
              114  POP_JUMP_IF_FALSE   128  'to 128'

 L. 552       116  LOAD_FAST                'printer'
              118  LOAD_METHOD              text
              120  LOAD_STR                 'Falsifying example:'
              122  CALL_METHOD_1         1  ''
              124  POP_TOP          
              126  JUMP_FORWARD        138  'to 138'
            128_0  COME_FROM           114  '114'

 L. 554       128  LOAD_FAST                'printer'
              130  LOAD_METHOD              text
              132  LOAD_STR                 'Trying example:'
              134  CALL_METHOD_1         1  ''
              136  POP_TOP          
            138_0  COME_FROM           126  '126'

 L. 556       138  LOAD_DEREF               'self'
              140  LOAD_ATTR                print_given_args
          142_144  POP_JUMP_IF_FALSE   396  'to 396'

 L. 557       146  LOAD_FAST                'printer'
              148  LOAD_METHOD              text
              150  LOAD_STR                 ' '
              152  CALL_METHOD_1         1  ''
              154  POP_TOP          

 L. 558       156  LOAD_FAST                'printer'
              158  LOAD_METHOD              text
              160  LOAD_DEREF               'test'
              162  LOAD_ATTR                __name__
              164  CALL_METHOD_1         1  ''
              166  POP_TOP          

 L. 559       168  LOAD_FAST                'printer'
              170  LOAD_ATTR                group
              172  LOAD_CONST               4
              174  LOAD_STR                 '('
              176  LOAD_STR                 ''
              178  LOAD_CONST               ('indent', 'open', 'close')
              180  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              182  SETUP_WITH          372  'to 372'
              184  POP_TOP          

 L. 560       186  LOAD_FAST                'printer'
              188  LOAD_METHOD              break_
              190  CALL_METHOD_0         0  ''
              192  POP_TOP          

 L. 561       194  LOAD_FAST                'args'
              196  GET_ITER         
              198  FOR_ITER            232  'to 232'
              200  STORE_FAST               'v'

 L. 562       202  LOAD_FAST                'printer'
              204  LOAD_METHOD              pretty
              206  LOAD_FAST                'v'
              208  CALL_METHOD_1         1  ''
              210  POP_TOP          

 L. 567       212  LOAD_FAST                'printer'
              214  LOAD_METHOD              text
              216  LOAD_STR                 ','
              218  CALL_METHOD_1         1  ''
              220  POP_TOP          

 L. 568       222  LOAD_FAST                'printer'
              224  LOAD_METHOD              breakable
              226  CALL_METHOD_0         0  ''
              228  POP_TOP          
              230  JUMP_BACK           198  'to 198'

 L. 573       232  LOAD_DICTCOMP            '<code_object <dictcomp>>'
              234  LOAD_STR                 'StateForActualGivenExecution.execute_once.<locals>.run.<locals>.<dictcomp>'
              236  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'

 L. 575       238  LOAD_GLOBAL              enumerate

 L. 576       240  LOAD_GLOBAL              getfullargspec
              242  LOAD_DEREF               'self'
              244  LOAD_ATTR                test
              246  CALL_FUNCTION_1       1  ''
              248  LOAD_ATTR                args

 L. 575       250  CALL_FUNCTION_1       1  ''

 L. 573       252  GET_ITER         
              254  CALL_FUNCTION_1       1  ''
              256  STORE_DEREF              'arg_order'

 L. 579       258  LOAD_GLOBAL              enumerate

 L. 580       260  LOAD_GLOBAL              sorted

 L. 581       262  LOAD_FAST                'kwargs'
              264  LOAD_METHOD              items
              266  CALL_METHOD_0         0  ''

 L. 582       268  LOAD_CLOSURE             'arg_order'
              270  BUILD_TUPLE_1         1 
              272  LOAD_LAMBDA              '<code_object <lambda>>'
              274  LOAD_STR                 'StateForActualGivenExecution.execute_once.<locals>.run.<locals>.<lambda>'
              276  MAKE_FUNCTION_8          'closure'

 L. 580       278  LOAD_CONST               ('key',)
              280  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'

 L. 579       282  CALL_FUNCTION_1       1  ''
              284  GET_ITER         
            286_0  COME_FROM           352  '352'
              286  FOR_ITER            368  'to 368'
              288  UNPACK_SEQUENCE_2     2 
              290  STORE_FAST               'i'
              292  UNPACK_SEQUENCE_2     2 
              294  STORE_FAST               'k'
              296  STORE_FAST               'v'

 L. 588       298  LOAD_FAST                'printer'
              300  LOAD_METHOD              text
              302  LOAD_FAST                'k'
              304  CALL_METHOD_1         1  ''
              306  POP_TOP          

 L. 589       308  LOAD_FAST                'printer'
              310  LOAD_METHOD              text
              312  LOAD_STR                 '='
              314  CALL_METHOD_1         1  ''
              316  POP_TOP          

 L. 590       318  LOAD_FAST                'printer'
              320  LOAD_METHOD              pretty
              322  LOAD_FAST                'v'
              324  CALL_METHOD_1         1  ''
              326  POP_TOP          

 L. 591       328  LOAD_FAST                'printer'
              330  LOAD_METHOD              text
              332  LOAD_STR                 ','
              334  CALL_METHOD_1         1  ''
              336  POP_TOP          

 L. 592       338  LOAD_FAST                'i'
              340  LOAD_CONST               1
              342  BINARY_ADD       
              344  LOAD_GLOBAL              len
              346  LOAD_FAST                'kwargs'
              348  CALL_FUNCTION_1       1  ''
              350  COMPARE_OP               <
          352_354  POP_JUMP_IF_FALSE   286  'to 286'

 L. 593       356  LOAD_FAST                'printer'
              358  LOAD_METHOD              breakable
              360  CALL_METHOD_0         0  ''
              362  POP_TOP          
          364_366  JUMP_BACK           286  'to 286'
              368  POP_BLOCK        
              370  BEGIN_FINALLY    
            372_0  COME_FROM_WITH      182  '182'
              372  WITH_CLEANUP_START
              374  WITH_CLEANUP_FINISH
              376  END_FINALLY      

 L. 594       378  LOAD_FAST                'printer'
              380  LOAD_METHOD              break_
              382  CALL_METHOD_0         0  ''
              384  POP_TOP          

 L. 595       386  LOAD_FAST                'printer'
              388  LOAD_METHOD              text
              390  LOAD_STR                 ')'
              392  CALL_METHOD_1         1  ''
              394  POP_TOP          
            396_0  COME_FROM           142  '142'

 L. 596       396  LOAD_FAST                'printer'
              398  LOAD_METHOD              flush
              400  CALL_METHOD_0         0  ''
              402  POP_TOP          

 L. 597       404  LOAD_GLOBAL              report
              406  LOAD_FAST                'output'
              408  LOAD_METHOD              getvalue
              410  CALL_METHOD_0         0  ''
              412  CALL_FUNCTION_1       1  ''
              414  POP_TOP          
            416_0  COME_FROM            94  '94'

 L. 598       416  LOAD_DEREF               'test'
              418  LOAD_FAST                'args'
              420  LOAD_FAST                'kwargs'
              422  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
              424  POP_BLOCK        
              426  ROT_TWO          
              428  BEGIN_FINALLY    
              430  WITH_CLEANUP_START
              432  WITH_CLEANUP_FINISH
              434  POP_FINALLY           0  ''
              436  POP_BLOCK        
              438  ROT_TWO          
              440  BEGIN_FINALLY    
              442  WITH_CLEANUP_START
              444  WITH_CLEANUP_FINISH
              446  POP_FINALLY           0  ''
              448  POP_BLOCK        
              450  ROT_TWO          
              452  BEGIN_FINALLY    
              454  WITH_CLEANUP_START
              456  WITH_CLEANUP_FINISH
              458  POP_FINALLY           0  ''
              460  RETURN_VALUE     
            462_0  COME_FROM_WITH       34  '34'
              462  WITH_CLEANUP_START
              464  WITH_CLEANUP_FINISH
              466  END_FINALLY      
              468  POP_BLOCK        
              470  BEGIN_FINALLY    
            472_0  COME_FROM_WITH       18  '18'
              472  WITH_CLEANUP_START
              474  WITH_CLEANUP_FINISH
              476  END_FINALLY      
              478  POP_BLOCK        
              480  BEGIN_FINALLY    
            482_0  COME_FROM_WITH        8  '8'
              482  WITH_CLEANUP_START
              484  WITH_CLEANUP_FINISH
              486  END_FINALLY      

Parse error at or near `ROT_TWO' instruction at offset 426

        result = self.test_runner(data, run)
        if expected_failure is not None:
            exception, traceback = expected_failure
            if isinstance(exception, DeadlineExceeded) and self._StateForActualGivenExecution__test_runtime is not None:
                report('Unreliable test timings! On an initial run, this test took %.2fms, which exceeded the deadline of %.2fms, but on a subsequent run it took %.2f ms, which did not. If you expect this sort of variability in your test timings, consider turning deadlines off for this test by setting deadline=None.' % (
                 exception.runtime.total_seconds() * 1000,
                 self.settings.deadline.total_seconds() * 1000,
                 self._StateForActualGivenExecution__test_runtime.total_seconds() * 1000))
            else:
                report('Failed to reproduce exception. Expected: \n' + traceback)
            self._StateForActualGivenExecution__flaky('Hypothesis %s(%s) produces unreliable results: Falsified on the first call but did not on a subsequent one' % (
             test.__name__, text_repr[0]))
        return result

    def _execute_once_for_engine(self, data):
        """Wrapper around ``execute_once`` that intercepts test failure
        exceptions and single-test control exceptions, and turns them into
        appropriate method calls to `data` instead.

        This allows the engine to assume that any exception other than
        ``StopTest`` must be a fatal error, and should stop the entire engine.
        """
        try:
            result = self.execute_once(data)
            if result is not None:
                fail_health_check(self.settings, 'Tests run under @given should return None, but %s returned %r instead.' % (
                 self.test.__name__, result), HealthCheck.return_value)
        except UnsatisfiedAssumption:
            data.mark_invalid()
        except StopTest:
            raise
        except (HypothesisDeprecationWarning,
         FailedHealthCheck) + skip_exceptions_to_reraise():
            raise
        except failure_exceptions_to_catch() as e:
            try:
                escalate_hypothesis_internal_error()
                if data.frozen:
                    raise StopTest(data.testcounter)
                else:
                    tb = get_trimmed_traceback()
                    info = data.extra_information
                    info._StateForActualGivenExecution__expected_traceback = ''.join(traceback.format_exception(type(e), e, tb))
                    info._StateForActualGivenExecution__expected_exception = e
                    verbose_report(info._StateForActualGivenExecution__expected_traceback)
                    origin = traceback.extract_tb(tb)[(-1)]
                    filename = origin[0]
                    lineno = origin[1]
                    data.mark_interesting((type(e), filename, lineno))
            finally:
                e = None
                del e

    def run_engine(self):
        """Run the test function many times, on database input and generated
        input, using the Conjecture engine.
        """
        __tracebackhide__ = True
        try:
            database_key = self.wrapped_test._hypothesis_internal_database_key
        except AttributeError:
            if global_force_seed is None:
                database_key = function_digest(self.test)
            else:
                database_key = None
        else:
            runner = ConjectureRunner((self._execute_once_for_engine),
              settings=(self.settings),
              random=(self.random),
              database_key=database_key)
            runner.run()
            note_engine_for_statistics(runner)
            if runner.call_count == 0:
                return
        if runner.interesting_examples:
            self.falsifying_examples = sorted((runner.interesting_examples.values()),
              key=(lambda d: sort_key(d.buffer)),
              reverse=True)
        else:
            if runner.valid_examples == 0:
                raise Unsatisfiable('Unable to satisfy assumptions of hypothesis %s.' % (
                 get_pretty_function_description(self.test),))
            elif not self.falsifying_examples:
                return
                if not self.settings.report_multiple_bugs:
                    del self.falsifying_examples[:-1]
                self.failed_normally = True
                flaky = 0
                for falsifying_example in self.falsifying_examples:
                    info = falsifying_example.extra_information
                    ran_example = ConjectureData.for_buffer(falsifying_example.buffer)
                    self._StateForActualGivenExecution__was_flaky = False
                    assert info._StateForActualGivenExecution__expected_exception is not None
                    try:
                        try:
                            self.execute_once(ran_example,
                              print_example=(not self.is_find),
                              is_final=True,
                              expected_failure=(
                             info._StateForActualGivenExecution__expected_exception,
                             info._StateForActualGivenExecution__expected_traceback))
                        except (UnsatisfiedAssumption, StopTest):
                            report(traceback.format_exc())
                            self._StateForActualGivenExecution__flaky('Unreliable assumption: An example which satisfied assumptions on the first run now fails it.')
                        except BaseException as e:
                            try:
                                if len(self.falsifying_examples) <= 1:
                                    raise
                                tb = get_trimmed_traceback()
                                report(''.join(traceback.format_exception(type(e), e, tb)))
                            finally:
                                e = None
                                del e

                    finally:
                        ran_example.freeze()
                        if self.settings.print_blob:
                            report('\nYou can reproduce this example by temporarily adding @reproduce_failure(%r, %r) as a decorator on your test case' % (
                             __version__, encode_failure(falsifying_example.buffer)))

                    if self._StateForActualGivenExecution__was_flaky:
                        flaky += 1
                    assert len(self.falsifying_examples) > 1
                    if flaky > 0:
                        raise Flaky('Hypothesis found %d distinct failures, but %d of them exhibited some sort of flaky behaviour.' % (
                         len(self.falsifying_examples), flaky))

            else:
                raise MultipleFailures('Hypothesis found %d distinct failures.' % len(self.falsifying_examples))

    def __flaky(self, message):
        if len(self.falsifying_examples) <= 1:
            raise Flaky(message)
        else:
            self._StateForActualGivenExecution__was_flaky = True
            report('Flaky example! ' + message)


@contextlib.contextmanager
def fake_subTest(self, msg=None, **__):
    """Monkeypatch for `unittest.TestCase.subTest` during `@given`.

    If we don't patch this out, each failing example is reported as a
    separate failing test by the unittest test runner, which is
    obviously incorrect. We therefore replace it for the duration with
    this version.
    """
    warnings.warn('subTest per-example reporting interacts badly with Hypothesis trying hundreds of examples, so we disable it for the duration of any test that uses `@given`.',
      HypothesisWarning,
      stacklevel=2)
    (yield)


@attr.s()
class HypothesisHandle:
    __doc__ = 'This object is provided as the .hypothesis attribute on @given tests.\n\n    Downstream users can reassign its attributes to insert custom logic into\n    the execution of each case, for example by converting an async into a\n    sync function.\n\n    This must be an attribute of an attribute, because reassignment of a\n    first-level attribute would not be visible to Hypothesis if the function\n    had been decorated before the assignment.\n\n    See https://github.com/HypothesisWorks/hypothesis/issues/1257 for more\n    information.\n    '
    inner_test = attr.ib()


def given(*_given_arguments: Union[(SearchStrategy, InferType)], **_given_kwargs: Union[(SearchStrategy, InferType)]) -> Callable[([Callable[(Ellipsis, None)]], Callable[(Ellipsis, None)])]:
    """A decorator for turning a test function that accepts arguments into a
    randomized test.

    This is the main entry point to Hypothesis.
    """

    def run_test_as_given(test):
        if inspect.isclass(test):
            raise InvalidArgument('@given cannot be applied to a class.')
        else:
            given_arguments = tuple(_given_arguments)
            given_kwargs = dict(_given_kwargs)
            original_argspec = getfullargspec(test)
            check_invalid = is_invalid_test(test.__name__, original_argspec, given_arguments, given_kwargs)
            if check_invalid is not None:
                return check_invalid
            if given_arguments:
                assert not given_kwargs
                for name, strategy in zip(reversed(original_argspec.args), reversed(given_arguments)):
                    given_kwargs[name] = strategy

        del given_arguments
        argspec = new_given_argspec(original_argspec, given_kwargs)

        @impersonate(test)
        @define_function_signature(test.__name__, test.__doc__, argspec)
        def wrapped_test(*arguments, **kwargs):
            __tracebackhide__ = True
            test = wrapped_test.hypothesis.inner_test
            if getattr(test, 'is_hypothesis_test', False):
                raise InvalidArgument('You have applied @given to the test %s more than once, which wraps the test several times and is extremely slow. A similar effect can be gained by combining the arguments of the two calls to given. For example, instead of @given(booleans()) @given(integers()), you could write @given(booleans(), integers())' % (
                 test.__name__,))
            settings = wrapped_test._hypothesis_internal_use_settings
            random = get_random_for_wrapped_test(test, wrapped_test)
            if infer in given_kwargs.values():
                hints = get_type_hints(test)
            for name in [name for name, value in given_kwargs.items() if value is infer]:
                if name not in hints:
                    raise InvalidArgument('passed %s=infer for %s, but %s has no type annotation' % (
                     name, test.__name__, name))
                given_kwargs[name] = st.from_type(hints[name])
            else:
                processed_args = process_arguments_to_given(wrapped_test, arguments, kwargs, given_kwargs, argspec, test, settings)
                arguments, kwargs, test_runner, search_strategy = processed_args
                runner = getattr(search_strategy, 'runner', None)
                if isinstance(runner, TestCase):
                    if test.__name__ in dir(TestCase):
                        msg = 'You have applied @given to the method %s, which is used by the unittest runner but is not itself a test.  This is not useful in any way.' % test.__name__
                        fail_health_check(settings, msg, HealthCheck.not_a_test_method)
                if bad_django_TestCase(runner):
                    raise InvalidArgument('You have applied @given to a method on %s, but this class does not inherit from the supported versions in `hypothesis.extra.django`.  Use the Hypothesis variants to ensure that each example is run in a separate database transaction.' % qualname(type(runner)))
                state = StateForActualGivenExecution(test_runner, search_strategy, test, settings, random, wrapped_test)
                reproduce_failure = wrapped_test._hypothesis_internal_use_reproduce_failure
                if reproduce_failure is not None:
                    expected_version, failure = reproduce_failure
                    if expected_version != __version__:
                        raise InvalidArgument('Attempting to reproduce a failure from a different version of Hypothesis. This failure is from %s, but you are currently running %r. Please change your Hypothesis version to a matching one.' % (
                         expected_version, __version__))
                    try:
                        state.execute_once((ConjectureData.for_buffer(decode_failure(failure))),
                          print_example=True,
                          is_final=True)
                        raise DidNotReproduce('Expected the test to raise an error, but it completed successfully.')
                    except StopTest:
                        raise DidNotReproduce("The shape of the test data has changed in some way from where this blob was defined. Are you sure you're running the same test?")
                    except UnsatisfiedAssumption:
                        raise DidNotReproduce('The test data failed to satisfy an assumption in the test. Have you added it since this blob was generated?')

                execute_explicit_examples(state, wrapped_test, arguments, kwargs)
                if not Phase.reuse in settings.phases:
                    if not Phase.generate in settings.phases:
                        return
                try:
                    if isinstance(runner, TestCase) and hasattr(runner, 'subTest'):
                        subTest = runner.subTest
                        try:
                            runner.subTest = fake_subTest
                            state.run_engine()
                        finally:
                            runner.subTest = subTest

                    else:
                        state.run_engine()
                except BaseException as e:
                    try:
                        generated_seed = wrapped_test._hypothesis_internal_use_generated_seed
                        with local_settings(settings):
                            if not state.failed_normally:
                                if not generated_seed is None:
                                    if running_under_pytest:
                                        report('You can add @seed(%(seed)d) to this test or run pytest with --hypothesis-seed=%(seed)d to reproduce this failure.' % {'seed': generated_seed})
                                    else:
                                        report('You can add @seed(%d) to this test to reproduce this failure.' % (
                                         generated_seed,))
                            the_error_hypothesis_found = e.with_traceback(get_trimmed_traceback())
                            raise the_error_hypothesis_found
                    finally:
                        e = None
                        del e

        for attrib in dir(test):
            if not attrib.startswith('_'):
                if not hasattr(wrapped_test, attrib):
                    setattr(wrapped_test, attrib, getattr(test, attrib))
            wrapped_test.is_hypothesis_test = True
            if hasattr(test, '_hypothesis_internal_settings_applied'):
                wrapped_test._hypothesis_internal_settings_applied = True
            wrapped_test._hypothesis_internal_use_seed = getattr(test, '_hypothesis_internal_use_seed', None)
            wrapped_test._hypothesis_internal_use_settings = getattr(test, '_hypothesis_internal_use_settings', None) or Settings.default
            wrapped_test._hypothesis_internal_use_reproduce_failure = getattr(test, '_hypothesis_internal_use_reproduce_failure', None)
            wrapped_test.hypothesis = HypothesisHandle(test)
            return wrapped_test

    return run_test_as_given


def find(specifier: SearchStrategy[Ex], condition: Callable[([Any], bool)], settings: Settings=None, random: Random=None, database_key: bytes=None) -> Ex:
    """Returns the minimal example from the given strategy ``specifier`` that
    matches the predicate function ``condition``."""
    if settings is None:
        settings = Settings(max_examples=2000)
    else:
        settings = Settings(settings,
          suppress_health_check=(HealthCheck.all()), report_multiple_bugs=False)
        if database_key is None:
            if settings.database is not None:
                database_key = function_digest(condition)
        assert isinstance(specifier, SearchStrategy), 'Expected SearchStrategy but got %r of type %s' % (
         specifier, type(specifier).__name__)
    specifier.validate()
    last = []

    @settings
    @given(specifier)
    def test(v):
        if condition(v):
            last[:] = [
             v]
            raise Found()

    if random is not None:
        test = seed(random.getrandbits(64))(test)
    test._hypothesis_internal_is_find = True
    test._hypothesis_internal_database_key = database_key
    try:
        test()
    except Found:
        return last[0]
    else:
        raise NoSuchExample(get_pretty_function_description(condition))