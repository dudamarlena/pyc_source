# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/joel/Workspace/multi-job/multi_job/validation/validate.py
# Compiled at: 2020-02-19 07:10:15
# Size of source mod 2**32: 1121 bytes
"""
Validation checks to be run sequentiatlly
"""
import ruamel.yaml
from .validate_structure import structure_validators
from .validate_jobs import job_validators
from .validate_routines import routine_validators
from .validate_projects import project_validators

def validate(config_path: str) -> dict:
    """Apply all validation functions to the given configuration
    
    Args:
        config_path (str): Path to the configuration file
    
    Returns:
        Any: Validated configuration
    """
    config = read(config_path)
    for validator in structure_validators + job_validators + routine_validators + project_validators:
        validator.validate(config)

    return config


def read(config_path: str) -> dict:
    """
    Read configuration from yaml file
    
    Args:
        config_path (str): Path to configuration file
    
    Returns:
        Any: Unvalidated configuration
    """
    with open(config_path, 'r') as (stream):
        return ruamel.yaml.load(stream, Loader=(ruamel.yaml.Loader))