# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/caviar/provider/machinery/docker/machine.py
# Compiled at: 2017-10-25 18:02:55
# Size of source mod 2**32: 1623 bytes


class Machine:

    def __init__(self, client, container_id):
        self._Machine__client = client
        self._Machine__container_id = container_id
        self._Machine__cached_info = None

    @property
    def __info(self):
        if self._Machine__cached_info is None:
            self._Machine__cached_info = MachineInfo(self._Machine__client, self._Machine__container_id)
        return self._Machine__cached_info

    @property
    def host(self):
        return self._Machine__info.host

    def ping_cmd(self):
        return 'echo'


class MachineInfo:

    def __init__(self, client, container_id):
        cont_list = client.containers(all=True, filters={'id': container_id})
        cont = cont_list[0]
        if cont['State'] != 'running':
            client.start(container=container_id)
        cont_list = client.containers(all=True, filters={'id': container_id})
        cont = cont_list[0]
        bridge_network = cont['NetworkSettings']['Networks']['bridge']
        self._MachineInfo__host = bridge_network['IPAddress']

    @property
    def host(self):
        return self._MachineInfo__host