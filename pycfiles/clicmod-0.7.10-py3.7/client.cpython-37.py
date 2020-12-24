# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/onedesk/client/client.py
# Compiled at: 2019-06-06 17:43:26
# Size of source mod 2**32: 580 bytes
import logging
logger = logging.getLogger('main')

def get_client(session, instance, client_name):
    params = {'size': 10000}
    client_list = session.get((instance + '/api/clients'), params=params)
    logger.debug('Response: %s', client_list.status_code)
    for client in client_list.json()['content']:
        if client['code'] == client_name:
            return client

    logger.debug('No client with the provided name found, exiting...')
    raise SystemExit


def create_client(name):
    raise NotImplementedError