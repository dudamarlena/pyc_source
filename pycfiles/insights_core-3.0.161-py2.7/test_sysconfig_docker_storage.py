# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_sysconfig_docker_storage.py
# Compiled at: 2019-05-16 13:41:33
from insights.parsers.sysconfig import DockerSysconfigStorage
from insights.tests import context_wrap
DOCKER_CONFIG_STORAGE = ('\nDOCKER_STORAGE_OPTIONS="--storage-driver devicemapper --storage-opt dm.fs=xfs --storage-opt dm.thinpooldev=/dev/mapper/dockervg-docker--pool --storage-opt dm.use_deferred_removal=true --storage-opt dm.use_deferred_deletion=true"\n').strip()

def test_sysconfig_docker_content():
    context = context_wrap(DOCKER_CONFIG_STORAGE, 'etc/sysconfig/docker-storage')
    sysconf = DockerSysconfigStorage(context)
    assert sorted(sysconf.keys()) == sorted(['DOCKER_STORAGE_OPTIONS'])
    assert 'DOCKER_STORAGE_OPTIONS' in sysconf
    assert sysconf['DOCKER_STORAGE_OPTIONS'] == '--storage-driver devicemapper --storage-opt dm.fs=xfs --storage-opt dm.thinpooldev=/dev/mapper/dockervg-docker--pool --storage-opt dm.use_deferred_removal=true --storage-opt dm.use_deferred_deletion=true'
    assert sysconf.storage_options == '--storage-driver devicemapper --storage-opt dm.fs=xfs --storage-opt dm.thinpooldev=/dev/mapper/dockervg-docker--pool --storage-opt dm.use_deferred_removal=true --storage-opt dm.use_deferred_deletion=true'