# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/joel/Workspace/multi-job/multi_job/validation/validation_utils.py
# Compiled at: 2020-02-19 06:56:33
# Size of source mod 2**32: 1238 bytes
from dataclasses import dataclass
from typing import Any, Callable, NoReturn, Optional
from multi_job.models.exceptions import ParserValidationError

@dataclass
class Result:
    success: bool
    details = None
    details: Optional[str]


@dataclass
class Validator:
    category: str
    subcategory: str
    check: Callable[(..., Result)]

    def validate(self, config: Any) -> None:
        """
        Apply the validator's check method and call its reject method if the
        result is a failure
        
        Args:
            config (Any): Validation target
        """
        result = self.check(config)
        if not result.success:
            self.reject(result.details)

    def reject(self, details: Optional[str]) -> NoReturn:
        """
        Raise a ParserValidationError with a formatted error message
        
        Args:
            details (Optional[str]): The specific case of failure reported in the check's result
        
        Raises:
            ParserValidationError:
 
        Returns:
            NoReturn:
        """
        msg = f"The config file failed validation.\nIssue catagory: {self.category}\nIssue subcatagory: {self.subcategory}\nDetails: {details}"
        raise ParserValidationError(msg)