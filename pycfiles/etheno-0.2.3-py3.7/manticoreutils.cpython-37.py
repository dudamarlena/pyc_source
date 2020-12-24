# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/etheno/manticoreutils.py
# Compiled at: 2019-06-27 23:49:12
# Size of source mod 2**32: 5293 bytes
import inspect, itertools, pkg_resources
from . import manticoreclient
del manticoreclient
from manticore.core.smtlib.operators import AND
from manticore.ethereum import ManticoreEVM, Detector
import manticore.ethereum.detectors

def manticore_version():
    return pkg_resources.get_distribution('manticore').version


def manticore_is_new_enough(*required_version):
    """Checks if Manticore is newer than the given version. Returns True or False if known, or None if uncertain."""
    if required_version is None or len(required_version) == 0:
        required_version = (0, 2, 2)
    try:
        version = manticore_version()
        version = list(map(int, version.split('.')))
        for v, required in itertools.zip_longest(version, required_version, fillvalue=0):
            if v < required:
                return False
                if v > required:
                    return True

    except Exception:
        return
    else:
        return True


if manticore_is_new_enough(0, 2, 3):
    DETECTOR_BLACKLIST = {
     manticore.ethereum.detectors.DetectDelegatecall,
     manticore.ethereum.detectors.DetectEnvInstruction,
     manticore.ethereum.detectors.DetectExternalCallAndLeak,
     manticore.ethereum.detectors.DetectIntegerOverflow,
     manticore.ethereum.detectors.DetectInvalid,
     manticore.ethereum.detectors.DetectRaceCondition,
     manticore.ethereum.detectors.DetectReentrancyAdvanced,
     manticore.ethereum.detectors.DetectReentrancySimple,
     manticore.ethereum.detectors.DetectSuicidal,
     manticore.ethereum.detectors.DetectUninitializedMemory,
     manticore.ethereum.detectors.DetectUninitializedStorage,
     manticore.ethereum.detectors.DetectUnusedRetVal}
else:
    DETECTOR_BLACKLIST = set()

def get_detectors():
    for name, obj in inspect.getmembers(manticore.ethereum.detectors):
        if inspect.isclass(obj) and issubclass(obj, manticore.ethereum.detectors.Detector) and obj != manticore.ethereum.detectors.Detector and obj not in DETECTOR_BLACKLIST:
            yield obj


def register_all_detectors(manticore):
    for detector in get_detectors():
        try:
            manticore.register_detector(detector())
        except Exception as e:
            try:
                manticore.logger.warning(f"Unable to register detector {detector!r}: {e!s}")
            finally:
                e = None
                del e


class StopAtDepth(Detector):
    __doc__ = 'This just aborts explorations that are too deep'

    def __init__(self, max_depth):
        self.max_depth = max_depth
        stop_at_death = self

        def will_start_run_callback(*args):
            with stop_at_death.manticore.locked_context('seen_rep', dict) as (reps):
                reps.clear()

        if manticore_is_new_enough(0, 3, 0):
            self.will_run_callback = will_start_run_callback
        else:
            self.will_start_run_callback = will_start_run_callback
        super().__init__()

    def will_decode_instruction_callback(self, state, pc):
        world = state.platform
        with self.manticore.locked_context('seen_rep', dict) as (reps):
            item = (
             world.current_transaction.sort == 'CREATE', world.current_transaction.address, pc)
            if item not in reps:
                reps[item] = 0
            reps[item] += 1
            if reps[item] > self.max_depth:
                state.abandon()


class ManticoreTest:

    def __init__(self, state, expression):
        self.state = state
        self.expression = expression

    def __bool__(self):
        return self.can_be_true()

    def can_be_true(self):
        return self.state.can_be_true(self.expression)

    def _solve_one(self, *variables, initial_state):
        with initial_state as (state):
            state.constrain(self.expression)
            for v in variables:
                value = state.solve_one(v)
                yield value
                state.constrain(v == value)

    def solve_one(self, *variables):
        """Finds a solution to the state and returns all of the variables in that solution"""
        return (self._solve_one)(*variables, **{'initial_state': self.state})

    def solve_all(self, *variables):
        """Enumerates all solutions to the state for the given variables"""
        with self.state as (state):
            while state.can_be_true(self.expression):
                solution = tuple((self._solve_one)(*variables, **{'initial_state': state}))
                if len(solution) < len(variables):
                    break
                yield solution
                state.constrain(AND(*(v != s for v, s in zip(variables, solution))))

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


if __name__ == '__main__':
    print('Available Manticore Detectors:')
    for detector in get_detectors():
        print('  %s' % detector)