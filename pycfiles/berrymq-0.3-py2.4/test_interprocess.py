# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-i386/egg/tests/test_interprocess.py
# Compiled at: 2009-10-02 06:52:30
"""test program for interprocess communication(JSON-RPC layer)
"""
import os, sys, time, unittest
rootdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, rootdir)
import berrymq, berrymq.jsonrpc.server, berrymq.jsonrpc.client, berrymq.adapter.growl
CONTROL_SERVER_URL = ('localhost', 12345)
PRIMARY_NODE_URL = ('localhost', 12346)
SECONDARY_NODE_URL = ('localhost', 12347)

def _url(URL):
    return 'http://%s:%s' % URL


def check(expected, actual):
    if actual == expected:
        print '  ok: %s' % expected
    else:
        print '  ng: expected=%s, acutal=%s' % (expected, actual)


def quit():
    print 'quit'
    jsonserver.shutdown(immediately=False)


class Style01Test(object):
    __module__ = __name__

    def __init__(self):
        self.received_messages = []

    def message_receiver(self, message):
        self.received_messages.append(message.id)

    def start(self):
        berrymq.regist_method('*', self.message_receiver)
        berrymq.init_connection(PRIMARY_NODE_URL)
        berrymq.interconnect(SECONDARY_NODE_URL)
        berrymq.twitter('style01c:test01')
        time.sleep(1)
        return True

    def exit(self):
        expected = [
         'style01c:test01', 'style01s:test02']
        check(expected, self.received_messages)
        berrymq.close_connection()
        return True


class Style02Test(object):
    __module__ = __name__

    def start(self):
        berrymq.connect_oneway(SECONDARY_NODE_URL)
        berrymq.send_message('style02c:test02', 1, 2, 3, a=1, b=2)
        return True

    def exit(self):
        berrymq.close_connection()
        return True


class Style03Test(object):
    __module__ = __name__

    def start(self):
        berrymq.connect_via_queue(SECONDARY_NODE_URL, 'style03s:*')
        berrymq.send_message('style03c:test01', 3, 2, 1, a=1, b=2)
        return True

    def check(self):
        check('style03s:test02', berrymq.get().id)
        return True

    def exit(self):
        check('style03s:test03', berrymq.get_nowait().id)
        berrymq.close_connection()
        return True


class TestSuite(object):
    __module__ = __name__

    def __init__(self):
        self.style01 = Style01Test()
        self.style02 = Style02Test()
        self.style03 = Style03Test()


def primary_node():
    global jsonserver
    jsonserver = berrymq.jsonrpc.server.SimpleJSONRPCServer(CONTROL_SERVER_URL)
    jsonserver.register_instance(TestSuite(), allow_dotted_names=True)
    jsonserver.register_function(quit)
    print 'start primary server. waiting secondary node.'

    @berrymq.following_function('style03s:*')
    def receive_messages(message):
        _primary_node_test_result.append(message)

    berrymq.twitter('start primary server:info')
    jsonserver.serve_forever()


def secondary_node():
    expected_at_secondary = [
     [
      'style02c:test02', [1, 2, 3], {'a': 1, 'b': 2}], ['style03c:test01', [3, 2, 1], {'a': 1, 'b': 2}], ['style03s:test02', (), {}], ['style03s:test03', (), {}], ['style01c:test01', [], {}], ['style01s:test02', (), {}]]
    test_results = []

    @berrymq.following_function('*:*')
    def test_receiver(message):
        expected = expected_at_secondary[0]
        if expected[0] == message.id and expected[1] == message.args and expected[2] == message.kwargs:
            result = 'ok'
        else:
            result = 'ng'
        del expected_at_secondary[0]
        test_results.append([str(expected), str([message.id, message.args, message.kwargs]), result])

    berrymq.init_connection(SECONDARY_NODE_URL)
    controller = berrymq.jsonrpc.client.ServerProxy(_url(CONTROL_SERVER_URL))
    controller.style02.start()
    controller.style02.exit()
    controller.style03.start()
    berrymq.twitter('style03s:test02')
    controller.style03.check()
    berrymq.twitter('style03s:test03')
    controller.style03.exit()
    controller.style01.start()
    berrymq.twitter('style01s:test02')
    time.sleep(1)
    controller.style01.exit()
    controller.quit()
    berrymq.close_connection()
    for (expected, actual, result) in test_results:
        if result == 'ok':
            print 'ok: expected = %s' % expected
        else:
            print 'ng: expected = %s, actual = %s' % (expected, actual)

    if len(test_results) == 0:
        print 'ng: no message received'


def usage():
    print 'test JSON-RPC level inter process communication\n\n    Run this scprit twice at same machine. First one is primary and second \n    is seconary.\n\nusage:\n    python test_interprocess_low.py -primary   [option]\n         : run this first\n    python test_interprocess_low.py -secondary [option]\n         : run after primary process\n\noption:\n    -growl : transfer messages to growl(for debug)\n'


if __name__ == '__main__':
    if '-growl' in sys.argv:
        listner = berrymq.adapter.growl.GrowlAdapter('*:*')
    if '-primary' in sys.argv:
        primary_node()
    elif '-secondary' in sys.argv:
        secondary_node()
    else:
        usage()