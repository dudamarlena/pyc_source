# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/toil/worker.py
# Compiled at: 2020-04-03 17:41:24
# Size of source mod 2**32: 25941 bytes
from __future__ import absolute_import, print_function
from future import standard_library
standard_library.install_aliases()
from builtins import str
from builtins import map
from builtins import filter
import os, sys, copy, random, json, tempfile, traceback, time, signal, socket, logging, shutil
from toil.lib.compatibility import USING_PYTHON2
from toil.lib.expando import MagicExpando
from toil.common import Toil, safeUnpickleFromStream
from toil.fileStores.abstractFileStore import AbstractFileStore
from toil import logProcessContext
from toil.job import Job
from toil.lib.bioio import setLogLevel
from toil.lib.bioio import getTotalCpuTime
from toil.lib.bioio import getTotalCpuTimeAndMemoryUsage
from toil.deferred import DeferredFunctionManager
try:
    from toil.cwl.cwltoil import CWL_INTERNAL_JOBS
except ImportError:
    CWL_INTERNAL_JOBS = ()

logging.basicConfig()
logger = logging.getLogger(__name__)

def nextChainableJobGraph(jobGraph, jobStore):
    """Returns the next chainable jobGraph after this jobGraph if one
    exists, or None if the chain must terminate.
    """
    if len(jobGraph.stack) == 0 or len(jobGraph.services) > 0 or jobGraph.checkpoint != None:
        logger.debug('Stopping running chain of jobs: length of stack: %s, services: %s, checkpoint: %s', len(jobGraph.stack), len(jobGraph.services), jobGraph.checkpoint != None)
        return
    else:
        jobs = jobGraph.stack[(-1)]
        assert len(jobs) > 0
        if len(jobs) >= 2:
            logger.debug("No more jobs can run in series by this worker, it's got %i children", len(jobs) - 1)
            return
        successorJobNode = jobs[0]
        if successorJobNode.memory > jobGraph.memory:
            logger.debug('We need more memory for the next job, so finishing')
            return
        if successorJobNode.cores > jobGraph.cores:
            logger.debug('We need more cores for the next job, so finishing')
            return
        if successorJobNode.disk > jobGraph.disk:
            logger.debug('We need more disk for the next job, so finishing')
            return
        if successorJobNode.preemptable != jobGraph.preemptable:
            logger.debug('Preemptability is different for the next job, returning to the leader')
            return
        if successorJobNode.predecessorNumber > 1:
            logger.debug('The jobGraph has multiple predecessors, we must return to the leader.')
            return
        successorJobGraph = jobStore.load(successorJobNode.jobStoreID)
        if successorJobGraph.command.startswith('_toil '):
            successorJob = Job._loadJob(successorJobGraph.command, jobStore)
            if successorJob.checkpoint:
                logger.debug('Next job is checkpoint, so finishing')
                return
        return successorJobGraph


def workerScript(jobStore, config, jobName, jobStoreID, redirectOutputToLogFile=True):
    """
    Worker process script, runs a job. 
    
    :param str jobName: The "job name" (a user friendly name) of the job to be run
    :param str jobStoreLocator: Specifies the job store to use
    :param str jobStoreID: The job store ID of the job to be run
    """
    logging.basicConfig()
    setLogLevel(config.logLevel)
    logFileByteReportLimit = config.maxLogFileSize
    if config.badWorker > 0:
        if random.random() < config.badWorker:
            killTarget = os.getpid()
            sleepTime = config.badWorkerFailInterval * random.random()
            if os.fork() == 0:
                time.sleep(sleepTime)
                os.kill(killTarget, signal.SIGUSR1)
                time.sleep(0.01)
                try:
                    os.kill(killTarget, signal.SIGKILL)
                except OSError:
                    pass

                os._exit(0)
    with jobStore.readSharedFileStream('environment.pickle') as (fileHandle):
        environment = safeUnpickleFromStream(fileHandle)
    env_blacklist = {'TMPDIR',
     'TMP',
     'HOSTNAME',
     'HOSTTYPE',
     'HOME',
     'LOGNAME',
     'USER',
     'DISPLAY',
     'JAVA_HOME'}
    for i in environment:
        if i == 'PATH':
            if i in os.environ:
                if os.environ[i] != '':
                    os.environ[i] = environment[i] + ':' + os.environ[i]
            else:
                os.environ[i] = environment[i]
        else:
            if i not in env_blacklist:
                os.environ[i] = environment[i]

    if 'PYTHONPATH' in environment:
        for e in environment['PYTHONPATH'].split(':'):
            if e != '':
                sys.path.append(e)

    toilWorkflowDir = Toil.getLocalWorkflowDir(config.workflowID, config.workDir)
    localWorkerTempDir = tempfile.mkdtemp(dir=toilWorkflowDir)
    os.chmod(localWorkerTempDir, 493)
    redirectOutputToLogFile = redirectOutputToLogFile and not config.disableWorkerOutputCapture
    tempWorkerLogPath = os.path.join(localWorkerTempDir, 'worker_log.txt')
    if redirectOutputToLogFile:
        logger.info('Redirecting logging to %s', tempWorkerLogPath)
        sys.stdout.flush()
        sys.stderr.flush()
        origStdOut = os.dup(1)
        origStdErr = os.dup(2)
        logFh = os.open(tempWorkerLogPath, os.O_WRONLY | os.O_CREAT | os.O_APPEND)
        os.dup2(logFh, 1)
        os.dup2(logFh, 2)
        os.close(logFh)
    debugging = logging.getLogger().isEnabledFor(logging.DEBUG)
    workerFailed = False
    statsDict = MagicExpando()
    statsDict.jobs = []
    statsDict.workers.logsToMaster = []
    blockFn = lambda : True
    listOfJobs = [jobName]
    job = None
    try:
        logger.info('---TOIL WORKER OUTPUT LOG---')
        sys.stdout.flush()
        logProcessContext(config)
        deferredFunctionManager = DeferredFunctionManager(toilWorkflowDir)
        jobGraph = jobStore.load(jobStoreID)
        listOfJobs[0] = str(jobGraph)
        logger.debug('Parsed job wrapper')
        if jobGraph.command == None:
            logger.debug('Wrapper has no user job to run.')
            f = lambda jobs: [z for z in [[y for y in x if jobStore.exists(y.jobStoreID)] for x in jobs] if len(z) > 0]
            jobGraph.stack = f(jobGraph.stack)
            jobGraph.services = f(jobGraph.services)
            logger.debug('Cleaned up any references to completed successor jobs')
        oldLogFile = jobGraph.logJobStoreFileID
        if oldLogFile != None:
            jobGraph.logJobStoreFileID = None
            jobStore.update(jobGraph)
            jobStore.deleteFile(oldLogFile)
        if jobGraph.checkpoint != None:
            logger.debug('Job is a checkpoint')
            if len([i for l in jobGraph.stack for i in l]) > 0 or len(jobGraph.services) > 0:
                logger.debug('Checkpoint has failed.')
                assert jobGraph.remainingRetryCount >= 0
                jobGraph.remainingRetryCount = max(0, jobGraph.remainingRetryCount - 1)
                jobGraph.restartCheckpoint(jobStore)
            else:
                logger.debug('The checkpoint jobs seems to have completed okay, removing any checkpoint files to delete.')
                list(map(jobStore.deleteFile, list(filter(jobStore.fileExists, jobGraph.checkpointFilesToDelete))))
        if config.stats:
            startClock = getTotalCpuTime()
        startTime = time.time()
        while True:
            if jobGraph.command is not None:
                assert jobGraph.command.startswith('_toil ')
                logger.debug('Got a command to run: %s' % jobGraph.command)
                job = Job._loadJob(jobGraph.command, jobStore)
                if job.checkpoint:
                    jobGraph.checkpoint = jobGraph.command
                fileStore = AbstractFileStore.createFileStore(jobStore, jobGraph, localWorkerTempDir, blockFn, caching=(not config.disableCaching))
                with job._executor(jobGraph=jobGraph, stats=(statsDict if config.stats else None),
                  fileStore=fileStore):
                    with deferredFunctionManager.open() as (defer):
                        with fileStore.open(job):
                            blockFn = fileStore.waitForCommit
                            job._runner(jobGraph=jobGraph, jobStore=jobStore, fileStore=fileStore, defer=defer)
                            fileStore.startCommit(jobState=False)
                statsDict.workers.logsToMaster += fileStore.loggingMessages
            else:
                logger.debug('No user job to run, so finishing')
                break
            if AbstractFileStore._terminateEvent.isSet():
                raise RuntimeError('The termination flag is set')
            successorJobGraph = nextChainableJobGraph(jobGraph, jobStore)
            if successorJobGraph is None or config.disableChaining:
                break
            listOfJobs.append(str(successorJobGraph))
            jobGraph = copy.deepcopy(jobGraph)
            jobGraph.stack.pop()
            jobGraph.command = successorJobGraph.command
            jobGraph.stack += successorJobGraph.stack
            jobGraph.unitName = successorJobGraph.unitName
            jobGraph.jobName = successorJobGraph.jobName
            assert jobGraph.memory >= successorJobGraph.memory
            assert jobGraph.cores >= successorJobGraph.cores
            fileStore = AbstractFileStore.createFileStore(jobStore, jobGraph, localWorkerTempDir, blockFn, caching=(not config.disableCaching))
            blockFn = fileStore.waitForCommit
            fileStore.jobsToDelete.add(successorJobGraph.jobStoreID)
            fileStore.startCommit(jobState=True)
            jobGraph = copy.deepcopy(jobGraph)
            logger.debug('Starting the next job')

        if config.stats:
            totalCPUTime, totalMemoryUsage = getTotalCpuTimeAndMemoryUsage()
            statsDict.workers.time = str(time.time() - startTime)
            statsDict.workers.clock = str(totalCPUTime - startClock)
            statsDict.workers.memory = str(totalMemoryUsage)
        if redirectOutputToLogFile:
            logger.info('Worker log can be found at %s. Set --cleanWorkDir to retain this log', localWorkerTempDir)
        logger.info('Finished running the chain of jobs on this node, we ran for a total of %f seconds', time.time() - startTime)
    except:
        traceback.print_exc()
        logger.error('Exiting the worker because of a failed job on host %s', socket.gethostname())
        AbstractFileStore._terminateEvent.set()

    blockFn()
    if AbstractFileStore._terminateEvent.isSet():
        jobGraph = jobStore.load(jobStoreID)
        jobGraph.setupJobAfterFailure(config)
        workerFailed = True
        if job:
            if jobGraph.remainingRetryCount == 0:
                job._succeeded = False
    sys.stdout.flush()
    sys.stderr.flush()
    if redirectOutputToLogFile:
        os.fsync(1)
        os.fsync(2)
        os.dup2(origStdOut, 1)
        os.dup2(origStdErr, 2)
        os.close(origStdOut)
        os.close(origStdErr)
    if workerFailed:
        if redirectOutputToLogFile:
            jobGraph.logJobStoreFileID = jobStore.getEmptyFileStoreID((jobGraph.jobStoreID), cleanup=True)
            jobGraph.chainedJobs = listOfJobs
            with jobStore.updateFileStream(jobGraph.logJobStoreFileID) as (w):
                with open(tempWorkerLogPath, 'rb') as (f):
                    if os.path.getsize(tempWorkerLogPath) > logFileByteReportLimit != 0:
                        if logFileByteReportLimit > 0:
                            f.seek(-logFileByteReportLimit, 2)
                        elif logFileByteReportLimit < 0:
                            f.seek(logFileByteReportLimit, 0)
                    w.write(f.read())
            jobStore.update(jobGraph)
    if debugging or config.writeLogsFromAllJobs and not jobName.startswith(CWL_INTERNAL_JOBS):
        if redirectOutputToLogFile:
            with open(tempWorkerLogPath, 'rb') as (logFile):
                if os.path.getsize(tempWorkerLogPath) > logFileByteReportLimit != 0:
                    if logFileByteReportLimit > 0:
                        logFile.seek(-logFileByteReportLimit, 2)
                    elif logFileByteReportLimit < 0:
                        logFile.seek(logFileByteReportLimit, 0)
                logMessages = [line.decode('utf-8', 'skip') for line in logFile.read().splitlines()]
            statsDict.logs.names = listOfJobs
            statsDict.logs.messages = logMessages
    if debugging or config.stats or statsDict.workers.logsToMaster:
        if not workerFailed:
            if USING_PYTHON2:
                jobStore.writeStatsAndLogging(json.dumps(statsDict, ensure_ascii=True))
            else:
                jobStore.writeStatsAndLogging(json.dumps(statsDict, ensure_ascii=True).encode())
    cleanUp = config.cleanWorkDir
    if cleanUp == 'always' or cleanUp == 'onSuccess' and not workerFailed or cleanUp == 'onError' and workerFailed:
        shutil.rmtree(localWorkerTempDir)
    if not workerFailed:
        if jobGraph.command == None:
            if len(jobGraph.stack) == 0:
                if len(jobGraph.services) == 0:
                    jobStore.delete(jobGraph.jobStoreID)


def main(argv=None):
    if argv is None:
        argv = sys.argv
    if len(argv) < 4:
        if len(argv) < 1:
            sys.stderr.write('Error: Toil worker invoked without its own name\n')
            sys.exit(1)
        else:
            sys.stderr.write('Error: usage: %s JOB_NAME JOB_STORE_LOCATOR JOB_STORE_ID\n' % argv[0])
            sys.exit(1)
    jobName = argv[1]
    jobStoreLocator = argv[2]
    jobStoreID = argv[3]
    jobStore = Toil.resumeJobStore(jobStoreLocator)
    config = jobStore.config
    workerScript(jobStore, config, jobName, jobStoreID)