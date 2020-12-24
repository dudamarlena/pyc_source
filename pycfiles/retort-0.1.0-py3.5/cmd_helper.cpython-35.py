# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/retort/cmd_helper.py
# Compiled at: 2017-10-06 17:42:00
# Size of source mod 2**32: 1024 bytes
import os, sys
from distutils.util import strtobool
from .constant import CONFIG_FILE_NAME
from .migration import Migration

def prompt(query):
    sys.stdout.write('%s [y/n]: ' % query)
    val = input()
    try:
        ret = strtobool(val)
    except ValueError:
        print('Please answer with a y/n\n')
        return prompt(query)

    return ret


def get_config():
    sys.path.append(os.getcwd())
    from importlib.machinery import SourceFileLoader
    retort_conf = SourceFileLoader('retort_conf', CONFIG_FILE_NAME).load_module()
    return retort_conf


def get_migrations(without_drop=False):
    config = get_config()
    return [Migration(target['engine'], target['metadata'], without_drop=without_drop) for target in config.TARGETS]


def print_codes(migrations, sql=False):
    for m in migrations:
        print_code(m, sql)


def print_code(migration, sql=False):
    print('====================')
    migration.print_engine_info()
    print('====================')
    migration.print_code(sql)