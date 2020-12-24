# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/lucaswiman/opensource/django-predicate/predicate/type_inference/inference.py
# Compiled at: 2016-04-07 03:58:36
from django.db import models
from django.db.models.constants import LOOKUP_SEP
from predicate.lookup_utils import get_field_and_accessor
from predicate.type_inference.field_registry import registry
from predicate.type_inference.field_registry import Relation
from predicate.type_inference.utils import is_specialization_of
from predicate.type_inference.utils import Nullable

def _infer(model, lookup_parts, inference_dict=None):
    """
    Return an inference path for the given lookup parts relative to the given lookup_parts.
    """
    if inference_dict is None:
        inference_dict = {'__type__': model, '__field__': None, 
           '__accessor__': None}
    if not lookup_parts:
        return inference_dict
    else:
        lookup, remainder = lookup_parts[0], lookup_parts[1:]
        if lookup not in inference_dict:
            if not issubclass(model, models.Model):
                model = Nullable.get_model(model)
            field, accessor = get_field_and_accessor(model, lookup)
            inferred_type = registry.get_type_for_field(field)
            inference_dict[lookup] = {'__type__': inferred_type, 
               '__field__': field, 
               '__accessor__': accessor}
        else:
            inferred_type = inference_dict[lookup]['__type__']
        if remainder:
            if is_specialization_of(inferred_type, Relation):
                inferred_type = inferred_type.__parameters__[0]
            _infer(inferred_type, remainder, inference_dict[lookup])
        return inference_dict


def infer(instance_or_model, *lookups):
    """
    Takes a list of lookups, and returns a ``Type`` object describing the attributes
    that are relevant to those lookups. ``ManyToManyField`` and reverse foreign key
    relations are modeled as ``QuerySet[T]`` (inherits from ``Iterable``), and
    ``Model`` classes are modeled as a ``NamedTuple`` with the fields used in the
    given lookups.  It is _not_ the case that models actually match the given type
    object, but the type object gives a reasonable structure for reasoning about the
    structure of the underlying models.
    """
    inference_dict = None
    if isinstance(instance_or_model, models.Model):
        model = type(instance_or_model)
    else:
        model = instance_or_model
    for lookup in lookups:
        inference_dict = _infer(model, lookup.split(LOOKUP_SEP))

    return inference_dict


def get_values(instance, *lookups):
    raise NotImplementedError