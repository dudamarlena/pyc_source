# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sqlflow/__main__.py
# Compiled at: 2020-04-10 03:26:06
# Size of source mod 2**32: 583 bytes
import argparse
from sqlflow.client import Client
parser = argparse.ArgumentParser()
parser.add_argument('sql', nargs='+', type=str, help='sql', action='store')
parser.add_argument('--url', type=str, help='server url', action='store', default=None)
parser.add_argument('--ca_crt', type=str, help='Path to CA certificates of SQLFlow client.', action='store', default=None)

def main():
    args = parser.parse_args()
    client = Client(server_url=(args.url), ca_crt=(args.ca_crt))
    for sql in args.sql:
        print('executing: {}'.format(sql))
        print(client.execute(sql))