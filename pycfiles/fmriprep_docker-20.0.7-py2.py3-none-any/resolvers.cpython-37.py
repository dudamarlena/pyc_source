# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-aejasjrz/pip/pip/_vendor/resolvelib/resolvers.py
# Compiled at: 2020-05-05 12:41:47
# Size of source mod 2**32: 14481 bytes
import collections
from .providers import AbstractResolver
from .structs import DirectedGraph
RequirementInformation = collections.namedtuple('RequirementInformation', ['requirement', 'parent'])

class ResolverException(Exception):
    __doc__ = 'A base class for all exceptions raised by this module.\n\n    Exceptions derived by this class should all be handled in this module. Any\n    bubbling pass the resolver should be treated as a bug.\n    '


class RequirementsConflicted(ResolverException):

    def __init__(self, criterion):
        super(RequirementsConflicted, self).__init__(criterion)
        self.criterion = criterion

    def __str__(self):
        return 'Requirements conflict: {}'.format(', '.join((repr(r) for r in self.criterion.iter_requirement())))


class InconsistentCandidate(ResolverException):

    def __init__(self, candidate, criterion):
        super(InconsistentCandidate, self).__init__(candidate, criterion)
        self.candidate = candidate
        self.criterion = criterion

    def __str__(self):
        return 'Provided candidate {!r} does not satisfy {}'.format(self.candidate, ', '.join((repr(r) for r in self.criterion.iter_requirement())))


class Criterion(object):
    __doc__ = 'Representation of possible resolution results of a package.\n\n    This holds three attributes:\n\n    * `information` is a collection of `RequirementInformation` pairs.\n      Each pair is a requirement contributing to this criterion, and the\n      candidate that provides the requirement.\n    * `incompatibilities` is a collection of all known not-to-work candidates\n      to exclude from consideration.\n    * `candidates` is a collection containing all possible candidates deducted\n      from the union of contributing requirements and known incompatibilities.\n      It should never be empty, except when the criterion is an attribute of a\n      raised `RequirementsConflicted` (in which case it is always empty).\n\n    .. note::\n        This class is intended to be externally immutable. **Do not** mutate\n        any of its attribute containers.\n    '

    def __init__(self, candidates, information, incompatibilities):
        self.candidates = candidates
        self.information = information
        self.incompatibilities = incompatibilities

    def __repr__(self):
        requirements = ', '.join(('{!r} from {!r}'.format(req, parent) for req, parent in self.information))
        return '<Criterion {}>'.format(requirements)

    @classmethod
    def from_requirement(cls, provider, requirement, parent):
        """Build an instance from a requirement.
        """
        candidates = provider.find_matches(requirement)
        criterion = cls(candidates=candidates,
          information=[
         RequirementInformation(requirement, parent)],
          incompatibilities=[])
        if not candidates:
            raise RequirementsConflicted(criterion)
        return criterion

    def iter_requirement(self):
        return (i.requirement for i in self.information)

    def iter_parent(self):
        return (i.parent for i in self.information)

    def merged_with(self, provider, requirement, parent):
        """Build a new instance from this and a new requirement.
        """
        infos = list(self.information)
        infos.append(RequirementInformation(requirement, parent))
        candidates = [c for c in self.candidates if provider.is_satisfied_by(requirement, c)]
        criterion = type(self)(candidates, infos, list(self.incompatibilities))
        if not candidates:
            raise RequirementsConflicted(criterion)
        return criterion

    def excluded_of(self, candidate):
        """Build a new instance from this, but excluding specified candidate.

        Returns the new instance, or None if we still have no valid candidates.
        """
        incompats = list(self.incompatibilities)
        incompats.append(candidate)
        candidates = [c for c in self.candidates if c != candidate]
        if not candidates:
            return
        criterion = type(self)(candidates, list(self.information), incompats)
        return criterion


class ResolutionError(ResolverException):
    pass


class ResolutionImpossible(ResolutionError):

    def __init__(self, causes):
        super(ResolutionImpossible, self).__init__(causes)
        self.causes = causes


class ResolutionTooDeep(ResolutionError):

    def __init__(self, round_count):
        super(ResolutionTooDeep, self).__init__(round_count)
        self.round_count = round_count


State = collections.namedtuple('State', 'mapping criteria')

class Resolution(object):
    __doc__ = 'Stateful resolution object.\n\n    This is designed as a one-off object that holds information to kick start\n    the resolution process, and holds the results afterwards.\n    '

    def __init__(self, provider, reporter):
        self._p = provider
        self._r = reporter
        self._states = []

    @property
    def state(self):
        try:
            return self._states[(-1)]
        except IndexError:
            raise AttributeError('state')

    def _push_new_state(self):
        """Push a new state into history.

        This new state will be used to hold resolution results of the next
        coming round.
        """
        try:
            base = self._states[(-1)]
        except IndexError:
            state = State(mapping=(collections.OrderedDict()), criteria={})
        else:
            state = State(mapping=(base.mapping.copy()),
              criteria=(base.criteria.copy()))
        self._states.append(state)

    def _merge_into_criterion(self, requirement, parent):
        self._r.adding_requirement(requirement)
        name = self._p.identify(requirement)
        try:
            crit = self.state.criteria[name]
        except KeyError:
            crit = Criterion.from_requirement(self._p, requirement, parent)
        else:
            crit = crit.merged_with(self._p, requirement, parent)
        return (
         name, crit)

    def _get_criterion_item_preference(self, item):
        name, criterion = item
        try:
            pinned = self.state.mapping[name]
        except KeyError:
            pinned = None

        return self._p.get_preference(pinned, criterion.candidates, criterion.information)

    def _is_current_pin_satisfying(self, name, criterion):
        try:
            current_pin = self.state.mapping[name]
        except KeyError:
            return False
        else:
            return all((self._p.is_satisfied_by(r, current_pin) for r in criterion.iter_requirement()))

    def _get_criteria_to_update(self, candidate):
        criteria = {}
        for r in self._p.get_dependencies(candidate):
            name, crit = self._merge_into_criterion(r, parent=candidate)
            criteria[name] = crit

        return criteria

    def _attempt_to_pin_criterion(self, name, criterion):
        causes = []
        for candidate in reversed(criterion.candidates):
            try:
                criteria = self._get_criteria_to_update(candidate)
            except RequirementsConflicted as e:
                try:
                    causes.append(e.criterion)
                    continue
                finally:
                    e = None
                    del e

            self._r.pinning(candidate)
            self.state.mapping.pop(name, None)
            self.state.mapping[name] = candidate
            self.state.criteria.update(criteria)
            if not self._is_current_pin_satisfying(name, criterion):
                raise InconsistentCandidate(candidate, criterion)
            return []

        return causes

    def _backtrack(self):
        while len(self._states) >= 3:
            del self._states[-1]
            name, candidate = self._states.pop().mapping.popitem()
            self._r.backtracking(candidate)
            self._push_new_state()
            criterion = self.state.criteria[name].excluded_of(candidate)
            if criterion is None:
                continue
            self.state.criteria[name] = criterion
            return True

        return False

    def resolve(self, requirements, max_rounds):
        if self._states:
            raise RuntimeError('already resolved')
        self._push_new_state()
        for r in requirements:
            try:
                name, crit = self._merge_into_criterion(r, parent=None)
            except RequirementsConflicted as e:
                try:
                    raise ResolutionImpossible(e.criterion.information)
                finally:
                    e = None
                    del e

            self.state.criteria[name] = crit

        self._r.starting()
        for round_index in range(max_rounds):
            self._r.starting_round(round_index)
            self._push_new_state()
            curr = self.state
            unsatisfied_criterion_items = [item for item in self.state.criteria.items() if not (self._is_current_pin_satisfying)(*item)]
            if not unsatisfied_criterion_items:
                del self._states[-1]
                self._r.ending(curr)
                return self.state
                name, criterion = min(unsatisfied_criterion_items,
                  key=(self._get_criterion_item_preference))
                failure_causes = self._attempt_to_pin_criterion(name, criterion)
                if failure_causes:
                    result = self._backtrack()
                    if not result:
                        causes = [i for crit in failure_causes for i in crit.information]
                        raise ResolutionImpossible(causes)
                self._r.ending_round(round_index, curr)

        raise ResolutionTooDeep(max_rounds)


def _has_route_to_root(criteria, key, all_keys, connected):
    if key in connected:
        return True
    if key not in criteria:
        return False
    for p in criteria[key].iter_parent():
        try:
            pkey = all_keys[id(p)]
        except KeyError:
            continue

        if pkey in connected:
            connected.add(key)
            return True
            if _has_route_to_root(criteria, pkey, all_keys, connected):
                connected.add(key)
                return True

    return False


Result = collections.namedtuple('Result', 'mapping graph criteria')

def _build_result(state):
    mapping = state.mapping
    all_keys = {id(v):k for k, v in mapping.items()}
    all_keys[id(None)] = None
    graph = DirectedGraph()
    graph.add(None)
    connected = {
     None}
    for key, criterion in state.criteria.items():
        if not _has_route_to_root(state.criteria, key, all_keys, connected):
            continue
        if key not in graph:
            graph.add(key)
        for p in criterion.iter_parent():
            try:
                pkey = all_keys[id(p)]
            except KeyError:
                continue

            if pkey not in graph:
                graph.add(pkey)
            graph.connect(pkey, key)

    return Result(mapping={k:v for k, v in mapping.items() if k in connected}, graph=graph,
      criteria=(state.criteria))


class Resolver(AbstractResolver):
    __doc__ = 'The thing that performs the actual resolution work.\n    '
    base_exception = ResolverException

    def resolve(self, requirements, max_rounds=100):
        """Take a collection of constraints, spit out the resolution result.

        The return value is a representation to the final resolution result. It
        is a tuple subclass with three public members:

        * `mapping`: A dict of resolved candidates. Each key is an identifier
            of a requirement (as returned by the provider's `identify` method),
            and the value is the resolved candidate.
        * `graph`: A `DirectedGraph` instance representing the dependency tree.
            The vertices are keys of `mapping`, and each edge represents *why*
            a particular package is included. A special vertex `None` is
            included to represent parents of user-supplied requirements.
        * `criteria`: A dict of "criteria" that hold detailed information on
            how edges in the graph are derived. Each key is an identifier of a
            requirement, and the value is a `Criterion` instance.

        The following exceptions may be raised if a resolution cannot be found:

        * `ResolutionImpossible`: A resolution cannot be found for the given
            combination of requirements. The `causes` attribute of the
            exception is a list of (requirement, parent), giving the
            requirements that could not be satisfied.
        * `ResolutionTooDeep`: The dependency tree is too deeply nested and
            the resolver gave up. This is usually caused by a circular
            dependency, but you can try to resolve this by increasing the
            `max_rounds` argument.
        """
        resolution = Resolution(self.provider, self.reporter)
        state = resolution.resolve(requirements, max_rounds=max_rounds)
        return _build_result(state)