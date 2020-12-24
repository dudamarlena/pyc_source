# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/lib/chimera_cli/configuration.py
# Compiled at: 2019-12-26 07:34:45
# Size of source mod 2**32: 245 bytes
from json import load

class ConfigurationFileException(Exception):
    pass


try:
    with open('.chimerarc') as (f):
        configs = load(f)
except Exception as e:
    try:
        raise ConfigurationFileException(f"Unable to read configuration file - {e}")
    finally:
        e = None
        del e