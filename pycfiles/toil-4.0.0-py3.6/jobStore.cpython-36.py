# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/toil/jobStores/aws/jobStore.py
# Compiled at: 2020-04-03 17:41:24
# Size of source mod 2**32: 67085 bytes
from __future__ import absolute_import
from future import standard_library
standard_library.install_aliases()
from builtins import str
from builtins import range
from contextlib import contextmanager, closing
import logging
try:
    import cPickle as pickle
except ImportError:
    import pickle

import re, time, uuid, base64, hashlib, itertools, urllib.parse, urllib.request, urllib.parse, urllib.error
from io import BytesIO
from six.moves import StringIO, reprlib
from toil.lib.memoize import strict_bool
from toil.lib.exceptions import panic
from toil.lib.objects import InnerClass
import boto3, boto.s3, boto.sdb
from boto.exception import S3CreateError
from boto.exception import SDBResponseError, S3ResponseError
import botocore.session, botocore.credentials
from toil.lib.compatibility import compat_bytes, compat_plain, USING_PYTHON2
from toil.lib.misc import AtomicFileCreate
from toil.fileStores import FileID
from toil.jobStores.abstractJobStore import AbstractJobStore, NoSuchJobException, ConcurrentFileModificationException, NoSuchFileException, NoSuchJobStoreException, JobStoreExistsException
from toil.jobStores.aws.utils import SDBHelper, retry_sdb, no_such_sdb_domain, sdb_unavailable, monkeyPatchSdbConnection, retry_s3, retryable_s3_errors, bucket_location_to_region, region_to_bucket_location, copyKeyMultipart, uploadFromPath, chunkedFileUpload, fileSizeAndTime
from toil.jobStores.utils import WritablePipe, ReadablePipe
from toil.jobGraph import JobGraph
import toil.lib.encryption as encryption
botocore_session = botocore.session.get_session()
botocore_session.get_component('credential_provider').get_provider('assume-role').cache = botocore.credentials.JSONFileCache()
boto3_session = boto3.Session(botocore_session=botocore_session)
s3_boto3_resource = boto3_session.resource('s3')
s3_boto3_client = boto3_session.client('s3')
log = logging.getLogger(__name__)

class AWSJobStore(AbstractJobStore):
    __doc__ = "\n    A job store that uses Amazon's S3 for file storage and SimpleDB for storing job info and\n    enforcing strong consistency on the S3 file storage. There will be SDB domains for jobs and\n    files and a versioned S3 bucket for file contents. Job objects are pickled, compressed,\n    partitioned into chunks of 1024 bytes and each chunk is stored as a an attribute of the SDB\n    item representing the job. UUIDs are used to identify jobs and files.\n    "
    bucketNameRe = re.compile('^[a-z0-9][a-z0-9-]+[a-z0-9]$')
    minBucketNameLen = 3
    maxBucketNameLen = 63
    maxNameLen = 10
    nameSeparator = '--'

    def __init__(self, locator, partSize=52428800):
        """
        Create a new job store in AWS or load an existing one from there.

        :param int partSize: The size of each individual part used for multipart operations like
               upload and copy, must be >= 5 MiB but large enough to not exceed 10k parts for the
               whole file
        """
        super(AWSJobStore, self).__init__()
        region, namePrefix = locator.split(':')
        if not self.bucketNameRe.match(namePrefix):
            raise ValueError("Invalid name prefix '%s'. Name prefixes must contain only digits, hyphens or lower-case letters and must not start or end in a hyphen." % namePrefix)
        if len(namePrefix) > self.maxBucketNameLen - self.maxNameLen - len(self.nameSeparator):
            raise ValueError("Invalid name prefix '%s'. Name prefixes may not be longer than 50 characters." % namePrefix)
        if '--' in namePrefix:
            raise ValueError("Invalid name prefix '%s'. Name prefixes may not contain %s." % (
             namePrefix, self.nameSeparator))
        log.debug("Instantiating %s for region %s and name prefix '%s'", self.__class__, region, namePrefix)
        self.locator = locator
        self.region = region
        self.namePrefix = namePrefix
        self.partSize = partSize
        self.jobsDomain = None
        self.filesDomain = None
        self.filesBucket = None
        self.db = self._connectSimpleDB()
        self.s3 = self._connectS3()

    def initialize(self, config):
        if self._registered:
            raise JobStoreExistsException(self.locator)
        self._registered = None
        try:
            self._bind(create=True)
        except:
            with panic(log):
                self.destroy()
        else:
            super(AWSJobStore, self).initialize(config)
            self._registered = True

    @property
    def sseKeyPath(self):
        return self.config.sseKey

    def resume(self):
        if not self._registered:
            raise NoSuchJobStoreException(self.locator)
        self._bind(create=False)
        super(AWSJobStore, self).resume()

    def _bind(self, create=False, block=True, check_versioning_consistency=True):

        def qualify(name):
            assert len(name) <= self.maxNameLen
            return self.namePrefix + self.nameSeparator + name

        if self.jobsDomain is None:
            self.jobsDomain = self._bindDomain((qualify('jobs')), create=create, block=block)
        if self.filesDomain is None:
            self.filesDomain = self._bindDomain((qualify('files')), create=create, block=block)
        if self.filesBucket is None:
            self.filesBucket = self._bindBucket((qualify('files')), create=create,
              block=block,
              versioning=True,
              check_versioning_consistency=check_versioning_consistency)

    @property
    def _registered(self):
        """
        A optional boolean property indidcating whether this job store is registered. The
        registry is the authority on deciding if a job store exists or not. If True, this job
        store exists, if None the job store is transitioning from True to False or vice versa,
        if False the job store doesn't exist.

        :type: bool|None
        """
        registry_domain = self._bindDomain(domain_name='toil-registry', create=False,
          block=False)
        if registry_domain is None:
            return False
        for attempt in retry_sdb():
            with attempt:
                attributes = registry_domain.get_attributes(item_name=(self.namePrefix), attribute_name='exists',
                  consistent_read=True)
                try:
                    exists = attributes['exists']
                except KeyError:
                    return False

                if exists == 'True':
                    return True
                if exists == 'False':
                    return
                assert False

    @_registered.setter
    def _registered(self, value):
        registry_domain = self._bindDomain(domain_name='toil-registry', create=(value is not False),
          block=False)
        if registry_domain is None:
            if value is False:
                pass
        else:
            for attempt in retry_sdb():
                with attempt:
                    if value is False:
                        registry_domain.delete_attributes(item_name=(self.namePrefix))
                    else:
                        if value is True:
                            attributes = dict(exists='True')
                        else:
                            if value is None:
                                attributes = dict(exists='False')
                            else:
                                assert False
                            registry_domain.put_attributes(item_name=(self.namePrefix), attributes=attributes)

    def _checkItem(self, item):
        if 'overlargeID' not in item:
            raise RuntimeError("overlargeID attribute isn't present: you are restarting an old, incompatible jobstore, or the jobstore logic is incorrect.")

    def _awsJobFromItem(self, item):
        self._checkItem(item)
        if item['overlargeID']:
            assert self.fileExists(item['overlargeID'])
            log.debug('Loading overlarge job from S3.')
            with self.readFileStream(item['overlargeID']) as (fh):
                binary = fh.read()
        else:
            binary, _ = SDBHelper.attributesToBinary(item)
            assert binary is not None
            job = pickle.loads(binary)
            return job

    def _awsJobToItem(self, job):
        binary = pickle.dumps(job, protocol=(pickle.HIGHEST_PROTOCOL))
        if len(binary) > SDBHelper.maxBinarySize(extraReservedChunks=1):
            with self.writeFileStream() as (writable, fileID):
                writable.write(binary)
            item = SDBHelper.binaryToAttributes(None)
            item['overlargeID'] = fileID
        else:
            item = SDBHelper.binaryToAttributes(binary)
            item['overlargeID'] = ''
        return item

    jobsPerBatchInsert = 25

    @contextmanager
    def batch(self):
        self._batchedJobGraphs = []
        yield
        batches = [self._batchedJobGraphs[i:i + self.jobsPerBatchInsert] for i in range(0, len(self._batchedJobGraphs), self.jobsPerBatchInsert)]
        for batch in batches:
            items = {jobGraph.jobStoreID:self._awsJobToItem(jobGraph) for jobGraph in batch}
            for attempt in retry_sdb():
                with attempt:
                    assert self.jobsDomain.batch_put_attributes(items)

        self._batchedJobGraphs = None

    def create(self, jobNode):
        jobStoreID = self._newJobID()
        log.debug("Creating job %s for '%s'", jobStoreID, '<no command>' if jobNode.command is None else jobNode.command)
        job = JobGraph.fromJobNode(jobNode, jobStoreID=jobStoreID, tryCount=(self._defaultTryCount()))
        if hasattr(self, '_batchedJobGraphs'):
            if self._batchedJobGraphs is not None:
                self._batchedJobGraphs.append(job)
        else:
            item = self._awsJobToItem(job)
            for attempt in retry_sdb():
                with attempt:
                    assert self.jobsDomain.put_attributes(job.jobStoreID, item)

        return job

    def exists(self, jobStoreID):
        for attempt in retry_sdb():
            with attempt:
                return bool(self.jobsDomain.get_attributes(item_name=(compat_bytes(jobStoreID)),
                  attribute_name=[
                 SDBHelper.presenceIndicator()],
                  consistent_read=True))

    def jobs(self):
        result = None
        for attempt in retry_sdb():
            with attempt:
                result = list(self.jobsDomain.select(consistent_read=True,
                  query=('select * from `%s`' % self.jobsDomain.name)))

        assert result is not None
        for jobItem in result:
            yield self._awsJobFromItem(jobItem)

    def load(self, jobStoreID):
        item = None
        for attempt in retry_sdb():
            with attempt:
                item = self.jobsDomain.get_attributes((compat_bytes(jobStoreID)), consistent_read=True)

        if not item:
            raise NoSuchJobException(jobStoreID)
        job = self._awsJobFromItem(item)
        if job is None:
            raise NoSuchJobException(jobStoreID)
        log.debug('Loaded job %s', jobStoreID)
        return job

    def update(self, job):
        log.debug('Updating job %s', job.jobStoreID)
        item = self._awsJobToItem(job)
        for attempt in retry_sdb():
            with attempt:
                assert self.jobsDomain.put_attributes(compat_bytes(job.jobStoreID), item)

    itemsPerBatchDelete = 25

    def delete(self, jobStoreID):
        log.debug('Deleting job %s', jobStoreID)
        item = None
        for attempt in retry_sdb():
            with attempt:
                item = self.jobsDomain.get_attributes((compat_bytes(jobStoreID)), consistent_read=True)

        self._checkItem(item)
        if item['overlargeID']:
            log.debug('Deleting job from filestore')
            self.deleteFile(item['overlargeID'])
        else:
            for attempt in retry_sdb():
                with attempt:
                    self.jobsDomain.delete_attributes(item_name=(compat_bytes(jobStoreID)))

            items = None
            for attempt in retry_sdb():
                with attempt:
                    items = list(self.filesDomain.select(consistent_read=True,
                      query=("select version from `%s` where ownerID='%s'" % (
                     self.filesDomain.name, jobStoreID))))

            assert items is not None
        if items:
            log.debug('Deleting %d file(s) associated with job %s', len(items), jobStoreID)
            n = self.itemsPerBatchDelete
            batches = [items[i:i + n] for i in range(0, len(items), n)]
            for batch in batches:
                itemsDict = {item.name:None for item in batch}
                for attempt in retry_sdb():
                    with attempt:
                        self.filesDomain.batch_delete_attributes(itemsDict)

            for item in items:
                version = item.get('version')
                for attempt in retry_s3():
                    with attempt:
                        if version:
                            self.filesBucket.delete_key(key_name=(compat_bytes(item.name)), version_id=version)
                        else:
                            self.filesBucket.delete_key(key_name=(compat_bytes(item.name)))

    def getEmptyFileStoreID(self, jobStoreID=None, cleanup=False):
        info = self.FileInfo.create(jobStoreID if cleanup else None)
        with info.uploadStream() as (_):
            pass
        info.save()
        log.debug('Created %r.', info)
        return info.fileID

    def _importFile(self, otherCls, url, sharedFileName=None, hardlink=False):
        if issubclass(otherCls, AWSJobStore):
            srcKey = self._getKeyForUrl(url, existing=True)
            size = srcKey.size
            try:
                if sharedFileName is None:
                    info = self.FileInfo.create(srcKey.name)
                else:
                    self._requireValidSharedFileName(sharedFileName)
                    jobStoreFileID = self._sharedFileID(sharedFileName)
                    info = self.FileInfo.loadOrCreate(jobStoreFileID=jobStoreFileID, ownerID=(str(self.sharedFileOwnerID)),
                      encrypted=None)
                info.copyFrom(srcKey)
                info.save()
            finally:
                srcKey.bucket.connection.close()

            if sharedFileName is None:
                return FileID(info.fileID, size)
            return
        else:
            return super(AWSJobStore, self)._importFile(otherCls, url, sharedFileName=sharedFileName)

    def _exportFile(self, otherCls, jobStoreFileID, url):
        if issubclass(otherCls, AWSJobStore):
            dstKey = self._getKeyForUrl(url)
            try:
                info = self.FileInfo.loadOrFail(jobStoreFileID)
                info.copyTo(dstKey)
            finally:
                dstKey.bucket.connection.close()

        else:
            super(AWSJobStore, self)._defaultExportFile(otherCls, jobStoreFileID, url)

    @classmethod
    def getSize(cls, url):
        key = cls._getKeyForUrl(url, existing=True)
        try:
            return key.size
        finally:
            key.bucket.connection.close()

    @classmethod
    def _readFromUrl(cls, url, writable):
        srcKey = cls._getKeyForUrl(url, existing=True)
        try:
            srcKey.get_contents_to_file(writable)
        finally:
            srcKey.bucket.connection.close()

        return srcKey.size

    @classmethod
    def _writeToUrl(cls, readable, url):
        dstKey = cls._getKeyForUrl(url)
        try:
            canDetermineSize = True
            try:
                readable.seek(0, 2)
                fileSize = readable.tell()
                readable.seek(0)
            except:
                canDetermineSize = False

            if canDetermineSize:
                if fileSize > 5000000:
                    log.debug('Uploading %s with size %s, will use multipart uploading', dstKey.name, fileSize)
                    chunkedFileUpload(readable=readable, bucket=(dstKey.bucket), fileID=(dstKey.name), file_size=fileSize)
            else:
                log.debug('Can not use multipart uploading for %s, uploading whole file at once', dstKey.name)
                dstKey.set_contents_from_string(readable.read())
        finally:
            dstKey.bucket.connection.close()

    @staticmethod
    def _getKeyForUrl(url, existing=None):
        """
        Extracts a key from a given s3:// URL. On return, but not on exceptions, this method
        leaks an S3Connection object. The caller is responsible to close that by calling
        key.bucket.connection.close().

        :param bool existing: If True, key is expected to exist. If False, key is expected not to
               exists and it will be created. If None, the key will be created if it doesn't exist.

        :rtype: Key
        """
        keyName = url.path[1:]
        bucketName = url.netloc
        try:
            with closing(boto.connect_s3()) as (s3):
                location = s3.get_bucket(bucketName).get_location()
                region = bucket_location_to_region(location)
        except S3ResponseError as e:
            if e.error_code == 'AccessDenied':
                s3 = boto.connect_s3()
            else:
                raise
        else:
            s3 = boto.s3.connect_to_region(region)
        try:
            bucket = s3.get_bucket(bucketName)
            key = bucket.get_key(keyName.encode('utf-8'))
            if existing is True:
                if key is None:
                    raise RuntimeError("Key '%s' does not exist in bucket '%s'." % (
                     keyName, bucketName))
            else:
                if existing is False:
                    if key is not None:
                        raise RuntimeError("Key '%s' exists in bucket '%s'." % (
                         keyName, bucketName))
                else:
                    if existing is None:
                        pass
                    else:
                        assert False
            if key is None:
                key = bucket.new_key(keyName)
        except:
            with panic():
                s3.close()
        else:
            return key

    @classmethod
    def _supportsUrl(cls, url, export=False):
        return url.scheme.lower() == 's3'

    def writeFile(self, localFilePath, jobStoreID=None, cleanup=False):
        info = self.FileInfo.create(jobStoreID if cleanup else None)
        info.upload(localFilePath, not self.config.disableJobStoreChecksumVerification)
        info.save()
        log.debug('Wrote %r of from %r', info, localFilePath)
        return info.fileID

    @contextmanager
    def writeFileStream(self, jobStoreID=None, cleanup=False):
        info = self.FileInfo.create(jobStoreID if cleanup else None)
        with info.uploadStream() as (writable):
            yield (
             writable, info.fileID)
        info.save()
        log.debug('Wrote %r.', info)

    @contextmanager
    def writeSharedFileStream(self, sharedFileName, isProtected=None):
        self._requireValidSharedFileName(sharedFileName)
        info = self.FileInfo.loadOrCreate(jobStoreFileID=(self._sharedFileID(sharedFileName)), ownerID=(str(self.sharedFileOwnerID)),
          encrypted=isProtected)
        with info.uploadStream() as (writable):
            yield writable
        info.save()
        log.debug('Wrote %r for shared file %r.', info, sharedFileName)

    def updateFile(self, jobStoreFileID, localFilePath):
        info = self.FileInfo.loadOrFail(jobStoreFileID)
        info.upload(localFilePath, not self.config.disableJobStoreChecksumVerification)
        info.save()
        log.debug('Wrote %r from path %r.', info, localFilePath)

    @contextmanager
    def updateFileStream(self, jobStoreFileID):
        info = self.FileInfo.loadOrFail(jobStoreFileID)
        with info.uploadStream() as (writable):
            yield writable
        info.save()
        log.debug('Wrote %r from stream.', info)

    def fileExists(self, jobStoreFileID):
        return self.FileInfo.exists(jobStoreFileID)

    def getFileSize(self, jobStoreFileID):
        if not self.fileExists(jobStoreFileID):
            return 0
        else:
            info = self.FileInfo.loadOrFail(jobStoreFileID)
            return info.getSize()

    def readFile(self, jobStoreFileID, localFilePath, symlink=False):
        info = self.FileInfo.loadOrFail(jobStoreFileID)
        log.debug('Reading %r into %r.', info, localFilePath)
        info.download(localFilePath, not self.config.disableJobStoreChecksumVerification)

    @contextmanager
    def readFileStream(self, jobStoreFileID):
        info = self.FileInfo.loadOrFail(jobStoreFileID)
        log.debug('Reading %r into stream.', info)
        with info.downloadStream() as (readable):
            yield readable

    @contextmanager
    def readSharedFileStream(self, sharedFileName):
        self._requireValidSharedFileName(sharedFileName)
        jobStoreFileID = self._sharedFileID(sharedFileName)
        info = self.FileInfo.loadOrFail(jobStoreFileID, customName=sharedFileName)
        log.debug('Reading %r for shared file %r into stream.', info, sharedFileName)
        with info.downloadStream() as (readable):
            yield readable

    def deleteFile(self, jobStoreFileID):
        info = self.FileInfo.load(jobStoreFileID)
        if info is None:
            log.debug('File %s does not exist, skipping deletion.', jobStoreFileID)
        else:
            info.delete()

    def writeStatsAndLogging(self, statsAndLoggingString):
        info = self.FileInfo.create(str(self.statsFileOwnerID))
        with info.uploadStream(multipart=False) as (writeable):
            if isinstance(statsAndLoggingString, str):
                statsAndLoggingString = statsAndLoggingString.encode('utf-8', errors='ignore')
            writeable.write(statsAndLoggingString)
        info.save()

    def readStatsAndLogging(self, callback, readAll=False):
        itemsProcessed = 0
        for info in self._readStatsAndLogging(callback, self.statsFileOwnerID):
            info._ownerID = self.readStatsFileOwnerID
            info.save()
            itemsProcessed += 1

        if readAll:
            for _ in self._readStatsAndLogging(callback, self.readStatsFileOwnerID):
                itemsProcessed += 1

        return itemsProcessed

    def _readStatsAndLogging(self, callback, ownerId):
        items = None
        for attempt in retry_sdb():
            with attempt:
                items = list(self.filesDomain.select(consistent_read=True,
                  query=("select * from `%s` where ownerID='%s'" % (
                 self.filesDomain.name, str(ownerId)))))

        assert items is not None
        for item in items:
            info = self.FileInfo.fromItem(item)
            with info.downloadStream() as (readable):
                callback(readable)
            yield info

    def getPublicUrl(self, jobStoreFileID):
        info = self.FileInfo.loadOrFail(jobStoreFileID)
        if info.content is not None:
            with info.uploadStream(allowInlining=False) as (f):
                f.write(info.content)
        for attempt in retry_s3():
            with attempt:
                key = self.filesBucket.get_key(key_name=(compat_bytes(jobStoreFileID)), version_id=(info.version))
                key.set_canned_acl('public-read')
                url = key.generate_url(query_auth=False, expires_in=(self.publicUrlExpiration.total_seconds()))
                scheme, netloc, path, query, fragment = urllib.parse.urlsplit(url)
                params = urllib.parse.parse_qs(query)
                if 'x-amz-security-token' in params:
                    del params['x-amz-security-token']
                query = urllib.parse.urlencode(params, doseq=True)
                url = urllib.parse.urlunsplit((scheme, netloc, path, query, fragment))
                return url

    def getSharedPublicUrl(self, sharedFileName):
        self._requireValidSharedFileName(sharedFileName)
        return self.getPublicUrl(self._sharedFileID(sharedFileName))

    def _connectSimpleDB(self):
        """
        :rtype: SDBConnection
        """
        db = boto.sdb.connect_to_region(self.region)
        if db is None:
            raise ValueError("Could not connect to SimpleDB. Make sure '%s' is a valid SimpleDB region." % self.region)
        monkeyPatchSdbConnection(db)
        return db

    def _connectS3(self):
        """
        :rtype: S3Connection
        """
        s3 = boto.s3.connect_to_region(self.region)
        if s3 is None:
            raise ValueError("Could not connect to S3. Make sure '%s' is a valid S3 region." % self.region)
        return s3

    def _bindBucket(self, bucket_name, create=False, block=True, versioning=False, check_versioning_consistency=True):
        """
        Return the Boto Bucket object representing the S3 bucket with the given name. If the
        bucket does not exist and `create` is True, it will be created.

        :param str bucket_name: the name of the bucket to bind to

        :param bool create: Whether to create bucket the if it doesn't exist

        :param bool block: If False, return None if the bucket doesn't exist. If True, wait until
               bucket appears. Ignored if `create` is True.

        :rtype: Bucket|None
        :raises S3ResponseError: If `block` is True and the bucket still doesn't exist after the
                retry timeout expires.
        """
        if not self.minBucketNameLen <= len(bucket_name) <= self.maxBucketNameLen:
            raise AssertionError
        elif not self.bucketNameRe.match(bucket_name):
            raise AssertionError
        log.debug("Binding to job store bucket '%s'.", bucket_name)

        def bucket_creation_pending(e):
            return isinstance(e, (S3CreateError, S3ResponseError)) and e.error_code in ('BucketAlreadyOwnedByYou',
                                                                                        'OperationAborted',
                                                                                        'NoSuchBucket')

        bucketExisted = True
        for attempt in retry_s3(predicate=bucket_creation_pending):
            with attempt:
                try:
                    bucket = self.s3.get_bucket(bucket_name, validate=True)
                except S3ResponseError as e:
                    if e.error_code == 'NoSuchBucket':
                        bucketExisted = False
                        log.debug("Bucket '%s' does not exist.", bucket_name)
                        if create:
                            log.debug("Creating bucket '%s'.", bucket_name)
                            location = region_to_bucket_location(self.region)
                            bucket = self.s3.create_bucket(bucket_name, location=location)
                            assert self._AWSJobStore__getBucketRegion(bucket) == self.region
                        else:
                            if block:
                                raise
                            else:
                                return
                    else:
                        if e.status == 301:
                            bucket = self.s3.get_bucket(bucket_name, validate=False)
                            raise BucketLocationConflictException(self._AWSJobStore__getBucketRegion(bucket))
                        else:
                            raise
                else:
                    if self._AWSJobStore__getBucketRegion(bucket) != self.region:
                        raise BucketLocationConflictException(self._AWSJobStore__getBucketRegion(bucket))
                    else:
                        if versioning:
                            if not bucketExisted:
                                bucket.configure_versioning(True)
                                time.sleep(1)
                                while self._getBucketVersioning(bucket) != True:
                                    log.warning("Waiting for versioning activation on bucket '%s'...", bucket_name)
                                    time.sleep(1)

                        if check_versioning_consistency:
                            bucket_versioning = self._getBucketVersioning(bucket)
                            if bucket_versioning != versioning:
                                assert False, 'Cannot modify versioning on existing bucket'
                            elif bucket_versioning is None:
                                assert False, 'Cannot use a bucket with versioning suspended'
                        if bucketExisted:
                            log.debug("Using pre-existing job store bucket '%s'.", bucket_name)
                        else:
                            log.debug("Created new job store bucket '%s' with versioning state %s.", bucket_name, str(versioning))
                    return bucket

    def _bindDomain(self, domain_name, create=False, block=True):
        """
        Return the Boto Domain object representing the SDB domain of the given name. If the
        domain does not exist and `create` is True, it will be created.

        :param str domain_name: the name of the domain to bind to

        :param bool create: True if domain should be created if it doesn't exist

        :param bool block: If False, return None if the domain doesn't exist. If True, wait until
               domain appears. This parameter is ignored if create is True.

        :rtype: Domain|None
        :raises SDBResponseError: If `block` is True and the domain still doesn't exist after the
                retry timeout expires.
        """
        log.debug("Binding to job store domain '%s'.", domain_name)
        retryargs = dict(predicate=(lambda e: no_such_sdb_domain(e) or sdb_unavailable(e)))
        if not block:
            retryargs['timeout'] = 15
        for attempt in retry_sdb(**retryargs):
            with attempt:
                try:
                    return self.db.get_domain(domain_name)
                except SDBResponseError as e:
                    if no_such_sdb_domain(e):
                        if create:
                            return self.db.create_domain(domain_name)
                        if block:
                            raise
                        else:
                            return
                    else:
                        raise

    def _newJobID(self):
        return str(uuid.uuid4())

    sharedFileOwnerID = uuid.UUID('891f7db6-e4d9-4221-a58e-ab6cc4395f94')
    statsFileOwnerID = uuid.UUID('bfcf5286-4bc7-41ef-a85d-9ab415b69d53')
    readStatsFileOwnerID = uuid.UUID('e77fc3aa-d232-4255-ae04-f64ee8eb0bfa')

    def _sharedFileID(self, sharedFileName):
        return str(uuid.uuid5(self.sharedFileOwnerID, sharedFileName))

    @InnerClass
    class FileInfo(SDBHelper):
        __doc__ = '\n        Represents a file in this job store.\n        '
        outer = None

        def __init__(self, fileID, ownerID, encrypted, version=None, content=None, numContentChunks=0, checksum=None):
            """
            :type fileID: str
            :param fileID: the file's ID

            :type ownerID: str
            :param ownerID: ID of the entity owning this file, typically a job ID aka jobStoreID

            :type encrypted: bool
            :param encrypted: whether the file is stored in encrypted form

            :type version: str|None
            :param version: a non-empty string containing the most recent version of the S3
            object storing this file's content, None if the file is new, or empty string if the
            file is inlined.

            :type content: str|None
            :param content: this file's inlined content

            :type numContentChunks: int
            :param numContentChunks: the number of SDB domain attributes occupied by this files

            :type checksum: str|None
            :param checksum: the sha1 checksum of the file, if available.

            inlined content. Note that an inlined empty string still occupies one chunk.
            """
            super(AWSJobStore.FileInfo, self).__init__()
            self._fileID = fileID
            self._ownerID = ownerID
            self.encrypted = encrypted
            self._version = version
            self._previousVersion = version
            self._content = content
            self._checksum = checksum
            self._numContentChunks = numContentChunks

        @property
        def fileID(self):
            return self._fileID

        @property
        def ownerID(self):
            return self._ownerID

        @property
        def version(self):
            return self._version

        @version.setter
        def version(self, version):
            assert self._previousVersion == self._version
            self._version = version
            if version:
                self.content = None

        @property
        def previousVersion(self):
            return self._previousVersion

        @property
        def content(self):
            return self._content

        @property
        def checksum(self):
            return self._checksum

        @checksum.setter
        def checksum(self, checksum):
            self._checksum = checksum

        @content.setter
        def content(self, content):
            if not content is None:
                if not isinstance(content, bytes):
                    raise AssertionError
            self._content = content
            if content is not None:
                self.version = ''

        @classmethod
        def create(cls, ownerID):
            return cls((str(uuid.uuid4())), ownerID, encrypted=(cls.outer.sseKeyPath is not None))

        @classmethod
        def presenceIndicator(cls):
            return 'encrypted'

        @classmethod
        def exists(cls, jobStoreFileID):
            for attempt in retry_sdb():
                with attempt:
                    return bool(cls.outer.filesDomain.get_attributes(item_name=(compat_bytes(jobStoreFileID)),
                      attribute_name=[
                     cls.presenceIndicator()],
                      consistent_read=True))

        @classmethod
        def load(cls, jobStoreFileID):
            for attempt in retry_sdb():
                with attempt:
                    self = cls.fromItem(cls.outer.filesDomain.get_attributes(item_name=(compat_bytes(jobStoreFileID)), consistent_read=True))
                    return self

        @classmethod
        def loadOrCreate(cls, jobStoreFileID, ownerID, encrypted):
            self = cls.load(jobStoreFileID)
            if encrypted is None:
                encrypted = cls.outer.sseKeyPath is not None
            if self is None:
                self = cls(jobStoreFileID, ownerID, encrypted=encrypted)
            else:
                if not self.fileID == jobStoreFileID:
                    raise AssertionError
                elif not self.ownerID == ownerID:
                    raise AssertionError
                self.encrypted = encrypted
            return self

        @classmethod
        def loadOrFail(cls, jobStoreFileID, customName=None):
            """
            :rtype: AWSJobStore.FileInfo
            :return: an instance of this class representing the file with the given ID
            :raises NoSuchFileException: if given file does not exist
            """
            self = cls.load(jobStoreFileID)
            if self is None:
                raise NoSuchFileException(jobStoreFileID, customName=customName)
            else:
                return self

        @classmethod
        def fromItem(cls, item):
            """
            Convert an SDB item to an instance of this class.

            :type item: Item
            """
            assert item is not None

            def strOrNone(s):
                if s is None:
                    return s
                else:
                    return str(s)

            ownerID = strOrNone(item.get('ownerID'))
            encrypted = item.get('encrypted')
            if ownerID is None:
                assert encrypted is None
                return
            else:
                version = strOrNone(item['version'])
                checksum = strOrNone(item.get('checksum'))
                encrypted = strict_bool(encrypted)
                content, numContentChunks = cls.attributesToBinary(item)
                if encrypted:
                    sseKeyPath = cls.outer.sseKeyPath
                    if sseKeyPath is None:
                        raise AssertionError('Content is encrypted but no key was provided.')
                    if content is not None:
                        content = encryption.decrypt(content, sseKeyPath)
                self = cls(fileID=(item.name), ownerID=ownerID, encrypted=encrypted, version=version, content=content,
                  numContentChunks=numContentChunks,
                  checksum=checksum)
                return self

        def toItem(self):
            """
            Convert this instance to an attribute dictionary suitable for SDB put_attributes().

            :rtype: (dict,int)

            :return: the attributes dict and an integer specifying the the number of chunk
                     attributes in the dictionary that are used for storing inlined content.
            """
            content = self.content
            if not content is None:
                if not isinstance(content, bytes):
                    raise AssertionError
            else:
                if self.encrypted:
                    if content is not None:
                        sseKeyPath = self.outer.sseKeyPath
                        if sseKeyPath is None:
                            raise AssertionError('Encryption requested but no key was provided.')
                        content = encryption.encrypt(content, sseKeyPath)
            if not content is None:
                if not isinstance(content, bytes):
                    raise AssertionError
            attributes = self.binaryToAttributes(content)
            numChunks = attributes['numChunks']
            attributes.update(dict(ownerID=(self.ownerID), encrypted=(self.encrypted),
              version=(self.version or ''),
              checksum=(self.checksum or '')))
            return (attributes, numChunks)

        @classmethod
        def _reservedAttributes(cls):
            return 3 + super(AWSJobStore.FileInfo, cls)._reservedAttributes()

        @staticmethod
        def maxInlinedSize():
            return 256

        def save(self):
            attributes, numNewContentChunks = self.toItem()
            expected = [
             'version', False if self.previousVersion is None else self.previousVersion]
            try:
                for attempt in retry_sdb():
                    with attempt:
                        assert self.outer.filesDomain.put_attributes(item_name=(compat_bytes(self.fileID)), attributes=attributes,
                          expected_value=expected)

                if self.previousVersion:
                    if self.previousVersion != self.version:
                        for attempt in retry_s3():
                            with attempt:
                                self.outer.filesBucket.delete_key((compat_bytes(self.fileID)), version_id=(self.previousVersion))

                self._previousVersion = self._version
                if numNewContentChunks < self._numContentChunks:
                    residualChunks = range(numNewContentChunks, self._numContentChunks)
                    attributes = [self._chunkName(i) for i in residualChunks]
                    for attempt in retry_sdb():
                        with attempt:
                            self.outer.filesDomain.delete_attributes((compat_bytes(self.fileID)), attributes=attributes)

                self._numContentChunks = numNewContentChunks
            except SDBResponseError as e:
                if e.error_code == 'ConditionalCheckFailed':
                    raise ConcurrentFileModificationException(self.fileID)
                else:
                    raise

        def upload(self, localFilePath, calculateChecksum=True):
            file_size, file_time = fileSizeAndTime(localFilePath)
            if file_size <= self.maxInlinedSize():
                with open(localFilePath, 'rb') as (f):
                    self.content = f.read()
            else:
                headers = self._s3EncryptionHeaders()
                self.checksum = self._get_file_checksum(localFilePath) if calculateChecksum else None
                self.version = uploadFromPath(localFilePath, partSize=(self.outer.partSize), bucket=(self.outer.filesBucket),
                  fileID=(compat_bytes(self.fileID)),
                  headers=headers)

        def _get_file_checksum(self, localFilePath):
            with open(localFilePath, 'rb') as (f):
                checksum = hashlib.sha1()
                contents = f.read(1048576)
                while contents != b'':
                    checksum.update(contents)
                    contents = f.read(1048576)

                return 'sha1$%s' % checksum.hexdigest()

        @contextmanager
        def uploadStream(self, multipart=True, allowInlining=True):
            """
            Context manager that gives out a binary-mode upload stream to upload data.
            """
            if not not (bool(self.version) and self.content is not None):
                raise AssertionError
            else:
                info = self
                store = self.outer

                class MultiPartPipe(WritablePipe):

                    def readFrom(self, readable):
                        buf = readable.read(store.partSize)
                        assert isinstance(buf, bytes)
                        if allowInlining and len(buf) <= info.maxInlinedSize():
                            log.debug('Inlining content of %d bytes', len(buf))
                            info.content = buf
                        else:
                            headers = info._s3EncryptionHeaders()
                            for attempt in retry_s3():
                                with attempt:
                                    log.debug('Starting multipart upload')
                                    upload = store.filesBucket.initiate_multipart_upload(key_name=(compat_bytes(info.fileID)),
                                      headers=headers)

                        try:
                            for part_num in itertools.count():
                                if len(buf) == 0:
                                    if part_num > 0:
                                        break
                                    for attempt in retry_s3():
                                        with attempt:
                                            log.debug('Uploading part %d of %d bytes', part_num + 1, len(buf))
                                            if USING_PYTHON2:
                                                upload.upload_part_from_file(fp=(StringIO(buf)), part_num=(part_num + 1),
                                                  headers=headers)
                                            else:
                                                upload.upload_part_from_file(fp=(BytesIO(buf)), part_num=(part_num + 1),
                                                  headers=headers)

                                    if len(buf) == 0:
                                        break
                                    buf = readable.read(info.outer.partSize)
                                    assert isinstance(buf, bytes)

                        except:
                            with panic(log=log):
                                for attempt in retry_s3():
                                    with attempt:
                                        upload.cancel_upload()

                        else:
                            while store._getBucketVersioning(store.filesBucket) != True:
                                log.warning('Versioning does not appear to be enabled yet. Deferring multipart upload completion...')
                                time.sleep(1)

                            for attempt in retry_s3():
                                with attempt:
                                    log.debug('Attempting to complete upload...')
                                    completed = upload.complete_upload()
                                    log.debug('Completed upload object of type %s: %s', str(type(completed)), repr(completed))
                                    info.version = completed.version_id
                                    log.debug('Completed upload with version %s', str(info.version))

                            if info.version is None:
                                for attempt in retry_s3(predicate=(lambda e: retryable_s3_errors(e) or isinstance(e, AssertionError))):
                                    with attempt:
                                        key = store.filesBucket.get_key((compat_bytes(info.fileID)), headers=headers)
                                        log.warning('Loaded key for upload with no version and got version %s', str(key.version_id))
                                        info.version = key.version_id
                                        assert info.version is not None

                            if not bool(info.version):
                                if not info.content is not None:
                                    raise AssertionError

                class SinglePartPipe(WritablePipe):

                    def readFrom(self, readable):
                        buf = readable.read()
                        assert isinstance(buf, bytes)
                        dataLength = len(buf)
                        if allowInlining and dataLength <= info.maxInlinedSize():
                            log.debug('Inlining content of %d bytes', len(buf))
                            info.content = buf
                        else:
                            key = store.filesBucket.new_key(key_name=(compat_bytes(info.fileID)))
                            buf = BytesIO(buf)
                            headers = info._s3EncryptionHeaders()
                            while store._getBucketVersioning(store.filesBucket) != True:
                                log.warning('Versioning does not appear to be enabled yet. Deferring single part upload...')
                                time.sleep(1)

                            for attempt in retry_s3():
                                with attempt:
                                    log.debug('Uploading single part of %d bytes', dataLength)
                                    assert dataLength == key.set_contents_from_file(fp=buf, headers=headers)
                                    log.debug('Upload received version %s', str(key.version_id))

                            info.version = key.version_id
                        if info.version is None:
                            for attempt in retry_s3(predicate=(lambda e: retryable_s3_errors(e) or isinstance(e, AssertionError))):
                                with attempt:
                                    key.reload()
                                    log.warning('Reloaded key with no version and got version %s', str(key.version_id))
                                    info.version = key.version_id
                                    assert info.version is not None

                        if not bool(info.version):
                            if not info.content is not None:
                                raise AssertionError

                pipe = MultiPartPipe() if multipart else SinglePartPipe()
                with pipe as (writable):
                    yield writable
                if not pipe.reader_done:
                    log.debug('Version: {} Content: {}'.format(self.version, self.content))
                    raise RuntimeError('Escaped context manager without written data being read!')
                if self.content is None:
                    if not bool(self.version):
                        log.debug('Version: {} Content: {}'.format(self.version, self.content))
                        raise RuntimeError('No content added and no version created')
                elif bool(self.version):
                    log.debug('Version: {} Content: {}'.format(self.version, self.content))
                    raise RuntimeError('Content added and version created')

        def copyFrom(self, srcKey):
            """
            Copies contents of source key into this file.

            :param srcKey: The key that will be copied from
            """
            if not srcKey.size is not None:
                raise AssertionError
            else:
                if srcKey.size <= self.maxInlinedSize():
                    self.content = srcKey.get_contents_as_string()
                else:
                    self.version = copyKeyMultipart(srcBucketName=(compat_plain(srcKey.bucket.name)), srcKeyName=(compat_plain(srcKey.name)),
                      srcKeyVersion=(compat_plain(srcKey.version_id)),
                      dstBucketName=(compat_plain(self.outer.filesBucket.name)),
                      dstKeyName=(compat_plain(self._fileID)),
                      sseAlgorithm='AES256',
                      sseKey=(self._getSSEKey()))

        def copyTo(self, dstKey):
            """
            Copies contents of this file to the given key.

            :param Key dstKey: The key to copy this file's content to
            """
            if self.content is not None:
                for attempt in retry_s3():
                    with attempt:
                        dstKey.set_contents_from_string(self.content)

            else:
                if self.version:
                    for attempt in retry_s3():
                        encrypted = True if self.outer.sseKeyPath else False
                        if encrypted:
                            srcKey = self.outer.filesBucket.get_key((compat_bytes(self.fileID)), headers=(self._s3EncryptionHeaders()))
                        else:
                            srcKey = self.outer.filesBucket.get_key(compat_bytes(self.fileID))
                        srcKey.version_id = self.version
                        with attempt:
                            copyKeyMultipart(srcBucketName=(compat_plain(srcKey.bucket.name)), srcKeyName=(compat_plain(srcKey.name)),
                              srcKeyVersion=(compat_plain(srcKey.version_id)),
                              dstBucketName=(compat_plain(dstKey.bucket.name)),
                              dstKeyName=(compat_plain(dstKey.name)),
                              copySourceSseAlgorithm='AES256',
                              copySourceSseKey=(self._getSSEKey()))

                elif not False:
                    raise AssertionError

        def download(self, localFilePath, verifyChecksum=True):
            if self.content is not None:
                with AtomicFileCreate(localFilePath) as (tmpPath):
                    with open(tmpPath, 'wb') as (f):
                        f.write(self.content)
            else:
                if self.version:
                    headers = self._s3EncryptionHeaders()
                    key = self.outer.filesBucket.get_key((compat_bytes(self.fileID)), validate=False)
                    for attempt in retry_s3():
                        with attempt:
                            with AtomicFileCreate(localFilePath) as (tmpPath):
                                key.get_contents_to_filename(tmpPath, version_id=(self.version),
                                  headers=headers)

                    if verifyChecksum:
                        if self.checksum:
                            downloadedChecksum = self._get_file_checksum(localFilePath)
                            if self.checksum != downloadedChecksum:
                                raise AssertionError('Checksums do not match for file %s. Expected: %s Actual: %s' % (
                                 localFilePath, self.checksum, downloadedChecksum))
                elif not False:
                    raise AssertionError

        @contextmanager
        def downloadStream(self):
            info = self

            class DownloadPipe(ReadablePipe):

                def writeTo(self, writable):
                    if info.content is not None:
                        writable.write(info.content)
                    else:
                        if info.version:
                            headers = info._s3EncryptionHeaders()
                            key = info.outer.filesBucket.get_key((compat_bytes(info.fileID)), validate=False)
                            for attempt in retry_s3():
                                with attempt:
                                    key.get_contents_to_file(writable, headers=headers,
                                      version_id=(info.version))

                        elif not False:
                            raise AssertionError

            with DownloadPipe() as (readable):
                yield readable

        def delete(self):
            store = self.outer
            if self.previousVersion is not None:
                for attempt in retry_sdb():
                    with attempt:
                        store.filesDomain.delete_attributes((compat_bytes(self.fileID)),
                          expected_values=[
                         'version', self.previousVersion])

                if self.previousVersion:
                    for attempt in retry_s3():
                        with attempt:
                            store.filesBucket.delete_key(key_name=(compat_bytes(self.fileID)), version_id=(self.previousVersion))

        def getSize(self):
            """
            Return the size of the referenced item in bytes.
            """
            if self.content is not None:
                return len(self.content)
            else:
                if self.version:
                    for attempt in retry_s3():
                        with attempt:
                            key = self.outer.filesBucket.get_key((compat_bytes(self.fileID)), validate=False)
                            return key.size

                else:
                    return 0

        def _getSSEKey(self):
            sseKeyPath = self.outer.sseKeyPath
            if sseKeyPath is None:
                return
            with open(sseKeyPath, 'rb') as (f):
                sseKey = f.read()
                return sseKey

        def _s3EncryptionHeaders(self):
            if self.encrypted:
                sseKey = self._getSSEKey()
                assert sseKey is not None, 'Content is encrypted but no key was provided.'
                assert len(sseKey) == 32
                encodedSseKey = base64.b64encode(sseKey).decode('utf-8')
                encodedSseKeyMd5 = base64.b64encode(hashlib.md5(sseKey).digest()).decode('utf-8')
                return {'x-amz-server-side-encryption-customer-algorithm':'AES256', 
                 'x-amz-server-side-encryption-customer-key':encodedSseKey, 
                 'x-amz-server-side-encryption-customer-key-md5':encodedSseKeyMd5}
            else:
                return {}

        def __repr__(self):
            r = custom_repr
            d = (('fileID', r(self.fileID)),
             (
              'ownerID', r(self.ownerID)),
             (
              'encrypted', r(self.encrypted)),
             (
              'version', r(self.version)),
             (
              'previousVersion', r(self.previousVersion)),
             (
              'content', r(self.content)),
             (
              'checksum', r(self.checksum)),
             (
              '_numContentChunks', r(self._numContentChunks)))
            return '{}({})'.format(type(self).__name__, ', '.join('%s=%s' % (k, v) for k, v in d))

    versionings = dict(Enabled=True, Disabled=False, Suspended=None)

    def _getBucketVersioning(self, bucket):
        """
        For newly created buckets get_versioning_status returns an empty dict. In the past we've
        seen None in this case. We map both to a return value of False.

        Otherwise, the 'Versioning' entry in the dictionary returned by get_versioning_status can
        be 'Enabled', 'Suspended' or 'Disabled' which we map to True, None and False
        respectively. Note that we've never seen a versioning status of 'Disabled', only the
        empty dictionary. Calling configure_versioning with False on a bucket will cause
        get_versioning_status to then return 'Suspended' even on a new bucket that never had
        versioning enabled.
        """
        for attempt in retry_s3():
            with attempt:
                status = bucket.get_versioning_status()
                if status:
                    return self.versionings[status['Versioning']]
                else:
                    return False

    def __getBucketRegion(self, bucket):
        for attempt in retry_s3():
            with attempt:
                return bucket_location_to_region(bucket.get_location())

    def destroy(self):
        try:
            self._bind(create=False, block=False, check_versioning_consistency=False)
        except BucketLocationConflictException:
            pass

        self._registered = None
        if self.filesBucket is not None:
            self._delete_bucket(self.filesBucket)
            self.filesBucket = None
        for name in ('filesDomain', 'jobsDomain'):
            domain = getattr(self, name)
            if domain is not None:
                self._delete_domain(domain)
                setattr(self, name, None)

        self._registered = False

    def _delete_domain(self, domain):
        for attempt in retry_sdb():
            with attempt:
                try:
                    domain.delete()
                except SDBResponseError as e:
                    if no_such_sdb_domain(e):
                        pass
                    else:
                        raise

    def _delete_bucket(self, b):
        for attempt in retry_s3():
            with attempt:
                try:
                    for upload in b.list_multipart_uploads():
                        upload.cancel_upload()

                    bucket = s3_boto3_resource.Bucket(compat_bytes(b.name))
                    bucket.objects.all().delete()
                    bucket.object_versions.delete()
                    bucket.delete()
                except s3_boto3_resource.meta.client.exceptions.NoSuchBucket:
                    pass
                except S3ResponseError as e:
                    if e.error_code != 'NoSuchBucket':
                        raise


aRepr = reprlib.Repr()
aRepr.maxstring = 38
custom_repr = aRepr.repr

class BucketLocationConflictException(Exception):

    def __init__(self, bucketRegion):
        super(BucketLocationConflictException, self).__init__('A bucket with the same name as the jobstore was found in another region (%s). Cannot proceed as the unique bucket name is already in use.' % bucketRegion)