# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/ChernMachine/register.py
# Compiled at: 2018-05-07 09:23:52
# Size of source mod 2**32: 327 bytes
"""
Register a Chern machine
"""
import os, uuid
from Chern.utils import metadata

def register():
    config_file = metadata.ConfigFile(os.path.join(os.environ['HOME'], '.ChernMachine/config.json'))
    config_file.write_variable('machine_id', uuid.uuid4().hex)
    config_file.write_variable('runner_type', 'docker')