# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/bonobo_sqlalchemy/util.py
# Compiled at: 2018-07-15 06:26:26
# Size of source mod 2**32: 975 bytes
from collections import defaultdict
from os import environ
from sqlalchemy import create_engine
from bonobo_sqlalchemy.logging import logger
POSTGRES_DEFAULTS = {'driver': 'postgres', 
 'host': 'localhost', 
 'port': '5432', 
 'name': 'postgres', 
 'user': 'postgres', 
 'pass': ''}
DSN_TEMPLATE = '{driver}://{user}:{pass}@{host}:{port}/{name}'

def create_postgresql_engine(*, options='client_encoding=utf8', env='POSTGRES', **kwargs):
    config = defaultdict(**POSTGRES_DEFAULTS)
    for var in ('driver', 'user', 'pass', 'host', 'port', 'name'):
        if var in kwargs:
            config[var] = kwargs.pop(var)
        elif env:
            env_var = '{}_{}'.format(env, var).upper()
            if env_var in environ:
                config[var] = environ[env_var]

    dsn = DSN_TEMPLATE.format(**config)
    if options:
        dsn += '?' + options
    logger.info('Creating database engine: ' + dsn)
    return create_engine(dsn, **kwargs)