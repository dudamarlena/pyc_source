# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/test_case/validation/ddv_validation.py
# Compiled at: 2019-12-27 10:07:44
# Size of source mod 2**32: 2397 bytes
from typing import Optional
from exactly_lib.common.report_rendering.text_doc import TextRenderer
from exactly_lib.test_case_file_structure.home_directory_structure import HomeDirectoryStructure
from exactly_lib.test_case_file_structure.tcds import Tcds

class DdvValidator:
    __doc__ = '\n    EXPERIMENTING WITH VALIDATOR THAT IS RESOLVED À LA SYMBOL VALUE.\n\n    Validates an object - either pre or post creation of SDS.\n\n    Symbols are expected to have been resolved at an earlier step.\n\n    Whether validation is done pre or post SDS depends on whether the validated\n    object is outside or inside the SDS.\n    '

    def validate_pre_sds_if_applicable(self, hds: HomeDirectoryStructure) -> Optional[TextRenderer]:
        """
        Validates the object if it is expected to exist pre-SDS.
        :return: Error message iff validation was applicable and validation failed.
        """
        raise NotImplementedError()

    def validate_post_sds_if_applicable(self, tcds: Tcds) -> Optional[TextRenderer]:
        """
        Validates the object if it is expected to NOT exist pre-SDS.
        :return: Error message iff validation was applicable and validation failed.
        """
        raise NotImplementedError()

    def validate_pre_or_post_sds(self, tcds: Tcds) -> Optional[TextRenderer]:
        """
        Validates the object using either pre- or post- SDS.
        :return: Error message iff validation failed.
        """
        error_message = self.validate_pre_sds_if_applicable(tcds.hds)
        if error_message is not None:
            return error_message
        return self.validate_post_sds_if_applicable(tcds)


class ConstantDdvValidator(DdvValidator):

    def __init__(self, pre_sds_result: Optional[TextRenderer]=None,
                 post_sds_result: Optional[TextRenderer]=None):
        self._pre_sds_result = pre_sds_result
        self._post_sds_result = post_sds_result

    @staticmethod
    def new_success() -> DdvValidator:
        return ConstantDdvValidator(None, None)

    def validate_pre_sds_if_applicable(self, hds: HomeDirectoryStructure) -> Optional[TextRenderer]:
        return self._pre_sds_result

    def validate_post_sds_if_applicable(self, tcds: Tcds) -> Optional[TextRenderer]:
        return self._post_sds_result


def constant_success_validator() -> DdvValidator:
    return ConstantDdvValidator(None, None)