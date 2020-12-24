# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/opentargets_validator/validator.py
# Compiled at: 2020-03-05 04:39:23
from __future__ import absolute_import
from __future__ import unicode_literals
from builtins import str
import logging, simplejson as json, multiprocessing, hashlib
from .helpers import generate_validator_from_schema
import pypeln, functools

def validate_start(schema_uri):
    validator = generate_validator_from_schema(schema_uri)
    logger = logging.getLogger(__name__)
    return (validator, logger)


def validator_mapped(data, validator, logger):
    line_counter, line = data
    try:
        parsed_line = json.loads(line)
    except Exception as e:
        logger.error(b'failed parsing line %i: %s %s', line_counter, line, e)
        return (line_counter, None, None)

    validation_errors = [ ((b'.').join(error.absolute_path), error.message) for error in validator.iter_errors(parsed_line) ]
    hash_line = hashlib.md5(json.dumps(parsed_line[b'unique_association_fields'], sort_keys=True).encode(b'utf-8')).hexdigest()
    return (
     line_counter, validation_errors, hash_line)


def validate(file_descriptor, schema_uri, do_hash):
    logger = logging.getLogger(__name__)
    hash_lines = dict()
    input_valid = True
    cpus = multiprocessing.cpu_count()
    is_file_fine = False
    stage = pypeln.process.map(validator_mapped, enumerate(file_descriptor, start=1), on_start=functools.partial(validate_start, schema_uri), workers=cpus, maxsize=1000)
    for line_counter, validation_errors, hash_line in stage:
        is_file_fine = True
        line_valid = True
        if validation_errors:
            line_valid = False
            input_valid = False
            for path, message in validation_errors:
                logger.error(b'fail @ %i.%s %s', line_counter, path, message)

        if do_hash and line_valid:
            if hash_line in hash_lines:
                line_valid = False
                input_valid = False
                line_min = min(line_counter, hash_lines[hash_line])
                line_max = max(line_counter, hash_lines[hash_line])
                logger.error(b'Duplicate hashes %d and %d ', line_min, line_max)
            else:
                hash_lines[hash_line] = line_counter

    if not is_file_fine:
        logger.error(b'Issue with input file, probably because it was empty')
        input_valid = False
    return input_valid