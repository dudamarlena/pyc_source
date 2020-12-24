# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyogp/lib/base/message/tests/test_circuits.py
# Compiled at: 2010-02-07 17:28:31
"""
Contributors can be viewed at:
http://svn.secondlife.com/svn/linden/projects/2008/pyogp/lib/base/trunk/CONTRIBUTORS.txt 

$LicenseInfo:firstyear=2008&license=apachev2$

Copyright 2009, Linden Research, Inc.

Licensed under the Apache License, Version 2.0.
You may obtain a copy of the License at:
    http://www.apache.org/licenses/LICENSE-2.0
or in 
    http://svn.secondlife.com/svn/linden/projects/2008/pyogp/lib/base/LICENSE.txt

$/LicenseInfo$
"""
import unittest, doctest, pprint
from pyogp.lib.base.message.circuit import CircuitManager, Circuit, Host
from pyogp.lib.base.message.message import Message, Block
from pyogp.lib.base.message.message import Message

class TestHost(unittest.TestCase):
    __module__ = __name__

    def tearDown(self):
        pass

    def setUp(self):
        pass

    def test(self):
        host = Host((1, 80))
        assert host.is_ok() == True, 'Good host thinks it is bad'

    def test_fail(self):
        host = Host((None, None))
        assert host.is_ok() == False, 'Bad host thinks it is good'
        return


class TestCircuit(unittest.TestCase):
    __module__ = __name__

    def tearDown(self):
        pass

    def setUp(self):
        self.host = Host((1, 80))

    def test(self):
        circuit = Circuit(self.host, 1)
        assert circuit.next_packet_id() == 1, 'Wrong next id'
        assert circuit.next_packet_id() == 2, 'Wrong next id 2'

    def test_add_reliable(self):
        circuit = Circuit(self.host, 1)
        assert circuit.unack_packet_count == 0, 'Has incorrect unack count'
        assert len(circuit.unacked_packets) == 0, 'Has incorrect unack'
        assert len(circuit.final_retry_packets) == 0, 'Has incorrect final unacked'
        msg = Message('PacketAck', Block('Packets', ID=3))
        circuit.add_reliable_packet(msg)
        assert circuit.unack_packet_count == 1, 'Has incorrect unack count'
        assert len(circuit.unacked_packets) == 1, 'Has incorrect unack, ' + str(len(circuit.unacked_packets))
        assert len(circuit.final_retry_packets) == 0, 'Has incorrect final unacked'


class TestCircuitManager(unittest.TestCase):
    __module__ = __name__

    def tearDown(self):
        pass

    def setUp(self):
        self.host = Host((1, 80))

    def test_(self):
        manager = CircuitManager()
        assert len(manager.circuit_map) == 0, 'Circuit list incorrect'
        manager.add_circuit(self.host, 1)
        assert len(manager.circuit_map) == 1, 'Circuit list incorrect 2'
        host = Host((17, 80))
        manager.add_circuit(host, 10)
        assert len(manager.circuit_map) == 2, 'Circuit list incorrect 4'
        circuit = manager.get_circuit(self.host)
        assert circuit.last_packet_in_id == 1, 'Got wrong circuit'
        circuit = manager.get_circuit(host)
        assert circuit.last_packet_in_id == 10, 'Got wrong circuit 1'
        assert manager.is_circuit_alive(self.host) == True, 'Incorrect circuit alive state'
        assert manager.is_circuit_alive(host) == True, 'Incorrect circuit alive state 2'


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestCircuit))
    suite.addTest(makeSuite(TestCircuitManager))
    suite.addTest(makeSuite(TestHost))
    return suite