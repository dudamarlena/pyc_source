# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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