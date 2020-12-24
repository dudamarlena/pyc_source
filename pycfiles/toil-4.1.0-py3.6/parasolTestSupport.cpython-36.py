# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/toil/batchSystems/parasolTestSupport.py
# Compiled at: 2020-05-07 00:32:15
# Size of source mod 2**32: 4450 bytes
from __future__ import absolute_import
from builtins import object
import logging, tempfile, threading, time, subprocess, signal, os, errno
from toil.lib.objects import InnerClass
from toil.lib.threading import cpu_count
from toil import physicalMemory
log = logging.getLogger(__name__)

def rm_f(path):
    """Remove the file at the given path with os.remove(), ignoring errors caused by the file's absence."""
    try:
        os.remove(path)
    except OSError as e:
        if e.errno == errno.ENOENT:
            pass
        else:
            raise


class ParasolTestSupport(object):
    __doc__ = '\n    For test cases that need a running Parasol leader and worker on the local host\n    '

    def _startParasol(self, numCores=None, memory=None):
        if numCores is None:
            numCores = cpu_count()
        if memory is None:
            memory = physicalMemory()
        self.numCores = numCores
        self.memory = memory
        self.leader = self.ParasolLeaderThread()
        self.leader.start()
        self.worker = self.ParasolWorkerThread()
        self.worker.start()
        while self.leader.popen is None or self.worker.popen is None:
            log.info('Waiting for leader and worker processes')
            time.sleep(0.1)

    def _stopParasol(self):
        self.worker.popen.kill()
        self.worker.join()
        self.leader.popen.kill()
        self.leader.join()
        for path in ('para.results', 'parasol.jid'):
            rm_f(path)

    class ParasolThread(threading.Thread):
        lock = threading.Lock()

        def __init__(self):
            threading.Thread.__init__(self)
            self.popen = None

        def parasolCommand(self):
            raise NotImplementedError

        def run(self):
            command = self.parasolCommand()
            with self.lock:
                self.popen = subprocess.Popen(command)
            status = self.popen.wait()
            if status != 0:
                if status != -signal.SIGKILL:
                    log.error("Command '%s' failed with %i.", command, status)
                    raise subprocess.CalledProcessError(status, command)
            log.info('Exiting %s', self.__class__.__name__)

    @InnerClass
    class ParasolLeaderThread(ParasolThread):

        def __init__(self):
            super(ParasolTestSupport.ParasolLeaderThread, self).__init__()
            self.machineList = None

        def run(self):
            with tempfile.NamedTemporaryFile(prefix='machineList.txt', mode='w') as (f):
                self.machineList = f.name
                f.write('localhost {numCores} {ramSize} {tempDir} {tempDir} 1024 foo'.format(numCores=(self.outer.numCores),
                  tempDir=(tempfile.gettempdir()),
                  ramSize=(self.outer.memory / 1024 / 1024)))
                f.flush()
                super(ParasolTestSupport.ParasolLeaderThread, self).run()

        def parasolCommand(self):
            return ['paraHub',
             '-spokes=1',
             '-debug',
             self.machineList]

    @InnerClass
    class ParasolWorkerThread(ParasolThread):

        def parasolCommand(self):
            return ['paraNode',
             '-cpu=%i' % self.outer.numCores,
             '-randomDelay=0',
             '-debug',
             'start']