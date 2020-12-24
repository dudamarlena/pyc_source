# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/jwql/database/reset_database.py
# Compiled at: 2019-08-26 11:08:03
# Size of source mod 2**32: 1157 bytes
"""Reset all tables in the ``jwqldb`` database.

Authors
-------

    - Matthew Bourque

Use
---

    This script is intended to be used in the command line:
    ::

        python reset_database.py

Dependencies
------------

    Users must have a ``config.json`` configuration file with a proper
    ``connection_string`` key that points to the ``jwqldb`` database.
    The ``connection_string`` format is
    ``postgresql+psycopg2://user:password@host:port/database``.
"""
from jwql.database.database_interface import base
from jwql.utils.utils import get_config
if __name__ == '__main__':
    connection_string = get_config()['connection_string']
    server_type = connection_string.split('@')[(-1)][0]
    assert server_type != 'p', 'Cannot reset production database!'
    prompt = 'About to reset all tables for database instance {}. Do you wish to proceed? (y/n)\n'.format(connection_string)
    response = input(prompt)
    if response.lower() == 'y':
        base.metadata.drop_all()
        base.metadata.create_all()
        print('\nDatabase instance {} has been reset'.format(connection_string))