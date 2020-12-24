# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/toil/jobStores/fileJobStore.py
# Compiled at: 2020-04-03 17:41:24
# Size of source mod 2**32: 37095 bytes
from __future__ import absolute_import
from builtins import range
from contextlib import contextmanager
import logging, random, shutil, os, re, tempfile, stat, errno, time
try:
    import cPickle as pickle
except ImportError:
    import pickle

from toil.fileStores import FileID
from toil.lib.bioio import absSymPath
from toil.lib.misc import mkdir_p, robust_rmtree, AtomicFileCreate, atomic_copy, atomic_copyobj
from toil.jobStores.abstractJobStore import AbstractJobStore, NoSuchJobException, NoSuchFileException, JobStoreExistsException, NoSuchJobStoreException
from toil.jobGraph import JobGraph
logger = logging.getLogger(__name__)

class FileJobStore(AbstractJobStore):
    __doc__ = '\n    A job store that uses a directory on a locally attached file system. To be compatible with\n    distributed batch systems, that file system must be shared by all worker nodes.\n    '
    validDirs = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
    validDirsSet = set(validDirs)
    JOB_DIR_PREFIX = 'instance-'
    JOB_NAME_DIR_PREFIX = 'kind-'
    BUFFER_SIZE = 10485760

    def __init__(self, path, fanOut=1000):
        """
        :param str path: Path to directory holding the job store
        :param int fanOut: Number of items to have in a directory before making
                           subdirectories
        """
        super(FileJobStore, self).__init__()
        self.jobStoreDir = absSymPath(path)
        logger.debug("Path to job store directory is '%s'.", self.jobStoreDir)
        self.jobsDir = os.path.join(self.jobStoreDir, 'jobs')
        self.statsDir = os.path.join(self.jobStoreDir, 'stats')
        self.filesDir = os.path.join(self.jobStoreDir, 'files/no-job')
        self.jobFilesDir = os.path.join(self.jobStoreDir, 'files/for-job')
        self.sharedFilesDir = os.path.join(self.jobStoreDir, 'files/shared')
        self.fanOut = fanOut
        self.linkImports = None
        self.moveExports = None

    def __repr__(self):
        return 'FileJobStore({})'.format(self.jobStoreDir)

    def initialize(self, config):
        try:
            os.mkdir(self.jobStoreDir)
        except OSError as e:
            if e.errno == errno.EEXIST:
                raise JobStoreExistsException(self.jobStoreDir)
            else:
                raise

        mkdir_p(self.jobsDir)
        mkdir_p(self.statsDir)
        mkdir_p(self.filesDir)
        mkdir_p(self.jobFilesDir)
        mkdir_p(self.sharedFilesDir)
        self.linkImports = config.linkImports
        self.moveExports = config.moveExports
        super(FileJobStore, self).initialize(config)

    def resume(self):
        if not os.path.isdir(self.jobStoreDir):
            raise NoSuchJobStoreException(self.jobStoreDir)
        super(FileJobStore, self).resume()

    def destroy(self):
        if os.path.exists(self.jobStoreDir):
            robust_rmtree(self.jobStoreDir)

    def create(self, jobNode):
        usefulFilename = self._makeStringFilenameSafe(jobNode.jobName)
        absJobDir = tempfile.mkdtemp(prefix=(self.JOB_DIR_PREFIX), dir=(self._getArbitraryJobsDirForName(usefulFilename)))
        job = JobGraph.fromJobNode(jobNode, jobStoreID=(self._getJobIdFromDir(absJobDir)), tryCount=(self._defaultTryCount()))
        if hasattr(self, '_batchedJobGraphs'):
            if self._batchedJobGraphs is not None:
                self._batchedJobGraphs.append(job)
        else:
            self.update(job)
        return job

    @contextmanager
    def batch(self):
        self._batchedJobGraphs = []
        yield
        for jobGraph in self._batchedJobGraphs:
            self.update(jobGraph)

        self._batchedJobGraphs = None

    def waitForExists(self, jobStoreID, maxTries=35, sleepTime=1):
        """Spin-wait and block for a file to appear before returning False if it does not.

        The total max wait time is maxTries * sleepTime. The current default is
        tuned to match Linux NFS defaults where the client's cache of the directory
        listing on the server is supposed to become coherent within 30 sec.
        Delayes beyond that would probably indicate a pathologically slow file system
        that just should not be used for the jobStore.

        The warning will be sent to the log only on the first retry.

        In practice, the need for retries happens rarely, but it does happen
        over the course of large workflows with a jobStore on a busy NFS."""
        for iTry in range(1, maxTries + 1):
            jobFile = self._getJobFileName(jobStoreID)
            if os.path.exists(jobFile):
                return True
            if iTry >= maxTries:
                return False
            if iTry == 1:
                logger.warning('Job file `{}` for job `{}` does not exist (yet). We will try #{} more times with {}s intervals.'.format(jobFile, jobStoreID, maxTries - iTry, sleepTime))
            time.sleep(sleepTime)

        return False

    def exists(self, jobStoreID):
        return os.path.exists(self._getJobFileName(jobStoreID))

    def getPublicUrl(self, jobStoreFileID):
        self._checkJobStoreFileID(jobStoreFileID)
        jobStorePath = self._getFilePathFromId(jobStoreFileID)
        if os.path.exists(jobStorePath):
            return 'file:' + jobStorePath
        raise NoSuchFileException(jobStoreFileID)

    def getSharedPublicUrl(self, sharedFileName):
        jobStorePath = os.path.join(self.sharedFilesDir, sharedFileName)
        if os.path.exists(jobStorePath):
            return 'file:' + jobStorePath
        raise NoSuchFileException(sharedFileName)

    def load(self, jobStoreID):
        self._checkJobStoreId(jobStoreID)
        jobFile = self._getJobFileName(jobStoreID)
        with open(jobFile, 'rb') as (fileHandle):
            job = pickle.load(fileHandle)
        if os.path.isfile(jobFile + '.new'):
            logger.warning('There was a .new file for the job: %s', jobStoreID)
            os.remove(jobFile + '.new')
            job.setupJobAfterFailure(self.config)
        return job

    def update(self, job):
        with open(self._getJobFileName(job.jobStoreID) + '.new', 'wb') as (f):
            pickle.dump(job, f)
        os.rename(self._getJobFileName(job.jobStoreID) + '.new', self._getJobFileName(job.jobStoreID))

    def delete(self, jobStoreID):
        if self.exists(jobStoreID):
            robust_rmtree(self._getJobFilesCleanupDir(jobStoreID))
            robust_rmtree(self._getJobDirFromId(jobStoreID))

    def jobs(self):
        for tempDir in self._jobDirectories():
            for i in os.listdir(tempDir):
                logger.warning('Job Dir: %s' % i)
                if i.startswith(self.JOB_DIR_PREFIX):
                    jobId = self._getJobIdFromDir(os.path.join(tempDir, i))
                    try:
                        if self.exists(jobId):
                            yield self.load(jobId)
                    except NoSuchJobException:
                        pass

    @contextmanager
    def optionalHardCopy(self, hardlink):
        if hardlink:
            saved = self.linkImports
            self.linkImports = False
        yield
        if hardlink:
            self.linkImports = saved

    def _copyOrLink(self, srcURL, destPath):
        srcPath = self._extractPathFromUrl(srcURL)
        if self.linkImports:
            os.symlink(os.path.realpath(srcPath), destPath)
        else:
            atomic_copy(srcPath, destPath)

    def _importFile(self, otherCls, url, sharedFileName=None, hardlink=False):
        if issubclass(otherCls, FileJobStore):
            if sharedFileName is None:
                absPath = self._getUniqueFilePath(url.path)
                with self.optionalHardCopy(hardlink):
                    self._copyOrLink(url, absPath)
                return FileID(self._getFileIdFromPath(absPath), os.stat(absPath).st_size)
            else:
                self._requireValidSharedFileName(sharedFileName)
                path = self._getSharedFilePath(sharedFileName)
                with self.optionalHardCopy(hardlink):
                    self._copyOrLink(url, path)
                return
        else:
            return super(FileJobStore, self)._importFile(otherCls, url, sharedFileName=sharedFileName)

    def _exportFile(self, otherCls, jobStoreFileID, url):
        if issubclass(otherCls, FileJobStore):
            srcPath = self._getFilePathFromId(jobStoreFileID)
            destPath = self._extractPathFromUrl(url)
            if self.moveExports:
                self._move_and_linkback(srcPath, destPath)
            else:
                atomic_copy(srcPath, destPath)
        else:
            super(FileJobStore, self)._defaultExportFile(otherCls, jobStoreFileID, url)

    def _move_and_linkback(self, srcPath, destPath):
        logger.debug('moveExports option, Moving src=%s to dest=%s ; then symlinking dest to src', srcPath, destPath)
        shutil.move(srcPath, destPath)
        os.symlink(destPath, srcPath)

    @classmethod
    def getSize(cls, url):
        return os.stat(cls._extractPathFromUrl(url)).st_size

    @classmethod
    def _readFromUrl(cls, url, writable):
        """
        Writes the contents of a file to a source (writes url to writable)
        using a ~10Mb buffer.

        :param str url: A path as a string of the file to be read from.
        :param object writable: An open file object to write to.
        """
        with open(cls._extractPathFromUrl(url), 'rb') as (readable):
            shutil.copyfileobj(readable, writable, length=(cls.BUFFER_SIZE))
            return readable.tell()

    @classmethod
    def _writeToUrl(cls, readable, url):
        """
        Writes the contents of a file to a source (writes readable to url)
        using a ~10Mb buffer.

        :param str url: A path as a string of the file to be written to.
        :param object readable: An open file object to read from.
        """
        atomic_copyobj(readable, (cls._extractPathFromUrl(url)), length=(cls.BUFFER_SIZE))

    @staticmethod
    def _extractPathFromUrl(url):
        """
        :return: local file path of file pointed at by the given URL
        """
        if url.netloc != '':
            if url.netloc != 'localhost':
                raise RuntimeError("The URL '%s' is invalid" % url.geturl())
        return url.netloc + url.path

    @classmethod
    def _supportsUrl(cls, url, export=False):
        return url.scheme.lower() == 'file'

    def _makeStringFilenameSafe(self, arbitraryString):
        """
        Given an arbitrary string, produce a filename-safe though not
        necessarily unique string based on it.

        The input string may be discarded altogether and replaced with any
        other nonempty filename-safe string.

        :param str arbitraryString: An arbitrary string

        :return: A filename-safe string
        """
        parts = []
        for substring in re.findall('[A-Za-z0-9._-]+', arbitraryString):
            parts.append(substring)

        if len(parts) == 0:
            parts.append('UNPRINTABLE')
        return '_'.join(parts)

    def writeFile(self, localFilePath, jobStoreID=None, cleanup=False):
        absPath = self._getUniqueFilePath(localFilePath, jobStoreID, cleanup)
        relPath = self._getFileIdFromPath(absPath)
        atomic_copy(localFilePath, absPath)
        return relPath

    @contextmanager
    def writeFileStream(self, jobStoreID=None, cleanup=False):
        absPath = self._getUniqueFilePath('stream', jobStoreID, cleanup)
        relPath = self._getFileIdFromPath(absPath)
        with open(absPath, 'wb') as (f):
            yield (
             f, relPath)

    def getEmptyFileStoreID(self, jobStoreID=None, cleanup=False):
        with self.writeFileStream(jobStoreID, cleanup) as (fileHandle, jobStoreFileID):
            return jobStoreFileID

    def updateFile(self, jobStoreFileID, localFilePath):
        self._checkJobStoreFileID(jobStoreFileID)
        jobStoreFilePath = self._getFilePathFromId(jobStoreFileID)
        if os.path.samefile(jobStoreFilePath, localFilePath):
            return
        atomic_copy(localFilePath, jobStoreFilePath)

    def readFile(self, jobStoreFileID, localFilePath, symlink=False):
        self._checkJobStoreFileID(jobStoreFileID)
        jobStoreFilePath = self._getFilePathFromId(jobStoreFileID)
        localDirPath = os.path.dirname(localFilePath)
        if not symlink:
            if os.path.islink(localFilePath):
                os.unlink(localFilePath)
        if os.path.exists(localFilePath):
            if os.path.samefile(jobStoreFilePath, localFilePath):
                return
        if symlink:
            try:
                os.symlink(jobStoreFilePath, localFilePath)
                return
            except OSError as e:
                if e.errno == errno.EEXIST:
                    os.unlink(localFilePath)
                    os.symlink(jobStoreFilePath, localFilePath)
                    return
                raise

        if os.stat(jobStoreFilePath).st_dev == os.stat(localDirPath).st_dev:
            try:
                os.link(jobStoreFilePath, localFilePath)
                return
            except OSError as e:
                if e.errno == errno.EEXIST:
                    os.unlink(localFilePath)
                    os.link(jobStoreFilePath, localFilePath)
                    return
                else:
                    if e.errno == errno.EXDEV:
                        pass
                    else:
                        logger.critical('Unexpected OSError when reading file from job store')
                        logger.critical('jobStoreFilePath: ' + jobStoreFilePath + ' ' + str(os.path.exists(jobStoreFilePath)))
                        logger.critical('localFilePath: ' + localFilePath + ' ' + str(os.path.exists(localFilePath)))
                        raise

        atomic_copy(jobStoreFilePath, localFilePath)

    def deleteFile(self, jobStoreFileID):
        if not self.fileExists(jobStoreFileID):
            return
        os.remove(self._getFilePathFromId(jobStoreFileID))

    def fileExists(self, jobStoreFileID):
        absPath = self._getFilePathFromId(jobStoreFileID)
        if not absPath.startswith(self.jobsDir):
            if not absPath.startswith(self.filesDir):
                if not absPath.startswith(self.jobFilesDir):
                    raise NoSuchFileException(jobStoreFileID)
        try:
            st = os.stat(absPath)
        except os.error:
            return False
        else:
            if not stat.S_ISREG(st.st_mode):
                raise NoSuchFileException(jobStoreFileID)
            return True

    def getFileSize(self, jobStoreFileID):
        absPath = self._getFilePathFromId(jobStoreFileID)
        if not absPath.startswith(self.jobsDir):
            if not absPath.startswith(self.filesDir):
                if not absPath.startswith(self.jobFilesDir):
                    raise NoSuchFileException(jobStoreFileID)
        try:
            st = os.stat(absPath)
        except os.error:
            return 0
        else:
            return st.st_size

    @contextmanager
    def updateFileStream(self, jobStoreFileID):
        self._checkJobStoreFileID(jobStoreFileID)
        with open(self._getFilePathFromId(jobStoreFileID), 'wb') as (f):
            yield f

    @contextmanager
    def readFileStream(self, jobStoreFileID):
        self._checkJobStoreFileID(jobStoreFileID)
        with open(self._getFilePathFromId(jobStoreFileID), 'rb') as (f):
            yield f

    def _getSharedFilePath(self, sharedFileName):
        return os.path.join(self.sharedFilesDir, sharedFileName)

    @contextmanager
    def writeSharedFileStream(self, sharedFileName, isProtected=None):
        self._requireValidSharedFileName(sharedFileName)
        with AtomicFileCreate(self._getSharedFilePath(sharedFileName)) as (tmpSharedFilePath):
            with open(tmpSharedFilePath, 'wb') as (f):
                yield f

    @contextmanager
    def readSharedFileStream(self, sharedFileName):
        self._requireValidSharedFileName(sharedFileName)
        try:
            with open(self._getSharedFilePath(sharedFileName), 'rb') as (f):
                yield f
        except IOError as e:
            if e.errno == errno.ENOENT:
                raise NoSuchFileException(sharedFileName)
            else:
                raise

    def writeStatsAndLogging(self, statsAndLoggingString):
        fd, tempStatsFile = tempfile.mkstemp(prefix='stats', suffix='.new', dir=(self._getArbitraryStatsDir()))
        writeFormat = 'w' if isinstance(statsAndLoggingString, str) else 'wb'
        with open(tempStatsFile, writeFormat) as (f):
            f.write(statsAndLoggingString)
        os.close(fd)
        os.rename(tempStatsFile, tempStatsFile[:-4])

    def readStatsAndLogging(self, callback, readAll=False):
        numberOfFilesProcessed = 0
        for tempDir in self._statsDirectories():
            for tempFile in os.listdir(tempDir):
                if tempFile.startswith('stats'):
                    absTempFile = os.path.join(tempDir, tempFile)
                    if os.path.isfile(absTempFile) and (readAll or not tempFile.endswith('.new')):
                        with open(absTempFile, 'rb') as (fH):
                            callback(fH)
                        numberOfFilesProcessed += 1
                        newName = tempFile.rsplit('.', 1)[0] + '.new'
                        newAbsTempFile = os.path.join(tempDir, newName)
                        os.rename(absTempFile, newAbsTempFile)

        return numberOfFilesProcessed

    def _getJobDirFromId(self, jobStoreID):
        """

        Find the directory for a job, which holds its job file.

        :param str jobStoreID: ID of a job, which is a relative to self.jobsDir.
        :rtype : string, string is the absolute path to a job directory inside self.jobsDir.
        """
        return os.path.join(self.jobsDir, jobStoreID)

    def _getJobIdFromDir(self, absPath):
        """
        :param str absPath: The absolute path to a job directory under self.jobsDir which represents a job.
        :rtype : string, string is the job ID, which is a path relative to self.jobsDir
        """
        return absPath[len(self.jobsDir) + 1:]

    def _getJobFileName(self, jobStoreID):
        """
        Return the path to the file containing the serialised JobGraph instance for the given
        job.

        :rtype: str
        """
        return os.path.join(self._getJobDirFromId(jobStoreID), 'job')

    def _getJobFilesDir(self, jobStoreID):
        """
        Return the path to the directory that should hold files made by the
        given job that should survive its deletion.

        This directory will only be created if files are to be put in it.

        :rtype : string, string is the absolute path to the job's files
                 directory
        """
        return os.path.join(self.jobFilesDir, jobStoreID)

    def _getJobFilesCleanupDir(self, jobStoreID):
        """
        Return the path to the directory that should hold files made by the
        given job that will be deleted when the job is deleted.

        This directory will only be created if files are to be put in it.

        It may or may not be a subdirectory of the job's own directory.

        :rtype : string, string is the absolute path to the job's cleanup
                 files directory
        """
        return os.path.join(self.jobFilesDir, jobStoreID, 'cleanup')

    def _checkJobStoreId(self, jobStoreID):
        """
        Raises a NoSuchJobException if the job with ID jobStoreID does not exist.
        """
        if not self.waitForExists(jobStoreID, 30):
            raise NoSuchJobException(jobStoreID)

    def _getFilePathFromId(self, jobStoreFileID):
        """
        :param str jobStoreFileID: The ID of a file

        :rtype : string, string is the absolute path that that file should
                 appear at on disk, under either self.jobsDir if it is to be
                 cleaned up with a job, or self.filesDir otherwise.
        """
        absPath = os.path.join(self.jobStoreDir, jobStoreFileID)
        return absPath

    def _getFileIdFromPath(self, absPath):
        """
        :param str absPath: The absolute path of a file.

        :rtype : string, string is the file ID.
        """
        return absPath[len(self.jobStoreDir) + 1:]

    def _checkJobStoreFileID(self, jobStoreFileID):
        """
        :raise NoSuchFileException: if the file with ID jobStoreFileID does
                                    not exist or is not a file
        """
        if not self.fileExists(jobStoreFileID):
            raise NoSuchFileException(jobStoreFileID)

    def _getArbitraryJobsDirForName(self, jobNameSlug):
        """
        Gets a temporary directory in a multi-level hierarchy in self.jobsDir.
        The directory is not unique and may already have other jobs' directories in it.
        We organize them at the top level by job name, to be user-inspectable.

        We make sure to prepend a string so that job names can't collide with
        spray directory names.

        :param str jobNameSlug: A partial filename derived from the job name.
                                Used as the first level of the directory hierarchy.

        :rtype : string, path to temporary directory in which to place files/directories.

        """
        if len(os.listdir(self.jobsDir)) > self.fanOut:
            return self._getDynamicSprayDir(os.path.join(self._getDynamicSprayDir(self.jobsDir), self.JOB_NAME_DIR_PREFIX + jobNameSlug))
        else:
            return self._getDynamicSprayDir(os.path.join(self.jobsDir, self.JOB_NAME_DIR_PREFIX + jobNameSlug))

    def _getArbitraryStatsDir(self):
        """
        Gets a temporary directory in a multi-level hierarchy in self.statsDir.
        The directory is not unique and may already have other stats files in it.

        :rtype : string, path to temporary directory in which to place files/directories.

        """
        return self._getDynamicSprayDir(self.statsDir)

    def _getArbitraryFilesDir(self):
        """
        Gets a temporary directory in a multi-level hierarchy in self.filesDir.
        The directory is not unique and may already have other user files in it.

        :rtype : string, path to temporary directory in which to place files/directories.

        """
        return self._getDynamicSprayDir(self.filesDir)

    def _getDynamicSprayDir(self, root):
        """
        Gets a temporary directory in a possibly multi-level hierarchy of
        directories under the given root.

        Each time a directory in the hierarchy starts to fill up, additional
        hierarchy levels are created under it, and we randomly "spray" further
        files and directories across them.

        We can't actually enforce that we never go over our internal limit for
        files in a directory, because any number of calls to this function can
        be happening simultaneously. But we can enforce that, once too many
        files are visible on disk, only subdirectories will be created.

        The returned directory will exist, and may contain other data already.

        The caller may not create any files or directories in the returned
        directory with single-character names that are in self.validDirs.

        :param str root : directory to put the hierarchy under, which will
                          fill first.

        :rtype : string, path to temporary directory in which to place
                 files/directories.
        """
        tempDir = root
        mkdir_p(tempDir)
        while len(os.listdir(tempDir)) >= self.fanOut:
            tempDir = os.path.join(tempDir, random.choice(self.validDirs))
            mkdir_p(tempDir)

        return tempDir

    def _walkDynamicSprayDir(self, root):
        """
        Walks over a directory tree filled in by _getDynamicSprayDir.

        Yields each directory _getDynamicSprayDir has ever returned, and no
        directories it has not returned (besides the root).

        If the caller looks in the directory, they must ignore subdirectories
        with single-character names in self.validDirs.

        :param str root : directory the hierarchy was put under

        :rtype : an iterator over directories
        """
        yield root
        children = []
        try:
            children = os.listdir(root)
        except:
            pass

        for child in children:
            if child not in self.validDirsSet:
                pass
            else:
                childPath = os.path.join(root, child)
                for item in self._walkDynamicSprayDir(childPath):
                    yield item

    def _jobDirectories(self):
        """
        :rtype : an iterator to the temporary directories containing job
                 files. They may also contain directories containing more
                 job files.
        """
        for jobHoldingDir in self._walkDynamicSprayDir(self.jobsDir):
            children = []
            try:
                children = os.listdir(jobHoldingDir)
            except:
                pass

            for jobNameDir in children:
                if not jobNameDir.startswith(self.JOB_NAME_DIR_PREFIX):
                    pass
                else:
                    for inner in self._walkDynamicSprayDir(os.path.join(jobHoldingDir, jobNameDir)):
                        yield inner

    def _statsDirectories(self):
        """
        :rtype : an iterator to the temporary directories containing stats
                 files. They may also contain directories containing more
                 stats files.
        """
        return self._walkDynamicSprayDir(self.statsDir)

    def _getUniqueFilePath(self, fileName, jobStoreID=None, cleanup=False):
        """
        Create unique file name within a jobStore directory or tmp directory.

        :param fileName: A file name, which can be a full path as only the
        basename will be used.
        :param jobStoreID: If given, the path returned will be in a directory including the job's ID as part of its path.
        :param bool cleanup: If True and jobStoreID is set, the path will be in
            a place such that it gets deleted when the job is deleted.
        :return: The full path with a unique file name.
        """
        directory = self._getFileDirectory(jobStoreID, cleanup)
        uniquePath = os.path.join(directory, os.path.basename(fileName))
        return uniquePath

    def _getFileDirectory(self, jobStoreID=None, cleanup=False):
        """
        Get a new empty directory path for a file to be stored at.

        :param str jobStoreID: If the jobStoreID is not None, the file wil
               be associated with the job with that ID.

        :param bool cleanup: If cleanup is also True, this directory
               will be cleaned up when the job is deleted.

        :rtype :string, string is the absolute path to a directory to put the file in.
        """
        if jobStoreID != None:
            self._checkJobStoreId(jobStoreID)
            jobFilesDir = self._getJobFilesDir(jobStoreID) if not cleanup else self._getJobFilesCleanupDir(jobStoreID)
            mkdir_p(jobFilesDir)
            return tempfile.mkdtemp(prefix='file-', dir=jobFilesDir)
        else:
            return tempfile.mkdtemp(prefix='file-', dir=(self._getArbitraryFilesDir()))