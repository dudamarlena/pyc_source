# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/toil_vg/iostore.py
# Compiled at: 2018-11-03 15:09:40
"""
IOStore class originated here 

https://github.com/BD2KGenomics/hgvm-graph-bakeoff-evaluations/blob/master/scripts/toillib.py

and was then here:

https://github.com/cmarkello/toil-lib/blob/master/src/toil_lib/toillib.py

In a perfect world, this would be deprecated and replaced with Toil's stores. 

Actually did this here:

https://github.com/glennhickey/toil-vg/tree/issues/110-fix-iostore

But couldn't get Toil's multipart S3 uploader working on large files.  Also,
the toil jobStore interface is a little less clean for our use. 

So for now keep as part of toil-vg where it works.  Could also consider merging
into the upstream toil-lib

https://github.com/BD2KGenomics/toil-lib
"""
import sys, os, os.path, json, collections, logging, logging.handlers, SocketServer, struct, socket, threading, tarfile, shutil, tempfile, functools, random, time, dateutil, traceback, stat
from toil.realtimeLogger import RealtimeLogger
import datetime
try:
    import boto3
    have_s3 = True
except ImportError:
    have_s3 = False

try:
    import azure
    from azure.storage.blob import BlobService
    import toil.jobStores.azureJobStore
    have_azure = True
except ImportError:
    have_azure = False

def robust_makedirs(directory):
    """
    Make a directory when other nodes may be trying to do the same on a shared
    filesystem.
    
    """
    if not os.path.exists(directory):
        try:
            os.makedirs(directory)
        except OSError:
            pass

    assert os.path.exists(directory) and os.path.isdir(directory)


def write_global_directory(file_store, path, cleanup=False, tee=None, compress=True):
    """
    Write the given directory into the file store, and return an ID that can be
    used to retrieve it. Writes the files in the directory and subdirectories
    into a tar file in the file store.

    Does not preserve the name or permissions of the given directory (only of
    its contents).

    If cleanup is true, directory will be deleted from the file store when this
    job and its follow-ons finish.
    
    If tee is passed, a tar.gz of the directory contents will be written to that
    filename. The file thus created must not be modified after this function is
    called.
    
    """
    write_stream_mode = 'w'
    if compress:
        write_stream_mode = 'w|gz'
    if tee is not None:
        with open(tee, 'w') as (file_handle):
            with tarfile.open(fileobj=file_handle, mode=write_stream_mode) as (tar):
                for file_name in os.listdir(path):
                    tar.add(os.path.join(path, file_name), arcname=file_name)

        return file_store.writeGlobalFile(tee)
    else:
        with file_store.writeGlobalFileStream(cleanup=cleanup) as (file_handle, file_id):
            with tarfile.open(fileobj=file_handle, mode=write_stream_mode) as (tar):
                for file_name in os.listdir(path):
                    tar.add(os.path.join(path, file_name), arcname=file_name)

            return file_id
        return


def read_global_directory(file_store, directory_id, path):
    """
    Reads a directory with the given tar file id from the global file store and
    recreates it at the given path.
    
    The given path, if it exists, must be a directory.
    
    Do not use to extract untrusted directories, since they could sneakily plant
    files anywhere on the filesystem.
    
    """
    robust_makedirs(path)
    with file_store.readGlobalFileStream(directory_id) as (file_handle):
        with tarfile.open(fileobj=file_handle, mode='r|*') as (tar):
            tar.extractall(path)


class IOStore(object):
    """
    A class that lets you get your input files and save your output files
    to/from a local filesystem, Amazon S3, or Microsoft Azure storage
    transparently.
    
    This is the abstract base class; other classes inherit from this and fill in
    the methods.
    
    """

    def __init__(self):
        """
        Make a new IOStore
        """
        raise NotImplementedError()

    def read_input_file(self, input_path, local_path):
        """
        Read an input file from wherever the input comes from and send it to the
        given path.
        
        If the file at local_path already exists, it is overwritten.
        
        If the file at local_path already exists and is a directory, behavior is
        undefined.
        
        """
        raise NotImplementedError()

    def list_input_directory(self, input_path, recursive=False, with_times=False):
        """
        Yields each of the subdirectories and files in the given input path.
        
        If recursive is false, yields files and directories in the given
        directory. If recursive is true, yields all files contained within the
        current directory, recursively, but does not yield folders.
        
        If with_times is True, yields (name, modification time) pairs instead of
        just names, with modification times represented as datetime objects in
        the GMT timezone. Modification times may be None on objects that do not
        support them.
        
        Gives relative file/directory names.
        
        """
        raise NotImplementedError()

    def write_output_file(self, local_path, output_path):
        """
        Save the given local file to the given output path. No output directory
        needs to exist already.
        
        If the output path already exists, it is overwritten.
        
        If the output path already exists and is a directory, behavior is
        undefined.
        
        """
        raise NotImplementedError()

    def exists(self, path):
        """
        Returns true if the given input or output file exists in the store
        already.
        
        """
        raise NotImplementedError()

    def get_mtime(self, path):
        """
        Returns the modification time of the given gile if it exists, or None
        otherwise.
        
        """
        raise NotImplementedError()

    def get_size(self, path):
        """
        Returns the size in bytes of the given file if it exists, or None
        otherwise.
        
        """
        raise NotImplementedError()

    @staticmethod
    def absolute(store_string):
        """
        Convert a relative path IOStore string to an absolute path one. Leaves
        strings that aren't FileIOStore specifications alone.
        
        Since new Toil versions change the working directory of SingleMachine
        batch system jobs, we need to have absolute paths passed into jobs.
        
        Recommended to be used as an argparse type, so that strings can be
        directly be passed to IOStore.get on the nodes.
        
        """
        if store_string == '':
            return ''
        if store_string[0] == '.':
            return os.path.abspath(store_string)
        if store_string.startswith('file:'):
            return 'file:' + os.path.abspath(store_string[5:])
        return store_string

    @staticmethod
    def get(store_string):
        """
        Get a concrete IOStore created from the given connection string.
        
        Valid formats are just like for a Toil JobStore, except with container
        names being specified on Azure.
        
        Formats:
        
        /absolute/filesystem/path
        
        ./relative/filesystem/path
        
        file:filesystem/path
        
        aws:region:bucket (TODO)
        
        aws:region:bucket/path/prefix (TODO)
        
        azure:account:container (instead of a container prefix) (gets keys like
        Toil)
        
        azure:account:container/path/prefix (trailing slash added automatically)
        
        """
        if store_string[0] in '/.':
            store_string = 'file:' + store_string
        try:
            store_type, store_arguments = store_string.split(':', 1)
        except ValueError:
            raise RuntimeError(('Incorrect IO store specification {}. Local paths must start with . or /').format(store_string))

        if store_type == 'file':
            return FileIOStore(store_arguments)
        if store_type == 'aws':
            region, bucket_name = store_arguments.split(':', 1)
            if '/' in bucket_name:
                bucket_name, path_prefix = bucket_name.split('/', 1)
            else:
                path_prefix = ''
            return S3IOStore(region, bucket_name, path_prefix)
        if store_type == 'azure':
            account, container = store_arguments.split(':', 1)
            if '/' in container:
                container, path_prefix = container.split('/', 1)
            else:
                path_prefix = ''
            return AzureIOStore(account, container, path_prefix)
        raise RuntimeError(('Unknown IOStore implementation {}').format(store_type))


class FileIOStore(IOStore):
    """
    A class that lets you get input from and send output to filesystem files.
    
    """

    def __init__(self, path_prefix=''):
        """
        Make a new FileIOStore that just treats everything as local paths,
        relative to the given prefix.
        
        """
        self.path_prefix = path_prefix

    def read_input_file(self, input_path, local_path):
        """
        Get input from the filesystem.
        """
        RealtimeLogger.debug(('Loading {} from FileIOStore in {} to {}').format(input_path, self.path_prefix, local_path))
        if os.path.exists(local_path):
            try:
                os.unlink(local_path)
            except:
                pass

        if not not os.path.exists(local_path):
            raise AssertionError
            real_path = os.path.abspath(os.path.join(self.path_prefix, input_path))
            os.path.exists(real_path) or RealtimeLogger.error(("Can't find {} from FileIOStore in {}!").format(input_path, self.path_prefix))
            raise RuntimeError(('File {} missing!').format(real_path))
        temp_handle, temp_path = tempfile.mkstemp(dir=os.path.dirname(local_path))
        os.close(temp_handle)
        shutil.copy2(real_path, temp_path)
        RealtimeLogger.info(('rename {} -> {}').format(temp_path, local_path))
        os.rename(temp_path, local_path)
        file_stats = os.stat(real_path)
        if file_stats.st_uid == os.getuid() and file_stats.st_mode & stat.S_IWUSR:
            try:
                os.chmod(real_path, file_stats.st_mode ^ stat.S_IWUSR)
            except OSError:
                pass

    def list_input_directory(self, input_path, recursive=False, with_times=False):
        """
        Loop over directories on the filesystem.
        """
        RealtimeLogger.info(('Enumerating {} from FileIOStore in {}').format(input_path, self.path_prefix))
        if not os.path.exists(os.path.join(self.path_prefix, input_path)):
            return
        if not os.path.isdir(os.path.join(self.path_prefix, input_path)):
            return
        for item in os.listdir(os.path.join(self.path_prefix, input_path)):
            if recursive and os.path.isdir(os.path.join(self.path_prefix, input_path, item)):
                for subitem in self.list_input_directory(os.path.join(input_path, item), recursive):
                    name_to_yield = os.path.join(item, subitem)
                    if with_times:
                        mtime_epoch_seconds = os.path.getmtime(os.path.join(input_path, item, subitem))
                        yield (
                         name_to_yield, mtime_epoch_seconds)
                    else:
                        yield name_to_yield

            elif with_times:
                mtime_epoch_seconds = os.path.getmtime(os.path.join(input_path, item))
                yield (
                 item, mtime_epoch_seconds)
            else:
                yield item

    def write_output_file(self, local_path, output_path):
        """
        Write output to the filesystem
        """
        RealtimeLogger.debug(('Saving {} to FileIOStore in {}').format(output_path, self.path_prefix))
        real_output_path = os.path.join(self.path_prefix, output_path)
        parent_dir = os.path.split(real_output_path)[0]
        if parent_dir != '':
            robust_makedirs(parent_dir)
        temp_handle, temp_path = tempfile.mkstemp(dir=self.path_prefix)
        os.close(temp_handle)
        shutil.copy2(local_path, temp_path)
        if os.path.exists(real_output_path):
            os.unlink(real_output_path)
        os.rename(temp_path, real_output_path)

    def exists(self, path):
        """
        Returns true if the given input or output file exists in the file system
        already.
        
        """
        return os.path.exists(os.path.join(self.path_prefix, path))

    def get_mtime(self, path):
        """
        Returns the modification time of the given file if it exists, or None
        otherwise.
        
        """
        if not self.exists(path):
            return None
        else:
            mtime_epoch_seconds = os.path.getmtime(os.path.join(self.path_prefix, path))
            mtime_datetime = datetime.datetime.utcfromtimestamp(mtime_epoch_seconds).replace(tzinfo=dateutil.tz.tzutc())
            return mtime_datetime

    def get_size(self, path):
        """
        Returns the size in bytes of the given file if it exists, or None
        otherwise.
        
        """
        if not self.exists(path):
            return None
        else:
            return os.stat(os.path.join(self.path_prefix, path)).st_size


class BackoffError(RuntimeError):
    """
    Represents an error from running out of retries during exponential back-off.
    """
    pass


def backoff_times(retries, base_delay):
    """
    A generator that yields times for random exponential back-off. You have to
    do the exception handling and sleeping yourself. Stops when the retries run
    out.
    
    """
    yield 0
    try_number = 1
    delay = float(base_delay) * 2
    while try_number <= retries:
        yield random.uniform(base_delay, delay)
        delay *= 2
        try_number += 1


def backoff(original_function, retries=6, base_delay=10):
    """
    We define a decorator that does randomized exponential back-off up to a
    certain number of retries. Raises BackoffError if the operation doesn't
    succeed after backing off for the specified number of retries (which may be
    float("inf")).
    
    Unfortunately doesn't really work on generators.
    """

    @functools.wraps(original_function)
    def new_function(*args, **kwargs):
        for delay in backoff_times(retries=kwargs.get('retries', retries), base_delay=kwargs.get('base_delay', base_delay)):
            if delay > 0:
                RealtimeLogger.error(('Retry after {} seconds').format(delay))
                time.sleep(delay)
            try:
                return original_function(*args, **kwargs)
            except:
                RealtimeLogger.error(('{} failed due to: {}').format(original_function.__name__, ('').join(traceback.format_exception(*sys.exc_info()))))

        raise BackoffError(('Ran out of retries calling {}').format(original_function.__name__))

    return new_function


class S3IOStore(IOStore):
    """
    A class that lets you get input from and send output to AWS S3 Storage.
    
    """

    def __init__(self, region, bucket_name, name_prefix=''):
        """
        Make a new S3IOStore that reads from and writes to the given
        container in the given account, adding the given prefix to keys. All
        paths will be interpreted as keys or key prefixes.
        
        """
        assert have_s3
        self.region = region
        self.bucket_name = bucket_name
        self.name_prefix = name_prefix
        self.s3 = None
        return

    def __connect(self):
        """
        Make sure we have an S3 Bucket connection, and set one up if we don't.
        Creates the S3 bucket if it doesn't exist.
        """
        if self.s3 is None:
            RealtimeLogger.debug(('Connecting to bucket {} in region').format(self.bucket_name, self.region))
            self.s3 = boto3.client('s3')
            try:
                self.s3.head_bucket(Bucket=self.bucket_name)
            except:
                self.s3.create_bucket(Bucket=self.bucket_name, CreateBucketConfiguration={'LocationConstraint': self.region})

        return

    def read_input_file(self, input_path, local_path):
        """
        Get input from S3.
        """
        self.__connect()
        RealtimeLogger.debug(('Loading {} from S3IOStore').format(input_path))
        self.s3.download_file(self.bucket_name, os.path.join(self.name_prefix, input_path), local_path)

    def list_input_directory(self, input_path, recursive=False, with_times=False):
        """
        Yields each of the subdirectories and files in the given input path.
        
        If recursive is false, yields files and directories in the given
        directory. If recursive is true, yields all files contained within the
        current directory, recursively, but does not yield folders.
        
        If with_times is True, yields (name, modification time) pairs instead of
        just names, with modification times represented as datetime objects in
        the GMT timezone. Modification times may be None on objects that do not
        support them.
        
        Gives relative file/directory names.
        
        """
        raise NotImplementedError()

    def write_output_file(self, local_path, output_path):
        """
        Write output to S3.
        """
        self.__connect()
        RealtimeLogger.debug(('Saving {} to S3IOStore').format(output_path))
        self.s3.upload_file(local_path, self.bucket_name, os.path.join(self.name_prefix, output_path))

    def exists(self, path):
        """
        Returns true if the given input or output file exists in the store
        already.
        
        """
        raise NotImplementedError()

    def get_mtime(self, path):
        """
        Returns the modification time of the given file if it exists, or None
        otherwise.
        
        """
        raise NotImplementedError()

    def get_size(self, path):
        """
        Returns the size in bytes of the given file if it exists, or None
        otherwise.
        
        """
        raise NotImplementedError()


class AzureIOStore(IOStore):
    """
    A class that lets you get input from and send output to Azure Storage.
    
    """

    def __init__(self, account_name, container_name, name_prefix=''):
        """
        Make a new AzureIOStore that reads from and writes to the given
        container in the given account, adding the given prefix to keys. All
        paths will be interpreted as keys or key prefixes.
        
        If the name prefix does not end with a trailing slash, and is not empty,
        one will be added automatically.
        
        Account keys are retrieved from the AZURE_ACCOUNT_KEY environment
        variable or from the ~/.toilAzureCredentials file, as in Toil itself.
        
        """
        assert have_azure
        self.account_name = account_name
        self.container_name = container_name
        self.name_prefix = name_prefix
        if self.name_prefix != '' and not self.name_prefix.endswith('/'):
            self.name_prefix += '/'
        self.account_key = toil.jobStores.azureJobStore._fetchAzureAccountKey(self.account_name)
        self.connection = None
        return

    def __getstate__(self):
        """
        Return the state to use for pickling. We don't want to try and pickle
        an open Azure connection.
        """
        return (
         self.account_name, self.account_key, self.container_name,
         self.name_prefix)

    def __setstate__(self, state):
        """
        Set up after unpickling.
        """
        self.account_name = state[0]
        self.account_key = state[1]
        self.container_name = state[2]
        self.name_prefix = state[3]
        self.connection = None
        return

    def __connect(self):
        """
        Make sure we have an Azure connection, and set one up if we don't.
        """
        if self.connection is None:
            RealtimeLogger.debug(('Connecting to account {}, using container {} and prefix {}').format(self.account_name, self.container_name, self.name_prefix))
            self.connection = BlobService(account_name=self.account_name, account_key=self.account_key)
        return

    @backoff
    def read_input_file(self, input_path, local_path):
        """
        Get input from Azure.
        """
        self.__connect()
        RealtimeLogger.debug(('Loading {} from AzureIOStore').format(input_path))
        self.connection.get_blob_to_path(self.container_name, self.name_prefix + input_path, local_path)

    def list_input_directory(self, input_path, recursive=False, with_times=False):
        """
        Loop over fake /-delimited directories on Azure. The prefix may or may
        not not have a trailing slash; if not, one will be added automatically.
        
        Returns the names of files and fake directories in the given input fake
        directory, non-recursively.
        
        If with_times is specified, will yield (name, time) pairs including
        modification times as datetime objects. Times on directories are None.
        
        """
        self.__connect()
        RealtimeLogger.info(('Enumerating {} from AzureIOStore').format(input_path))
        fake_directory = self.name_prefix + input_path
        if fake_directory != '' and not fake_directory.endswith('/'):
            fake_directory += '/'
        marker = None
        subdirectories = set()
        while True:
            result = self.connection.list_blobs(self.container_name, prefix=fake_directory, marker=marker)
            RealtimeLogger.info(('Found {} files').format(len(result)))
            for blob in result:
                relative_path = blob.name[len(fake_directory):]
                if not recursive and '/' in relative_path:
                    subdirectory, _ = relative_path.split('/', 1)
                    if subdirectory not in subdirectories:
                        subdirectories.add(subdirectory)
                        if with_times:
                            yield (
                             subdirectory, None)
                        else:
                            yield subdirectory
                elif with_times:
                    mtime = blob.properties.last_modified
                    if isinstance(mtime, datetime.datetime):
                        assert mtime.tzinfo is not None and mtime.tzinfo.utcoffset(mtime) is not None
                    else:
                        mtime = dateutil.parser.parse(mtime).replace(tzinfo=dateutil.tz.tzutc())
                    yield (relative_path, mtime)
                else:
                    yield relative_path

            marker = result.next_marker
            if not marker:
                break

        return

    @backoff
    def write_output_file(self, local_path, output_path):
        """
        Write output to Azure. Will create the container if necessary.
        """
        self.__connect()
        RealtimeLogger.debug(('Saving {} to AzureIOStore').format(output_path))
        try:
            self.connection.create_container(self.container_name)
        except azure.WindowsAzureConflictError:
            pass

        self.connection.put_block_blob_from_path(self.container_name, self.name_prefix + output_path, local_path)

    @backoff
    def exists(self, path):
        """
        Returns true if the given input or output file exists in Azure already.
        
        """
        self.__connect()
        marker = None
        while True:
            try:
                self.connection.create_container(self.container_name)
            except azure.WindowsAzureConflictError:
                pass

            result = self.connection.list_blobs(self.container_name, prefix=self.name_prefix + path, marker=marker)
            for blob in result:
                if blob.name == self.name_prefix + path:
                    return True

            marker = result.next_marker
            if not marker:
                break

        return False

    @backoff
    def get_mtime(self, path):
        """
        Returns the modification time of the given blob if it exists, or None
        otherwise.
        
        """
        self.__connect()
        marker = None
        while True:
            result = self.connection.list_blobs(self.container_name, prefix=self.name_prefix + path, marker=marker)
            for blob in result:
                if blob.name == self.name_prefix + path:
                    mtime = blob.properties.last_modified
                    if isinstance(mtime, datetime.datetime):
                        if not (mtime.tzinfo is not None and mtime.tzinfo.utcoffset(mtime) is not None):
                            raise AssertionError
                        else:
                            mtime = dateutil.parser.parse(mtime).replace(tzinfo=dateutil.tz.tzutc())
                        return mtime

            marker = result.next_marker
            if not marker:
                break

        return

    @backoff
    def get_size(self, path):
        """
        Returns the size in bytes of the given blob if it exists, or None
        otherwise.
        
        """
        self.__connect()
        marker = None
        while True:
            result = self.connection.list_blobs(self.container_name, prefix=self.name_prefix + path, marker=marker)
            for blob in result:
                if blob.name == self.name_prefix + path:
                    size = blob.properties.content_length
                    return size

            marker = result.next_marker
            if not marker:
                break

        return