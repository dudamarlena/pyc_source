# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-i386/egg/tests/test_mqas_network_1st_node.py
# Compiled at: 2009-07-27 05:39:54
mqas = None
from SimpleXMLRPCServer import SimpleXMLRPCServer
running = True

def quit():
    global running
    running = False
    return True


def run_server(server):
    global mqas
    print 'start running 1st test node'
    while running:
        server.handle_request()

    mqas.p2p.p2p_quit()


test1_result = False

def check_test1_result():
    global test1_result
    return test1_result


def test(mqas_module):
    global mqas
    mqas = mqas_module
    server = SimpleXMLRPCServer(('localhost', 9999))
    server.register_function(quit)
    server.register_function(check_test1_result)
    mqas.p2p.p2p_init('http://localhost:12345')

    @mqas.following_function('twitter_test_from_client:call')
    def test_receiver(message):
        global test1_result
        print 'twitter_test_from_client:call called'
        test1_result = True

    print mqas.show_followers()
    run_server(server)