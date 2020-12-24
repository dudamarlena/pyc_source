# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.8-intel/egg/dovetail/directives/core.py
# Compiled at: 2012-08-13 23:02:49
"""The core directives."""
from functools import wraps
from dovetail.model import LoadedTask, Dependencies, TaskWrapper, Task
from dovetail.engine import PROCESSOR, STATE
from dovetail.util import Logger, NonZeroReturnCode, Skipped, FailIf
PREDICATE_ARG_CACHE = {}

def call_predicate(predicate, execution):
    """Calls a predicate, resolving whether the predicate uses the optional
    Execution argument, and returns the result of the call.

    This method caches whether the predicate uses the optional argument in
    the PREDICATE_ARG_CACHE.

    :param predicate: A function or callable which, when called,
                      returns True or False
    :type predicate:  function, callable
    :param execution: An Execution object containing current state
    :type execution:  Execution
    :return: The current value of the predicate
    :rtype: boolean
    """
    if type(predicate) == type:
        raise TypeError(('Predicate {0} is a type, not an instance. Perhaps you need to call the constructor').format(predicate))
    try:
        with_arg = PREDICATE_ARG_CACHE[predicate]
    except KeyError:
        from inspect import getargspec
        try:
            spec = getargspec(predicate)
            with_arg = spec[0] or spec[1]
        except TypeError:
            spec = getargspec(predicate.__call__)
            with_arg = len(spec[0]) > 1 or spec[1]

        PREDICATE_ARG_CACHE[predicate] = with_arg

    if with_arg:
        return predicate(execution)
    else:
        return predicate()


def coalesce(predicate, predicates):
    """Internal function to produce a single list from a mandatory predicate
    and an optional list of further predicates.

    :param predicate: A predicate
    :type predicate: function, callable
    :param predicates: A list or iterable of further Predicates, or None
    :type predicates: duck-typed iterable of Predicate
    :return: A list consisting of all Predicates
    :rtype list:
    """
    if predicates is None or len(predicates) == 0:
        return [predicate]
    else:
        result = list(predicates)
        result.insert(0, predicate)
        return result
        return


def task(f):
    """The task directive declares that a function is a Dovetail Task and
    causes an Instance of LoadedTask (subclass of Task) to be instantiated
    and registered in the Dovetail model."""
    task_instance = LoadedTask(f)
    Logger.debug('Loaded ' + str(task_instance))

    @wraps(f)
    def wrapped(*kw, **kwargs):
        """A decorator that prints a warning if a Task is called directly"""
        if PROCESSOR.current_task != task_instance:
            print ('WARNING: {0}() has been called directly rather than by the Dovetail processor').format(f.__name__)
            print '         Dovetail directives and logging may not work as expected.'
            print ("         Use dovetail.build('{0}') instead").format(task_instance.name)
        return f(*kw, **kwargs)

    return wrapped


def depends--- This code section failed: ---

 L. 109         0  LOAD_GLOBAL           0  'any'
                3  LOAD_GENEXPR             '<code_object <genexpr>>'
                6  MAKE_FUNCTION_0       0  None
                9  LOAD_DEREF            0  'tasks'
               12  GET_ITER         
               13  CALL_FUNCTION_1       1  None
               16  CALL_FUNCTION_1       1  None
               19  UNARY_NOT        
               20  POP_JUMP_IF_TRUE     32  'to 32'
               23  LOAD_ASSERT              AssertionError

 L. 113        26  LOAD_CONST               '@depends: Each argument must be a Task, the name of a Task or a function implementing a Task'
               29  RAISE_VARARGS_2       2  None

 L. 115        32  LOAD_CLOSURE          0  'tasks'
               38  LOAD_CODE                <code_object run_once>
               41  MAKE_CLOSURE_0        0  None
               44  STORE_FAST            1  'run_once'

 L. 121        47  LOAD_FAST             1  'run_once'
               50  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `RETURN_VALUE' instruction at offset 50


def do_if--- This code section failed: ---

 L. 130         0  LOAD_GLOBAL           0  'coalesce'
                3  LOAD_FAST             0  'predicate'
                6  LOAD_DEREF            0  'predicates'
                9  CALL_FUNCTION_2       2  None
               12  STORE_DEREF           0  'predicates'

 L. 131        15  LOAD_GLOBAL           1  'any'
               18  LOAD_GENEXPR             '<code_object <genexpr>>'
               21  MAKE_FUNCTION_0       0  None
               24  LOAD_DEREF            0  'predicates'
               27  GET_ITER         
               28  CALL_FUNCTION_1       1  None
               31  CALL_FUNCTION_1       1  None
               34  UNARY_NOT        
               35  POP_JUMP_IF_TRUE     47  'to 47'
               38  LOAD_ASSERT              AssertionError

 L. 133        41  LOAD_CONST               '@do_if: All predicate arguments must be callable'
               44  RAISE_VARARGS_2       2  None

 L. 134        47  LOAD_CLOSURE          0  'predicates'
               53  LOAD_CODE                <code_object before>
               56  MAKE_CLOSURE_0        0  None
               59  STORE_FAST            2  'before'

 L. 144        62  LOAD_GLOBAL           3  'TaskWrapper'
               65  LOAD_ATTR             4  'decorator_maker'
               68  LOAD_CONST               '@do_if'
               71  LOAD_CONST               'before'
               74  LOAD_FAST             2  'before'
               77  CALL_FUNCTION_257   257  None
               80  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `RETURN_VALUE' instruction at offset 80


def skip_if--- This code section failed: ---

 L. 161         0  LOAD_GLOBAL           0  'coalesce'
                3  LOAD_FAST             0  'predicate'
                6  LOAD_DEREF            0  'predicates'
                9  CALL_FUNCTION_2       2  None
               12  STORE_DEREF           0  'predicates'

 L. 162        15  LOAD_GLOBAL           1  'any'
               18  LOAD_GENEXPR             '<code_object <genexpr>>'
               21  MAKE_FUNCTION_0       0  None
               24  LOAD_DEREF            0  'predicates'
               27  GET_ITER         
               28  CALL_FUNCTION_1       1  None
               31  CALL_FUNCTION_1       1  None
               34  UNARY_NOT        
               35  POP_JUMP_IF_TRUE     47  'to 47'
               38  LOAD_ASSERT              AssertionError

 L. 164        41  LOAD_CONST               "@skip_if: All predicate arguments must be callable. Did you mean to set working='message'?"
               44  RAISE_VARARGS_2       2  None

 L. 165        47  LOAD_GLOBAL           3  'len'
               50  LOAD_FAST             2  'kwargs'
               53  CALL_FUNCTION_1       1  None
               56  POP_JUMP_IF_TRUE    108  'to 108'

 L. 166        59  BUILD_LIST_0          0 
               62  LOAD_DEREF            0  'predicates'
               65  GET_ITER         
               66  FOR_ITER             18  'to 87'
               69  STORE_FAST            0  'predicate'
               72  LOAD_GLOBAL           4  'str'
               75  LOAD_FAST             0  'predicate'
               78  CALL_FUNCTION_1       1  None
               81  LIST_APPEND           2  None
               84  JUMP_BACK            66  'to 66'
               87  STORE_FAST            3  'string'

 L. 167        90  LOAD_CONST               'and '
               93  LOAD_ATTR             5  'join'
               96  LOAD_FAST             3  'string'
               99  CALL_FUNCTION_1       1  None
              102  STORE_DEREF           1  'message'
              105  JUMP_FORWARD         58  'to 166'

 L. 168       108  LOAD_GLOBAL           3  'len'
              111  LOAD_FAST             2  'kwargs'
              114  CALL_FUNCTION_1       1  None
              117  LOAD_CONST               1
              120  COMPARE_OP            2  ==
              123  POP_JUMP_IF_FALSE   139  'to 139'

 L. 169       126  LOAD_FAST             2  'kwargs'
              129  LOAD_CONST               'message'
              132  BINARY_SUBSCR    
              133  STORE_DEREF           1  'message'
              136  JUMP_FORWARD         27  'to 166'

 L. 171       139  LOAD_GLOBAL           3  'len'
              142  LOAD_FAST             2  'kwargs'
              145  CALL_FUNCTION_1       1  None
              148  LOAD_CONST               1
              151  COMPARE_OP            1  <=
              154  POP_JUMP_IF_TRUE    166  'to 166'
              157  LOAD_ASSERT              AssertionError
              160  LOAD_CONST               "kwargs may contain only a single argument, 'message'"
              163  RAISE_VARARGS_2       2  None
            166_0  COME_FROM           136  '136'
            166_1  COME_FROM           105  '105'

 L. 173       166  LOAD_CLOSURE          0  'predicates'
              169  LOAD_CLOSURE          1  'message'
              175  LOAD_CODE                <code_object before>
              178  MAKE_CLOSURE_0        0  None
              181  STORE_FAST            4  'before'

 L. 187       184  LOAD_GLOBAL           6  'TaskWrapper'
              187  LOAD_ATTR             7  'decorator_maker'
              190  LOAD_CONST               '@skip_if'
              193  LOAD_CONST               'before'
              196  LOAD_FAST             4  'before'
              199  CALL_FUNCTION_257   257  None
              202  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `COME_FROM' instruction at offset 166_0


def fail_if--- This code section failed: ---

 L. 206         0  LOAD_GLOBAL           0  'coalesce'
                3  LOAD_FAST             0  'predicate'
                6  LOAD_DEREF            0  'predicates'
                9  CALL_FUNCTION_2       2  None
               12  STORE_DEREF           0  'predicates'

 L. 207        15  LOAD_GLOBAL           1  'any'
               18  LOAD_GENEXPR             '<code_object <genexpr>>'
               21  MAKE_FUNCTION_0       0  None
               24  LOAD_DEREF            0  'predicates'
               27  GET_ITER         
               28  CALL_FUNCTION_1       1  None
               31  CALL_FUNCTION_1       1  None
               34  UNARY_NOT        
               35  POP_JUMP_IF_TRUE     47  'to 47'
               38  LOAD_ASSERT              AssertionError

 L. 209        41  LOAD_CONST               "@fail_if: All predicate arguments must be callable. Did you mean to set working='message'?"
               44  RAISE_VARARGS_2       2  None

 L. 210        47  LOAD_GLOBAL           3  'len'
               50  LOAD_FAST             2  'kwargs'
               53  CALL_FUNCTION_1       1  None
               56  POP_JUMP_IF_TRUE     68  'to 68'

 L. 211        59  LOAD_CONST               None
               62  STORE_DEREF           1  'message'
               65  JUMP_FORWARD         58  'to 126'

 L. 212        68  LOAD_GLOBAL           3  'len'
               71  LOAD_FAST             2  'kwargs'
               74  CALL_FUNCTION_1       1  None
               77  LOAD_CONST               1
               80  COMPARE_OP            2  ==
               83  POP_JUMP_IF_FALSE    99  'to 99'

 L. 213        86  LOAD_FAST             2  'kwargs'
               89  LOAD_CONST               'message'
               92  BINARY_SUBSCR    
               93  STORE_DEREF           1  'message'
               96  JUMP_FORWARD         27  'to 126'

 L. 215        99  LOAD_GLOBAL           3  'len'
              102  LOAD_FAST             2  'kwargs'
              105  CALL_FUNCTION_1       1  None
              108  LOAD_CONST               1
              111  COMPARE_OP            1  <=
              114  POP_JUMP_IF_TRUE    126  'to 126'
              117  LOAD_ASSERT              AssertionError
              120  LOAD_CONST               "kwargs may contain only a single argument, 'message'"
              123  RAISE_VARARGS_2       2  None
            126_0  COME_FROM            96  '96'
            126_1  COME_FROM            65  '65'

 L. 218       126  LOAD_CLOSURE          0  'predicates'
              129  LOAD_CLOSURE          1  'message'
              135  LOAD_CODE                <code_object after>
              138  MAKE_CLOSURE_0        0  None
              141  STORE_FAST            3  'after'

 L. 236       144  LOAD_GLOBAL           5  'TaskWrapper'
              147  LOAD_ATTR             6  'decorator_maker'
              150  LOAD_CONST               '@fail_if'
              153  LOAD_CONST               'after'
              156  LOAD_FAST             3  'after'
              159  CALL_FUNCTION_257   257  None
              162  RETURN_VALUE     

Parse error at or near `COME_FROM' instruction at offset 126_0


class Not(object):
    """A negation predicate which wraps another predicate.

    :class:`Not` instances are callable, optionally with an :class:`dovetail.engine.Execution`.
    Their return value is the boolean negation of the predicate which they wrap.

    Not's value is evaluated on demand, not when it is instantiated::

        n = Not(Env("BASH"))
        print p()    # Evaluation occurs here"""

    def __init__(self, predicate):
        self.predicate = predicate

    def __call__(self, execution=None):
        return not call_predicate(self.predicate, execution)

    def __str__(self):
        return ('Not({0})').format(self.predicate)


class Any(object):
    r"""A predicate that evaluates to True if any of its arguments is True.

    :class:`Any` instances are callable, optionally with an :class:`dovetail.engine.Execution`.
    This predicate has the same semantics as Pythons :func:`any` function.

    Instantiate with a comma separated list of predicates, or use Python's
    \*kw argument modifier::

        a = Any(p1, p2, p3)

    Or::

        l = [ p1, p2, p3 ]
        a = Any(*l)

    Any's value is evaluated on demand, not when it is instantiated::

        print a()
    """

    def __init__(self, *predicates):
        self.predicates = predicates

    def __call__(self, execution=None):
        return any(call_predicate(predicate, execution) for predicate in self.predicates)

    def __str__(self):
        string = (', ').join(str(predicate) for predicate in self.predicates)
        return ('Any({0})').format(string)


class All(object):
    r"""A predicate that returns True if all of its arguments are True.

    :class:`Any` instances are callable, optionally with an :class:`dovetail.engine.Execution`.
    This predicate has the same semantics as Pythons :func:`all` function.

    Instantiate with a comma separated list of predicates, or use Python's
    \*kw argument modifier::

        a = All(p1, p2, p3)

    Or::

        l = [ p1, p2, p3 ]
        a = All(*l)

    Any's value is evaluated on demand, not when it is instantiated::

        print a()
    """

    def __init__(self, *predicates):
        self.predicates = predicates

    def __call__(self, execution=None):
        return all([ call_predicate(predicate, execution) for predicate in self.predicates ])

    def __str__(self):
        string = (', ').join(str(predicate) for predicate in self.predicates)
        return ('All({0})').format(string)


def check_result(f):
    """Checks the return of the decorated function as if it were a shell script - anything
    other than None or 0 is considered an error and an exception will be thrown.

    This is similar to the longer::

        @fail_if(Not(ResultZero()))

    but issues a more specific message and exception"""

    def after(execution, result):
        """Implementation of the algorithm described in check_result()"""
        if execution.state in [STATE.SKIPPED, STATE.ABORTED, STATE.FAILED, STATE.REPEATED]:
            Logger.log(('@check_result: skipping because the task is {0}').format(execution.state))
        if result is None or result == 0:
            Logger.debug('@check_result: Zero/None return')
        else:
            Logger.major(('@check_result: FAILING: Non-zero return value: {0}').format(result))
            execution.fail(NonZeroReturnCode(('Function {0} returned {1}').format(f.__name__, result)))
        return

    return TaskWrapper.decorate('@check_result', f, after=after)


def fail_if_skipped(f):
    """If the wrapped Task was skipped by any directive, the Task will be failed.

    This is useful to force an error if the environment is, for example, not correct.

    This is similar to the longer::

        @fail_if(StateSkipped())

    but issues a more specific message and exception"""

    def after(execution, result):
        """Implementation of the algorithm described in fail_if_skipped"""
        if execution.state == STATE.SKIPPED:
            Logger.major('@fail_if_skipped: FAILING')
            reason = (' and ').join(execution.skip_reasons)
            execution.fail(Skipped(('{0} was skipped because {1}').format(execution.task, reason)))
        else:
            Logger.debug('@fail_if_skipped: Task was not skipped')

    return TaskWrapper.decorate('@fail_if_skipped', f, after=after)