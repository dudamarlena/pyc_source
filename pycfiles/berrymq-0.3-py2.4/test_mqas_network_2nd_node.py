# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-i386/egg/tests/test_mqas_network_2nd_node.py
# Compiled at: 2009-07-27 05:39:54
mqas = None
import time, xmlrpclib

def test_twitter_from_client(server):
    global mqas
    mqas.twitter('twitter_test_from_client:call')
    time.sleep(1)
    assert server.check_test1_result()
    print 'mqas: test_twitter_from_client() OK!'


def test(mqas_module):
    global mqas
    mqas = mqas_module
    server = xmlrpclib.ServerProxy('http://localhost:9999')
    mqas.p2p.p2p_init('http://localhost:12346')
    mqas.p2p.p2p_connect('http://localhost:12345')
    test_twitter_from_client(server)
    server.quit()
    mqas.p2p.p2p_quit()