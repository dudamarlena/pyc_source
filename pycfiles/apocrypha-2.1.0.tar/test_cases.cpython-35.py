# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/leaf/working/apocrypha/test/test_cases.py
# Compiled at: 2018-06-30 18:08:12
# Size of source mod 2**32: 11353 bytes
import unittest, time, apocrypha.client
from apocrypha.exceptions import DatabaseError

def query(args, raw=False):
    """ list of string -> string
    """
    return apocrypha.client.query(args, interpret=raw, port=49999)


client = apocrypha.client.Client(port=49999)

class ServerCases(unittest.TestCase):
    database = None

    def test_delete(self):
        client.set('test item', value='hello')
        self.assertEqual(client.get('test item'), 'hello')
        client.delete('test item')
        self.assertEqual(client.get('test item'), None)