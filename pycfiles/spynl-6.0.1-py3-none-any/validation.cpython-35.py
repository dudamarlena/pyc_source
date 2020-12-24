# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nicolas/workspace/spynl-git/venv/src/spynl/spynl/main/validation.py
# Compiled at: 2017-02-02 09:30:23
# Size of source mod 2**32: 6002 bytes
"""
support checking Spynl request or response data against schemas
"""
import os, json
from functools import wraps
import jsonschema
from spynl.main.utils import get_logger, get_settings, get_yaml_from_docstring
from spynl.main.exceptions import InvalidResponse, BadValidationInstructions
from spynl.main.locale import SpynlTranslationString as _

def validate_json_schema(endpoint, info):
    """
    Validate JSON in- and output against a schema
    if the endpoint definition says so.

    This is a view deriver for Spynl endpoints.
    """
    if info.options.get('is_error_view', False) is True:
        return endpoint

    @wraps(endpoint)
    def validate(context, request):
        """Function wrapping our endpoint."""
        yaml_doc = get_yaml_from_docstring(endpoint.__doc__)
        validations = []
        if yaml_doc and 'validations' in yaml_doc:
            validations = yaml_doc['validations']
        if request.content_type == 'application/json' and hasattr(request, 'args'):
            interprete_validation_instructions(request.args, validations, 'request')
        response = endpoint(context, request)
        if request.response.content_type == 'application/json':
            interprete_validation_instructions(json.loads(response.text), validations, 'response')
        return response

    return validate


validate_json_schema.options = ('is_error_view', )

def interprete_validation_instructions(json_data, validations, req_res):
    """
    Run JSON schema validations against JSON data.

    The validations list consists of dictionaries with the following spec:
      - schema: my-schema.json   [required]
        apply-to: some-key       [optional, applies to all data of not given
        in: response             [required, one of (request|response)]
        repeat: True             [optional, defaults to False]

    Schema files are expected to reside in the folder 'docs/docson/schemas'.
    The policy is to raise Exceptions when the validation instructions are
    malformed, but only log warnings when validation cannot happen.
    """
    if not validations:
        return
    logger = get_logger(__name__)
    if not isinstance(validations, list):
        raise BadValidationInstructions(_('validations-is-not-list', default='Validations should be a list.'))
    else:
        for validation in validations:
            for required in ('schema', 'in'):
                if required not in validation:
                    raise BadValidationInstructions(_('bad-validation-instructions-missing-field', default='Missing field: ${field}', mapping={'field': required}))

            if validation['in'] not in ('request', 'response'):
                raise BadValidationInstructions(_('bad-validation-instructions-setting-in', 'Setting "in" should be either "request" or "response"'))
            if validation['in'] != req_res:
                pass
            else:
                data = json_data
                if 'apply-to' in validation:
                    data = json_data[validation['apply-to']]
                if 'repeat' in validation and validation['repeat']:
                    if not isinstance(data, list):
                        logger.warning('Validation for schema %s cannot be repeated on %s (type %s).', validation['schema'], validation['apply-to'], type(data))
                    else:
                        for dat in data:
                            apply_schema(dat, validation['schema'])

                else:
                    apply_schema(data, validation['schema'])


def apply_schema(data, schema_name):
    """Find and apply a JSON schema to JSON data and deal with any problems."""
    logger = get_logger(__name__)
    settings = get_settings()
    p2s = '%s/%s' % (os.environ.get('VIRTUAL_ENV', ''),
     settings.get('spynl.schemas', '').strip())
    schema_path = os.path.join(p2s, schema_name)
    if os.path.exists(schema_path):
        schema_str = open(schema_path, 'r').read()
        our_file = '"file:{}/shared/'.format(p2s)
        schema_str = schema_str.replace('"./shared/', our_file)
        schema_str = schema_str.replace('"/shared/', our_file)
        schema = json.loads(schema_str)
        try:
            if not isinstance(data, dict):
                logger.warning('The data %s cannot be validatedagainst a schema', data)
            jsonschema.validate(data, schema)
        except (KeyError, jsonschema.ValidationError) as val_exc:
            raise InvalidResponse(_('invalid-response', default=val_exc.message))
        except (AttributeError, jsonschema.SchemaError) as sch_exc:
            logger.error('The schema %s is not valid: %s.', schema_path, str(sch_exc))
            raise BadValidationInstructions(_('bad-validation-instructions-bad-schema', default='The schema ${schema} is not valid', mapping={'schema': schema_name}))

    else:
        logger.error('The schema %s could not be found.', schema_path)
        raise BadValidationInstructions(_('bad-validation-instructions-schema-not-found', default='The required schema ${schema} could not be found to perform validation.', mapping={'schema': schema_name}))