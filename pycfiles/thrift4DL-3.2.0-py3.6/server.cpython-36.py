# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/thrift4DL/server/tcp/server.py
# Compiled at: 2020-01-17 02:23:50
# Size of source mod 2**32: 8868 bytes
from queue import Empty
from queue import Queue
from threading import Thread
import asyncio
from multiprocessing import Manager
import time, multiprocessing
from thrift.transport import TSocket
import traceback
from thrift.transport.TTransport import TTransportException
from thrift.protocol import TBinaryProtocol
import warnings, numpy as np
from thrift.Thrift import TType, TMessageType, TApplicationException
import random, pprint
from ..http import HTTPServer
IDLE_QUEUE_BLOCK_TIME_SEC = 10
__all__ = [
 'TModelPoolServer']

class TModelPoolServerBase:

    def __init__(self):
        pass

    def serve(self):
        pass


class TModelPoolServerV1(TModelPoolServerBase):

    def __init__(self, host, port, handler_cls, model_path, gpu_ids, mem_fractions, http_port=None, batch_infer_size=1, batch_group_timeout=1, verbose=True, logger=None, log_file=None):
        self.logger = logger
        self.log_file = log_file
        self.handler_cls = handler_cls
        self.model_path = model_path
        self.gpu_ids = gpu_ids
        self.mem_fractions = mem_fractions
        self.host = host
        self.port = port
        self.socket = TSocket.TServerSocket(host=(self.host), port=(self.port))
        self.batch_infer_size = batch_infer_size
        self.batch_group_timeout = batch_group_timeout / 1000
        self.handlers = []
        self.is_running = False
        self.verbose = verbose
        self.client_queue = Queue()
        self.http_port = http_port

    def print_server_info(self):
        pp = pprint.PrettyPrinter(indent=3)
        print('=' * 50)
        print('Server Information:\n')
        pp.pprint(self.__dict__)
        print('=' * 50)

    def prepare(self):
        for i in range(len(self.gpu_ids)):
            wrk = self.handler_cls(model_path=(self.model_path), gpu_id=(self.gpu_ids[i]),
              mem_fraction=(self.mem_fractions[i]),
              client_queue=(self.client_queue),
              batch_infer_size=(self.batch_infer_size),
              batch_group_timeout=(self.batch_group_timeout))
            wrk.daemon = True
            wrk.start()
            self.handlers.append(wrk)

        if self.http_port is not None:
            http_server = HTTPServer(host=(self.host),
              port=(self.port),
              http_port=(self.http_port))
            http_server.daemon = True
            http_server.start()
        self.is_running = True
        if self.verbose:
            self.print_server_info()

    def serve(self):
        self.prepare()
        self.socket.listen()
        print('Service started')
        while self.is_running:
            try:
                client = self.socket.accept()
                if not client:
                    continue
                self.client_queue.put(client)
            except (SystemExit, KeyboardInterrupt):
                break
            except Exception as err:
                print(traceback.format_exc())


class TModelPoolServerV2(TModelPoolServerV1):

    def prepare(self):
        self.list_clients = []
        for i in range(len(self.gpu_ids)):
            client_queue = multiprocessing.Queue()
            wrk = self.handler_cls(model_path=(self.model_path), gpu_id=(self.gpu_ids[i]),
              mem_fraction=(self.mem_fractions[i]),
              client_queue=client_queue,
              batch_infer_size=(self.batch_infer_size),
              batch_group_timeout=(self.batch_group_timeout),
              logger=(self.logger),
              log_file=(self.log_file))
            wrk.daemon = True
            wrk.start()
            self.handlers.append(wrk)
            self.list_clients.append(client_queue)

        if self.http_port is not None:
            http_server = HTTPServer(host=(self.host),
              port=(self.port),
              http_port=(self.http_port))
            http_server.daemon = True
            http_server.start()
        self.is_running = True
        if self.verbose:
            self.print_server_info()

    def serve(self):
        self.prepare()
        self.socket.listen()
        print('Service started')
        while self.is_running:
            try:
                client = self.socket.accept()
                if not client:
                    continue
                rand_idx = random.randint(0, len(self.list_clients) - 1)
                self.list_clients[rand_idx].put(client)
            except (SystemExit, KeyboardInterrupt):
                break
            except Exception as err:
                print(traceback.format_exc())


class Ventilator(Thread):

    def __init__(self, client_queue, list_client_pipe_conn, batch_group_timeout, batch_infer_size):
        Thread.__init__(self)
        print('Init Ventilator')
        self.list_client_pipe_conn = list_client_pipe_conn
        self.client_queue = client_queue
        self.batch_group_timeout = batch_group_timeout
        self.batch_infer_size = batch_infer_size

    def get_batch(self):
        """ Block queue for a while to wait incomming request
        """
        batch_clients = []
        is_done = False
        is_empty = False
        timeout = IDLE_QUEUE_BLOCK_TIME_SEC
        while True:
            try:
                if is_done:
                    batch_clients.clear()
                    is_done = False
                    is_empty = False
                    timeout = IDLE_QUEUE_BLOCK_TIME_SEC
                try:
                    client = self.client_queue.get(block=True, timeout=timeout)
                    batch_clients.append(client)
                    timeout = self.batch_group_timeout
                except Empty:
                    is_empty = True

                if len(batch_clients) >= self.batch_infer_size or is_empty and len(batch_clients) > 0:
                    print(len(batch_clients))
                    is_done = True
                    yield batch_clients
            except Exception as e:
                print(traceback.format_exc())

    def run(self):
        for batch_clients in self.get_batch():
            rand_idx = random.randint(0, len(self.list_client_pipe_conn) - 1)
            self.list_client_pipe_conn[rand_idx].send(batch_clients)


class TModelPoolServerV3(TModelPoolServerV1):
    __doc__ = 'The Implementation of AsyncIO server'

    def prepare(self):
        self.client_queue = Queue()
        self.list_client_pipe_conn = []
        for i in range(len(self.gpu_ids)):
            client_pipe_conn, processor_pipe_conn = multiprocessing.Pipe()
            self.list_client_pipe_conn.append(client_pipe_conn)
            wrk = self.handler_cls(model_path=(self.model_path), gpu_id=(self.gpu_ids[i]),
              mem_fraction=(self.mem_fractions[i]),
              processor_pipe_conn=processor_pipe_conn,
              batch_infer_size=(self.batch_infer_size),
              batch_group_timeout=(self.batch_group_timeout))
            wrk.daemon = True
            wrk.start()

        if self.http_port is not None:
            http_server = HTTPServer(host=(self.host),
              port=(self.port),
              http_port=(self.http_port))
            http_server.daemon = True
            http_server.start()
        ventilator = Ventilator(self.client_queue, self.list_client_pipe_conn, self.batch_group_timeout, self.batch_infer_size)
        ventilator.daemon = True
        ventilator.start()
        self.is_running = True

    def serve(self):
        self.prepare()
        self.socket.listen()
        print('Service started')
        while self.is_running:
            try:
                client = self.socket.accept()
                if not client:
                    continue
                self.client_queue.put(client)
            except (SystemExit, KeyboardInterrupt):
                break
            except Exception as err:
                print(traceback.format_exc())


class TModelPoolServer:

    def __init__(self, *args, **kwargs):
        self._TModelPoolServer__server = TModelPoolServerV2(*args, **kwargs)

    def __getattr__(self, name):
        return getattr(self._TModelPoolServer__server, name)