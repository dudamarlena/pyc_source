# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/chrisrink/Projects/dataspec/src/dataspec/base.py
# Compiled at: 2020-04-10 13:55:29
# Size of source mod 2**32: 24124 bytes
import functools, inspect, re, sys
from abc import ABC, abstractmethod
from collections import namedtuple
from enum import EnumMeta
from itertools import chain
from typing import Any, Callable, FrozenSet, Generic, Iterable, Iterator, List, Mapping, MutableMapping, NamedTuple, Optional, Sequence, Set, Tuple, Type, TypeVar, Union, cast
import attr
T = TypeVar('T')
V = TypeVar('V')

class Invalid:
    pass


INVALID = Invalid()
Conformer = Callable[([T], Union[(V, Invalid)])]
PredicateFn = Callable[([Any], bool)]
ValidatorFn = Callable[([Any], Iterable['ErrorDetails'])]
Tag = str
SpecPredicate = Union[(
 Mapping[(Any, 'SpecPredicate')],
 Tuple[('SpecPredicate', Ellipsis)],
 List['SpecPredicate'],
 FrozenSet[Any],
 Set[Any],
 PredicateFn,
 ValidatorFn,
 'Spec')]
NO_ERROR_PATH = object()

@attr.s(auto_attribs=True, slots=True)
class ErrorDetails:
    message: str
    pred: SpecPredicate
    value: Any
    via = attr.ib(factory=list)
    via: List[Tag]
    path = attr.ib(factory=list)
    path: List[Any]

    def with_details(self, tag: Tag, loc: Any=NO_ERROR_PATH) -> 'ErrorDetails':
        """
        Add the given tag to the `via` list and add a key path if one is specified by
        the caller.

        This method mutates the `via` and `path` list attributes directly rather than
        returning a new `ErrorDetails` instance.
        """
        self.via.insert(0, tag)
        if loc is not NO_ERROR_PATH:
            self.path.insert(0, loc)
        return self


@attr.s(auto_attribs=True, slots=True)
class ValidationError(Exception):
    errors: Sequence[ErrorDetails]


class Spec(ABC):

    @property
    @abstractmethod
    def tag(self) -> Tag:
        """
        Return the tag used to identify this Spec.

        Tags are useful for debugging and in validation messages.
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def _conformer(self) -> Optional[Conformer]:
        """Return the custom conformer for this Spec."""
        raise NotImplementedError

    @property
    def conformer(self) -> Conformer:
        """Return the conformer attached to this Spec."""
        return self._conformer or self._default_conform

    @abstractmethod
    def validate(self, v: Any) -> Iterator[ErrorDetails]:
        """
        Validate the value `v` against the Spec.

        Yields an iterable of Spec failures, if any.
        """
        raise NotImplementedError

    def validate_ex(self, v: Any):
        """
        Validate the value `v` against the Spec.

        Throws a `ValidationError` with a list of Spec failures, if any.
        """
        errors = list(self.validate(v))
        if errors:
            raise ValidationError(errors)

    def is_valid(self, v: Any) -> bool:
        """Returns True if `v` is valid according to the Spec, otherwise returns
        False."""
        try:
            next(self.validate(v))
        except StopIteration:
            return True
        else:
            return False

    def _default_conform(self, v):
        """
        Default conformer for the Spec.

        If no custom conformer is specified, this conformer will be invoked.
        """
        return v

    def conform_valid(self, v):
        """
        Conform `v` to the Spec without checking if v is valid first and return the
        possibly conformed value or `INVALID` if the value cannot be conformed.

        This function should be used only if `v` has already been check for validity.
        """
        return self.conformer(v)

    def conform(self, v: Any):
        """Conform `v` to the Spec, first checking if v is valid, and return the
        possibly conformed value or `INVALID` if the value cannot be conformed."""
        if self.is_valid(v):
            return self.conform_valid(v)
        else:
            return INVALID

    def with_conformer(self, conformer: Conformer) -> 'Spec':
        """Return a new Spec instance with the new conformer."""
        return attr.evolve(self, conformer=conformer)

    def with_tag(self, tag: Tag) -> 'Spec':
        """Return a new Spec instance with the new tag applied."""
        return attr.evolve(self, tag=tag)


@attr.s(auto_attribs=True, frozen=True, slots=True)
class ValidatorSpec(Spec):
    __doc__ = 'Validator Specs yield richly detailed errors from their validation functions and\n    can be useful for answering more detailed questions about their their input data\n    than a simple predicate function.'
    tag: Tag
    _validate: ValidatorFn
    _conformer = None
    _conformer: Optional[Conformer]

    def validate(self, v) -> Iterator[ErrorDetails]:
        try:
            yield from _enrich_errors(self._validate(v), self.tag)
        except Exception as e:
            yield ErrorDetails(message=f"Exception occurred during Validation: {e}",
              pred=self,
              value=v,
              via=[
             self.tag])

    @classmethod
    def from_validators(cls, tag: Tag, *preds: Union[(ValidatorFn, 'ValidatorSpec')], conformer: Optional[Conformer]=None) -> 'ValidatorSpec':
        """Return a single Validator spec from the composition of multiple validator
        functions or ValidatorSpec instances."""
        assert len(preds) > 0, 'At least on predicate must be specified'
        if len(preds) == 1:
            if isinstance(preds[0], ValidatorSpec):
                return preds[0]
            return ValidatorSpec(tag, (preds[0]), conformer=conformer)
        else:
            specs = []
            for pred in preds:
                if isinstance(pred, ValidatorSpec):
                    specs.append(pred)
                else:
                    specs.append(ValidatorSpec(pred.__name__, pred))

            def do_validate(v):
                for spec in specs:
                    yield from spec.validate(v)

                if False:
                    yield None

            return cls(tag, do_validate, compose_conformers(*specs, **{'conform_final': conformer}))


@attr.s(auto_attribs=True, frozen=True, slots=True)
class PredicateSpec(Spec):
    __doc__ = '\n    Predicate Specs are useful for validating data with a boolean predicate function.\n\n    Predicate specs can be useful for validating simple yes/no questions about data, but\n    the errors they can produce are limited by the nature of the predicate return value.\n    '
    tag: Tag
    _pred: PredicateFn
    _conformer = None
    _conformer: Optional[Conformer]

    def validate(self, v) -> Iterator[ErrorDetails]:
        try:
            if not self._pred(v):
                yield ErrorDetails(message=f"Value '{v}' does not satisfy predicate '{self.tag or self._pred}'",
                  pred=(self._pred),
                  value=v,
                  via=[
                 self.tag])
        except Exception as e:
            yield ErrorDetails(message=f"Exception occurred during Validation: {e}",
              pred=self,
              value=v)


@attr.s(auto_attribs=True, frozen=True, slots=True)
class CollSpec(Spec):
    tag: Tag
    _spec: Spec
    _conformer = None
    _conformer: Optional[Conformer]
    _out_type = None
    _out_type: Optional[Type]
    _validate_coll = None
    _validate_coll: Optional[ValidatorSpec]

    @classmethod
    def from_val(cls, tag: Optional[Tag], sequence: Sequence[Union[(SpecPredicate, Mapping[(str, Any)])]], conformer: Conformer=None):
        spec = make_spec(sequence[0])
        validate_coll = None
        try:
            kwargs = sequence[1]
            if not isinstance(kwargs, dict):
                raise TypeError('Collection spec options must be a dict')
        except IndexError:
            kwargs = {}

        validators = []
        allow_str = kwargs.get('allow_str', False)
        maxlength = kwargs.get('maxlength', None)
        minlength = kwargs.get('minlength', None)
        count = kwargs.get('count', None)
        type_ = kwargs.get('kind', None)
        out_type = kwargs.get('into', None)
        if not allow_str:
            if type_ is None:

                @pred_to_validator('Collection is a string, not a collection')
                def coll_is_str(v) -> bool:
                    return isinstance(v, str)

                validators.append(coll_is_str)
        if maxlength is not None:
            if not isinstance(maxlength, int):
                raise TypeError('Collection maxlength spec must be an integer length')
            if maxlength < 0:
                raise ValueError('Collection maxlength spec cannot be less than 0')

            @pred_to_validator(f"Collection length {{value}} exceeds max length {maxlength}",
              convert_value=len)
            def coll_has_max_length(v):
                return len(v) > maxlength

            validators.append(coll_has_max_length)
        if minlength is not None:
            if not isinstance(minlength, int):
                raise TypeError('Collection minlength spec must be an integer length')
            if minlength < 0:
                raise ValueError('Collection minlength spec cannot be less than 0')

            @pred_to_validator(f"Collection length {{value}} does not meet minimum length {minlength}",
              convert_value=len)
            def coll_has_min_length(v):
                return len(v) < minlength

            validators.append(coll_has_min_length)
        if minlength is not None:
            if maxlength is not None:
                if minlength > maxlength:
                    raise ValueError('Cannot define a spec with minlength greater than maxlength')
        if count is not None:
            if not isinstance(count, int):
                raise TypeError('Collection count spec must be an integer length')
            else:
                if count < 0:
                    raise ValueError('Collection count spec cannot be less than 0')
                if minlength is not None or maxlength is not None:
                    raise ValueError('Cannot define a collection spec with count and minlength or maxlength')

            @pred_to_validator(f"Collection length does not equal {count}",
              convert_value=len)
            def coll_is_exactly_len(v):
                return len(v) != count

            validators.append(coll_is_exactly_len)
        if type_:
            if isinstance(type_, type):

                @pred_to_validator(f"Collection is not of type {type_}",
                  complement=True,
                  convert_value=type)
                def coll_is_type(v):
                    return isinstance(v, type_)

                validators.append(coll_is_type)
        if validators:
            validate_coll = (ValidatorSpec.from_validators)(*('coll', ), *validators)
        return cls((tag or 'coll'),
          spec=spec,
          conformer=conformer,
          out_type=out_type,
          validate_coll=validate_coll)

    def validate(self, v) -> Iterator[ErrorDetails]:
        if self._validate_coll:
            yield from _enrich_errors(self._validate_coll.validate(v), self.tag)
        for i, e in enumerate(v):
            yield from _enrich_errors(self._spec.validate(e), self.tag, i)

        if False:
            yield None

    def _default_conform(self, v):
        return self._out_type or type(v)(self._spec.conform(e) for e in v)


@attr.s(auto_attribs=True, frozen=True, slots=(sys.version_info >= (3, 7)))
class OptionalKey(Generic[T]):
    key: T


@attr.s(auto_attribs=True, frozen=True, slots=True)
class DictSpec(Spec):
    tag: Tag
    _reqkeyspecs = attr.ib(factory=dict)
    _reqkeyspecs: Mapping[(Any, Spec)]
    _optkeyspecs = attr.ib(factory=dict)
    _optkeyspecs: Mapping[(Any, Spec)]
    _conformer = None
    _conformer: Optional[Conformer]

    @classmethod
    def from_val(cls, tag: Optional[Tag], kvspec: Mapping[(str, SpecPredicate)], conformer: Conformer=None):
        reqkeys = {}
        optkeys = {}
        for k, v in kvspec.items():
            if isinstance(k, OptionalKey):
                optkeys[k.key] = make_spec(v)
            else:
                reqkeys[k] = make_spec(v)

        return cls((tag or 'map'),
          reqkeyspecs=reqkeys, optkeyspecs=optkeys, conformer=conformer)

    def validate(self, d) -> Iterator[ErrorDetails]:
        try:
            for k, vspec in self._reqkeyspecs.items():
                if k in d:
                    yield from _enrich_errors(vspec.validate(d[k]), self.tag, k)
                else:
                    yield ErrorDetails(message=f"Mapping missing key {k}",
                      pred=vspec,
                      value=d,
                      via=[
                     self.tag],
                      path=[
                     k])

        except TypeError:
            yield ErrorDetails(message='Value is not a mapping type',
              pred=self,
              value=d,
              via=[
             self.tag])
            return
        else:
            for k, vspec in self._optkeyspecs.items():
                if k in d:
                    yield from _enrich_errors(vspec.validate(d[k]), self.tag, k)

    def _default_conform(self, d):
        conformed_d = {}
        for k, spec in self._reqkeyspecs.items():
            conformed_d[k] = spec.conform(d[k])

        for k, spec in self._optkeyspecs.items():
            if k in d:
                conformed_d[k] = spec.conform(d[k])

        return conformed_d


class ObjectSpec(DictSpec):

    def validate(self, o) -> Iterator[ErrorDetails]:
        for k, vspec in self._reqkeyspecs.items():
            if hasattr(o, k):
                yield from _enrich_errors(vspec.validate(getattr(o, k)), self.tag, k)
            else:
                yield ErrorDetails(message=f"Object missing attribute '{k}'",
                  pred=vspec,
                  value=o,
                  via=[
                 self.tag],
                  path=[
                 k])

        for k, vspec in self._optkeyspecs.items():
            if hasattr(o, k):
                yield from _enrich_errors(vspec.validate(getattr(o, k)), self.tag, k)

    def _default_conform(self, o):
        raise TypeError('Cannot use a default conformer for an Object')


def _enum_conformer(e: EnumMeta) -> Conformer:
    """Create a conformer for Enum types which accepts Enum instances, Enum values,
    and Enum names."""

    def conform_enum(v):
        try:
            return e(v)
        except ValueError:
            try:
                return e[v]
            except KeyError:
                return INVALID

    return conform_enum


@attr.s(auto_attribs=True, frozen=True, slots=True)
class SetSpec(Spec):
    tag: Tag
    _values: Union[(Set, FrozenSet)]
    _conformer = None
    _conformer: Optional[Conformer]

    def validate(self, v) -> Iterator[ErrorDetails]:
        if v not in self._values:
            yield ErrorDetails(message=f"Value '{v}' not in '{self._values}'",
              pred=(self._values),
              value=v,
              via=[
             self.tag])


@attr.s(auto_attribs=True, frozen=True, slots=True)
class TupleSpec(Spec):
    tag: Tag
    _pred: Tuple[(SpecPredicate, ...)]
    _specs: Tuple[(Spec, ...)]
    _conformer = None
    _conformer: Optional[Conformer]
    _namedtuple = None
    _namedtuple: Optional[Type[NamedTuple]]

    @classmethod
    def from_val(cls, tag: Optional[Tag], pred: Tuple[(SpecPredicate, ...)], conformer: Conformer=None):
        specs = tuple(make_spec(e_pred) for e_pred in pred)
        spec_tags = tuple(re.sub(_MUNGE_NAMES, '_', spec.tag) for spec in specs)
        if tag is not None:
            if len(specs) == len(set(spec_tags)):
                namedtuple_type = namedtuple(re.sub(_MUNGE_NAMES, '_', tag), spec_tags)
        else:
            namedtuple_type = None
        return cls((tag or 'tuple'),
          pred=pred,
          specs=specs,
          conformer=conformer,
          namedtuple=namedtuple_type)

    def validate(self, t) -> Iterator[ErrorDetails]:
        try:
            if len(t) != len(self._specs):
                yield ErrorDetails(message=f"Expected {len(self._specs)} values; found {len(t)}",
                  pred=self,
                  value=(len(t)),
                  via=[
                 self.tag])
                return
            for i, (e_pred, elem) in enumerate(zip(self._specs, t)):
                yield from _enrich_errors(e_pred.validate(elem), self.tag, i)

        except TypeError:
            yield ErrorDetails(message='Value is not a tuple type',
              pred=self,
              value=t,
              via=[self.tag])

    def _default_conform(self, v):
        return self._namedtuple and self._namedtuple._make or tuple(spec.conform(v) for spec, v in zip(self._specs, v))


def _enrich_errors(errors: Iterable[ErrorDetails], tag: Tag, loc: Any=NO_ERROR_PATH) -> Iterable[ErrorDetails]:
    """
    Enrich the stream of errors with tag and location information.

    Tags are useful for determining which specs were evaluated to produce the error.
    Location information can help callers pinpoint exactly where in their data structure
    the error occurred. If no location information is relevant for the error (perhaps
    for a scalar spec type), then the default `NO_ERROR_PATH` should be used.
    """
    for error in errors:
        yield error.with_details(tag, loc=loc)


def compose_conformers(*specs: Spec, conform_final: Optional[Conformer]=None) -> Conformer:
    """
    Return a single conformer which is the composition of the conformers from each of
    the child specs.

    Apply the `conform_final` conformer on the final return from the composition, if
    any.
    """

    def do_conform(v):
        conformed_v = v
        for spec in specs:
            conformed_v = spec.conform(conformed_v)
            if conformed_v is INVALID:
                break

        if conform_final is None:
            return conformed_v
        else:
            return conform_final(conformed_v)

    return do_conform


_MUNGE_NAMES = re.compile('[\\s|-]')

def _complement(pred: PredicateFn) -> PredicateFn:
    """Return the complement to the predicate function `pred`."""

    @functools.wraps(pred)
    def complement(v):
        return not pred(v)

    return complement


def _identity(x: T) -> T:
    """Return the argument."""
    return x


def pred_to_validator(message: str, complement: bool=False, convert_value: Callable[([Any], Any)]=_identity, **fmtkwargs) -> Callable[([PredicateFn], ValidatorFn)]:
    """
    Decorator which converts a simple predicate function to a validator function.

    If the wrapped predicate returns a truthy value, the wrapper function will emit a
    single :py:class:`dataspec.base.ErrorDetails` object with the ``message`` format
    string interpolated with the failing value as ``value`` (possibly subject to
    conversion by the optional keyword argument ``convert_value``) and any other
    key/value pairs from ``fmtkwargs``.

    If ``complement`` keyword argument is ``True``, the return value of the decorated
    predicate will be converted as by Python's ``not`` operator and the return value
    will be used to determine whether or not an error has occurred. This is a
    convenient way to negate a predicate function without having to modify the function
    itself.

    :param message: a format string which will be the base error message in the
        resulting :py:class:`dataspec.base.ErrorDetails` object
    :param complement: if :py:obj:`True`, the boolean complement of the decorated
        function's return value will indicate failure
    :param convert_value: an optional function which can convert the value before
        interpolating it into the error message
    :param fmtkwargs: optional key/value pairs which will be interpolated into
        the error message
    :return: a validator function which can be fed into a
        :py:class:`dataspec.base.ValidatorSpec`
    """
    assert 'value' not in fmtkwargs, "Key 'value' is not allowed in pred format kwargs"

    def to_validator(pred):
        pred = _complement(pred) if complement else pred

        @functools.wraps(pred)
        def validator(v):
            if pred(v):
                yield ErrorDetails(message=(message.format)(value=convert_value(v), **fmtkwargs),
                  pred=pred,
                  value=v)

        return validator

    return to_validator


def type_spec(tag: Optional[Tag]=None, tp: Type=object, conformer: Optional[Conformer]=None) -> Spec:
    """Return a spec that validates inputs are instances of tp."""

    @pred_to_validator(f"Value '{{value}}' is not a {tp.__name__}", complement=True)
    def is_instance_of_type(v):
        return isinstance(v, tp)

    return ValidatorSpec((tag or f"is_{tp.__name__}"),
      is_instance_of_type, conformer=conformer)


def make_spec(*args: Union[(Tag, SpecPredicate)], conformer: Optional[Conformer]=None) -> Spec:
    """Return a new Spec from the given predicate or spec."""
    tag = args[0] if isinstance(args[0], str) else None
    pred = args[0] if tag is None else args[1]
    if isinstance(pred, (frozenset, set)):
        return SetSpec((tag or 'set'), pred, conformer=conformer)
    if isinstance(pred, EnumMeta):
        return SetSpec((tag or pred.__name__),
          (frozenset(chain.from_iterable([mem, mem.name, mem.value] for mem in pred))),
          conformer=(conformer or _enum_conformer(pred)))
    if isinstance(pred, tuple):
        return TupleSpec.from_val(tag, pred, conformer=conformer)
    if isinstance(pred, list):
        return CollSpec.from_val(tag, pred, conformer=conformer)
    if isinstance(pred, dict):
        return DictSpec.from_val(tag, pred, conformer=conformer)
    else:
        if isinstance(pred, Spec):
            if conformer is not None:
                return pred.with_conformer(conformer)
            else:
                return pred
        elif isinstance(pred, type):
            return type_spec(tag, pred, conformer=conformer)
        else:
            if callable(pred):
                try:
                    sig = inspect.signature(pred)
                except (TypeError, ValueError):
                    sig = None

                if sig is not None:
                    if sig.return_annotation is Iterator[ErrorDetails]:
                        return ValidatorSpec((tag or pred.__name__),
                          (cast(ValidatorFn, pred)), conformer=conformer)
                return PredicateSpec((tag or pred.__name__),
                  (cast(PredicateFn, pred)), conformer=conformer)
            else:
                raise TypeError(f"Expected some spec predicate; received type {type(pred)}")