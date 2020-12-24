# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/autobahntestsuite/wampcase/wampcase_tmpl.py
# Compiled at: 2018-12-17 11:51:20
__all__ = [
 'Cases']
Cases = []
from autobahntestsuite.util import AttributeBag
from wampcase import WampCase, WampCaseFactory, WampCaseProtocol

class WampCase4_1_1_Params(AttributeBag):
    ATTRIBUTES = [
     'peerCount']


class WampCase4_1_1_Protocol(WampCaseProtocol):

    def test(self):
        self.ready()


class WampCase4_1_1_Factory(WampCaseFactory):
    protocol = WampCase4_1_1_Protocol


class WampCase4_1_1(WampCase):
    factory = WampCase4_1_1_Factory
    index = (4, 1, 1, 0)
    description = 'A NOP test.'
    expectation = 'Nothing.'
    params = WampCase4_1_1_Params(peerCount=10)

    def test(self, log, result, clients):
        msg = 'NOP test running using %d sessions\n' % len(clients)
        log(msg)
        print msg
        result.passed = True


Cases.append(WampCase4_1_1)