# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/amcnabb/python/mrs/serial.py
# Compiled at: 2012-11-01 14:16:29
"""Mrs Serial Runner"""
import multiprocessing, select, threading, traceback
from . import runner
import logging
logger = logging.getLogger('mrs')

class SerialRunner(runner.BaseRunner):

    def __init__(self, *args):
        super(SerialRunner, self).__init__(*args)
        self.program = None
        self.worker_conn = None
        return

    def run(self):
        try:
            self.program = self.program_class(self.opts, self.args)
        except Exception as e:
            logger.critical('Exception while instantiating the program: %s' % traceback.format_exc())
            return 1

        self.start_worker()
        self.event_loop.register_fd(self.worker_conn.fileno(), self.read_worker_conn)
        self.event_loop.run()
        return self.exitcode

    def start_worker(self):
        self.worker_conn, remote_worker_conn = multiprocessing.Pipe()
        worker = SerialWorker(self.program, self.datasets, remote_worker_conn)
        worker_thread = threading.Thread(target=worker.run, name='Serial Worker')
        worker_thread.daemon = True
        worker_thread.start()

    def compute_dataset(self, dataset):
        """Called when a new ComputedData set is submitted."""
        self.worker_conn.send(dataset.id)

    def read_worker_conn(self):
        """Read a response from the worker.

        Each SerialWorkerSuccess response will contain an id of a dataset
        that has finished being computed.
        """
        try:
            response = self.worker_conn.recv()
            if isinstance(response, SerialWorkerSuccess):
                dataset_id = response.dataset_id
            else:
                logger.error(response.traceback)
                self.exitcode = 1
                self.event_loop.running = False
                return
        except EOFError:
            logger.critical('Got an EOF from the Worker')
            self.exitcode = 1
            self.event_loop.running = False
            return

        ds = self.datasets[dataset_id]
        self.dataset_done(ds)


class SerialWorker(object):

    def __init__(self, program, datasets, conn):
        self.program = program
        self.datasets = datasets
        self.conn = conn

    def run(self):
        while True:
            try:
                try:
                    dataset_id = self.conn.recv()
                except EOFError:
                    return

                ds = self.datasets[dataset_id]
                ds.run_serial(self.program, self.datasets)
                response = SerialWorkerSuccess(dataset_id)
            except Exception as e:
                response = SerialWorkerFailure(e, traceback.format_exc())

            self.conn.send(response)


class SerialWorkerSuccess(object):
    """Successful response from SerialWorker."""

    def __init__(self, dataset_id):
        self.dataset_id = dataset_id


class SerialWorkerFailure(object):
    """Failure response from SerialWorker."""

    def __init__(self, exception, traceback):
        self.exception = exception
        self.traceback = traceback