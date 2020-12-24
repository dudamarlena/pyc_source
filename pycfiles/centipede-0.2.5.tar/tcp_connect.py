# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/centinel/experiments/tcp_connect.py
# Compiled at: 2015-09-29 14:51:18
import socket
from centinel.experiment import Experiment

class TCPConnectExperiment(Experiment):
    name = 'tcp_connect'

    def __init__(self, input_file):
        self.input_file = input_file
        self.results = []
        self.host = None
        self.port = None
        return

    def run(self):
        for line in self.input_file:
            self.host, self.port = line.strip().split(' ')
            self.tcp_connect()

    def tcp_connect(self):
        result = {'host': self.host, 
           'port': self.port}
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((self.host, int(self.port)))
            sock.close()
            result['success'] = 'true'
        except Exception as err:
            result['failure'] = str(err)

        self.results.append(result)