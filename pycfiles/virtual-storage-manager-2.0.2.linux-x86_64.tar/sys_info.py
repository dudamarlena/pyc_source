# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/vsm/manifest/sys_info.py
# Compiled at: 2016-06-13 14:11:03
"""
Collect system information.
"""
import os, time, socket
from vsm import flags
from vsm.openstack.common import log as logging
from vsm import utils
LOG = logging.getLogger(__name__)
FLAGS = flags.FLAGS

def get_hostname():
    """Return the hostname."""
    return socket.gethostname()


def get_local_ip():
    """Return the ip address."""
    ip_list = os.popen('hostname -I').read().strip()
    return ip_list.replace(' ', ',')


def get_rsa_key():
    """Return public key of this server."""
    key, err = utils.execute('cat', FLAGS.id_rsa_pub, run_as_root=True)
    return key


def get_ntp_keys():
    """Return public key of this server."""
    if not os.path.exists(FLAGS.ntp_keys):
        return None
    else:
        wait_disk_ready(FLAGS.ntp_keys)
        key = open(FLAGS.ntp_keys).read()
        return key


def wait_disk_ready(file_path, run_times=3):
    """Wait disk ready for file store"""
    try_times = 1
    while not utils.file_is_exist_as_root(file_path):
        time.sleep(1)
        try_times = try_times + 1
        if try_times > run_times:
            LOG.error('Can not find the %s' % file_path)
            raise