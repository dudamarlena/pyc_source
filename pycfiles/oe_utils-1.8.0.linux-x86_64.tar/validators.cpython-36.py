# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/claeyswo/Envs/env_oe_utils/lib/python3.6/site-packages/oe_utils/validation/validators.py
# Compiled at: 2020-03-25 06:12:47
# Size of source mod 2**32: 1398 bytes
import logging
from cornice import validators
from oe_utils.validation import ValidationFailure
LOG = logging.getLogger(__name__)

def schema_validator(request, schema=None, deserializer=None, **kwargs):
    """
    Validate the request against the configured schema.

    This method exists because the default cornice validators do not bind the
    request to the schema, and our schemas need it often. For example to get
    the database session to validate database ids.
    """
    if schema is None:
        return
    schema = schema.bind(request=request)
    (validators.colander_validator)(request, schema=schema, deserializer=deserializer, **kwargs)


def cornice_error_handler(request):
    """
    Handle validation errors in a OE-compatible way.

    This mimics the behaviour in other applications who use manual validation
    The 2nd parameter of ValidationFailure in other applications is normally
    `colander.Invalid.asdict()`. Here we replicate this output from the errors
    given by cornice in `request.errors`.
    """
    service_name = request.current_service.name
    raise ValidationFailure('Fouten bij het valideren van de {} request.'.format(service_name), {error['location'] + '.' + error['name']:error['description'] for error in request.errors})