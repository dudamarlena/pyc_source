# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/galaxy/util/sockets.py
# Compiled at: 2018-04-20 03:19:42
import random, shlex, socket, subprocess

def unused_port(range=None):
    if range:
        return __unused_port_on_range(range)
    else:
        return __unused_port_rangeless()


def __unused_port_rangeless():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('localhost', 0))
    addr, port = s.getsockname()
    s.close()
    return port


def __unused_port_on_range(range):
    assert range[0] and range[1]
    cmd_netstat = shlex.split('netstat tuln')
    p1 = subprocess.Popen(cmd_netstat, stdout=subprocess.PIPE)
    occupied_ports = set()
    for line in p1.stdout.read().split('\n'):
        if line.startswith('tcp') or line.startswith('tcp6'):
            col = line.split()
            local_address = col[3]
            local_port = local_address.split(':')[1]
            occupied_ports.add(int(local_port))

    while True:
        port = random.randrange(range[0], range[1])
        if port not in occupied_ports:
            break

    return port