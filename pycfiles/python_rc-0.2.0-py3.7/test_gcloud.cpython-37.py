# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/rc/test/test_gcloud.py
# Compiled at: 2019-11-09 17:43:22
# Size of source mod 2**32: 2456 bytes
from rc import gcloud
from rc.util import run
from rc.test.util import Timer

def create_test_machine():
    return gcloud.create(name='test-rc-node', machine_type='n1-standard-1', disk_size='20G', image_project='ubuntu-os-cloud', image_family='ubuntu-1804-lts', zone='us-west2-a',
      preemptible=False,
      firewall_allows=['tcp:8080'])


def test_gcloud():
    a = gcloud.get('test-rc-node')
    if a is not None:
        a.delete()
    with Timer('list machine'):
        old_machines = gcloud.list()
    assert len(list(filter(lambda machine: machine.name == 'test-rc-node', old_machines))) == 0
    assert gcloud.get('test-rc-node') is None
    with Timer('create machine'):
        machine1 = create_test_machine()
    assert machine1.name == 'test-rc-node'
    assert machine1.ip != ''
    assert machine1.ssh_key_path != ''
    assert machine1.username != ''
    assert machine1.status() == 'RUNNING'
    with Timer('get machine'):
        machine1_get = gcloud.get('test-rc-node')
    assert machine1 == machine1_get
    new_machines = gcloud.list()
    assert len(list(filter(lambda machine: machine.name == 'test-rc-node', new_machines))) == 1
    assert len(new_machines) == len(old_machines) + 1
    with Timer('shutdown'):
        machine1.shutdown()
    assert machine1.status() == 'TERMINATED'
    with Timer('bootup'):
        machine1.bootup()
    assert machine1.status() == 'RUNNING'
    machine1.upload(local_path='rc/test/test_gcloud.py', machine_path='/tmp/')
    assert machine1.run('ls /tmp/test_gcloud.py')
    machine1.download(machine_path='/tmp/test_gcloud.py', local_path='/tmp/test_gcloud.py')
    assert open('/tmp/test_gcloud.py').read() == open('/tmp/test_gcloud.py').read()
    run(['rm', '/tmp/test_gcloud.py'])
    machine1.run(['echo', 'aaa', '>', '/tmp/aaaa.txt'])
    assert run('ls /tmp/aaaa.txt').returncode != 0
    machine1.run(['grep', '', '/tmp/aaaa.txt'])
    p = machine1.run('cat /tmp/aaaa.txt')
    assert p.stdout == 'aaa\n'
    with Timer('delete machine'):
        machine1.delete()
    assert gcloud.get('test-rc-node') is None