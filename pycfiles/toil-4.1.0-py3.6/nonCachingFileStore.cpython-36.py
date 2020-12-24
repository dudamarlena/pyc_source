# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/toil/fileStores/nonCachingFileStore.py
# Compiled at: 2020-05-07 00:32:15
# Size of source mod 2**32: 11565 bytes
from __future__ import absolute_import, print_function
from future import standard_library
standard_library.install_aliases()
from builtins import map
from builtins import str
from collections import defaultdict
from contextlib import contextmanager
import dill, errno, fcntl, logging, os, sys, uuid
from toil.lib.misc import robust_rmtree
from toil.lib.threading import get_process_name, process_name_exists
from toil.lib.humanize import bytes2human
from toil.common import getDirSizeRecursively, getFileSystemSize
from toil.lib.bioio import makePublicDir
from toil.fileStores.abstractFileStore import AbstractFileStore
from toil.fileStores import FileID
logger = logging.getLogger(__name__)
if sys.version_info[0] < 3:
    FileNotFoundError = OSError

class NonCachingFileStore(AbstractFileStore):

    def __init__(self, jobStore, jobGraph, localTempDir, waitForPreviousCommit):
        super(NonCachingFileStore, self).__init__(jobStore, jobGraph, localTempDir, waitForPreviousCommit)
        self.jobStateFile = None
        self.localFileMap = defaultdict(list)

    @contextmanager
    def open(self, job):
        jobReqs = job.disk
        startingDir = os.getcwd()
        self.localTempDir = makePublicDir(os.path.join(self.localTempDir, str(uuid.uuid4())))
        self._removeDeadJobs(self.workDir)
        self.jobStateFile = self._createJobStateFile()
        freeSpace, diskSize = getFileSystemSize(self.localTempDir)
        if freeSpace <= 0.1 * diskSize:
            logger.warning('Starting job %s with less than 10%% of disk space remaining.', self.jobName)
        try:
            os.chdir(self.localTempDir)
            yield
        finally:
            diskUsed = getDirSizeRecursively(self.localTempDir)
            logString = 'Job {jobName} used {percent:.2f}% ({humanDisk}B [{disk}B] used, {humanRequestedDisk}B [{requestedDisk}B] requested) at the end of its run.'.format(jobName=(self.jobName),
              percent=(float(diskUsed) / jobReqs * 100 if jobReqs > 0 else 0.0),
              humanDisk=(bytes2human(diskUsed)),
              disk=diskUsed,
              humanRequestedDisk=(bytes2human(jobReqs)),
              requestedDisk=jobReqs)
            self.logToMaster(logString, level=(logging.DEBUG))
            if diskUsed > jobReqs:
                self.logToMaster(('Job used more disk than requested. Consider modifying the user script to avoid the chance of failure due to incorrectly requested resources. ' + logString),
                  level=(logging.WARNING))
            os.chdir(startingDir)
            os.remove(self.jobStateFile)

    def writeGlobalFile(self, localFileName, cleanup=False):
        absLocalFileName = self._resolveAbsoluteLocalPath(localFileName)
        creatorID = self.jobGraph.jobStoreID
        fileStoreID = self.jobStore.writeFile(absLocalFileName, creatorID, cleanup)
        self.localFileMap[fileStoreID].append(absLocalFileName)
        return FileID.forPath(fileStoreID, absLocalFileName)

    def readGlobalFile(self, fileStoreID, userPath=None, cache=True, mutable=False, symlink=False):
        if userPath is not None:
            localFilePath = self._resolveAbsoluteLocalPath(userPath)
            if os.path.exists(localFilePath):
                raise RuntimeError(' File %s ' % localFilePath + ' exists. Cannot Overwrite.')
        else:
            localFilePath = self.getLocalTempFileName()
        self.jobStore.readFile(fileStoreID, localFilePath, symlink=symlink)
        self.localFileMap[fileStoreID].append(localFilePath)
        return localFilePath

    @contextmanager
    def readGlobalFileStream(self, fileStoreID):
        with self.jobStore.readFileStream(fileStoreID) as (f):
            yield f

    def exportFile(self, jobStoreFileID, dstUrl):
        self.jobStore.exportFile(jobStoreFileID, dstUrl)

    def deleteLocalFile(self, fileStoreID):
        try:
            localFilePaths = self.localFileMap.pop(fileStoreID)
        except KeyError:
            raise OSError(errno.ENOENT, 'Attempting to delete a non-local file')
        else:
            for localFilePath in localFilePaths:
                os.remove(localFilePath)

    def deleteGlobalFile(self, fileStoreID):
        try:
            self.deleteLocalFile(fileStoreID)
        except OSError as e:
            if e.errno == errno.ENOENT:
                pass
            else:
                raise

        self.filesToDelete.add(str(fileStoreID))

    def waitForCommit(self):
        return True

    def startCommit(self, jobState=False):
        if self.waitForPreviousCommit is not None:
            self.waitForPreviousCommit()
        else:
            if not jobState:
                return
            try:
                self.jobGraph.filesToDelete = list(self.filesToDelete)
                self.jobStore.update(self.jobGraph)
                list(map(self.jobStore.delete, self.jobsToDelete))
                list(map(self.jobStore.deleteFile, self.filesToDelete))
                if len(self.filesToDelete) > 0:
                    self.jobGraph.filesToDelete = []
                    self.jobStore.update(self.jobGraph)
            except:
                self._terminateEvent.set()
                raise

    def __del__(self):
        """
        Cleanup function that is run when destroying the class instance.  Nothing to do since there
        are no async write events.
        """
        pass

    @classmethod
    def _removeDeadJobs(cls, nodeInfo, batchSystemShutdown=False):
        """
        Look at the state of all jobs registered in the individual job state files, and handle them
        (clean up the disk)

        :param str nodeInfo: The location of the workflow directory on the node.
        :param bool batchSystemShutdown: Is the batch system in the process of shutting down?
        :return:
        """
        for jobState in cls._getAllJobStates(nodeInfo):
            if not process_name_exists(nodeInfo, jobState['jobProcessName']):
                try:
                    dirFD = os.open(jobState['jobDir'], os.O_RDONLY)
                except FileNotFoundError:
                    continue

                try:
                    fcntl.lockf(dirFD, fcntl.LOCK_EX | fcntl.LOCK_NB)
                except IOError as e:
                    os.close(dirFD)
                else:
                    logger.warning('Detected that job (%s) prematurely terminated.  Fixing the state of the job on disk.', jobState['jobName'])
                    try:
                        if not batchSystemShutdown:
                            logger.debug('Deleting the stale working directory.')
                            robust_rmtree(jobState['jobDir'])
                    finally:
                        fcntl.lockf(dirFD, fcntl.LOCK_UN)
                        os.close(dirFD)

    @staticmethod
    def _getAllJobStates(workflowDir):
        """
        Generator function that deserializes and yields the job state for every job on the node,
        one at a time.

        :param str workflowDir: The location of the workflow directory on the node.
        :return: dict with keys (jobName,  jobProcessName, jobDir)
        :rtype: dict
        """
        jobStateFiles = []
        for root, dirs, files in os.walk(workflowDir.encode('utf-8')):
            for filename in files:
                if filename == '.jobState'.encode('utf-8'):
                    jobStateFiles.append(os.path.join(root, filename).decode('utf-8'))

        for filename in jobStateFiles:
            try:
                yield NonCachingFileStore._readJobState(filename)
            except IOError as e:
                if e.errno == 2:
                    continue
                else:
                    raise

    @staticmethod
    def _readJobState(jobStateFileName):
        with open(jobStateFileName, 'rb') as (fH):
            state = dill.load(fH)
        return state

    def _createJobStateFile(self):
        """
        Create the job state file for the current job and fill in the required
        values.

        :return: Path to the job state file
        :rtype: str
        """
        jobStateFile = os.path.join(self.localTempDir, '.jobState')
        jobState = {'jobProcessName':get_process_name(self.workDir),  'jobName':self.jobName, 
         'jobDir':self.localTempDir}
        with open(jobStateFile + '.tmp', 'wb') as (fH):
            dill.dump(jobState, fH)
        os.rename(jobStateFile + '.tmp', jobStateFile)
        return jobStateFile

    @classmethod
    def shutdown(cls, dir_):
        """
        :param dir_: The workflow directory that will contain all the individual worker directories.
        """
        cls._removeDeadJobs(dir_, batchSystemShutdown=True)