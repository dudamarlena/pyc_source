# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_docker_info.py
# Compiled at: 2019-05-16 13:41:33
from insights.parsers import dockerinfo
from insights.tests import context_wrap
docker_info1 = '\nContainers: 0\nImages: 1\nServer Version: 1.9.1\nStorage Driver: devicemapper\n Pool Name: docker-253:0-10499681-pool\n Pool Blocksize: 65.54 kB\n Base Device Size: 107.4 GB\n Backing Filesystem:\n Data file: /dev/loop0\n Metadata file: /dev/loop1\n Data Space Used: 295.9 MB\n Data Space Total: 107.4 GB\n Data Space Available: 3.611 GB\n Metadata Space Used: 716.8 kB\n Metadata Space Total: 2.147 GB\n Metadata Space Available: 2.147 GB\n Udev Sync Supported: true\n Deferred Removal Enabled: false\n Deferred Deletion Enabled: false\n Deferred Deleted Device Count: 0\n Data loop file: /var/lib/docker/devicemapper/devicemapper/data\n Metadata loop file: /var/lib/docker/devicemapper/devicemapper/metadata\n Library Version: 1.02.107-RHEL7 (2015-12-01)\nExecution Driver: native-0.2\nLogging Driver: json-file\nKernel Version: 3.10.0-327.el7.x86_64\nOperating System: Employee SKU\nCPUs: 1\nTotal Memory: 993 MiB\nName: dhcp.example.com\nID: QPOX:46K6:RZK5:GPBT:DEUD:QM6H:5LRE:R63D:42DI:4BH3:6ZOZ:5EUM\n'
docker_info2 = '\nContainers: 0\nImages: 0\nServer Version: 1.9.1\nStorage Driver: devicemapper\n Pool Name: rhel-docker--pool\n Pool Blocksize: 524.3 kB\n Base Device Size: 107.4 GB\n Backing Filesystem: xfs\n Data file:\n Metadata file:\n Data Space Used: 62.39 MB\n Data Space Total: 3.876 GB\n Data Space Available: 3.813 GB\n Metadata Space Used: 40.96 kB\n Metadata Space Total: 8.389 MB\n Metadata Space Available: 8.348 MB\n Udev Sync Supported: true\n Deferred Removal Enabled: true\n Deferred Deletion Enabled: true\n Deferred Deleted Device Count: 0\n Library Version: 1.02.107-RHEL7 (2015-12-01)\nExecution Driver: native-0.2\nLogging Driver: json-file\nKernel Version: 3.10.0-327.el7.x86_64\nOperating System: Employee SKU\nCPUs: 1\nTotal Memory: 993 MiB\nName: dhcp.example.com\nID: QPOX:46K6:RZK5:GPBT:DEUD:QM6H:5LRE:R63D:42DI:4BH3:6ZOZ:5EUM\n'
docker_info3 = '\nCannot connect to the Docker daemon. Is the docker daemon running on this host?\n'

def test_docker_info():
    result = dockerinfo.DockerInfo(context_wrap(docker_info1)).data
    sub_key = ['Data loop file', 'Server Version', 'Data file']
    sub_result = dict([ (key, result[key]) for key in sub_key ])
    expected = {'Data loop file': '/var/lib/docker/devicemapper/devicemapper/data', 'Data file': '/dev/loop0', 'Server Version': '1.9.1'}
    assert expected == sub_result
    result = dockerinfo.DockerInfo(context_wrap(docker_info2)).data
    assert result.get('Data loop file') is None
    result = dockerinfo.DockerInfo(context_wrap(docker_info3)).data
    assert result == {}
    return