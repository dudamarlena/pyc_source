# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/plecos/plecos.py
# Compiled at: 2019-11-07 16:34:06
# Size of source mod 2**32: 4813 bytes
import json, logging
from pathlib import Path
import jsonschema as jschema, pkg_resources
LOCAL_SCHEMA_FILE = Path(pkg_resources.resource_filename('plecos', 'schemas/metadata_local_v0_4.json'))
if not LOCAL_SCHEMA_FILE.exists():
    raise AssertionError("Can't find schema file {}".format(LOCAL_SCHEMA_FILE))
else:
    REMOTE_SCHEMA_FILE = Path(pkg_resources.resource_filename('plecos', 'schemas/metadata_remote_v0_4.json'))
    assert LOCAL_SCHEMA_FILE.exists(), "Can't find schema file {}".format(REMOTE_SCHEMA_FILE)

def load_serial_data_file_path(file_path):
    file_path_obj = Path(file_path)
    if not Path(file_path_obj).exists():
        raise AssertionError('File path {} does not exist'.format(file_path))
    elif not file_path_obj.is_file():
        raise AssertionError
    if file_path_obj.suffix == '.json':
        with open(file_path_obj) as (fp):
            json_dict = json.load(fp)
        return json_dict


def validator_file(schema_file):
    logging.info('Schema: {}'.format(schema_file))
    this_json_schema_dict = load_serial_data_file_path(schema_file)
    return jschema.validators.Draft7Validator(this_json_schema_dict)


def validator_dict(schema_dict):
    return jschema.validators.Draft7Validator(schema_dict)


def validate_dict(this_json_dict, schema_file):
    validator = validator_file(schema_file)
    return validator.validate(this_json_dict)


def validate_file(json_file_abs_path, schema_file):
    this_json_dict = load_serial_data_file_path(json_file_abs_path)
    return validate_dict(this_json_dict, schema_file)


def validate_file_local(json_file_abs_path):
    return validate_file(json_file_abs_path, LOCAL_SCHEMA_FILE)


def validate_file_remote(json_file_abs_path):
    return validate_file(json_file_abs_path, REMOTE_SCHEMA_FILE)


def validate_dict_local(this_json_dict):
    return validate_dict(this_json_dict, LOCAL_SCHEMA_FILE)


def validate_dict_remote(this_json_dict):
    return validate_dict(this_json_dict, REMOTE_SCHEMA_FILE)


def is_valid_file(json_file_abs_path, schema_file):
    validator = validator_file(schema_file)
    this_json_dict = load_serial_data_file_path(json_file_abs_path)
    return validator.is_valid(this_json_dict)


def is_valid_dict(this_json_dict, schema_file=LOCAL_SCHEMA_FILE):
    validator = validator_file(schema_file)
    return validator.is_valid(this_json_dict)


def is_valid_file_local(json_file_abs_path):
    return is_valid_file(json_file_abs_path, LOCAL_SCHEMA_FILE)


def is_valid_file_remote(json_file_abs_path):
    return is_valid_file(json_file_abs_path, REMOTE_SCHEMA_FILE)


def is_valid_dict_local(this_json_dict):
    return is_valid_dict(this_json_dict, schema_file=LOCAL_SCHEMA_FILE)


def is_valid_dict_remote(this_json_dict):
    return is_valid_dict(this_json_dict, schema_file=REMOTE_SCHEMA_FILE)


def list_errors(json_dict, schema_file):
    """ Iterate over the validation errors, print to log.warn

    :param json_dict:
    :param schema_file:
    :return:
    """
    validator = validator_file(schema_file)
    errors = sorted((validator.iter_errors(json_dict)), key=(lambda e: e.path))
    error_summary = list()
    for i, err in enumerate(errors):
        stack_path = list(err.relative_path)
        stack_path = [str(p) for p in stack_path]
        error_string = 'Error {} at {}'.format(i, '/'.join(stack_path))
        error_summary.append((error_string, err))

    return error_summary


def list_errors_file_local(json_file_abs_path):
    this_json_dict = load_serial_data_file_path(json_file_abs_path)
    return list_errors(this_json_dict, LOCAL_SCHEMA_FILE)


def list_errors_file_remote(json_file_abs_path):
    this_json_dict = load_serial_data_file_path(json_file_abs_path)
    return list_errors(this_json_dict, REMOTE_SCHEMA_FILE)


def list_errors_dict_local(this_json_dict):
    return list_errors(this_json_dict, LOCAL_SCHEMA_FILE)


def list_errors_dict_remote(this_json_dict):
    return list_errors(this_json_dict, REMOTE_SCHEMA_FILE)