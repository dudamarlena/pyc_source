# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/rc/test/test_azure.py
# Compiled at: 2019-12-12 21:11:02
# Size of source mod 2**32: 865 bytes
from rc import azure
from rc.util import run
from rc.test.util import Timer

def create_test_machine():
    return azure.create(name='test-rc-node', machine_size='Standard_D1', image='ubuntults', location='westus')


def test_azure():
    a = azure.get('test-rc-node')
    print(a)
    if a is not None:
        a.delete()
    with Timer('create machine'):
        machine1 = create_test_machine()
    assert machine1.name == 'test-rc-node'
    assert machine1.ip != ''
    assert machine1.ssh_key_path != ''
    assert machine1.username != ''
    with Timer('get machine'):
        machine1_get = azure.get('test-rc-node')
    assert machine1 == machine1_get
    with Timer('delete machine'):
        machine1.delete()
    assert azure.get('test-rc-node') is None