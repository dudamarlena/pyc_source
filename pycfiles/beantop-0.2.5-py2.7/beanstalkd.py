# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/beantop/beanstalkd.py
# Compiled at: 2013-05-19 05:54:46
import yaml

class Beanstalkd:

    def __init__(self, conn, host, port):
        self._conn = conn
        self._host = host
        self._port = port

    def connect(self):
        self._conn.open(self._host, self._port)

    def yaml_data_filtered(self, msg, fields_to_show):
        stats = self.yaml_data(msg)
        ret_data = dict()
        for field in fields_to_show:
            ret_data[field] = stats[field]

        return ret_data

    def yaml_data(self, msg):
        self._send(msg)
        self._read_line()
        self._read_line()
        stats = yaml.load(self._conn.read_until('\r\n'))
        return stats

    def _send(self, mess):
        self._conn.write(mess + '\r\n')

    def _read_line(self):
        return self._conn.read_until('\n')