# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/datalogue/models/transformations/commons.py
# Compiled at: 2020-04-14 15:37:55
# Size of source mod 2**32: 3404 bytes
from uuid import UUID
from datalogue.errors import DtlError, _enum_parse_error, _invalid_parameter_error
from datalogue.utils import _parse_string_list, SerializableStringEnum
import abc
from typing import Union, List, Optional

class Transformation(abc.ABC):
    type_field = 'type'

    def __init__(self, transformation_type):
        self.type = transformation_type
        super().__init__()

    def _base_payload(self) -> dict:
        return dict([(Transformation.type_field, self.type)])

    @abc.abstractmethod
    def _as_payload(self) -> dict:
        """
        Represents the transformation in its dictionary construction

        :return:
        """
        pass


class RegexTransformation(Transformation):

    def __init__(self, regex: Optional[str], regex_id: Optional[UUID], regex_transformation_type: str):
        Transformation.__init__(self, regex_transformation_type)
        if regex is None:
            if regex_id is None:
                raise _invalid_parameter_error('neither regex nor regex_id is/are not defined!', regex_transformation_type)
        if regex is not None:
            if regex_id is not None:
                raise _invalid_parameter_error('both regex and regex_id are defined! Please provide only either.', regex_transformation_type)


class DataType(SerializableStringEnum):
    __doc__ = '\n    Data Types that can be specified in the pipeline\n    '
    String = 'String'
    Boolean = 'Boolean'
    Integer = 'Integer'
    DateTime = 'DateTime'
    Double = 'Double'

    @staticmethod
    def parse_error(s: str) -> str:
        return _enum_parse_error('data type', s)

    @staticmethod
    def from_str(string: str) -> Union[(DtlError, 'DataType')]:
        return SerializableStringEnum.from_str(DataType)(string)


def _array_from_dict(json: dict, transformation_type: str, array_field_key: str) -> Union[(DtlError, List[str])]:
    """
    Generic method to extract an array from a json transformation dictionary

    :param json: dictionary built from json
    :param transformation_type: type of the transformation
    :param array_field_key: key at which the array is
    :return:
    """
    if json.get(Transformation.type_field) != transformation_type:
        return DtlError('Dictionary input is not of type %s' % transformation_type)
    else:
        array_field = json.get(array_field_key)
        if array_field is None:
            return DtlError("'%s' is missing from the json transformation" % array_field_key)
        array = _parse_string_list(array_field)
        if isinstance(array, DtlError):
            return array
        return array


class ByClass:

    def __init__(self, class_id: Union[(str, UUID)]):
        self.class_id = class_id

    def __repr__(self):
        return f"ByClass(class_id: {self.class_id!r})"


class ByFieldName:

    def __init__(self, field_name: List[str]):
        self.field_name = field_name

    def __repr__(self):
        return f"ByFieldName(field_name: {self.field_name!r})"