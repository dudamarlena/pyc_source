# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/multicore/__init__.py
# Compiled at: 2017-08-13 05:19:27
try:
    import cPickle as pickle
except ImportError:
    import pickle

import json, mmap, multiprocessing, os, sys, time, traceback, dill
from multicore import exceptions
PY3 = sys.version_info[0] == 3
default_app_config = 'multicore.app.MulticoreAppConfig'
NUMBER_OF_WORKERS = multiprocessing.cpu_count()
_workers = []
_input_buffers = None
_input_buffers_states = None
MMAP_SIZE = 100000
_output_buffers = None
BUFFER_DEPTH = NUMBER_OF_WORKERS * 8
_lock_run = multiprocessing.Lock()
_lock_fetch = multiprocessing.Lock()

class Process(multiprocessing.Process):
    """Wrap Process so exception handling propagates to parent process"""

    def __init__(self, *args, **kwargs):
        multiprocessing.Process.__init__(self, *args, **kwargs)
        self._pconn, self._cconn = multiprocessing.Pipe()
        self._exception = None
        return

    def run(self):
        try:
            multiprocessing.Process.run(self)
            self._cconn.send(None)
        except Exception as e:
            tb = traceback.format_exc()
            self._cconn.send((e, tb))
            raise

        return

    @property
    def exception(self):
        if self._pconn.poll():
            self._exception = self._pconn.recv()
        return self._exception


class Traceback(object):

    def __init__(self, exc, msg):
        self.exc = exc
        self.msg = msg

    def __call__(self):
        raise self.exc.__class__(self.msg)


class Task(object):

    def __new__(cls, *args, **kwargs):
        global NUMBER_OF_WORKERS
        global _workers
        if not _workers:
            return
        else:
            v = kwargs.get('max_load_average', None)
            if v is not None and os.getloadavg()[0] > v * NUMBER_OF_WORKERS:
                return
            return super(Task, cls).__new__(cls, *args, **kwargs)

    def __init__(self, **kwargs):
        self.count = 0
        self.complete = False
        self.buffer_index_map = {}

    def run(self, runnable, *args, **kwargs):
        global _input_buffers
        global _input_buffers_states
        global _lock_run
        if self.complete:
            raise exceptions.TaskCompleteError()
        serialization_format = kwargs.pop('serialization_format', 'pickle')
        if serialization_format not in ('pickle', 'json', 'string'):
            raise RuntimeError('Unrecognized serialization_format %s' % serialization_format)
        use_dill = kwargs.pop('use_dill', False)
        if not use_dill:
            pickled = pickle.dumps((
             runnable, serialization_format, use_dill, args, kwargs), 0).decode('utf-8')
        else:
            pickled = pickle.dumps((
             dill.dumps(runnable), serialization_format, use_dill,
             dill.dumps(args), dill.dumps(kwargs)), 0).decode('utf-8')
        _lock_run.acquire()
        try:
            found = False
            for index, state in enumerate(_input_buffers_states[:]):
                if state in (0, '0'):
                    found = True
                    break

            if not found:
                for i in self.buffer_index_map.keys():
                    _input_buffers_states[index] = 0 if PY3 else '0'

                raise exceptions.NoAvailableInputBufferError()
            self.buffer_index_map[index] = self.count
            mm = _input_buffers[index]
            mm.seek(0)
            try:
                mm.write(('%.6d' % len(pickled) + pickled).encode('utf-8'))
            except ValueError:
                raise exceptions.InputBufferTooSmallError()

            _input_buffers_states[index] = 1 if PY3 else '1'
        finally:
            _lock_run.release()

        self.count += 1

    def get(self, timeout=10.0):
        global _output_buffers
        if self.complete:
            raise exceptions.TaskCompleteError()
        SLEEP = 0.005
        max_iterations = int(timeout / SLEEP)
        datas = [
         None] * self.count
        will_timeout = False
        fetches = self.count
        while fetches > 0:
            states = _input_buffers_states[:]
            for buf_index, run_index in self.buffer_index_map.items():
                if datas[run_index] is None and states[buf_index] in (3, '3'):
                    data = _output_buffers[buf_index][:].decode('utf-8')
                    if int(data[:6]):
                        datas[run_index] = data
                        fetches -= 1

            max_iterations -= 1
            if max_iterations <= 0:
                will_timeout = True
                break
            time.sleep(SLEEP)

        self.complete = True
        for index in self.buffer_index_map.keys():
            _input_buffers_states[index] = 0 if PY3 else '0'

        if will_timeout:
            raise exceptions.TimeoutExceededError()
        results = []
        for data in datas:
            length = int(data[:6])
            data = data[6:length + 6]
            serialization_format = data[:6].strip()
            if serialization_format == 'pickle':
                result = pickle.loads(data[6:].encode('utf-8'))
            elif serialization_format == 'json':
                result = json.loads(data[6:])
            else:
                result = data[6:]
            results.append(result)
            if isinstance(result, Traceback):
                result()

        return results


def fetch_and_run(lock):
    global BUFFER_DEPTH
    SLEEP = 0.005
    while True:
        for index in range(BUFFER_DEPTH):
            if _input_buffers_states[index] not in (1, '1'):
                continue
            lock.acquire()
            if _input_buffers_states[index] not in (1, '1'):
                lock.release()
                continue
            _input_buffers_states[index] = 2 if PY3 else '2'
            lock.release()
            data = _input_buffers[index][:].decode('utf-8')
            length = int(data[:6])
            data = data[6:length + 6]
            runnable, serialization_format, use_dill, args, kwargs = pickle.loads(data.encode('utf-8'))
            if use_dill:
                runnable = dill.loads(runnable)
                args = dill.loads(args)
            try:
                result = runnable(*args)
                if serialization_format == 'pickle':
                    serialized = pickle.dumps(result, 0).decode('utf-8')
                elif serialization_format == 'json':
                    serialization_format = 'json  '
                    serialized = json.dumps(result)
                elif serialization_format == 'string':
                    serialized = result
                mm = _output_buffers[index]
                mm.seek(0)
                mm.write(('%.6d' % (len(serialized) + 6) + serialization_format + serialized).encode('utf-8'))
                _input_buffers_states[index] = 3 if PY3 else '3'
            except Exception as exc:
                msg = traceback.format_exc()
                pickled = pickle.dumps(Traceback(exc, msg), 0).decode('utf-8')
                mm = _output_buffers[index]
                mm.seek(0)
                mm.write(('%.6d' % (len(pickled) + 6) + 'pickle' + pickled).encode('utf-8'))

        time.sleep(SLEEP)


def initialize(force=False):
    """Start the queue workers if needed. Called by __main__ and unit tests."""
    global _input_buffers
    global _input_buffers_states
    global _lock_fetch
    global _output_buffers
    if _workers:
        return
    _input_buffers = []
    _output_buffers = []
    for i in range(BUFFER_DEPTH):
        _input_buffers.append(mmap.mmap(-1, 10000))
        _output_buffers.append(mmap.mmap(-1, MMAP_SIZE))

    _input_buffers_states = mmap.mmap(-1, BUFFER_DEPTH)
    for i in range(BUFFER_DEPTH):
        _input_buffers_states[i] = 0 if PY3 else '0'

    for i in range(0, NUMBER_OF_WORKERS):
        p = Process(target=fetch_and_run, args=(_lock_fetch,))
        _workers.append(p)
        p.start()


def shutdown():
    """Stop the queue workers. Called by __main__ and unit tests."""
    global _workers
    for p in _workers:
        p.terminate()
        del p

    _workers = []