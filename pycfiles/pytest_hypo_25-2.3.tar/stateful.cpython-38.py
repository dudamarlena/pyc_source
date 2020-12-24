# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\User\AppData\Local\Temp\pip-install-oj_abz_z\hypothesis\hypothesis\stateful.py
# Compiled at: 2020-01-12 08:06:33
# Size of source mod 2**32: 31326 bytes
"""This module provides support for a stateful style of testing, where tests
attempt to find a sequence of operations that cause a breakage rather than just
a single value.

Notably, the set of steps available at any point may depend on the
execution to date.
"""
import inspect
from collections.abc import Iterable
from copy import copy
from io import StringIO
from typing import Any, Dict, List
from unittest import TestCase
import attr
import hypothesis.internal.conjecture.utils as cu
import hypothesis.strategies as st
from hypothesis._settings import HealthCheck, Verbosity, settings as Settings
from hypothesis.control import current_build_context
from hypothesis.core import given
from hypothesis.errors import InvalidArgument, InvalidDefinition
from hypothesis.internal.reflection import function_digest, nicerepr, proxies, qualname
from hypothesis.internal.validation import check_type
from hypothesis.reporting import current_verbosity, report
from hypothesis.strategies._internal.featureflags import FeatureStrategy
from hypothesis.strategies._internal.strategies import OneOfStrategy, SearchStrategy
from hypothesis.vendor.pretty import RepresentationPrinter
STATE_MACHINE_RUN_LABEL = cu.calc_label_from_name('another state machine step')
SHOULD_CONTINUE_LABEL = cu.calc_label_from_name('should we continue drawing')

class TestCaseProperty:

    def __get__(self, obj, typ=None):
        if obj is not None:
            typ = type(obj)
        return typ._to_test_case()

    def __set__(self, obj, value):
        raise AttributeError('Cannot set TestCase')

    def __delete__(self, obj):
        raise AttributeError('Cannot delete TestCase')


def run_state_machine_as_test(state_machine_factory, settings=None):
    """Run a state machine definition as a test, either silently doing nothing
    or printing a minimal breaking program and raising an exception.

    state_machine_factory is anything which returns an instance of
    RuleBasedStateMachine when called with no arguments - it can be a class or a
    function. settings will be used to control the execution of the test.
    """
    if settings is None:
        try:
            settings = state_machine_factory.TestCase.settings
            check_type(Settings, settings, 'state_machine_factory.TestCase.settings')
        except AttributeError:
            settings = Settings(deadline=None, suppress_health_check=(HealthCheck.all()))

    check_type(Settings, settings, 'settings')

    @settings
    @given(st.data())
    def run_state_machine(factory, data):
        machine = factory()
        if not isinstance(machine, _GenericStateMachine):
            raise InvalidArgument('Expected RuleBasedStateMachine but state_machine_factory() returned %r (type=%s)' % (
             machine, type(machine).__name__))
        data.conjecture_data.hypothesis_runner = machine
        print_steps = current_build_context().is_final or current_verbosity() >= Verbosity.debug
        try:
            if print_steps:
                machine.print_start()
            machine.check_invariants()
            max_steps = settings.stateful_step_count
            steps_run = 0
            cd = data.conjecture_data
            while True:
                cd.start_example(STATE_MACHINE_RUN_LABEL)
                if steps_run == 0:
                    cd.draw_bits(16, forced=1)
                else:
                    if steps_run >= max_steps:
                        cd.draw_bits(16, forced=0)
                        break
                    else:
                        cd.start_example(SHOULD_CONTINUE_LABEL)
                        should_continue_value = cd.draw_bits(16)
                        if should_continue_value > 1:
                            cd.stop_example(discard=True)
                            cd.draw_bits(16, forced=(int(bool(should_continue_value))))
                        else:
                            cd.stop_example()
                            if should_continue_value == 0:
                                break
                steps_run += 1
                value = data.conjecture_data.draw(machine.steps())
                result = multiple()
                try:
                    result = machine.execute_step(value)
                finally:
                    if print_steps:
                        machine.print_step(value, result)

                machine.check_invariants()
                data.conjecture_data.stop_example()

        finally:
            if print_steps:
                machine.print_end()
            machine.teardown()

    run_state_machine.hypothesis.inner_test._hypothesis_internal_add_digest = function_digest(state_machine_factory)
    run_state_machine._hypothesis_internal_use_seed = getattr(state_machine_factory, '_hypothesis_internal_use_seed', None)
    run_state_machine._hypothesis_internal_use_reproduce_failure = getattr(state_machine_factory, '_hypothesis_internal_use_reproduce_failure', None)
    run_state_machine._hypothesis_internal_print_given_args = False
    run_state_machine(state_machine_factory)


class GenericStateMachineMeta(type):

    def __init__(self, *args, **kwargs):
        (super().__init__)(*args, **kwargs)

    def __setattr__(self, name, value):
        if name == 'settings':
            if isinstance(value, Settings):
                raise AttributeError('Assigning {cls}.settings = {value} does nothing. Assign to {cls}.TestCase.settings, or use @{value} as a decorator on the {cls} class.'.format(cls=(self.__name__),
                  value=value))
        return type.__setattr__(self, name, value)


class _GenericStateMachine(GenericStateMachineMeta('_GenericStateMachine', (object,), {})):

    def steps(self):
        """Return a SearchStrategy instance the defines the available next
        steps."""
        raise NotImplementedError('%r.steps()' % (self,))

    def execute_step(self, step):
        """Execute a step that has been previously drawn from self.steps()

        Returns the result of the step execution.
        """
        raise NotImplementedError('%r.execute_step()' % (self,))

    def print_start(self):
        """Called right at the start of printing.

        By default does nothing.
        """
        pass

    def print_end(self):
        """Called right at the end of printing.

        By default does nothing.
        """
        pass

    def print_step(self, step, result):
        """Print a step to the current reporter.

        This is called right after a step is executed.
        """
        self.step_count = getattr(self, 'step_count', 0) + 1
        report('Step #%d: %s' % (self.step_count, nicerepr(step)))

    def teardown(self):
        """Called after a run has finished executing to clean up any necessary
        state.

        Does nothing by default.
        """
        pass

    def check_invariants(self):
        """Called after initializing and after executing each step."""
        pass

    _test_case_cache = {}
    TestCase = TestCaseProperty()

    @classmethod
    def _to_test_case--- This code section failed: ---

 L. 233         0  SETUP_FINALLY        14  'to 14'

 L. 234         2  LOAD_DEREF               'state_machine_class'
                4  LOAD_ATTR                _test_case_cache
                6  LOAD_DEREF               'state_machine_class'
                8  BINARY_SUBSCR    
               10  POP_BLOCK        
               12  RETURN_VALUE     
             14_0  COME_FROM_FINALLY     0  '0'

 L. 235        14  DUP_TOP          
               16  LOAD_GLOBAL              KeyError
               18  COMPARE_OP               exception-match
               20  POP_JUMP_IF_FALSE    32  'to 32'
               22  POP_TOP          
               24  POP_TOP          
               26  POP_TOP          

 L. 236        28  POP_EXCEPT       
               30  JUMP_FORWARD         34  'to 34'
             32_0  COME_FROM            20  '20'
               32  END_FINALLY      
             34_0  COME_FROM            30  '30'

 L. 238        34  LOAD_BUILD_CLASS 
               36  LOAD_CODE                <code_object StateMachineTestCase>
               38  LOAD_STR                 'StateMachineTestCase'
               40  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
               42  LOAD_STR                 'StateMachineTestCase'
               44  LOAD_GLOBAL              TestCase
               46  CALL_FUNCTION_3       3  ''
               48  STORE_FAST               'StateMachineTestCase'

 L. 243        50  LOAD_CLOSURE             'state_machine_class'
               52  BUILD_TUPLE_1         1 
               54  LOAD_CODE                <code_object runTest>
               56  LOAD_STR                 '_GenericStateMachine._to_test_case.<locals>.runTest'
               58  MAKE_FUNCTION_8          'closure'
               60  STORE_FAST               'runTest'

 L. 246        62  LOAD_CONST               True
               64  LOAD_FAST                'runTest'
               66  STORE_ATTR               is_hypothesis_test

 L. 247        68  LOAD_FAST                'runTest'
               70  LOAD_FAST                'StateMachineTestCase'
               72  STORE_ATTR               runTest

 L. 248        74  LOAD_DEREF               'state_machine_class'
               76  LOAD_ATTR                __name__
               78  STORE_FAST               'base_name'

 L. 249        80  LOAD_FAST                'base_name'
               82  LOAD_STR                 '.TestCase'
               84  BINARY_ADD       
               86  LOAD_FAST                'StateMachineTestCase'
               88  STORE_ATTR               __name__

 L. 251        90  LOAD_GLOBAL              getattr
               92  LOAD_DEREF               'state_machine_class'
               94  LOAD_STR                 '__qualname__'
               96  LOAD_FAST                'base_name'
               98  CALL_FUNCTION_3       3  ''
              100  LOAD_STR                 '.TestCase'
              102  BINARY_ADD       

 L. 250       104  LOAD_FAST                'StateMachineTestCase'
              106  STORE_ATTR               __qualname__

 L. 253       108  LOAD_FAST                'StateMachineTestCase'
              110  LOAD_DEREF               'state_machine_class'
              112  LOAD_ATTR                _test_case_cache
              114  LOAD_DEREF               'state_machine_class'
              116  STORE_SUBSCR     

 L. 254       118  LOAD_FAST                'StateMachineTestCase'
              120  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `POP_TOP' instruction at offset 24


@attr.s()
class Rule:
    targets = attr.ib()
    function = attr.ib(repr=qualname)
    arguments = attr.ib()
    precondition = attr.ib()
    bundles = attr.ib(init=False)

    def __attrs_post_init__(self):
        arguments = {}
        bundles = []
        for k, v in sorted(self.arguments.items()):
            assert not isinstance(v, BundleReferenceStrategy)
            if isinstance(v, Bundle):
                bundles.append(v)
                consume = isinstance(v, BundleConsumer)
                arguments[k] = BundleReferenceStrategy(v.name, consume)
            else:
                arguments[k] = v
        else:
            self.bundles = tuple(bundles)
            self.arguments_strategy = st.fixed_dictionaries(arguments)


self_strategy = st.runner()

class BundleReferenceStrategy(SearchStrategy):

    def __init__(self, name, consume=False):
        self.name = name
        self.consume = consume

    def do_draw(self, data):
        machine = data.draw(self_strategy)
        bundle = machine.bundle(self.name)
        if not bundle:
            data.mark_invalid()
        position = cu.integer_range(data, 0, (len(bundle) - 1), center=(len(bundle)))
        if self.consume:
            return bundle.pop(position)
        return bundle[position]


class Bundle(SearchStrategy):

    def __init__(self, name, consume=False):
        self.name = name
        self._Bundle__reference_strategy = BundleReferenceStrategy(name, consume)

    def do_draw(self, data):
        machine = data.draw(self_strategy)
        reference = data.draw(self._Bundle__reference_strategy)
        return machine.names_to_values[reference.name]

    def __repr__(self):
        consume = self._Bundle__reference_strategy.consume
        if consume is False:
            return 'Bundle(name=%r)' % (self.name,)
        return 'Bundle(name=%r, consume=%r)' % (self.name, consume)

    def calc_is_empty(self, recur):
        return False

    def available(self, data):
        machine = data.draw(self_strategy)
        return bool(machine.bundle(self.name))


class BundleConsumer(Bundle):

    def __init__(self, bundle):
        super().__init__((bundle.name), consume=True)


def consumes(bundle):
    """When introducing a rule in a RuleBasedStateMachine, this function can
    be used to mark bundles from which each value used in a step with the
    given rule should be removed. This function returns a strategy object
    that can be manipulated and combined like any other.

    For example, a rule declared with

    ``@rule(value1=b1, value2=consumes(b2), value3=lists(consumes(b3)))``

    will consume a value from Bundle ``b2`` and several values from Bundle
    ``b3`` to populate ``value2`` and ``value3`` each time it is executed.
    """
    if not isinstance(bundle, Bundle):
        raise TypeError('Argument to be consumed must be a bundle.')
    return BundleConsumer(bundle)


@attr.s()
class MultipleResults(Iterable):
    values = attr.ib()

    def __iter__(self):
        return iter(self.values)


def multiple(*args):
    """This function can be used to pass multiple results to the target(s) of
    a rule. Just use ``return multiple(result1, result2, ...)`` in your rule.

    It is also possible to use ``return multiple()`` with no arguments in
    order to end a rule without passing any result.
    """
    return MultipleResults(args)


def _convert_targets(targets, target):
    """Single validator and convertor for target arguments."""
    if target is not None:
        if targets:
            raise InvalidArgument('Passing both targets=%r and target=%r is redundant - pass targets=%r instead.' % (
             targets, target, tuple(targets) + (target,)))
        targets = (target,)
    converted_targets = []
    for t in targets:
        if not isinstance(t, Bundle):
            msg = 'Got invalid target %r of type %r, but all targets must be Bundles.'
            if isinstance(t, OneOfStrategy):
                msg += '\nIt looks like you passed `one_of(a, b)` or `a | b` as a target.  You should instead pass `targets=(a, b)` to add the return value of this rule to both the `a` and `b` bundles, or define a rule for each target if it should be added to exactly one.'
            raise InvalidArgument(msg % (t, type(t)))
            while isinstance(t, Bundle):
                t = t.name

            converted_targets.append(t)
        return tuple(converted_targets)


RULE_MARKER = 'hypothesis_stateful_rule'
INITIALIZE_RULE_MARKER = 'hypothesis_stateful_initialize_rule'
PRECONDITION_MARKER = 'hypothesis_stateful_precondition'
INVARIANT_MARKER = 'hypothesis_stateful_invariant'

def rule(targets=(), target=None, **kwargs):
    """Decorator for RuleBasedStateMachine. Any name present in target or
    targets will define where the end result of this function should go. If
    both are empty then the end result will be discarded.

    ``target`` must be a Bundle, or if the result should go to multiple
    bundles you can pass a tuple of them as the ``targets`` argument.
    It is invalid to use both arguments for a single rule.  If the result
    should go to exactly one of several bundles, define a separate rule for
    each case.

    kwargs then define the arguments that will be passed to the function
    invocation. If their value is a Bundle, or if it is ``consumes(b)``
    where ``b`` is a Bundle, then values that have previously been produced
    for that bundle will be provided. If ``consumes`` is used, the value
    will also be removed from the bundle.

    Any other kwargs should be strategies and values from them will be
    provided.
    """
    converted_targets = _convert_targets(targets, target)
    for k, v in kwargs.items():
        check_type(SearchStrategy, v, k)
    else:

        def accept(f):
            existing_rule = getattr(f, RULE_MARKER, None)
            existing_initialize_rule = getattr(f, INITIALIZE_RULE_MARKER, None)
            if existing_rule is not None or existing_initialize_rule is not None:
                raise InvalidDefinition('A function cannot be used for two distinct rules. ', Settings.default)
            precondition = getattr(f, PRECONDITION_MARKER, None)
            rule = Rule(targets=converted_targets,
              arguments=kwargs,
              function=f,
              precondition=precondition)

            @proxies(f)
            def rule_wrapper(*args, **kwargs):
                return f(*args, **kwargs)

            setattr(rule_wrapper, RULE_MARKER, rule)
            return rule_wrapper

        return accept


def initialize(targets=(), target=None, **kwargs):
    """Decorator for RuleBasedStateMachine.

    An initialize decorator behaves like a rule, but the decorated
    method is called at most once in a run. All initialize decorated
    methods will be called before any rule decorated methods, in an
    arbitrary order.
    """
    converted_targets = _convert_targets(targets, target)
    for k, v in kwargs.items():
        check_type(SearchStrategy, v, k)
    else:

        def accept(f):
            existing_rule = getattr(f, RULE_MARKER, None)
            existing_initialize_rule = getattr(f, INITIALIZE_RULE_MARKER, None)
            if existing_rule is not None or existing_initialize_rule is not None:
                raise InvalidDefinition('A function cannot be used for two distinct rules. ', Settings.default)
            precondition = getattr(f, PRECONDITION_MARKER, None)
            if precondition:
                raise InvalidDefinition('An initialization rule cannot have a precondition. ', Settings.default)
            rule = Rule(targets=converted_targets,
              arguments=kwargs,
              function=f,
              precondition=precondition)

            @proxies(f)
            def rule_wrapper(*args, **kwargs):
                return f(*args, **kwargs)

            setattr(rule_wrapper, INITIALIZE_RULE_MARKER, rule)
            return rule_wrapper

        return accept


@attr.s()
class VarReference:
    name = attr.ib()


def precondition(precond):
    """Decorator to apply a precondition for rules in a RuleBasedStateMachine.
    Specifies a precondition for a rule to be considered as a valid step in the
    state machine. The given function will be called with the instance of
    RuleBasedStateMachine and should return True or False. Usually it will need
    to look at attributes on that instance.

    For example::

        class MyTestMachine(RuleBasedStateMachine):
            state = 1

            @precondition(lambda self: self.state != 0)
            @rule(numerator=integers())
            def divide_with(self, numerator):
                self.state = numerator / self.state

    This is better than using assume in your rule since more valid rules
    should be able to be run.
    """

    def decorator(f):

        @proxies(f)
        def precondition_wrapper(*args, **kwargs):
            return f(*args, **kwargs)

        existing_initialize_rule = getattr(f, INITIALIZE_RULE_MARKER, None)
        if existing_initialize_rule is not None:
            raise InvalidDefinition('An initialization rule cannot have a precondition. ', Settings.default)
        else:
            rule = getattr(f, RULE_MARKER, None)
            if rule is None:
                setattr(precondition_wrapper, PRECONDITION_MARKER, precond)
            else:
                new_rule = Rule(targets=(rule.targets),
                  arguments=(rule.arguments),
                  function=(rule.function),
                  precondition=precond)
            setattr(precondition_wrapper, RULE_MARKER, new_rule)
        invariant = getattr(f, INVARIANT_MARKER, None)
        if invariant is not None:
            new_invariant = Invariant(function=(invariant.function), precondition=precond)
            setattr(precondition_wrapper, INVARIANT_MARKER, new_invariant)
        return precondition_wrapper

    return decorator


@attr.s()
class Invariant:
    function = attr.ib()
    precondition = attr.ib()


def invariant():
    """Decorator to apply an invariant for rules in a RuleBasedStateMachine.
    The decorated function will be run after every rule and can raise an
    exception to indicate failed invariants.

    For example::

        class MyTestMachine(RuleBasedStateMachine):
            state = 1

            @invariant()
            def is_nonzero(self):
                assert self.state != 0
    """

    def accept(f):
        existing_invariant = getattr(f, INVARIANT_MARKER, None)
        if existing_invariant is not None:
            raise InvalidDefinition('A function cannot be used for two distinct invariants.', Settings.default)
        precondition = getattr(f, PRECONDITION_MARKER, None)
        rule = Invariant(function=f, precondition=precondition)

        @proxies(f)
        def invariant_wrapper(*args, **kwargs):
            return f(*args, **kwargs)

        setattr(invariant_wrapper, INVARIANT_MARKER, rule)
        return invariant_wrapper

    return accept


LOOP_LABEL = cu.calc_label_from_name('RuleStrategy loop iteration')

class RuleStrategy(SearchStrategy):

    def __init__(self, machine):
        SearchStrategy.__init__(self)
        self.machine = machine
        self.rules = list(machine.rules())
        self.enabled_rules_strategy = st.shared((FeatureStrategy()),
          key=('enabled rules', machine))
        self.rules.sort(key=(lambda rule: (
         sorted(rule.targets),
         len(rule.arguments),
         rule.function.__name__)))

    def __repr__(self):
        return '%s(machine=%s({...}))' % (
         self.__class__.__name__,
         self.machine.__class__.__name__)

    def do_draw(self, data):
        if not any((self.is_valid(rule) for rule in self.rules)):
            msg = 'No progress can be made from state %r' % (self.machine,)
            raise InvalidDefinition(msg) from None
        feature_flags = data.draw(self.enabled_rules_strategy)
        rule = data.draw(st.sampled_from(self.rules).filter(self.is_valid).filter(lambda r: feature_flags.is_enabled(r.function.__name__)))
        return (
         rule, data.draw(rule.arguments_strategy))

    def is_valid(self, rule):
        if rule.precondition:
            if not rule.precondition(self.machine):
                return False
        for b in rule.bundles:
            bundle = self.machine.bundle(b.name)
            if not bundle:
                return False
            return True


class RuleBasedStateMachine(_GenericStateMachine):
    __doc__ = 'A RuleBasedStateMachine gives you a structured way to define state machines.\n\n    The idea is that a state machine carries a bunch of types of data\n    divided into Bundles, and has a set of rules which may read data\n    from bundles (or just from normal strategies) and push data onto\n    bundles. At any given point a random applicable rule will be\n    executed.\n    '
    _rules_per_class = {}
    _invariants_per_class = {}
    _base_rules_per_class = {}
    _initializers_per_class = {}
    _base_initializers_per_class = {}

    def __init__(self):
        if not self.rules():
            raise InvalidDefinition('Type %s defines no rules' % (type(self).__name__,))
        self.bundles = {}
        self.name_counter = 1
        self.names_to_values = {}
        self._RuleBasedStateMachine__stream = StringIO()
        self._RuleBasedStateMachine__printer = RepresentationPrinter(self._RuleBasedStateMachine__stream)
        self._initialize_rules_to_run = copy(self.initialize_rules())
        self._RuleBasedStateMachine__rules_strategy = RuleStrategy(self)

    def __pretty(self, value):
        if isinstance(value, VarReference):
            return value.name
        self._RuleBasedStateMachine__stream.seek(0)
        self._RuleBasedStateMachine__stream.truncate(0)
        self._RuleBasedStateMachine__printer.output_width = 0
        self._RuleBasedStateMachine__printer.buffer_width = 0
        self._RuleBasedStateMachine__printer.buffer.clear()
        self._RuleBasedStateMachine__printer.pretty(value)
        self._RuleBasedStateMachine__printer.flush()
        return self._RuleBasedStateMachine__stream.getvalue()

    def __repr__(self):
        return '%s(%s)' % (type(self).__name__, nicerepr(self.bundles))

    def upcoming_name(self):
        return 'v%d' % (self.name_counter,)

    def last_names(self, n):
        assert self.name_counter > n
        count = self.name_counter
        return ['v%d' % (i,) for i in range(count - n, count)]

    def new_name(self):
        result = self.upcoming_name()
        self.name_counter += 1
        return result

    def bundle(self, name):
        return self.bundles.setdefault(name, [])

    @classmethod
    def initialize_rules--- This code section failed: ---

 L. 723         0  SETUP_FINALLY        14  'to 14'

 L. 724         2  LOAD_FAST                'cls'
                4  LOAD_ATTR                _initializers_per_class
                6  LOAD_FAST                'cls'
                8  BINARY_SUBSCR    
               10  POP_BLOCK        
               12  RETURN_VALUE     
             14_0  COME_FROM_FINALLY     0  '0'

 L. 725        14  DUP_TOP          
               16  LOAD_GLOBAL              KeyError
               18  COMPARE_OP               exception-match
               20  POP_JUMP_IF_FALSE    32  'to 32'
               22  POP_TOP          
               24  POP_TOP          
               26  POP_TOP          

 L. 726        28  POP_EXCEPT       
               30  JUMP_FORWARD         34  'to 34'
             32_0  COME_FROM            20  '20'
               32  END_FINALLY      
             34_0  COME_FROM            30  '30'

 L. 728        34  LOAD_GLOBAL              inspect
               36  LOAD_METHOD              getmembers
               38  LOAD_FAST                'cls'
               40  CALL_METHOD_1         1  ''
               42  GET_ITER         
             44_0  COME_FROM            70  '70'
               44  FOR_ITER             98  'to 98'
               46  UNPACK_SEQUENCE_2     2 
               48  STORE_FAST               '_'
               50  STORE_FAST               'v'

 L. 729        52  LOAD_GLOBAL              getattr
               54  LOAD_FAST                'v'
               56  LOAD_GLOBAL              INITIALIZE_RULE_MARKER
               58  LOAD_CONST               None
               60  CALL_FUNCTION_3       3  ''
               62  STORE_FAST               'r'

 L. 730        64  LOAD_FAST                'r'
               66  LOAD_CONST               None
               68  COMPARE_OP               is-not
               70  POP_JUMP_IF_FALSE    44  'to 44'

 L. 731        72  LOAD_FAST                'cls'
               74  LOAD_METHOD              define_initialize_rule

 L. 732        76  LOAD_FAST                'r'
               78  LOAD_ATTR                targets

 L. 732        80  LOAD_FAST                'r'
               82  LOAD_ATTR                function

 L. 732        84  LOAD_FAST                'r'
               86  LOAD_ATTR                arguments

 L. 732        88  LOAD_FAST                'r'
               90  LOAD_ATTR                precondition

 L. 731        92  CALL_METHOD_4         4  ''
               94  POP_TOP          
               96  JUMP_BACK            44  'to 44'

 L. 734        98  LOAD_FAST                'cls'
              100  LOAD_ATTR                _base_initializers_per_class
              102  LOAD_METHOD              pop
              104  LOAD_FAST                'cls'
              106  BUILD_LIST_0          0 
              108  CALL_METHOD_2         2  ''
              110  LOAD_FAST                'cls'
              112  LOAD_ATTR                _initializers_per_class
              114  LOAD_FAST                'cls'
              116  STORE_SUBSCR     

 L. 735       118  LOAD_FAST                'cls'
              120  LOAD_ATTR                _initializers_per_class
              122  LOAD_FAST                'cls'
              124  BINARY_SUBSCR    
              126  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `POP_TOP' instruction at offset 24

    @classmethod
    def rules--- This code section failed: ---

 L. 739         0  SETUP_FINALLY        14  'to 14'

 L. 740         2  LOAD_FAST                'cls'
                4  LOAD_ATTR                _rules_per_class
                6  LOAD_FAST                'cls'
                8  BINARY_SUBSCR    
               10  POP_BLOCK        
               12  RETURN_VALUE     
             14_0  COME_FROM_FINALLY     0  '0'

 L. 741        14  DUP_TOP          
               16  LOAD_GLOBAL              KeyError
               18  COMPARE_OP               exception-match
               20  POP_JUMP_IF_FALSE    32  'to 32'
               22  POP_TOP          
               24  POP_TOP          
               26  POP_TOP          

 L. 742        28  POP_EXCEPT       
               30  JUMP_FORWARD         34  'to 34'
             32_0  COME_FROM            20  '20'
               32  END_FINALLY      
             34_0  COME_FROM            30  '30'

 L. 744        34  LOAD_GLOBAL              inspect
               36  LOAD_METHOD              getmembers
               38  LOAD_FAST                'cls'
               40  CALL_METHOD_1         1  ''
               42  GET_ITER         
             44_0  COME_FROM            70  '70'
               44  FOR_ITER             98  'to 98'
               46  UNPACK_SEQUENCE_2     2 
               48  STORE_FAST               '_'
               50  STORE_FAST               'v'

 L. 745        52  LOAD_GLOBAL              getattr
               54  LOAD_FAST                'v'
               56  LOAD_GLOBAL              RULE_MARKER
               58  LOAD_CONST               None
               60  CALL_FUNCTION_3       3  ''
               62  STORE_FAST               'r'

 L. 746        64  LOAD_FAST                'r'
               66  LOAD_CONST               None
               68  COMPARE_OP               is-not
               70  POP_JUMP_IF_FALSE    44  'to 44'

 L. 747        72  LOAD_FAST                'cls'
               74  LOAD_METHOD              define_rule
               76  LOAD_FAST                'r'
               78  LOAD_ATTR                targets
               80  LOAD_FAST                'r'
               82  LOAD_ATTR                function
               84  LOAD_FAST                'r'
               86  LOAD_ATTR                arguments
               88  LOAD_FAST                'r'
               90  LOAD_ATTR                precondition
               92  CALL_METHOD_4         4  ''
               94  POP_TOP          
               96  JUMP_BACK            44  'to 44'

 L. 748        98  LOAD_FAST                'cls'
              100  LOAD_ATTR                _base_rules_per_class
              102  LOAD_METHOD              pop
              104  LOAD_FAST                'cls'
              106  BUILD_LIST_0          0 
              108  CALL_METHOD_2         2  ''
              110  LOAD_FAST                'cls'
              112  LOAD_ATTR                _rules_per_class
              114  LOAD_FAST                'cls'
              116  STORE_SUBSCR     

 L. 749       118  LOAD_FAST                'cls'
              120  LOAD_ATTR                _rules_per_class
              122  LOAD_FAST                'cls'
              124  BINARY_SUBSCR    
              126  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `POP_TOP' instruction at offset 24

    @classmethod
    def invariants--- This code section failed: ---

 L. 753         0  SETUP_FINALLY        14  'to 14'

 L. 754         2  LOAD_FAST                'cls'
                4  LOAD_ATTR                _invariants_per_class
                6  LOAD_FAST                'cls'
                8  BINARY_SUBSCR    
               10  POP_BLOCK        
               12  RETURN_VALUE     
             14_0  COME_FROM_FINALLY     0  '0'

 L. 755        14  DUP_TOP          
               16  LOAD_GLOBAL              KeyError
               18  COMPARE_OP               exception-match
               20  POP_JUMP_IF_FALSE    32  'to 32'
               22  POP_TOP          
               24  POP_TOP          
               26  POP_TOP          

 L. 756        28  POP_EXCEPT       
               30  JUMP_FORWARD         34  'to 34'
             32_0  COME_FROM            20  '20'
               32  END_FINALLY      
             34_0  COME_FROM            30  '30'

 L. 758        34  BUILD_LIST_0          0 
               36  STORE_FAST               'target'

 L. 759        38  LOAD_GLOBAL              inspect
               40  LOAD_METHOD              getmembers
               42  LOAD_FAST                'cls'
               44  CALL_METHOD_1         1  ''
               46  GET_ITER         
             48_0  COME_FROM            74  '74'
               48  FOR_ITER             88  'to 88'
               50  UNPACK_SEQUENCE_2     2 
               52  STORE_FAST               '_'
               54  STORE_FAST               'v'

 L. 760        56  LOAD_GLOBAL              getattr
               58  LOAD_FAST                'v'
               60  LOAD_GLOBAL              INVARIANT_MARKER
               62  LOAD_CONST               None
               64  CALL_FUNCTION_3       3  ''
               66  STORE_FAST               'i'

 L. 761        68  LOAD_FAST                'i'
               70  LOAD_CONST               None
               72  COMPARE_OP               is-not
               74  POP_JUMP_IF_FALSE    48  'to 48'

 L. 762        76  LOAD_FAST                'target'
               78  LOAD_METHOD              append
               80  LOAD_FAST                'i'
               82  CALL_METHOD_1         1  ''
               84  POP_TOP          
               86  JUMP_BACK            48  'to 48'

 L. 763        88  LOAD_FAST                'target'
               90  LOAD_FAST                'cls'
               92  LOAD_ATTR                _invariants_per_class
               94  LOAD_FAST                'cls'
               96  STORE_SUBSCR     

 L. 764        98  LOAD_FAST                'cls'
              100  LOAD_ATTR                _invariants_per_class
              102  LOAD_FAST                'cls'
              104  BINARY_SUBSCR    
              106  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `POP_TOP' instruction at offset 24

    @classmethod
    def define_initialize_rule(cls, targets, function, arguments, precondition=None):
        converted_arguments = {}
        for k, v in arguments.items():
            converted_arguments[k] = v
        else:
            if cls in cls._initializers_per_class:
                target = cls._initializers_per_class[cls]
            else:
                target = cls._base_initializers_per_class.setdefault(cls, [])
            return target.append(Rule(targets, function, converted_arguments, precondition))

    @classmethod
    def define_rule(cls, targets, function, arguments, precondition=None):
        converted_arguments = {}
        for k, v in arguments.items():
            converted_arguments[k] = v
        else:
            if cls in cls._rules_per_class:
                target = cls._rules_per_class[cls]
            else:
                target = cls._base_rules_per_class.setdefault(cls, [])
            return target.append(Rule(targets, function, converted_arguments, precondition))

    def steps(self):
        if self._initialize_rules_to_run:
            return st.one_of([st.tuples(st.just(rule), st.fixed_dictionaries(rule.arguments)) for rule in self._initialize_rules_to_run])
        return self._RuleBasedStateMachine__rules_strategy

    def print_start(self):
        report('state = %s()' % (self.__class__.__name__,))

    def print_end(self):
        report('state.teardown()')

    def print_step(self, step, result):
        rule, data = step
        data_repr = {}
        for k, v in data.items():
            data_repr[k] = self._RuleBasedStateMachine__pretty(v)
        else:
            self.step_count = getattr(self, 'step_count', 0) + 1
            if isinstance(result, MultipleResults):
                n_output_vars = len(result.values)
            else:
                n_output_vars = 1
            output_assignment = '%s = ' % (', '.join(self.last_names(n_output_vars)),) if (rule.targets and n_output_vars >= 1) else ''
            report('%sstate.%s(%s)' % (
             output_assignment,
             rule.function.__name__,
             ', '.join(('%s=%s' % kv for kv in data_repr.items()))))

    def _add_result_to_targets(self, targets, result):
        name = self.new_name()
        self._RuleBasedStateMachine__printer.singleton_pprinters.setdefault(id(result), lambda obj, p, cycle: p.text(name))
        self.names_to_values[name] = result
        for target in targets:
            self.bundle(target).append(VarReference(name))

    def execute_step(self, step):
        rule, data = step
        data = dict(data)
        for k, v in list(data.items()):
            if isinstance(v, VarReference):
                data[k] = self.names_to_values[v.name]
            result = (rule.function)(self, **data)
            if rule.targets:
                if isinstance(result, MultipleResults):
                    for single_result in result.values:
                        self._add_result_to_targets(rule.targets, single_result)

                else:
                    self._add_result_to_targets(rule.targets, result)
            if self._initialize_rules_to_run:
                self._initialize_rules_to_run.remove(rule)
            return result

    def check_invariants(self):
        for invar in self.invariants():
            if invar.precondition and not invar.precondition(self):
                pass
            else:
                invar.function(self)