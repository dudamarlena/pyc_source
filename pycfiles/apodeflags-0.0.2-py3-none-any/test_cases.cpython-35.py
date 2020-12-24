# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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