# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/joel/Workspace/multi-job/multi_job/validation/validate_structure.py
# Compiled at: 2020-02-19 07:46:13
# Size of source mod 2**32: 1201 bytes
from .validation_utils import Result, Validator

def check_top_level_dicts(config: dict) -> Result:
    return Result(True)


def check_projects_jobs_dicts(config: dict) -> Result:
    return Result(True)


def check_routines_list(config: dict) -> Result:
    return Result(True)


structure_validators = [
 Validator('Configuration structure', 'The configuration must not be blank', lambda x: Result(x != None)),
 Validator('Top level type structure', 'The configuration must be a dictionary', lambda x: Result(type(x) == dict)),
 Validator('Configuration structure', "The configuration's top level must contain only 'jobs', 'projects' or 'routines'", lambda x: Result(set(x) <= set(['jobs', 'projects', 'routines']))),
 Validator('Top level type structure', 'Jobs, projects and routines must be dictionaries', check_top_level_dicts),
 Validator('Top level type structure', 'Each job and project must be a dictionary', check_projects_jobs_dicts),
 Validator('Structure', 'Each routine must be a list', check_routines_list)]