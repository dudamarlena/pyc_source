# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/devenv/local_network_bridge.py
# Compiled at: 2016-02-29 05:33:22
import subprocess
from common.cluster_config import NETWORK_BRIDGE_NAME, NETWORK_BRIDGE_ADDR
from common.cluster import DEVNULL

def exists():
    return subprocess.call('ip addr show dev %s' % NETWORK_BRIDGE_NAME, shell=True, stderr=DEVNULL, stdout=DEVNULL) == 0


def create_if_needed():
    if not exists():
        create()


def create():
    print 'Adding bridge %s with address %s' % (NETWORK_BRIDGE_NAME, NETWORK_BRIDGE_ADDR)
    subprocess.check_call('sudo brctl addbr %s' % NETWORK_BRIDGE_NAME, shell=True)
    subprocess.check_call('sudo ip addr add %s dev %s' % (NETWORK_BRIDGE_ADDR, NETWORK_BRIDGE_NAME), shell=True)
    subprocess.check_call('sudo ip link set dev %s up' % NETWORK_BRIDGE_NAME, shell=True)


def remove():
    subprocess.check_call('sudo ip link set dev %s down' % NETWORK_BRIDGE_NAME, shell=True)
    subprocess.check_call('sudo brctl delbr %s' % NETWORK_BRIDGE_NAME, shell=True)