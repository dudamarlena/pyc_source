# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/waferslim/specs/fixtures_spec.py
# Compiled at: 2010-02-27 12:29:13
"""
BDD-style Lancelot specifications for the behaviour of the core library classes
"""
from waferslim.fixtures import EchoFixture
import lancelot

class EchoFixtureBehaviour(object):

    @lancelot.verifiable
    def echo_should_return_str_passed_in(self):
        echoer = lancelot.Spec(EchoFixture())
        echoer.echo('hello world').should_be('hello world')
        echoer.echo('1').should_be('1')


lancelot.grouping(EchoFixtureBehaviour)
if __name__ == '__main__':
    lancelot.verify()