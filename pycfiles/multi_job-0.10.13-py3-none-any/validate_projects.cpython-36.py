# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/joel/Workspace/multi-job/multi_job/validation/validate_projects.py
# Compiled at: 2020-02-19 07:46:13
# Size of source mod 2**32: 956 bytes
from .validation_utils import Result, Validator

def check_project_has_path(config: dict) -> Result:
    return Result(True)


def check_project_path_str(config: dict) -> Result:
    return Result(True)


def check_project_path_exists(config: dict) -> Result:
    return Result(True)


def check_project_context_dict(config: dict) -> Result:
    return Result(True)


project_validators = [
 Validator('Project configuration', 'Projects must have a path field', check_project_has_path),
 Validator('Project configuration', "A project's path field must be a string", check_project_path_str),
 Validator('Project configuration', "A project's path field must be resolvable", check_project_path_exists),
 Validator('Project configuration', 'A project context field can only be a dictionary', check_project_context_dict)]