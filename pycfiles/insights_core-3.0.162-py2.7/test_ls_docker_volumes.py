# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_ls_docker_volumes.py
# Compiled at: 2019-05-16 13:41:33
from insights.parsers.ls_docker_volumes import DockerVolumesDir
from insights.tests import context_wrap
DOCKER_VOLUME_EMPTY_DIR = '\n/var/lib/docker/volumes/:\ntotal 0\ndrwx------. 3 0 0   77 Mar 15 10:50 .\ndrwx-----x. 9 0 0 4096 Nov 18 22:04 ..\n'
DOCKER_VOLUME_HAS_VOL_DIR = '\n/var/lib/docker/volumes/:\ntotal 4\ndrwx------. 3 0 0   77 Mar 15 10:50 .\ndrwx-----x. 9 0 0 4096 Nov 18 22:04 ..\ndrwxr-xr-x. 3 0 0   18 Mar 15 10:50 7HASH7\n\n/var/lib/docker/volumes/7HASH7:\ntotal 0\ndrwxr-xr-x. 3 0 0 18 Mar 15 10:50 .\ndrwx------. 3 0 0 77 Mar 15 10:50 ..\ndrwxr-xr-x. 2 0 0  6 Mar 15 10:50 _data\n\n/var/lib/docker/volumes/7HASH7/_data:\ntotal 0\ndrwxr-xr-x. 2 0 0  6 Mar 15 10:50 .\ndrwxr-xr-x. 3 0 0 18 Mar 15 10:50 ..\n'
BASE_DIR = '/var/lib/docker/volumes/'

def test_empty_dir():
    ctx = context_wrap(DOCKER_VOLUME_EMPTY_DIR, path='/bin/ls -lanR /var/lib/docker/volumes')
    dirs = DockerVolumesDir(ctx)
    assert BASE_DIR in dirs
    assert dirs.dirs_of(BASE_DIR) == ['.', '..']
    assert dirs.files_of(BASE_DIR) == []


def test_has_volumes():
    ctx = context_wrap(DOCKER_VOLUME_HAS_VOL_DIR, path='/bin/ls -lanR /var/lib/docker/volumes')
    dirs = DockerVolumesDir(ctx)
    assert BASE_DIR in dirs
    assert dirs.dirs_of(BASE_DIR) == ['.', '..', '7HASH7']
    assert dirs.files_of(BASE_DIR) == []
    volume_dir = BASE_DIR + '7HASH7'
    assert volume_dir in dirs
    assert dirs.dirs_of(volume_dir) == ['.', '..', '_data']
    assert dirs.files_of(volume_dir) == []