# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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