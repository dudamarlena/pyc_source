# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tests/behave/common/config.py
# Compiled at: 2018-07-31 13:26:37
# Size of source mod 2**32: 1102 bytes
import collections, copy, os
from conflagration import api
from conflagration.namespace import ModifiableNamespace
from src.tests.behave.common.const import ConfigVars, Sources
DEFAULT_CONFIG_FILES = ()

def get_conflagration(config_file_paths=DEFAULT_CONFIG_FILES):
    """Instantiate a conflagration instance.

    This defaults to loading from two files:

    1. mercury_tests_creds.config - contains sensitive information
    2. mercury_tests.config - contains non-sensitive information

    This lets us encrypt just the sensitive bits for jenkins and quickly make
    changes to the non-sensitive configs, which we can store in plaintext.
    """
    here = os.getcwd()
    paths = [os.path.join(here, filename) for filename in config_file_paths]
    if config_file_paths:
        cfg = api.conflagration(files=paths, namespace_obj=(ModifiableNamespace()))
    else:
        cfg = api.conflagration(default_to_env=True)
    return cfg