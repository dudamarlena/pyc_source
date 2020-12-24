# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ../ZMQRPCServer.py
# Compiled at: 2020-03-10 14:33:38
# Size of source mod 2**32: 3694 bytes
import json, zmq, threading
from threading import Lock
from concurrent.futures import ThreadPoolExecutor
import time

class ZMQRPCServer(object):
    m_instance = None
    m_mutex = Lock()

    def __init__(self):
        self.m_num = 0
        self.m_pool = None
        self.m_servers = None
        self.m_workers = None
        self.m_context = None
        self.m_callback = {'sub': None}

    @classmethod
    def getInstance(cls):
        if cls.m_instance == None:
            cls.m_mutex.acquire()
            if cls.m_instance == None:
                cls.m_instance = ZMQRPCServer()
            cls.m_mutex.release()
        return cls.m_instance

    def initServer(self, endpoint, threadCount):
        self.m_num = threadCount
        self.m_pool = ThreadPoolExecutor(max_workers=threadCount)
        print('ZMQ RPC Binding to ', endpoint)
        self.m_context = zmq.Context()
        self.m_workers = self.m_context.socket(zmq.DEALER)
        self.m_workers.bind('inproc://workers')
        self.m_servers = self.m_context.socket(zmq.ROUTER)
        self.m_servers.bind(endpoint)

    def registerCall(self, name, callback):
        self.m_callback[name] = callback

    def send_str(self, socket, response):
        json_bytes = bytes(response, encoding='utf8')
        socket.send(json_bytes)

    def DealRequest(self):
        context = ZMQRPCServer.getInstance().m_context
        socket = context.socket(zmq.REP)
        socket.connect('inproc://workers')
        while True:
            try:
                request = socket.recv()
                json_str = str(request, encoding='utf-8')
                json_dict = json.loads(json_str)
                if json_dict.get('params') == None:
                    json_dict['params'] = None
                try:
                    if 'jsonrpc' in json_dict and 'method' in json_dict and 'id' in json_dict:
                        if json_dict['jsonrpc'] != '2.0':
                            raise Exception('Invalid Jsonrpc version, version must be 2.0')
                        if json_dict['method'] in self.m_callback.keys():
                            callback = self.m_callback[json_dict['method']]
                            response_result = callback(json_dict['id'], json_dict['params'])
                            self.send_str(socket, response_result)
                except Exception as e:
                    print('jsonrpc server excetion ', e)

            except zmq.error as e:
                print('zmq exception ({0}): {1}'.format(e.errno, e.strerror))
                sys.exit()

    def run(self):
        for index in range(self.m_num):
            self.m_pool.submit(self.DealRequest)

        zmq.proxy(self.m_servers, self.m_workers)