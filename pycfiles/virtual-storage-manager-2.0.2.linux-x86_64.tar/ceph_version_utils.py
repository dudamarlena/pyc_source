# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/vsm/common/ceph_version_utils.py
# Compiled at: 2016-06-13 14:11:03
from vsm.common import constant
from vsm import utils

def get_ceph_version():
    """

    Get the ceph version from ceph cluster.
    Run command "ceph --version" to get it.

    :return: string: version
    """
    args = [
     'ceph',
     '--version']
    try:
        out, err = utils.execute(run_as_root=True, *args)
        version = out.split(' ')[2]
    except:
        version = ''

    return version


def get_ceph_version_code():
    """

    Get the ceph version first from funtion get_ceph_version.
    Then analyze and return the ceph version code.

    :return: string: code
    """
    code = 'firefly'
    version = get_ceph_version()
    prefix_version = ('.').join(version.split('.')[0:2])
    for k, v in constant.CEPH_VERSION_CODE:
        if prefix_version == k:
            code = v

    return code