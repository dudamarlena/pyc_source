# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\User\AppData\Local\Temp\pip-install-oj_abz_z\hypothesis\hypothesis\errors.py
# Compiled at: 2020-01-12 08:06:33
# Size of source mod 2**32: 5761 bytes


class HypothesisException(Exception):
    __doc__ = 'Generic parent class for exceptions thrown by Hypothesis.'


class CleanupFailed(HypothesisException):
    __doc__ = 'At least one cleanup task failed and no other exception was raised.'


class UnsatisfiedAssumption(HypothesisException):
    __doc__ = "An internal error raised by assume.\n\n    If you're seeing this error something has gone wrong.\n    "


class NoSuchExample(HypothesisException):
    __doc__ = 'The condition we have been asked to satisfy appears to be always false.\n\n    This does not guarantee that no example exists, only that we were\n    unable to find one.\n    '

    def __init__(self, condition_string, extra=''):
        super().__init__('No examples found of condition %s%s' % (condition_string, extra))


class Unsatisfiable(HypothesisException):
    __doc__ = 'We ran out of time or examples before we could find enough examples\n    which satisfy the assumptions of this hypothesis.\n\n    This could be because the function is too slow. If so, try upping\n    the timeout. It could also be because the function is using assume\n    in a way that is too hard to satisfy. If so, try writing a custom\n    strategy or using a better starting point (e.g if you are requiring\n    a list has unique values you could instead filter out all duplicate\n    values from the list)\n    '


class Flaky(HypothesisException):
    __doc__ = "This function appears to fail non-deterministically: We have seen it\n    fail when passed this example at least once, but a subsequent invocation\n    did not fail.\n\n    Common causes for this problem are:\n        1. The function depends on external state. e.g. it uses an external\n           random number generator. Try to make a version that passes all the\n           relevant state in from Hypothesis.\n        2. The function is suffering from too much recursion and its failure\n           depends sensitively on where it's been called from.\n        3. The function is timing sensitive and can fail or pass depending on\n           how long it takes. Try breaking it up into smaller functions which\n           don't do that and testing those instead.\n    "


class InvalidArgument(HypothesisException, TypeError):
    __doc__ = 'Used to indicate that the arguments to a Hypothesis function were in\n    some manner incorrect.'


class ResolutionFailed(InvalidArgument):
    __doc__ = 'Hypothesis had to resolve a type to a strategy, but this failed.\n\n    Type inference is best-effort, so this only happens when an\n    annotation exists but could not be resolved for a required argument\n    to the target of ``builds()``, or where the user passed ``infer``.\n    '


class InvalidState(HypothesisException):
    __doc__ = 'The system is not in a state where you were allowed to do that.'


class InvalidDefinition(HypothesisException, TypeError):
    __doc__ = 'Used to indicate that a class definition was not well put together and\n    has something wrong with it.'


class HypothesisWarning(HypothesisException, Warning):
    __doc__ = 'A generic warning issued by Hypothesis.'


class FailedHealthCheck(HypothesisWarning):
    __doc__ = 'Raised when a test fails a preliminary healthcheck that occurs before\n    execution.'

    def __init__(self, message, check):
        super().__init__(message)
        self.health_check = check


class NonInteractiveExampleWarning(HypothesisWarning):
    __doc__ = 'SearchStrategy.example() is designed for interactive use,\n    but should never be used in the body of a test.\n    '


class HypothesisDeprecationWarning(HypothesisWarning, FutureWarning):
    __doc__ = 'A deprecation warning issued by Hypothesis.\n\n    Actually inherits from FutureWarning, because DeprecationWarning is\n    hidden by the default warnings filter.\n\n    You can configure the Python :mod:`python:warnings` to handle these\n    warnings differently to others, either turning them into errors or\n    suppressing them entirely.  Obviously we would prefer the former!\n    '


class Frozen(HypothesisException):
    __doc__ = 'Raised when a mutation method has been called on a ConjectureData object\n    after freeze() has been called.'


class MultipleFailures(HypothesisException):
    __doc__ = 'Indicates that Hypothesis found more than one distinct bug when testing\n    your code.'


class DeadlineExceeded(HypothesisException):
    __doc__ = 'Raised when an individual test body has taken too long to run.'

    def __init__(self, runtime, deadline):
        super().__init__('Test took %.2fms, which exceeds the deadline of %.2fms' % (
         runtime.total_seconds() * 1000, deadline.total_seconds() * 1000))
        self.runtime = runtime
        self.deadline = deadline


class StopTest(BaseException):
    __doc__ = 'Raised when a test should stop running and return control to\n    the Hypothesis engine, which should then continue normally.\n    '

    def __init__(self, testcounter):
        super().__init__(repr(testcounter))
        self.testcounter = testcounter


class DidNotReproduce(HypothesisException):
    pass


class Found(Exception):
    __doc__ = 'Signal that the example matches condition. Internal use only.'
    hypothesis_internal_never_escalate = True