# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/f1nal/Dropbox/python/jet-bridge/src/packages/jet_bridge_base/jet_bridge_base/utils/exceptions.py
# Compiled at: 2019-11-08 11:55:37
# Size of source mod 2**32: 1945 bytes
import re, six
from sqlalchemy import inspect
from jet_bridge_base.exceptions.validation_error import ValidationError

def serialize_validation_error(exc):

    def process(e, root=False):
        if isinstance(e.detail, dict):
            return dict(map(lambda x: (x[0], process(x[1])), e.detail.items()))
        else:
            if isinstance(e.detail, list):
                return list(map(lambda x: process(x), e.detail))
            if root:
                return {'non_field_errors': [e.detail]}
            return e.detail

    return process(exc, root=True)


def validation_error_from_database_error(e, model):
    if hasattr(e, 'orig') and hasattr(e.orig, 'args') and hasattr(e.orig.args, '__getitem__'):
        if len(e.orig.args) == 1:
            message = e.orig.args[0]
        else:
            if len(e.orig.args) == 2:
                message = e.orig.args[1]
            else:
                message = e.orig.args
            message = six.text_type(message)
            regex = [
             [
              'Key\\s\\((.+)\\)=\\((.+)\\)\\salready\\sexists', 1, 2],
             [
              "Duplicate\\sentry\\s\\'(.+)\\'\\sfor key\\s\\'(.+)\\'", 2, 1],
             [
              'UNIQUE\\sconstraint\\sfailed\\:\\s(.+)\\.(.+)', 2, None]]
            for r, field_index, value_index in regex:
                match = re.search(r, message, re.IGNORECASE | re.MULTILINE)
                if match:
                    mapper = inspect(model)
                    columns = dict(map(lambda x: (x.key, x), mapper.columns))
                    column_name = match.group(field_index)
                    if column_name in columns:
                        error = dict()
                        error[column_name] = ValidationError('record with the same value already exists')
                        return ValidationError(error)

            return ValidationError(message)
        return ValidationError('Query failed')