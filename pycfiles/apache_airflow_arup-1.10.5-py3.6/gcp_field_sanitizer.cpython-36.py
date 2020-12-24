# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/utils/gcp_field_sanitizer.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 6103 bytes
"""Sanitizer for body fields sent via GCP API.

The sanitizer removes fields specified from the body.

Context
-------
In some cases where GCP operation requires modification of existing resources (such
as instances or instance templates) we need to sanitize body of the resources returned
via GCP APIs. This is in the case when we retrieve information from GCP first,
modify the body and either update the existing resource or create a new one with the
modified body. Usually when you retrieve resource from GCP you get some extra fields which
are Output-only, and we need to delete those fields if we want to use
the body as input for subsequent create/insert type operation.

Field specification
-------------------

Specification of fields is an array of strings which denote names of fields to be removed.
The field can be either direct field name to remove from the body or the full
specification of the path you should delete - separated with '.'

>>> FIELDS_TO_SANITIZE = [
>>>    "kind",
>>>    "properties.disks.kind",
>>>    "properties.metadata.kind",
>>>]
>>> body = {
>>>     "kind": "compute#instanceTemplate",
>>>     "name": "instance",
>>>     "properties": {
>>>         "disks": [
>>>             {
>>>                 "name": "a",
>>>                 "kind": "compute#attachedDisk",
>>>                 "type": "PERSISTENT",
>>>                 "mode": "READ_WRITE",
>>>             },
>>>             {
>>>                 "name": "b",
>>>                 "kind": "compute#attachedDisk",
>>>                 "type": "PERSISTENT",
>>>                 "mode": "READ_WRITE",
>>>             }
>>>         ],
>>>         "metadata": {
>>>             "kind": "compute#metadata",
>>>             "fingerprint": "GDPUYxlwHe4="
>>>         },
>>>     }
>>> }
>>> sanitizer=GcpBodyFieldSanitizer(FIELDS_TO_SANITIZE)
>>> SANITIZED_BODY = sanitizer.sanitize(body)
>>> json.dumps(SANITIZED_BODY, indent=2)
{
    "name":  "instance",
    "properties": {
        "disks": [
            {
                "name": "a",
                "type": "PERSISTENT",
                "mode": "READ_WRITE",
            },
            {
                "name": "b",
                "type": "PERSISTENT",
                "mode": "READ_WRITE",
            }
        ],
        "metadata": {
            "fingerprint": "GDPUYxlwHe4="
        },
    }
}

Note that the components of the path can be either dictionaries or arrays of dictionaries.
In case  they are dictionaries, subsequent component names key of the field, in case of
arrays - the sanitizer iterates through all dictionaries in the array and searches
components in all elements of the array.
"""
from typing import List
from airflow import LoggingMixin, AirflowException

class GcpFieldSanitizerException(AirflowException):
    __doc__ = 'Thrown when sanitizer finds unexpected field type in the path\n    (other than dict or array).\n    '

    def __init__(self, message):
        super(GcpFieldSanitizerException, self).__init__(message)


class GcpBodyFieldSanitizer(LoggingMixin):
    __doc__ = 'Sanitizes the body according to specification.\n\n    :param sanitize_specs: array of strings that specifies which fields to remove\n    :type sanitize_specs: list[str]\n\n    '

    def __init__(self, sanitize_specs):
        super(GcpBodyFieldSanitizer, self).__init__()
        self._sanitize_specs = sanitize_specs

    def _sanitize(self, dictionary, remaining_field_spec, current_path):
        field_split = remaining_field_spec.split('.', 1)
        if len(field_split) == 1:
            field_name = field_split[0]
            if field_name in dictionary:
                self.log.info('Deleted %s [%s]', field_name, current_path)
                del dictionary[field_name]
            else:
                self.log.debug('The field %s is missing in %s at the path %s.', field_name, dictionary, current_path)
        else:
            field_name = field_split[0]
            remaining_path = field_split[1]
            child = dictionary.get(field_name)
            if child is None:
                self.log.debug('The field %s is missing in %s at the path %s. ', field_name, dictionary, current_path)
            else:
                if isinstance(child, dict):
                    self._sanitize(child, remaining_path, '{}.{}'.format(current_path, field_name))
                else:
                    if isinstance(child, list):
                        for index, elem in enumerate(child):
                            if not isinstance(elem, dict):
                                self.log.warning('The field %s element at index %s is of wrong type. It should be dict and is %s. Skipping it.', current_path, index, elem)
                            self._sanitize(elem, remaining_path, '{}.{}[{}]'.format(current_path, field_name, index))

                    else:
                        self.log.warning('The field %s is of wrong type. It should be dict or list and it is %s. Skipping it.', current_path, child)

    def sanitize(self, body):
        for elem in self._sanitize_specs:
            self._sanitize(body, elem, '')