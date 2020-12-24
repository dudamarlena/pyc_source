# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python2.7/site-packages/pyzjnettest/testserver.py
# Compiled at: 2014-12-12 03:34:47
from __future__ import print_function
from pyjznet import Server, rpc_method
import unittest, logging

class DemoService(object):

    def sayHi(self, name, remote_service):
        try:
            age = remote_service.call_rpc('demo', 'getAge')
        except Exception as e:
            logging.error(e)
            return str(e)

        logging.info("got say hi request of %s who's age is %d" % (name, age))
        return "Hi, %s who's age is %d!" % (name, age)


class TestNetServer(unittest.TestCase):

    def setUp(self):
        pass

    def test_server(self):
        server = Server()
        server.add_rpc_service('demo', DemoService())
        server.start()


if __name__ == '__main__':
    unittest.main()