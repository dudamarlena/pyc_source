# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/rc/test/test_concurrent.py
# Compiled at: 2019-11-11 13:13:03
# Size of source mod 2**32: 1016 bytes
from rc.test.util import Timer
from rc import gcloud
from rc.util import go, pmap, as_completed

def create_or_get(*, name, **kwargs):
    return gcloud.get(name) or (gcloud.create)(name=name, **kwargs)


def test_create_delete_5_instance():
    futures = []
    machines = []
    with Timer('create 5 instances'):
        for i in range(5):
            futures.append(go(create_or_get, name=('test-rc-node-' + str(i)), machine_type='n1-standard-1', disk_size='20G', image_project='ubuntu-os-cloud', image_family='ubuntu-1804-lts', zone='us-west2-a',
              preemptible=False,
              firewall_allows=['tcp:8080']))

        for f in as_completed(futures):
            m = f.result()
            print('Created machine:', m.name)
            machines.append(m)

    futures = {}

    def delete_print(m):
        m.delete()
        print('Deleted machine:', m.name)

    with Timer('delete 5 instances'):
        pmap(delete_print, machines)
    for m in machines:
        assert gcloud.get(m.name) is None