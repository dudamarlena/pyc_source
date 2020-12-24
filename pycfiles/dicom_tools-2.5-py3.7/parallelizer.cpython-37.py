# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/dicom_tools/pyqtgraph/multiprocess/parallelizer.py
# Compiled at: 2018-05-21 04:28:19
# Size of source mod 2**32: 12243 bytes
import os, sys, time, multiprocessing, re
from .processes import ForkedProcess
from .remoteproxy import ClosedError

class CanceledError(Exception):
    __doc__ = 'Raised when the progress dialog is canceled during a processing operation.'


class Parallelize(object):
    __doc__ = '\n    Class for ultra-simple inline parallelization on multi-core CPUs\n    \n    Example::\n    \n        ## Here is the serial (single-process) task:\n        \n        tasks = [1, 2, 4, 8]\n        results = []\n        for task in tasks:\n            result = processTask(task)\n            results.append(result)\n        print(results)\n        \n        \n        ## Here is the parallelized version:\n        \n        tasks = [1, 2, 4, 8]\n        results = []\n        with Parallelize(tasks, workers=4, results=results) as tasker:\n            for task in tasker:\n                result = processTask(task)\n                tasker.results.append(result)\n        print(results)\n        \n        \n    The only major caveat is that *result* in the example above must be picklable,\n    since it is automatically sent via pipe back to the parent process.\n    '

    def __init__(self, tasks=None, workers=None, block=True, progressDialog=None, randomReseed=True, **kwds):
        """
        ===============  ===================================================================
        **Arguments:**
        tasks            list of objects to be processed (Parallelize will determine how to 
                         distribute the tasks). If unspecified, then each worker will receive
                         a single task with a unique id number.
        workers          number of worker processes or None to use number of CPUs in the 
                         system
        progressDialog   optional dict of arguments for ProgressDialog
                         to update while tasks are processed
        randomReseed     If True, each forked process will reseed its random number generator
                         to ensure independent results. Works with the built-in random
                         and numpy.random.
        kwds             objects to be shared by proxy with child processes (they will 
                         appear as attributes of the tasker)
        ===============  ===================================================================
        """
        self.showProgress = False
        if progressDialog is not None:
            self.showProgress = True
            if isinstance(progressDialog, basestring):
                progressDialog = {'labelText': progressDialog}
            import widgets.ProgressDialog as ProgressDialog
            self.progressDlg = ProgressDialog(**progressDialog)
        if workers is None:
            workers = self.suggestedWorkerCount()
        if not hasattr(os, 'fork'):
            workers = 1
        self.workers = workers
        if tasks is None:
            tasks = range(workers)
        self.tasks = list(tasks)
        self.reseed = randomReseed
        self.kwds = kwds.copy()
        self.kwds['_taskStarted'] = self._taskStarted

    def __enter__(self):
        self.proc = None
        if self.workers == 1:
            return self.runSerial()
        return self.runParallel()

    def __exit__(self, *exc_info):
        if self.proc is not None:
            exceptOccurred = exc_info[0] is not None
            try:
                if exceptOccurred:
                    (sys.excepthook)(*exc_info)
            finally:
                os._exit(1 if exceptOccurred else 0)

        else:
            if self.showProgress:
                self.progressDlg.__exit__(None, None, None)

    def runSerial(self):
        if self.showProgress:
            self.progressDlg.__enter__()
            self.progressDlg.setMaximum(len(self.tasks))
        self.progress = {os.getpid(): []}
        return Tasker(self, None, self.tasks, self.kwds)

    def runParallel(self):
        self.childs = []
        workers = self.workers
        chunks = [[] for i in xrange(workers)]
        i = 0
        for i in range(len(self.tasks)):
            chunks[(i % workers)].append(self.tasks[i])

        for i in range(workers):
            proc = ForkedProcess(target=None, preProxy=(self.kwds), randomReseed=(self.reseed))
            if not proc.isParent:
                self.proc = proc
                return Tasker(self, proc, chunks[i], proc.forkedProxies)
                self.childs.append(proc)

        self.progress = dict([(ch.childPid, []) for ch in self.childs])
        try:
            if self.showProgress:
                self.progressDlg.__enter__()
                self.progressDlg.setMaximum(len(self.tasks))
            activeChilds = self.childs[:]
            self.exitCodes = []
            pollInterval = 0.01
            while len(activeChilds) > 0:
                waitingChildren = 0
                rem = []
                for ch in activeChilds:
                    try:
                        n = ch.processRequests()
                        if n > 0:
                            waitingChildren += 1
                    except ClosedError:
                        rem.append(ch)
                        if self.showProgress:
                            self.progressDlg += 1

                for ch in rem:
                    activeChilds.remove(ch)
                    while True:
                        try:
                            pid, exitcode = os.waitpid(ch.childPid, 0)
                            self.exitCodes.append(exitcode)
                            break
                        except OSError as ex:
                            try:
                                if ex.errno == 4:
                                    continue
                                else:
                                    raise
                            finally:
                                ex = None
                                del ex

                if self.showProgress:
                    if self.progressDlg.wasCanceled():
                        for ch in activeChilds:
                            ch.kill()

                        raise CanceledError()
                if waitingChildren > 1:
                    pollInterval *= 0.7
                else:
                    if waitingChildren == 0:
                        pollInterval /= 0.7
                    pollInterval = max(min(pollInterval, 0.5), 0.0005)
                    time.sleep(pollInterval)

        finally:
            if self.showProgress:
                self.progressDlg.__exit__(None, None, None)

        if len(self.exitCodes) < len(self.childs):
            raise Exception('Parallelizer started %d processes but only received exit codes from %d.' % (len(self.childs), len(self.exitCodes)))
        for code in self.exitCodes:
            if code != 0:
                raise Exception('Error occurred in parallel-executed subprocess (console output may have more information).')

        return []

    @staticmethod
    def suggestedWorkerCount():
        if 'linux' in sys.platform:
            try:
                cores = {}
                pid = None
                for line in open('/proc/cpuinfo'):
                    m = re.match('physical id\\s+:\\s+(\\d+)', line)
                    if m is not None:
                        pid = m.groups()[0]
                    m = re.match('cpu cores\\s+:\\s+(\\d+)', line)
                    if m is not None:
                        cores[pid] = int(m.groups()[0])

                return sum(cores.values())
            except:
                return multiprocessing.cpu_count()

        else:
            return multiprocessing.cpu_count()

    def _taskStarted(self, pid, i, **kwds):
        if self.showProgress:
            if len(self.progress[pid]) > 0:
                self.progressDlg += 1
            if pid == os.getpid():
                if self.progressDlg.wasCanceled():
                    raise CanceledError()
        self.progress[pid].append(i)


class Tasker(object):

    def __init__(self, parallelizer, process, tasks, kwds):
        self.proc = process
        self.par = parallelizer
        self.tasks = tasks
        for k, v in kwds.iteritems():
            setattr(self, k, v)

    def __iter__(self):
        for i, task in enumerate(self.tasks):
            self.index = i
            self._taskStarted((os.getpid()), i, _callSync='off')
            yield task

        if self.proc is not None:
            self.proc.close()

    def process(self):
        """
        Process requests from parent.
        Usually it is not necessary to call this unless you would like to 
        receive messages (such as exit requests) during an iteration.
        """
        if self.proc is not None:
            self.proc.processRequests()

    def numWorkers(self):
        """
        Return the number of parallel workers
        """
        return self.par.workers