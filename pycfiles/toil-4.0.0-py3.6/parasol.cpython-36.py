# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/toil/batchSystems/parasol.py
# Compiled at: 2020-04-03 17:41:24
# Size of source mod 2**32: 16708 bytes
from __future__ import absolute_import
from __future__ import division
from builtins import next
from builtins import str
from past.utils import old_div
from future.utils import listitems
import logging, os, re, sys, subprocess, tempfile, time
from threading import Thread
from six.moves.queue import Empty, Queue
from six import itervalues
from toil.lib.iterables import concat
from shutil import which
from toil.batchSystems.abstractBatchSystem import BatchSystemSupport, UpdatedBatchJobInfo
from toil.lib.bioio import getTempFile
from toil.common import Toil
logger = logging.getLogger(__name__)

class ParasolBatchSystem(BatchSystemSupport):
    __doc__ = '\n    The interface for Parasol.\n    '

    @classmethod
    def supportsWorkerCleanup(cls):
        return False

    @classmethod
    def supportsAutoDeployment(cls):
        return False

    def __init__(self, config, maxCores, maxMemory, maxDisk):
        super(ParasolBatchSystem, self).__init__(config, maxCores, maxMemory, maxDisk)
        if maxMemory != sys.maxsize:
            logger.warning('The Parasol batch system does not support maxMemory.')
        command = config.parasolCommand
        if os.path.sep not in command:
            try:
                command = which(command)
            except StopIteration:
                raise RuntimeError("Can't find %s on PATH." % command)

        logger.debug('Using Parasol at %s', command)
        self.parasolCommand = command
        jobStoreType, path = Toil.parseLocator(config.jobStore)
        if jobStoreType != 'file':
            raise RuntimeError("The parasol batch system doesn't currently work with any jobStore type except file jobStores.")
        self.parasolResultsDir = tempfile.mkdtemp(dir=(os.path.abspath(path)))
        logger.debug('Using parasol results dir: %s', self.parasolResultsDir)
        self.resultsFiles = dict()
        self.maxBatches = config.parasolMaxBatches
        self.cpuUsageQueue = Queue()
        self.updatedJobsQueue = Queue()
        self.running = True
        self.worker = Thread(target=(self.updatedJobWorker), args=())
        self.worker.start()
        self.usedCpus = 0
        self.jobIDsToCpu = {}
        self.runningJobs = set()

    def _runParasol(self, command, autoRetry=True):
        """
        Issues a parasol command using popen to capture the output. If the command fails then it
        will try pinging parasol until it gets a response. When it gets a response it will
        recursively call the issue parasol command, repeating this pattern for a maximum of N
        times. The final exit value will reflect this.
        """
        command = list(concat(self.parasolCommand, command))
        while True:
            logger.debug('Running %r', command)
            process = subprocess.Popen(command, stdout=(subprocess.PIPE),
              stderr=(subprocess.PIPE),
              bufsize=(-1))
            stdout, stderr = process.communicate()
            status = process.wait()
            for line in stderr.decode('utf-8').split('\n'):
                if line:
                    logger.warning(line)

            if status == 0:
                return (0, stdout.decode('utf-8').split('\n'))
            else:
                message = 'Command %r failed with exit status %i' % (command, status)
                if autoRetry:
                    logger.warning(message)
                else:
                    logger.error(message)
                return (
                 status, None)
            logger.warning('Waiting for a 10s, before trying again')
            time.sleep(10)

    parasolOutputPattern = re.compile('your job ([0-9]+).*')

    def issueBatchJob(self, jobNode):
        """
        Issues parasol with job commands.
        """
        self.checkResourceRequest(jobNode.memory, jobNode.cores, jobNode.disk)
        MiB = 1048576
        truncatedMemory = old_div(jobNode.memory, MiB) * MiB
        if len(self.resultsFiles) >= self.maxBatches:
            raise RuntimeError('Number of batches reached limit of %i' % self.maxBatches)
        try:
            results = self.resultsFiles[(truncatedMemory, jobNode.cores)]
        except KeyError:
            results = getTempFile(rootDir=(self.parasolResultsDir))
            self.resultsFiles[(truncatedMemory, jobNode.cores)] = results

        command = ' '.join(concat('env', self._ParasolBatchSystem__environment(), jobNode.command))
        parasolCommand = ['-verbose',
         '-ram=%i' % jobNode.memory,
         '-cpu=%i' % jobNode.cores,
         '-results=' + results,
         'add', 'job', command]
        self.usedCpus += jobNode.cores
        while 1:
            try:
                jobID = self.cpuUsageQueue.get_nowait()
            except Empty:
                break

            if jobID in list(self.jobIDsToCpu.keys()):
                self.usedCpus -= self.jobIDsToCpu.pop(jobID)
            assert self.usedCpus >= 0

        while self.usedCpus > self.maxCores:
            jobID = self.cpuUsageQueue.get()
            if jobID in list(self.jobIDsToCpu.keys()):
                self.usedCpus -= self.jobIDsToCpu.pop(jobID)
            assert self.usedCpus >= 0

        while 1:
            line = self._runParasol(parasolCommand)[1][0]
            match = self.parasolOutputPattern.match(line)
            if match is None:
                logger.debug('We failed to properly add the job, we will try again after a 5s.')
                time.sleep(5)
            else:
                jobID = int(match.group(1))
                self.jobIDsToCpu[jobID] = jobNode.cores
                self.runningJobs.add(jobID)
                logger.debug('Got the parasol job id: %s from line: %s' % (jobID, line))
                return jobID

    def setEnv(self, name, value=None):
        if value:
            if ' ' in value:
                raise ValueError('Parasol does not support spaces in environment variable values.')
        return super(ParasolBatchSystem, self).setEnv(name, value)

    def __environment(self):
        return (k + '=' + (os.environ[k] if v is None else v) for k, v in listitems(self.environment))

    def killBatchJobs(self, jobIDs):
        """Kills the given jobs, represented as Job ids, then checks they are dead by checking
        they are not in the list of issued jobs.
        """
        while True:
            for jobID in jobIDs:
                if jobID in self.runningJobs:
                    self.runningJobs.remove(jobID)
                exitValue = self._runParasol(['remove', 'job', str(jobID)], autoRetry=False)[0]
                logger.debug('Tried to remove jobID: %i, with exit value: %i' % (jobID, exitValue))

            runningJobs = self.getIssuedBatchJobIDs()
            if set(jobIDs).difference(set(runningJobs)) == set(jobIDs):
                break
            logger.warning('Tried to kill some jobs, but something happened and they are still going, will try againin 5s.')
            time.sleep(5)

        for jobID in jobIDs:
            if jobID in list(self.jobIDsToCpu.keys()):
                self.usedCpus -= self.jobIDsToCpu.pop(jobID)

    runningPattern = re.compile('r\\s+([0-9]+)\\s+[\\S]+\\s+[\\S]+\\s+([0-9]+)\\s+[\\S]+')

    def getJobIDsForResultsFile(self, resultsFile):
        """
        Get all queued and running jobs for a results file.
        """
        jobIDs = []
        for line in self._runParasol(['-extended', 'list', 'jobs'])[1]:
            fields = line.strip().split()
            if not len(fields) == 0:
                if fields[(-1)] != resultsFile:
                    pass
                else:
                    jobID = fields[0]
                    jobIDs.append(int(jobID))

        return set(jobIDs)

    def getIssuedBatchJobIDs(self):
        """
        Gets the list of jobs issued to parasol in all results files, but not including jobs
        created by other users.
        """
        issuedJobs = set()
        for resultsFile in itervalues(self.resultsFiles):
            issuedJobs.update(self.getJobIDsForResultsFile(resultsFile))

        return list(issuedJobs)

    def getRunningBatchJobIDs(self):
        """
        Returns map of running jobIDs and the time they have been running.
        """
        runningJobs = {}
        issuedJobs = self.getIssuedBatchJobIDs()
        for line in self._runParasol(['pstat2'])[1]:
            if line != '':
                match = self.runningPattern.match(line)
                if match is not None:
                    jobID = int(match.group(1))
                    startTime = int(match.group(2))
                    if jobID in issuedJobs:
                        runningJobs[jobID] = time.time() - startTime

        return runningJobs

    def getUpdatedBatchJob(self, maxWait):
        while True:
            try:
                item = self.updatedJobsQueue.get(timeout=maxWait)
            except Empty:
                return
            else:
                try:
                    self.runningJobs.remove(item.jobID)
                except KeyError:
                    pass
                else:
                    return item

    def updatedJobWorker(self):
        """
        We use the parasol results to update the status of jobs, adding them
        to the list of updated jobs.

        Results have the following structure.. (thanks Mark D!)

        int status;    /* Job status - wait() return format. 0 is good. */
        char *host;    /* Machine job ran on. */
        char *jobId;    /* Job queuing system job ID */
        char *exe;    /* Job executable file (no path) */
        int usrTicks;    /* 'User' CPU time in ticks. */
        int sysTicks;    /* 'System' CPU time in ticks. */
        unsigned submitTime;    /* Job submission time in seconds since 1/1/1970 */
        unsigned startTime;    /* Job start time in seconds since 1/1/1970 */
        unsigned endTime;    /* Job end time in seconds since 1/1/1970 */
        char *user;    /* User who ran job */
        char *errFile;    /* Location of stderr file on host */

        Plus you finally have the command name.
        """
        resultsFiles = set()
        resultsFileHandles = []
        try:
            try:
                while self.running:
                    newResultsFiles = set(os.listdir(self.parasolResultsDir)).difference(resultsFiles)
                    for newFile in newResultsFiles:
                        newFilePath = os.path.join(self.parasolResultsDir, newFile)
                        resultsFileHandles.append(open(newFilePath, 'r'))
                        resultsFiles.add(newFile)

                    for fileHandle in resultsFileHandles:
                        while self.running:
                            line = fileHandle.readline()
                            if not line:
                                break
                            assert line[(-1)] == '\n'
                            status, host, jobId, exe, usrTicks, sysTicks, submitTime, startTime, endTime, user, errFile, command = line[:-1].split(None, 11)
                            status = int(status)
                            jobId = int(jobId)
                            if os.WIFEXITED(status):
                                status = os.WEXITSTATUS(status)
                            else:
                                status = -status
                            self.cpuUsageQueue.put(jobId)
                            startTime = int(startTime)
                            endTime = int(endTime)
                            if endTime == startTime:
                                usrTicks = int(usrTicks)
                                sysTicks = int(sysTicks)
                                wallTime = float(max(1, usrTicks + sysTicks)) * 0.01
                            else:
                                wallTime = float(endTime - startTime)
                            self.updatedJobsQueue.put(UpdatedBatchJobInfo(jobID=jobId, exitStatus=status, wallTime=wallTime, exitReason=None))

                    time.sleep(1)

            except:
                logger.warning('Error occurred while parsing parasol results files.')
                raise

        finally:
            for fileHandle in resultsFileHandles:
                fileHandle.close()

    def shutdown(self):
        self.killBatchJobs(self.getIssuedBatchJobIDs())
        for results in itervalues(self.resultsFiles):
            exitValue = self._runParasol(['-results=' + results, 'clear', 'sick'], autoRetry=False)[0]
            if exitValue is not None:
                logger.warning('Could not clear sick status of the parasol batch %s' % results)
            exitValue = self._runParasol(['-results=' + results, 'flushResults'], autoRetry=False)[0]
            if exitValue is not None:
                logger.warning('Could not flush the parasol batch %s' % results)

        self.running = False
        logger.debug('Joining worker thread...')
        self.worker.join()
        logger.debug('... joined worker thread.')
        for results in list(self.resultsFiles.values()):
            os.remove(results)

        os.rmdir(self.parasolResultsDir)

    @classmethod
    def setOptions(cls, setOption):
        from toil.common import iC
        setOption('parasolCommand', None, None, 'parasol')
        setOption('parasolMaxBatches', int, iC(1), 10000)