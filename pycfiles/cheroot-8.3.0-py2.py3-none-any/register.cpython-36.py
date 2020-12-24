# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/ChernMachine/register.py
# Compiled at: 2018-05-07 09:23:52
# Size of source mod 2**32: 327 bytes
__doc__ = '\nRegister a Chern machine\n'
import os, uuid
from Chern.utils import metadata

def register():
    config_file = metadata.ConfigFile(os.path.join(os.environ['HOME'], '.ChernMachine/config.json'))
    config_file.write_variable('machine_id', uuid.uuid4().hex)
    config_file.write_variable('runner_type', 'docker')