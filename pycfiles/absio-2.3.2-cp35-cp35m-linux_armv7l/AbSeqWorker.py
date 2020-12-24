# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/abseqPy/IgMultiRepertoire/AbSeqWorker.py
# Compiled at: 2019-04-23 02:08:32
import traceback, sys
from multiprocessing import Process, current_process, Lock, Value

class AbSeqWorker(Process):
    ops = FASTQC, ANNOT, ABUN, PROD, DIVER, SECR, UTR5, RSA, PRIM, SEQLEN = ('runFastqc',
                                                                             'annotateClones',
                                                                             'analyzeAbundance',
                                                                             'analyzeProductivity',
                                                                             'analyzeDiversity',
                                                                             'analyzeSecretionSignal',
                                                                             'analyze5UTR',
                                                                             'analyzeRestrictionSites',
                                                                             'analyzePrimerSpecificity',
                                                                             'analyzeSeqLen')

    def __init__(self, repertoire, resultQueue, resourcePool):
        super(AbSeqWorker, self).__init__()
        self.repertoire = repertoire
        self.resultQueue = resultQueue
        self.resourcePool = resourcePool

    def run(self):
        while True:
            task, args, kwargs = self.repertoire._nextTask()
            if task is None:
                self.repertoire._minimize()
                self.resultQueue.put(self.repertoire)
                self.resourcePool.increment(self.repertoire.threads)
                break
            try:
                self.repertoire.threads += self.resourcePool.consume()
                getattr(self.repertoire, task)(*args, **kwargs)
            except Exception as e:
                exceptionType, exceptionValue, exceptionTraceback = sys.exc_info()
                fmtMsg = 'Job name: ' + str(self.repertoire.name) + ' :: An error occurred while processing ' + str(task)
                newE = e.message
                if self.resultQueue is not None:
                    self.resultQueue.put((newE, fmtMsg,
                     traceback.format_exception(exceptionType, exceptionValue, exceptionTraceback)))
                continue

        return


class AbSeqWorkerException(Exception):

    def __init__(self, message, errors, tracebackMsg):
        super(AbSeqWorkerException, self).__init__(message)
        self.errors = errors
        self.tracebackMsg = ('').join(tracebackMsg)


class ResourcePool:

    def __init__(self, initResource):
        self._lock = Lock()
        self.n = Value('i', initResource)

    def increment(self, n=1):
        with self._lock:
            self.n.value += n
            assert self.n.value >= 0

    def value(self):
        with self._lock:
            return self.n.value

    def consume(self):
        with self._lock:
            if self.n.value > 0:
                n = self.n.value
                self.n.value = 0
                return n
            else:
                return 0