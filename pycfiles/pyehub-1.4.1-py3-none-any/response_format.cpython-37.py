# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/juancomish/miniconda3/lib/python3.7/site-packages/pyehub/data_formats/response_format.py
# Compiled at: 2019-07-03 19:21:52
# Size of source mod 2**32: 3402 bytes
__doc__ = '\nProvides functionality for handling the response format.\n\nExamples:\n\n    If you want to validate a dictionary against the response format::\n\n    >>> from data_formats import response_format\n    >>> example = {}\n    >>> response_format.validate(example)\n    Traceback (most recent call last):\n        ...\n    data_formats.response_format.ResponseValidationError\n'
from typing import Dict, Any, Union
import jsonschema
from energy_hub.param_var import ConstantOrVar
from pylp import Variable, Status
SCHEMA = {'type':'object', 
 'properties':{'version':{'description':'The SemVer version number for the format', 
   'type':'string', 
   'enum':[
    '0.1.0']}, 
  'solution':{'type': 'object'}, 
  'solver':{'type':'object', 
   'properties':{'termination_condition':{'type': 'string'}, 
    'time':{'type':'number', 
     'minimum':0}}, 
   'required':[
    'termination_condition', 'time'], 
   'additionalProperties':False}}, 
 'required':[
  'version', 'solution', 'solver'], 
 'additionalProperties':False}

class ResponseValidationError(Exception):
    """ResponseValidationError"""
    pass


def _is_valid_json_type(json: Any) -> bool:
    if json is None:
        return True
    return any((isinstance(json, t) for t in [str, float, int, dict, list]))


def _is_valid(mapping: Union[(dict, list, str, float, int)]) -> bool:
    if isinstance(mapping, list):
        return all((_is_valid(x) for x in mapping))
    if isinstance(mapping, dict):
        return all((_is_valid(key) and _is_valid(value) for key, value in mapping.items()))
    return _is_valid_json_type(mapping)


def validate(instance: dict) -> None:
    """
    Validate the instance against the schema.

    Args:
        instance: The potential instance of the schema

    Raises:
        ValidationError: the instance does not match the schema
    """
    if not _is_valid(instance):
        raise ResponseValidationError
    try:
        jsonschema.validate(instance, SCHEMA)
    except jsonschema.ValidationError as exc:
        try:
            raise ResponseValidationError from exc
        finally:
            exc = None
            del exc


def _get_value(value: Any) -> Any:
    if isinstance(value, Variable):
        return value.evaluate()
    if isinstance(value, range):
        return list(value)
    if isinstance(value, ConstantOrVar):
        return _get_value(value.values)
    if isinstance(value, dict):
        return {key:_get_value(value) for key, value in value.items()}
    return value


def _get_stuff(model: Dict) -> Dict[(str, Any)]:
    return {name:_get_value(value) for name, value in model.items()}


def create_response(status: Status, model: Dict) -> Dict[(str, Any)]:
    """
    Create a new response format dictionary.

    Args:
        status: The status of the problem
        model: A dictionary of the variables and their values that were used in
            the model
    """
    result = {'version':'0.1.0', 
     'solver':{'termination_condition':status.status, 
      'time':status.time}, 
     'solution':_get_stuff(model)}
    validate(result)
    return result