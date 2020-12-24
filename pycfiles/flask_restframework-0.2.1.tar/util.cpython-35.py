# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/stas/workspace/partners/flask_restframework/flask_restframework/utils/util.py
# Compiled at: 2017-11-03 05:35:30
# Size of source mod 2**32: 410 bytes
import contextlib
from flask_restframework import exceptions

@contextlib.contextmanager
def wrap_mongoengine_errors(updater=None):
    from mongoengine.errors import FieldDoesNotExist, ValidationError
    try:
        yield
    except (FieldDoesNotExist, ValidationError) as e:
        data = e.to_dict()
        if updater:
            data = updater(data)
        raise exceptions.ValidationError(data)