# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dez/samples/op_callback_test.py
# Compiled at: 2015-11-19 18:49:54
from dez.op.server.connection import Callback_Handler
import event

def main(**kwargs):
    c = Callback_Handler(None)
    domain = kwargs['domain']
    port = kwargs['port']
    c.set_url('success', 'http://' + domain + ':' + str(port) + '/')
    c.set_url('failure', 'http://' + domain + ':' + str(port) + '/')
    c.dispatch('success', {'key1': 'value1', 'key2': 'value2'})
    c.dispatch('failure', {'fkey': 'fval', 'recipients': ['r1', 'r2', 'r3', 'r4', 'r5']})
    event.timeout(2, event.abort)
    event.dispatch()
    return