# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/utils/gcp_field_sanitizer.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 6103 bytes
__doc__ = 'Sanitizer for body fields sent via GCP API.\n\nThe sanitizer removes fields specified from the body.\n\nContext\n-------\nIn some cases where GCP operation requires modification of existing resources (such\nas instances or instance templates) we need to sanitize body of the resources returned\nvia GCP APIs. This is in the case when we retrieve information from GCP first,\nmodify the body and either update the existing resource or create a new one with the\nmodified body. Usually when you retrieve resource from GCP you get some extra fields which\nare Output-only, and we need to delete those fields if we want to use\nthe body as input for subsequent create/insert type operation.\n\n\nField specification\n-------------------\n\nSpecification of fields is an array of strings which denote names of fields to be removed.\nThe field can be either direct field name to remove from the body or the full\nspecification of the path you should delete - separated with \'.\'\n\n\n>>> FIELDS_TO_SANITIZE = [\n>>>    "kind",\n>>>    "properties.disks.kind",\n>>>    "properties.metadata.kind",\n>>>]\n>>> body = {\n>>>     "kind": "compute#instanceTemplate",\n>>>     "name": "instance",\n>>>     "properties": {\n>>>         "disks": [\n>>>             {\n>>>                 "name": "a",\n>>>                 "kind": "compute#attachedDisk",\n>>>                 "type": "PERSISTENT",\n>>>                 "mode": "READ_WRITE",\n>>>             },\n>>>             {\n>>>                 "name": "b",\n>>>                 "kind": "compute#attachedDisk",\n>>>                 "type": "PERSISTENT",\n>>>                 "mode": "READ_WRITE",\n>>>             }\n>>>         ],\n>>>         "metadata": {\n>>>             "kind": "compute#metadata",\n>>>             "fingerprint": "GDPUYxlwHe4="\n>>>         },\n>>>     }\n>>> }\n>>> sanitizer=GcpBodyFieldSanitizer(FIELDS_TO_SANITIZE)\n>>> SANITIZED_BODY = sanitizer.sanitize(body)\n>>> json.dumps(SANITIZED_BODY, indent=2)\n{\n    "name":  "instance",\n    "properties": {\n        "disks": [\n            {\n                "name": "a",\n                "type": "PERSISTENT",\n                "mode": "READ_WRITE",\n            },\n            {\n                "name": "b",\n                "type": "PERSISTENT",\n                "mode": "READ_WRITE",\n            }\n        ],\n        "metadata": {\n            "fingerprint": "GDPUYxlwHe4="\n        },\n    }\n}\n\nNote that the components of the path can be either dictionaries or arrays of dictionaries.\nIn case  they are dictionaries, subsequent component names key of the field, in case of\narrays - the sanitizer iterates through all dictionaries in the array and searches\ncomponents in all elements of the array.\n'
from typing import List
from airflow import LoggingMixin, AirflowException

class GcpFieldSanitizerException(AirflowException):
    """GcpFieldSanitizerException"""

    def __init__(self, message):
        super(GcpFieldSanitizerException, self).__init__(message)


class GcpBodyFieldSanitizer(LoggingMixin):
    """GcpBodyFieldSanitizer"""

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