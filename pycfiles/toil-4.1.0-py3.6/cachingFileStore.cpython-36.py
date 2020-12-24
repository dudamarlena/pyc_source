# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/toil/fileStores/cachingFileStore.py
# Compiled at: 2020-05-07 00:32:15
# Size of source mod 2**32: 82470 bytes
from __future__ import absolute_import, print_function
from future import standard_library
standard_library.install_aliases()
from builtins import map
from builtins import str
from contextlib import contextmanager
import errno, hashlib, logging, os, re, shutil, sqlite3, sys, tempfile, threading, time, uuid
from toil.common import cacheDirName, getDirSizeRecursively, getFileSystemSize
from toil.lib.bioio import makePublicDir
from toil.lib.humanize import bytes2human
from toil.lib.misc import mkdir_p, robust_rmtree, atomic_copy, atomic_copyobj
from toil.lib.retry import retry
from toil.lib.threading import get_process_name, process_name_exists
from toil.fileStores.abstractFileStore import AbstractFileStore
from toil.fileStores import FileID
logger = logging.getLogger(__name__)
if sys.version_info[0] < 3:
    FileNotFoundError = OSError
SQLITE_TIMEOUT_SECS = 60.0

class CacheError(Exception):
    __doc__ = '\n    Error Raised if the user attempts to add a non-local file to cache\n    '

    def __init__(self, message):
        super(CacheError, self).__init__(message)


class CacheUnbalancedError(CacheError):
    __doc__ = "\n    Raised if file store can't free enough space for caching\n    "
    message = 'Unable unable to free enough space for caching.  This error frequently arises due to jobs using more disk than they have requested.  Turn on debug logging to see more information leading up to this error through cache usage logs.'

    def __init__(self):
        super(CacheUnbalancedError, self).__init__(self.message)


class IllegalDeletionCacheError(CacheError):
    __doc__ = '\n    Error raised if the caching code discovers a file that represents a\n    reference to a cached file to have gone missing.\n\n    This can be a big problem if a hard link is moved, because then the cache\n    will be unable to evict the file it links to.\n\n    Remember that files read with readGlobalFile may not be deleted by the user\n    and need to be deleted with deleteLocalFile.\n    '

    def __init__(self, deletedFile):
        message = 'Cache tracked file (%s) has been deleted or moved by user  without updating cache database. Use deleteLocalFile to delete such files.' % deletedFile
        super(IllegalDeletionCacheError, self).__init__(message)


class InvalidSourceCacheError(CacheError):
    __doc__ = '\n    Error raised if the user attempts to add a non-local file to cache\n    '

    def __init__(self, message):
        super(InvalidSourceCacheError, self).__init__(message)


class CachingFileStore(AbstractFileStore):
    __doc__ = '\n    A cache-enabled file store.\n\n    Provides files that are read out as symlinks or hard links into a cache\n    directory for the node, if permitted by the workflow.\n\n    Also attempts to write files back to the backing JobStore asynchronously,\n    after quickly taking them into the cache. Writes are only required to\n    finish when the job\'s actual state after running is committed back to the\n    job store.\n\n    Internaly, manages caching using a database. Each node has its own\n    database, shared between all the workers on the node. The database contains\n    several tables:\n\n    files contains one entry for each file in the cache. Each entry knows the\n    path to its data on disk. It also knows its global file ID, its state, and\n    its owning worker PID. If the owning worker dies, another worker will pick\n    it up. It also knows its size.\n\n    File states are:\n\n    - "cached": happily stored in the cache. Reads can happen immediately.\n      Owner is null. May be adopted and moved to state "deleting" by anyone, if\n      it has no outstanding immutable references.\n\n    - "downloading": in the process of being saved to the cache by a non-null\n      owner. Reads must wait for the state to become "cached". If the worker\n      dies, goes to state "deleting", because we don\'t know if it was fully\n      downloaded or if anyone still needs it. No references can be created to a\n      "downloading" file except by the worker responsible for downloading it.\n\n    - "uploadable": stored in the cache and ready to be written to the job\n      store by a non-null owner. Transitions to "uploading" when a (thread of)\n      the owning worker process picks it up and begins uploading it, to free\n      cache space or to commit a completed job. If the worker dies, goes to\n      state "cached", because it may have outstanding immutable references from\n      the dead-but-not-cleaned-up job that was going to write it.\n\n    - "uploading": stored in the cache and being written to the job store by a\n      non-null owner. Transitions to "cached" when successfully uploaded. If\n      the worker dies, goes to state "cached", because it may have outstanding\n      immutable references from the dead-but-not-cleaned-up job that was\n      writing it.\n\n    - "deleting": in the process of being removed from the cache by a non-null\n      owner. Will eventually be removed from the database.\n\n    refs contains one entry for each outstanding reference to a cached file\n    (hard link, symlink, or full copy). The table name is refs instead of\n    references because references is an SQL reserved word. It remembers what\n    job ID has the reference, and the path the reference is at. References have\n    three states:\n\n    - "immutable": represents a hardlink or symlink to a file in the cache.\n      Dedicates the file\'s size in bytes of the job\'s disk requirement to the\n      cache, to be used to cache this file or to keep around other files\n      without references. May be upgraded to "copying" if the link can\'t\n      actually be created.\n\n    - "copying": records that a file in the cache is in the process of being\n      copied to a path. Will be upgraded to a mutable reference eventually.\n\n    - "mutable": records that a file from the cache was copied to a certain\n      path. Exist only to support deleteLocalFile\'s API. Only files with only\n      mutable references (or no references) are eligible for eviction.\n\n    jobs contains one entry for each job currently running. It keeps track of\n    the job\'s ID, the worker that is supposed to be running the job, the job\'s\n    disk requirement, and the job\'s local temp dir path that will need to be\n    cleaned up. When workers check for jobs whose workers have died, they null\n    out the old worker, and grab ownership of and clean up jobs and their\n    references until the null-worker jobs are gone.\n\n    properties contains key, value pairs for tracking total space available,\n    and whether caching is free for this run.\n\n    '

    def __init__(self, jobStore, jobGraph, localTempDir, waitForPreviousCommit):
        super(CachingFileStore, self).__init__(jobStore, jobGraph, localTempDir, waitForPreviousCommit)
        self.forceNonFreeCaching = False
        self.forceDownloadDelay = None
        self.contentionBackoff = 15
        self.localCacheDir = os.path.join(os.path.dirname(localTempDir), cacheDirName(self.jobStore.config.workflowID))
        self.jobName = str(self.jobGraph)
        self.jobID = self.jobGraph.jobStoreID
        logger.debug('Starting job (%s) with ID (%s).', self.jobName, self.jobID)
        self.jobDiskBytes = None
        self.workflowAttemptNumber = self.jobStore.config.workflowAttemptNumber
        mkdir_p(self.localCacheDir)
        self.dbPath = os.path.join(self.localCacheDir, 'cache-{}.db'.format(self.workflowAttemptNumber))
        self.con = sqlite3.connect((self.dbPath), timeout=SQLITE_TIMEOUT_SECS)
        self.cur = self.con.cursor()
        self._ensureTables(self.con)
        freeSpace, _ = getFileSystemSize(self.localCacheDir)
        self._write([('INSERT OR IGNORE INTO properties VALUES (?, ?)', ('maxSpace', freeSpace))])
        self.commitThread = None

    @staticmethod
    def _staticWrite(con, cur, operations):
        """
        Write to the caching database, using the given connection.

        If we can't get an SQLite write lock on the database, retry with some
        backoff until we can.

        operations is a list of tuples of (sql string, optional tuple of values
        to substitute), or bare sql strings.

        All operations are executed in a single transaction, which is
        committed.

        :param sqlite3.Connection con: Connection to the cache database.
        :param sqlite3.Cursor cur: Cursor in the cache database.
        :param list operations: List of sql strings or tuples of (sql, optional values) to execute.
        :return: Number of rows modified by the last operation
        :rtype: int
        """
        for attempt in retry(timeout=(float('inf')), predicate=(lambda e: isinstance(e, sqlite3.OperationalError) and 'is locked' in str(e))):
            with attempt:
                try:
                    for item in operations:
                        if not isinstance(item, tuple):
                            item = (item,)
                        else:
                            command = item[0]
                            if len(item) < 2:
                                args = ()
                            else:
                                args = item[1]
                        cur.execute(command, args)

                except Exception as e:
                    logging.error('Error talking to caching database: %s', str(e))
                    try:
                        con.rollback()
                    except:
                        pass

                    raise e
                else:
                    con.commit()

        return cur.rowcount

    def _write(self, operations):
        """
        Write to the caching database, using the instance's connection

        If we can't get an SQLite write lock on the database, retry with some
        backoff until we can.

        operations is a list of tuples of (sql string, optional tuple of values
        to substitute), or bare sql strings.

        All operations are executed in a single transaction, which is
        committed.

        :param list operations: List of sql strings or tuples of (sql, optional values) to execute.
        :return: Number of rows modified by the last operation
        :rtype: int
        """
        return self._staticWrite(self.con, self.cur, operations)

    @classmethod
    def _ensureTables(cls, con):
        """
        Ensure that the database tables we expect exist.

        :param sqlite3.Connection con: Connection to the cache database.
        """
        cur = con.cursor()
        cls._staticWrite(con, cur, [
         '\n            CREATE TABLE IF NOT EXISTS files (\n                id TEXT NOT NULL PRIMARY KEY,\n                path TEXT UNIQUE NOT NULL,\n                size INT NOT NULL,\n                state TEXT NOT NULL,\n                owner TEXT\n            )\n        ',
         '\n            CREATE TABLE IF NOT EXISTS refs (\n                path TEXT NOT NULL,\n                file_id TEXT NOT NULL,\n                job_id TEXT NOT NULL,\n                state TEXT NOT NULL,\n                PRIMARY KEY (path, file_id)\n            )\n        ',
         '\n            CREATE TABLE IF NOT EXISTS jobs (\n                id TEXT NOT NULL PRIMARY KEY,\n                tempdir TEXT NOT NULL,\n                disk INT NOT NULL,\n                worker TEXT\n            )\n        ',
         '\n            CREATE TABLE IF NOT EXISTS properties (\n                name TEXT NOT NULL PRIMARY KEY,\n                value INT NOT NULL\n            )\n        '])

    def getCacheLimit(self):
        """
        Return the total number of bytes to which the cache is limited.

        If no limit is available, raises an error.
        """
        for row in self.cur.execute('SELECT value FROM properties WHERE name = ?', ('maxSpace', )):
            return row[0]

        raise RuntimeError('Unable to retrieve cache limit')

    def getCacheUsed(self):
        """
        Return the total number of bytes used in the cache.

        If no value is available, raises an error.
        """
        if self.cachingIsFree():
            return 0
        for row in self.cur.execute('SELECT TOTAL(size) FROM files'):
            return row[0]

        raise RuntimeError('Unable to retrieve cache usage')

    def getCacheExtraJobSpace(self):
        """
        Return the total number of bytes of disk space requested by jobs
        running against this cache but not yet used.

        We can get into a situation where the jobs on the node take up all its
        space, but then they want to write to or read from the cache. So when
        that happens, we need to debit space from them somehow...

        If no value is available, raises an error.
        """
        for row in self.cur.execute("\n            SELECT (\n                (SELECT TOTAL(disk) FROM jobs) -\n                (SELECT TOTAL(files.size) FROM refs INNER JOIN files ON refs.file_id = files.id WHERE refs.state == 'immutable')\n            ) as result\n        "):
            return row[0]

        raise RuntimeError('Unable to retrieve extra job space')

    def getCacheAvailable(self):
        """
        Return the total number of free bytes available for caching, or, if
        negative, the total number of bytes of cached files that need to be
        evicted to free up enough space for all the currently scheduled jobs.

        If no value is available, raises an error.
        """
        for row in self.cur.execute("SELECT value FROM properties WHERE name = 'maxSpace'"):
            logger.debug('Max space: %d', row[0])

        for row in self.cur.execute('SELECT TOTAL(size) FROM files'):
            logger.debug('Total file size: %d', row[0])

        for row in self.cur.execute('SELECT TOTAL(disk) FROM jobs'):
            logger.debug('Total job disk requirement size: %d', row[0])

        for row in self.cur.execute("SELECT TOTAL(files.size) FROM refs INNER JOIN files ON refs.file_id = files.id WHERE refs.state = 'immutable'"):
            logger.debug('Total immutable reference size: %d', row[0])

        if self.cachingIsFree():
            for row in self.cur.execute("SELECT value FROM properties WHERE name = 'maxSpace'"):
                return row[0]

            raise RuntimeError('Unable to retrieve available cache space')
        for row in self.cur.execute("\n            SELECT (\n                (SELECT value FROM properties WHERE name = 'maxSpace') -\n                (SELECT TOTAL(size) FROM files) -\n                ((SELECT TOTAL(disk) FROM jobs) -\n                (SELECT TOTAL(files.size) FROM refs INNER JOIN files ON refs.file_id = files.id WHERE refs.state = 'immutable'))\n            ) as result\n        "):
            return row[0]

        raise RuntimeError('Unable to retrieve available cache space')

    def getSpaceUsableForJobs(self):
        """
        Return the total number of bytes that are not taken up by job requirements, ignoring files and file usage.
        We can't ever run more jobs than we actually have room for, even with caching.

        If not retrievable, raises an error.
        """
        for row in self.cur.execute("\n            SELECT (\n                (SELECT value FROM properties WHERE name = 'maxSpace') -\n                (SELECT TOTAL(disk) FROM jobs)\n            ) as result\n        "):
            return row[0]

        raise RuntimeError('Unable to retrieve usabel space for jobs')

    def getCacheUnusedJobRequirement(self):
        """
        Return the total number of bytes of disk space requested by the current
        job and not used by files the job is using in the cache.

        Mutable references don't count, but immutable/uploading ones do.

        If no value is available, raises an error.
        """
        logger.debug('Get unused space for job %s', self.jobID)
        for row in self.cur.execute('SELECT * FROM files'):
            logger.debug('File record: %s', str(row))

        for row in self.cur.execute('SELECT * FROM refs'):
            logger.debug('Ref record: %s', str(row))

        for row in self.cur.execute('SELECT TOTAL(files.size) FROM refs INNER JOIN files ON refs.file_id = files.id WHERE refs.job_id = ? AND refs.state != ?', (
         self.jobID, 'mutable')):
            return self.jobDiskBytes - row[0]

        raise RuntimeError('Unable to retrieve unused job requirement space')

    def adjustCacheLimit(self, newTotalBytes):
        """
        Adjust the total cache size limit to the given number of bytes.
        """
        self._write([('UPDATE properties SET value = ? WHERE name = ?', (newTotalBytes, 'maxSpace'))])

    def fileIsCached(self, fileID):
        """
        Return true if the given file is currently cached, and false otherwise.

        Note that this can't really be relied upon because a file may go cached
        -> deleting after you look at it. If you need to do something with the
        file you need to do it in a transaction.
        """
        for row in self.cur.execute('SELECT COUNT(*) FROM files WHERE id = ? AND (state = ? OR state = ? OR state = ?)', (
         fileID, 'cached', 'uploadable', 'uploading')):
            return row[0] > 0

        return False

    def getFileReaderCount(self, fileID):
        """
        Return the number of current outstanding reads of the given file.

        Counts mutable references too.
        """
        for row in self.cur.execute('SELECT COUNT(*) FROM refs WHERE file_id = ?', (fileID,)):
            return row[0]

        return 0

    def cachingIsFree(self):
        """
        Return true if files can be cached for free, without taking up space.
        Return false otherwise.

        This will be true when working with certain job stores in certain
        configurations, most notably the FileJobStore.
        """
        for row in self.cur.execute('SELECT value FROM properties WHERE name = ?', ('freeCaching', )):
            return row[0] == 1

        from toil.jobStores.fileJobStore import FileJobStore
        if isinstance(self.jobStore, FileJobStore):
            if not self.forceNonFreeCaching:
                emptyID = self.jobStore.getEmptyFileStoreID()
                destDir = tempfile.mkdtemp(dir=(self.localCacheDir))
                cachedFile = os.path.join(destDir, 'sniffLinkCount')
                self.jobStore.readFile(emptyID, cachedFile, symlink=False)
                if os.stat(cachedFile).st_nlink == 2:
                    free = 1
                else:
                    free = 0
                os.unlink(cachedFile)
                os.rmdir(destDir)
                self.jobStore.deleteFile(emptyID)
        else:
            free = 0
        self._write([('INSERT OR IGNORE INTO properties VALUES (?, ?)', ('freeCaching', free))])
        return free == 1

    def _getNewCachingPath(self, fileStoreID):
        """
        Get a path at which the given file ID can be cached.

        Will be unique for every call.

        The file will not be created if it does not exist.
        """
        hasher = hashlib.sha1()
        hasher.update(fileStoreID.encode('utf-8'))
        handle, path = tempfile.mkstemp(dir=(self.localCacheDir), suffix=(hasher.hexdigest()))
        os.close(handle)
        os.unlink(path)
        return path

    def _stealWorkFromTheDead(self):
        """
        Take ownership of any files we can see whose owners have died.

        We don't actually process them here. We take action based on the states of files we own later.
        """
        me = get_process_name(self.workDir)
        owners = []
        for row in self.cur.execute('SELECT DISTINCT owner FROM files WHERE owner IS NOT NULL'):
            owners.append(row[0])

        deadOwners = []
        for owner in owners:
            if not process_name_exists(self.workDir, owner):
                deadOwners.append(owner)

        for owner in deadOwners:
            self._write([
             ('UPDATE files SET owner = ?, state = ? WHERE owner = ? AND state = ?',
              (
               me, 'deleting', owner, 'deleting')),
             (
              'UPDATE files SET owner = ?, state = ? WHERE owner = ? AND state = ?',
              (
               me, 'deleting', owner, 'downloading')),
             (
              'UPDATE files SET owner = NULL, state = ? WHERE owner = ? AND (state = ? OR state = ?)',
              (
               'cached', owner, 'uploadable', 'uploading'))])
            logger.debug('Tried to adopt file operations from dead worker %d', owner)

    @classmethod
    def _executePendingDeletions(cls, workDir, con, cur):
        """
        Delete all the files that are registered in the database as in the
        process of being deleted from the cache by us.

        Returns the number of files that were deleted.

        Implemented as a class method so it can use the database connection
        appropriate to its thread without any chance of getting at the main
        thread's connection and cursor in self.

        :param str workDir: The Toil work directory.
        :param sqlite3.Connection con: Connection to the cache database.
        :param sqlite3.Cursor cur: Cursor in the cache database.
        """
        me = get_process_name(workDir)
        deletedFiles = []
        for row in cur.execute('SELECT id, path FROM files WHERE owner = ? AND state = ?', (me, 'deleting')):
            fileID = row[0]
            filePath = row[1]
            try:
                os.unlink(filePath)
            except OSError:
                continue

            deletedFiles.append(fileID)

        for fileID in deletedFiles:
            cls._staticWrite(con, cur, [('DELETE FROM files WHERE id = ? AND state = ?', (fileID, 'deleting')),
             (
              'DELETE FROM refs WHERE file_id = ?', (fileID,))])

        return len(deletedFiles)

    def _executePendingUploads(self, con, cur):
        """
        Uploads all files in uploadable state that we own.

        Returns the number of files that were uploaded.

        Needs access to self to get at the job store for uploading files, but
        still needs to take con and cur so it can run in a thread with the
        thread's database connection.

        :param sqlite3.Connection con: Connection to the cache database.
        :param sqlite3.Cursor cur: Cursor in the cache database.
        """
        me = get_process_name(self.workDir)
        uploadedCount = 0
        while True:
            fileID = None
            filePath = None
            for row in cur.execute('SELECT id, path FROM files WHERE state = ? AND owner = ? LIMIT 1', ('uploadable', me)):
                fileID = row[0]
                filePath = row[1]

            if fileID is None:
                break
            rowCount = self._staticWrite(con, cur, [('UPDATE files SET state = ? WHERE id = ? AND state = ?', ('uploading', fileID, 'uploadable'))])
            if rowCount != 1:
                logger.debug('Lost race to upload %s', fileID)
            else:
                logger.debug('Actually executing upload for file %s', fileID)
                self.jobStore.updateFile(fileID, filePath)
                uploadedCount += 1
                self._staticWrite(con, cur, [('UPDATE files SET state = ?, owner = NULL WHERE id = ?', ('cached', fileID))])

        return uploadedCount

    def _allocateSpaceForJob(self, newJobReqs):
        """
        A new job is starting that needs newJobReqs space.

        We need to record that we have a job running now that needs this much space.

        We also need to evict enough stuff from the cache so that we have room
        for this job to fill up that much space even if it doesn't cache
        anything.

        localTempDir must have already been pointed to the job's temp dir.

        :param float newJobReqs: the total number of bytes that this job requires.
        """
        me = get_process_name(self.workDir)
        self._write([('INSERT INTO jobs VALUES (?, ?, ?, ?)', (self.jobID, self.localTempDir, newJobReqs, me))])
        available = self.getCacheAvailable()
        logger.debug('Available space with job: %d bytes', available)
        if available >= 0:
            return
        self._freeUpSpace()

    @classmethod
    def _removeJob(cls, con, cur, jobID):
        """
        Get rid of the job with the given ID.
        The job must be owned by us.

        Deletes the job's database entry, all its references, and its whole
        temporary directory.

        :param sqlite3.Connection con: Connection to the cache database.
        :param sqlite3.Cursor cur: Cursor in the cache database.
        :param str jobID: Hash-based ID of the job being removed. Not a Toil JobStore ID.
        """
        for row in cur.execute('SELECT tempdir FROM jobs WHERE id = ?', (jobID,)):
            jobTemp = row[0]

        for row in cur.execute('SELECT path FROM refs WHERE job_id = ?', (jobID,)):
            try:
                os.unlink(row[0])
            except OSError:
                pass

        cls._staticWrite(con, cur, [('DELETE FROM refs WHERE job_id = ?', (jobID,))])
        try:
            shutil.rmtree(jobTemp)
        except OSError:
            pass

        cls._staticWrite(con, cur, [('DELETE FROM jobs WHERE id = ?', (jobID,))])

    def _deallocateSpaceForJob(self):
        """
        Our current job that was using oldJobReqs space has finished.

        We need to record that the job is no longer running, so its space not
        taken up by files in the cache will be free.

        """
        self._removeJob(self.con, self.cur, self.jobID)

    def _tryToFreeUpSpace(self):
        """
        If disk space is overcommitted, try one round of collecting files to upload/download/delete/evict.
        Return whether we manage to get any space freed or not.
        """
        self._removeDeadJobs(self.workDir, self.con)
        self._stealWorkFromTheDead()
        if self._executePendingDeletions(self.workDir, self.con, self.cur) > 0:
            logger.debug('Successfully executed pending deletions to free space')
            return True
        if self._executePendingUploads(self.con, self.cur) > 0:
            logger.debug('Successfully executed pending uploads to free space')
            return True
        self.cur.execute("\n            SELECT files.id FROM files WHERE files.state = 'cached' AND NOT EXISTS (\n                SELECT NULL FROM refs WHERE refs.file_id = files.id AND refs.state != 'mutable'\n            ) LIMIT 1\n        ")
        row = self.cur.fetchone()
        if row is None:
            logger.debug('Could not find anything to evict! Cannot free up space!')
            return False
        fileID = row[0]
        me = get_process_name(self.workDir)
        self._write([
         (
          "\n            UPDATE files SET owner = ?, state = ? WHERE id = ? AND state = ?\n            AND owner IS NULL AND NOT EXISTS (\n                SELECT NULL FROM refs WHERE refs.file_id = files.id AND refs.state != 'mutable'\n            )\n            ",
          (
           me, 'deleting', fileID, 'cached'))])
        logger.debug('Evicting file %s', fileID)
        if self._executePendingDeletions(self.workDir, self.con, self.cur) > 0:
            logger.debug('Successfully executed pending deletions to free space')
            return True

    def _freeUpSpace(self):
        """
        If disk space is overcomitted, block and evict eligible things from the
        cache until it is no longer overcommitted.
        """
        availableSpace = self.getCacheAvailable()
        patience = 10
        while availableSpace < 0:
            logger.debug('Cache is full (%d bytes free). Trying to free up space!', availableSpace)
            progress = self._tryToFreeUpSpace()
            availableSpace = self.getCacheAvailable()
            if progress:
                patience = 10
            else:
                jobSpace = self.getSpaceUsableForJobs()
                if jobSpace < 0:
                    logger.critical('Jobs on this machine have oversubscribed our total available space (%d bytes)!', jobSpace)
                    raise CacheUnbalancedError
                else:
                    patience -= 1
                    if patience <= 0:
                        logger.critical('Waited implausibly long for active uploads and deletes.')
                        raise CacheUnbalancedError
                    else:
                        time.sleep(2)

        logger.debug('Cache has %d bytes free.', availableSpace)

    @contextmanager
    def open(self, job):
        """
        This context manager decorated method allows cache-specific operations to be conducted
        before and after the execution of a job in worker.py
        """
        startingDir = os.getcwd()
        self.localTempDir = makePublicDir(os.path.join(self.localTempDir, str(uuid.uuid4())))
        self._removeDeadJobs(self.workDir, self.con)
        self.jobDiskBytes = job.disk
        logger.debug('Actually running job (%s) with ID (%s) which wants %d of our %d bytes.', self.jobName, self.jobID, self.jobDiskBytes, self.getCacheLimit())
        self._allocateSpaceForJob(self.jobDiskBytes)
        try:
            os.chdir(self.localTempDir)
            yield
        finally:
            diskUsed = getDirSizeRecursively(self.localTempDir)
            logString = 'Job {jobName} used {percent:.2f}% ({humanDisk}B [{disk}B] used, {humanRequestedDisk}B [{requestedDisk}B] requested) at the end of its run.'.format(jobName=(self.jobName),
              percent=(float(diskUsed) / self.jobDiskBytes * 100 if self.jobDiskBytes > 0 else 0.0),
              humanDisk=(bytes2human(diskUsed)),
              disk=diskUsed,
              humanRequestedDisk=(bytes2human(self.jobDiskBytes)),
              requestedDisk=(self.jobDiskBytes))
            self.logToMaster(logString, level=(logging.DEBUG))
            if diskUsed > self.jobDiskBytes:
                self.logToMaster(('Job used more disk than requested. Please reconsider modifying the user script to avoid the chance  of failure due to incorrectly requested resources. ' + logString),
                  level=(logging.WARNING))
            os.chdir(startingDir)
            self.cleanupInProgress = True
            self._deallocateSpaceForJob()

    def writeGlobalFile(self, localFileName, cleanup=False):
        absLocalFileName = self._resolveAbsoluteLocalPath(localFileName)
        fileSize = os.stat(absLocalFileName).st_size
        creatorID = self.jobGraph.jobStoreID
        fileID = self.jobStore.getEmptyFileStoreID(creatorID, cleanup)
        me = get_process_name(self.workDir)
        cachePath = self._getNewCachingPath(fileID)
        self._write([('INSERT INTO files VALUES (?, ?, ?, ?, ?)', (fileID, cachePath, fileSize, 'uploadable', me)),
         (
          'INSERT INTO refs VALUES (?, ?, ?, ?)', (absLocalFileName, fileID, creatorID, 'immutable'))])
        if absLocalFileName.startswith(self.localTempDir):
            try:
                os.link(absLocalFileName, cachePath)
                linkedToCache = True
                logger.debug('Linked file %s into cache at %s; deferring write to job store', localFileName, cachePath)
            except OSError:
                linkedToCache = False

        else:
            linkedToCache = False
        if not linkedToCache:
            self._write([('UPDATE refs SET state = ? WHERE path = ? AND file_id = ?', ('mutable', absLocalFileName, fileID)),
             (
              'DELETE FROM files WHERE id = ?', (fileID,))])
            logger.debug('Actually executing upload for file %s', fileID)
            self.jobStore.updateFile(fileID, absLocalFileName)
        return FileID.forPath(fileID, absLocalFileName)

    def readGlobalFile(self, fileStoreID, userPath=None, cache=True, mutable=False, symlink=False):
        if str(fileStoreID) in self.filesToDelete:
            raise FileNotFoundError('Attempted to read deleted file: {}'.format(fileStoreID))
        else:
            if userPath is not None:
                localFilePath = self._resolveAbsoluteLocalPath(userPath)
                if os.path.exists(localFilePath):
                    raise RuntimeError(' File %s ' % localFilePath + ' exists. Cannot Overwrite.')
            else:
                localFilePath = self.getLocalTempFileName()
            readerID = self.jobGraph.jobStoreID
            if cache:
                if mutable:
                    return self._readGlobalFileMutablyWithCache(fileStoreID, localFilePath, readerID)
                else:
                    return self._readGlobalFileWithCache(fileStoreID, localFilePath, symlink, readerID)
            else:
                return self._readGlobalFileWithoutCache(fileStoreID, localFilePath, mutable, symlink, readerID)

    def _readGlobalFileWithoutCache(self, fileStoreID, localFilePath, mutable, symlink, readerID):
        """
        Read a file without putting it into the cache.

        :param toil.fileStores.FileID fileStoreID: job store id for the file
        :param str localFilePath: absolute destination path. Already known not to exist.
        :param bool mutable: Whether a mutable copy should be created, instead of a hard link or symlink.
        :param bool symlink: Whether a symlink is acceptable.
        :param str readerID: Job ID of the job reading the file.
        :return: An absolute path to a local, temporary copy of or link to the file keyed by fileStoreID.
        :rtype: str
        """
        self._write([
         ('INSERT INTO refs SELECT ?, id, ?, ? FROM files WHERE id = ? AND (state = ? OR state = ?)',
          (
           localFilePath, readerID, 'copying', fileStoreID, 'uploadable', 'uploading'))])
        have_reference = False
        for row in self.cur.execute('SELECT COUNT(*) FROM refs WHERE path = ? and file_id = ?', (localFilePath, fileStoreID)):
            have_reference = row[0] > 0

        if have_reference:
            cachedPath = None
            for row in self.cur.execute('SELECT path FROM files WHERE id = ?', (fileStoreID,)):
                cachedPath = row[0]

            if cachedPath is None:
                raise RuntimeError('File %s went away while we had a reference to it!' % fileStoreID)
            if self.forceDownloadDelay is not None:
                time.sleep(self.forceDownloadDelay)
            atomic_copy(cachedPath, localFilePath)
            self._write([('UPDATE refs SET state = ? WHERE path = ? and file_id = ?', ('mutable', localFilePath, fileStoreID))])
        else:
            self._write([
             ('INSERT INTO refs VALUES (?, ?, ?, ?)',
              (
               localFilePath, fileStoreID, readerID, 'mutable'))])
            if self.forceDownloadDelay is not None:
                time.sleep(self.forceDownloadDelay)
            if mutable or self.forceNonFreeCaching:
                with self.jobStore.readFileStream(fileStoreID) as (inStream):
                    atomic_copyobj(inStream, localFilePath)
            else:
                self.jobStore.readFile(fileStoreID, localFilePath, symlink=symlink)
        return localFilePath

    def _downloadToCache(self, fileStoreID, cachedPath):
        """
        Copy a file from the file store into the cache.

        Will hardlink if appropriate.

        :param toil.fileStores.FileID fileStoreID: job store id for the file
        :param str cachedPath: absolute destination path in the cache. Already known not to exist.
        """
        if self.forceDownloadDelay is not None:
            time.sleep(self.forceDownloadDelay)
        else:
            if self.forceNonFreeCaching:
                with self.jobStore.readFileStream(fileStoreID) as (inStream):
                    atomic_copyobj(inStream, cachedPath)
            else:
                self.jobStore.readFile(fileStoreID, cachedPath, symlink=False)

    def _readGlobalFileMutablyWithCache(self, fileStoreID, localFilePath, readerID):
        """
        Read a mutable copy of a file, putting it into the cache if possible.

        :param toil.fileStores.FileID fileStoreID: job store id for the file
        :param str localFilePath: absolute destination path. Already known not to exist.
        :param str readerID: Job ID of the job reading the file.
        :return: An absolute path to a local, temporary copy of or link to the file keyed by fileStoreID.
        :rtype: str
        """
        me = get_process_name(self.workDir)
        cachedPath = self._getNewCachingPath(fileStoreID)
        while True:
            logger.debug('Trying to make file record for id %s', fileStoreID)
            self._write([
             ('INSERT OR IGNORE INTO files VALUES (?, ?, ?, ?, ?)',
              (
               fileStoreID, cachedPath, self.getGlobalFileSize(fileStoreID), 'downloading', me))])
            self.cur.execute('SELECT COUNT(*) FROM files WHERE id = ? AND state = ? AND owner = ?', (fileStoreID, 'downloading', me))
            if self.cur.fetchone()[0] > 0:
                logger.debug('We are now responsible for downloading file %s', fileStoreID)
                self._freeUpSpace()
                self._downloadToCache(fileStoreID, cachedPath)
                self._write([
                 ('INSERT INTO refs VALUES (?, ?, ?, ?)',
                  (
                   localFilePath, fileStoreID, readerID, 'copying'))])
                self._fulfillCopyingReference(fileStoreID, cachedPath, localFilePath)
                return localFilePath
            logger.debug('Someone else is already responsible for file %s', fileStoreID)
            logger.debug('Trying to make reference to file %s', fileStoreID)
            self._write([
             ('INSERT INTO refs SELECT ?, id, ?, ? FROM files WHERE id = ? AND (state = ? OR state = ? OR state = ?)',
              (
               localFilePath, readerID, 'copying', fileStoreID, 'cached', 'uploadable', 'uploading'))])
            self.cur.execute('SELECT COUNT(*) FROM refs WHERE path = ? and file_id = ?', (localFilePath, fileStoreID))
            if self.cur.fetchone()[0] > 0:
                logger.debug('Obtained reference to file %s', fileStoreID)
                for row in self.cur.execute('SELECT path FROM files WHERE id = ?', (fileStoreID,)):
                    cachedPath = row[0]

                while self.getCacheAvailable() < 0:
                    self._tryToFreeUpSpace()
                    if self.getCacheAvailable() >= 0:
                        break
                    self._write([
                     (
                      "\n                            UPDATE files SET files.owner = ?, files.state = ? WHERE files.id = ? AND files.state = ?\n                            AND files.owner IS NULL AND NOT EXISTS (\n                                SELECT NULL FROM refs WHERE refs.file_id = files.id AND refs.state != 'mutable'\n                            )\n                            ",
                      (
                       me, 'downloading', fileStoreID, 'cached'))])
                    if self._giveAwayDownloadingFile(fileStoreID, cachedPath, localFilePath):
                        return localFilePath
                    time.sleep(self.contentionBackoff)

                if self.forceDownloadDelay is not None:
                    time.sleep(self.forceDownloadDelay)
                atomic_copy(cachedPath, localFilePath)
                self._write([('UPDATE refs SET state = ? WHERE path = ? AND file_id = ?', ('mutable', localFilePath, fileStoreID))])
                return localFilePath
            logger.debug('Could not obtain reference to file %s', fileStoreID)
            self._removeDeadJobs(self.workDir, self.con)
            self._stealWorkFromTheDead()
            self._executePendingDeletions(self.workDir, self.con, self.cur)
            time.sleep(self.contentionBackoff)

    def _fulfillCopyingReference(self, fileStoreID, cachedPath, localFilePath):
        """
        For use when you own a file in 'downloading' state, and have a
        'copying' reference to it.

        Makes a full copy from the cache, and changes 'downloading' file state
        to 'cached', if space can be found, or gives away the cached copy if
        space cannot be found.

        :param toil.fileStores.FileID or str fileStoreID: job store id for the file
        :param str cachedPath: absolute source path in the cache.
        :param str localFilePath: absolute destination path. Already known not to exist.
        """
        if self.getCacheAvailable() < 0:
            self._tryToFreeUpSpace()
        else:
            if self.getCacheAvailable() < 0:
                assert self._giveAwayDownloadingFile(fileStoreID, cachedPath, localFilePath)
                return
            self._write([
             ('UPDATE files SET state = ?, owner = NULL WHERE id = ?',
              (
               'cached', fileStoreID))])
            if self.forceDownloadDelay is not None:
                time.sleep(self.forceDownloadDelay)
        atomic_copy(cachedPath, localFilePath)
        self._write([('UPDATE refs SET state = ? WHERE path = ? AND file_id = ?', ('mutable', localFilePath, fileStoreID))])

    def _giveAwayDownloadingFile(self, fileStoreID, cachedPath, localFilePath):
        """
        Move a downloaded file in 'downloading' state, owned by us, from the cache to a user-specified destination path.

        Used when there's no room for both a cached copy of the file and the user's actual mutable copy.

        Returns true if the file was moved, and false if the file was not owned by us in 'downloading' state.

        :param toil.fileStores.FileID or str fileStoreID: job store id for the file
        :param str cachedPath: absolute source path in the cache.
        :param str localFilePath: absolute destination path. Already known not to exist.
        :return: True if the file is successfully moved. False if the file is not owned by us in 'downloading' state.
        :rtype: bool
        """
        me = get_process_name(self.workDir)
        self.cur.execute('SELECT COUNT(*) FROM files WHERE id = ? AND state = ? AND owner = ?', (
         fileStoreID, 'downloading', me))
        if self.cur.fetchone()[0] > 0:
            shutil.move(cachedPath, localFilePath)
            self._write([('UPDATE refs SET state = ? WHERE path = ? AND file_id = ?', ('mutable', localFilePath, fileStoreID)),
             (
              'DELETE FROM files WHERE id = ?', (fileStoreID,))])
            return True
        else:
            return False

    def _createLinkFromCache(self, cachedPath, localFilePath, symlink=True):
        """
        Create a hardlink or symlink from the given path in the cache to the
        given user-provided path. Destination must not exist.

        Only creates a symlink if a hardlink cannot be created and symlink is
        true.

        If no link can be created, returns False. Otherwise, returns True.

        :param str cachedPath: absolute source path in the cache.
        :param str localFilePath: absolute destination path. Already known not to exist.
        :param bool symlink: True if a symlink is allowed, False otherwise.
        :return: True if the file is successfully linked. False if the file cannot be linked.
        :rtype: bool
        """
        try:
            os.link(cachedPath, localFilePath)
            return True
        except OSError:
            if symlink:
                try:
                    os.symlink(cachedPath, localFilePath)
                    return True
                except OSError:
                    return False

            else:
                return False

    def _readGlobalFileWithCache(self, fileStoreID, localFilePath, symlink, readerID):
        """
        Read a file, putting it into the cache if possible.

        :param toil.fileStores.FileID or str fileStoreID: job store id for the file
        :param str localFilePath: absolute destination path. Already known not to exist.
        :param bool symlink: Whether a symlink is acceptable.
        :param str readerID: Job ID of the job reading the file.
        :return: An absolute path to a local, temporary copy of or link to the file keyed by fileStoreID.
        :rtype: str
        """
        me = get_process_name(self.workDir)
        cachedPath = self._getNewCachingPath(fileStoreID)
        while True:
            logger.debug('Trying to make file record and reference for id %s', fileStoreID)
            self._write([
             ('INSERT OR IGNORE INTO files VALUES (?, ?, ?, ?, ?)',
              (
               fileStoreID, cachedPath, self.getGlobalFileSize(fileStoreID), 'downloading', me)),
             (
              'INSERT INTO refs SELECT ?, id, ?, ? FROM files WHERE id = ? AND state = ? AND owner = ?',
              (
               localFilePath, readerID, 'immutable', fileStoreID, 'downloading', me))])
            self.cur.execute('SELECT COUNT(*) FROM files WHERE id = ? AND state = ? AND owner = ?', (fileStoreID, 'downloading', me))
            if self.cur.fetchone()[0] > 0:
                logger.debug('We are now responsible for downloading file %s', fileStoreID)
                self._freeUpSpace()
                self._downloadToCache(fileStoreID, cachedPath)
                if self._createLinkFromCache(cachedPath, localFilePath, symlink):
                    self._write([
                     ('UPDATE files SET state = ?, owner = NULL WHERE id = ?',
                      (
                       'cached', fileStoreID))])
                    return localFilePath
                else:
                    self._write([('UPDATE refs SET state = ? WHERE path = ? AND file_id = ?', ('copying', localFilePath, fileStoreID))])
                    self._fulfillCopyingReference(fileStoreID, cachedPath, localFilePath)
                    return localFilePath
            else:
                logger.debug('Someone else is already responsible for file %s', fileStoreID)
                logger.debug('Trying to make reference to file %s', fileStoreID)
                self._write([
                 ('INSERT INTO refs SELECT ?, id, ?, ? FROM files WHERE id = ? AND (state = ? OR state = ? OR state = ?)',
                  (
                   localFilePath, readerID, 'immutable', fileStoreID, 'cached', 'uploadable', 'uploading'))])
                self.cur.execute('SELECT COUNT(*) FROM refs WHERE path = ? and file_id = ?', (localFilePath, fileStoreID))
                if self.cur.fetchone()[0] > 0:
                    logger.debug('Obtained reference to file %s', fileStoreID)
                    for row in self.cur.execute('SELECT path FROM files WHERE id = ?', (fileStoreID,)):
                        cachedPath = row[0]

                    if self._createLinkFromCache(cachedPath, localFilePath, symlink):
                        return localFilePath
                    else:
                        self._write([('DELETE FROM refs WHERE path = ? AND file_id = ?', (localFilePath, fileStoreID))])
                        return self._readGlobalFileMutablyWithCache(fileStoreID, localFilePath, readerID)
                else:
                    logger.debug('Could not obtain reference to file %s', fileStoreID)
                    self._removeDeadJobs(self.workDir, self.con)
                    self._stealWorkFromTheDead()
                    self._executePendingDeletions(self.workDir, self.con, self.cur)
                    time.sleep(self.contentionBackoff)

    def readGlobalFileStream(self, fileStoreID):
        if str(fileStoreID) in self.filesToDelete:
            raise FileNotFoundError('Attempted to read deleted file: {}'.format(fileStoreID))
        return self.jobStore.readFileStream(fileStoreID)

    def deleteLocalFile(self, fileStoreID):
        jobID = self.jobID
        deleted = []
        missingFile = None
        for row in self.cur.execute('SELECT path FROM refs WHERE file_id = ? AND job_id = ?', (fileStoreID, jobID)):
            path = row[0]
            if path.startswith(self.localTempDir):
                try:
                    os.remove(path)
                except FileNotFoundError as err:
                    if err.errno != errno.ENOENT:
                        raise
                    missingFile = path
                    break

                deleted.append(path)

        for path in deleted:
            self._write([('DELETE FROM refs WHERE file_id = ? AND job_id = ? AND path = ?', (fileStoreID, jobID, path))])

        self._freeUpSpace()
        if missingFile is not None:
            raise IllegalDeletionCacheError(missingFile)

    def deleteGlobalFile(self, fileStoreID):
        self.deleteLocalFile(fileStoreID)
        me = get_process_name(self.workDir)
        for row in self.cur.execute('SELECT job_id FROM refs WHERE file_id = ? AND state != ?', (fileStoreID, 'mutable')):
            raise RuntimeError('Deleted file ID %s which is still in use by job %s' % (fileStoreID, row[0]))

        self._write([('UPDATE files SET state = ?, owner = ? WHERE id = ?', ('deleting', me, fileStoreID))])
        self._executePendingDeletions(self.workDir, self.con, self.cur)
        self.filesToDelete.add(str(fileStoreID))
        self.logToMaster(("Added file with ID '%s' to the list of files to be" % fileStoreID + ' globally deleted.'),
          level=(logging.DEBUG))

    def exportFile(self, jobStoreFileID, dstUrl):
        self._executePendingUploads(self.con, self.cur)
        self.jobStore.exportFile(jobStoreFileID, dstUrl)

    def waitForCommit(self):
        if self.commitThread is not None:
            self.commitThread.join()
        return True

    def startCommit(self, jobState=False):
        self.waitForCommit()
        self.commitThread = threading.Thread(target=(self.startCommitThread), args=(jobState,))
        self.commitThread.start()

    def startCommitThread(self, jobState):
        """
        Run in a thread to actually commit the current job.
        """
        if self.waitForPreviousCommit is not None:
            self.waitForPreviousCommit()
        try:
            con = sqlite3.connect((self.dbPath), timeout=SQLITE_TIMEOUT_SECS)
            cur = con.cursor()
            logger.debug('Committing file uploads asynchronously')
            self._executePendingUploads(con, cur)
            self._executePendingDeletions(self.workDir, con, cur)
            if jobState:
                logger.debug('Committing file deletes and job state changes asynchronously')
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

    @classmethod
    def shutdown(cls, dir_):
        """
        :param dir_: The workflow diorectory for the node, which is used as the
                     cache directory, containing cache state database. Job
                     local temp directories will be removed due to their
                     appearance in the database.
        """
        if os.path.isdir(dir_):
            dbFilename = None
            dbAttempt = float('-inf')
            for dbCandidate in os.listdir(dir_):
                match = re.match('cache-([0-9]+).db', dbCandidate)
                if match and int(match.group(1)) > dbAttempt:
                    dbFilename = dbCandidate
                    dbAttempt = int(match.group(1))

            if dbFilename is not None:
                logger.debug('Connecting to latest caching database %s for cleanup', dbFilename)
                dbPath = os.path.join(dir_, dbFilename)
                if os.path.exists(dbPath):
                    try:
                        con = sqlite3.connect(dbPath, timeout=SQLITE_TIMEOUT_SECS)
                    except:
                        pass
                    else:
                        cls._ensureTables(con)
                        cls._removeDeadJobs(dir_, con)
                        con.close()
            else:
                logger.debug('No caching database found in %s', dir_)
            robust_rmtree(dir_)

    def __del__(self):
        """
        Cleanup function that is run when destroying the class instance that ensures that all the
        file writing threads exit.
        """
        self.waitForCommit()

    @classmethod
    def _removeDeadJobs(cls, workDir, con):
        """
        Look at the state of all jobs registered in the database, and handle them
        (clean up the disk)

        :param str workDir: Toil work directory.
        :param sqlite3.Connection con: Connection to the cache database.
        """
        cur = con.cursor()
        me = get_process_name(workDir)
        workers = []
        for row in cur.execute('SELECT DISTINCT worker FROM jobs WHERE worker IS NOT NULL'):
            workers.append(row[0])

        deadWorkers = []
        for worker in workers:
            if not process_name_exists(workDir, worker):
                deadWorkers.append(worker)

        for deadWorker in deadWorkers:
            cls._staticWrite(con, cur, [('UPDATE jobs SET worker = NULL WHERE worker = ?', (deadWorker,))])

        if len(deadWorkers) > 0:
            logger.debug('Reaped %d dead workers', len(deadWorkers))
        while True:
            cur.execute('SELECT id FROM jobs WHERE worker IS NULL LIMIT 1')
            row = cur.fetchone()
            if row is None:
                break
            jobID = row[0]
            cls._staticWrite(con, cur, [('UPDATE jobs SET worker = ? WHERE id = ? AND worker IS NULL', (me, jobID))])
            cur.execute('SELECT id, tempdir FROM jobs WHERE id = ? AND worker = ?', (jobID, me))
            row = cur.fetchone()
            if row is None:
                pass
            else:
                cls._removeJob(con, cur, jobID)
                logger.debug('Cleaned up orphanded job %s', jobID)