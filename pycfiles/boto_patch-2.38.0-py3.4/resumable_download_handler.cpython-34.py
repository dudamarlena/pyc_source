# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/boto/s3/resumable_download_handler.py
# Compiled at: 2015-11-24 05:02:18
# Size of source mod 2**32: 15595 bytes
import errno, httplib, os, re, socket, time, boto
from boto import config, storage_uri_for_key
from boto.connection import AWSAuthConnection
from boto.exception import ResumableDownloadException
from boto.exception import ResumableTransferDisposition
from boto.s3.keyfile import KeyFile
from boto.gs.key import Key as GSKey

class ByteTranslatingCallbackHandler(object):
    __doc__ = "\n    Proxy class that translates progress callbacks made by\n    boto.s3.Key.get_file(), taking into account that we're resuming\n    a download.\n    "

    def __init__(self, proxied_cb, download_start_point):
        self.proxied_cb = proxied_cb
        self.download_start_point = download_start_point

    def call(self, total_bytes_uploaded, total_size):
        self.proxied_cb(self.download_start_point + total_bytes_uploaded, total_size)


def get_cur_file_size(fp, position_to_eof=False):
    """
    Returns size of file, optionally leaving fp positioned at EOF.
    """
    if isinstance(fp, KeyFile) and not position_to_eof:
        return fp.getkey().size
    if not position_to_eof:
        cur_pos = fp.tell()
    fp.seek(0, os.SEEK_END)
    cur_file_size = fp.tell()
    if not position_to_eof:
        fp.seek(cur_pos, os.SEEK_SET)
    return cur_file_size


class ResumableDownloadHandler(object):
    __doc__ = '\n    Handler for resumable downloads.\n    '
    MIN_ETAG_LEN = 5
    RETRYABLE_EXCEPTIONS = (
     httplib.HTTPException, IOError, socket.error,
     socket.gaierror)

    def __init__(self, tracker_file_name=None, num_retries=None):
        """
        Constructor. Instantiate once for each downloaded file.

        :type tracker_file_name: string
        :param tracker_file_name: optional file name to save tracking info
            about this download. If supplied and the current process fails
            the download, it can be retried in a new process. If called
            with an existing file containing an unexpired timestamp,
            we'll resume the transfer for this file; else we'll start a
            new resumable download.

        :type num_retries: int
        :param num_retries: the number of times we'll re-try a resumable
            download making no progress. (Count resets every time we get
            progress, so download can span many more than this number of
            retries.)
        """
        self.tracker_file_name = tracker_file_name
        self.num_retries = num_retries
        self.etag_value_for_current_download = None
        if tracker_file_name:
            self._load_tracker_file_etag()
        self.download_start_point = None

    def _load_tracker_file_etag(self):
        f = None
        try:
            try:
                f = open(self.tracker_file_name, 'r')
                self.etag_value_for_current_download = f.readline().rstrip('\n')
                if len(self.etag_value_for_current_download) < self.MIN_ETAG_LEN:
                    print("Couldn't read etag in tracker file (%s). Restarting download from scratch." % self.tracker_file_name)
            except IOError as e:
                if e.errno != errno.ENOENT:
                    print("Couldn't read URI tracker file (%s): %s. Restarting download from scratch." % (
                     self.tracker_file_name, e.strerror))

        finally:
            if f:
                f.close()

    def _save_tracker_info(self, key):
        self.etag_value_for_current_download = key.etag.strip('"\'')
        if not self.tracker_file_name:
            return
        f = None
        try:
            try:
                f = open(self.tracker_file_name, 'w')
                f.write('%s\n' % self.etag_value_for_current_download)
            except IOError as e:
                raise ResumableDownloadException("Couldn't write tracker file (%s): %s.\nThis can happenif you're using an incorrectly configured download tool\n(e.g., gsutil configured to save tracker files to an unwritable directory)" % (
                 self.tracker_file_name, e.strerror), ResumableTransferDisposition.ABORT)

        finally:
            if f:
                f.close()

    def _remove_tracker_file(self):
        if self.tracker_file_name:
            if os.path.exists(self.tracker_file_name):
                os.unlink(self.tracker_file_name)

    def _attempt_resumable_download(self, key, fp, headers, cb, num_cb, torrent, version_id, hash_algs):
        """
        Attempts a resumable download.

        Raises ResumableDownloadException if any problems occur.
        """
        cur_file_size = get_cur_file_size(fp, position_to_eof=True)
        if cur_file_size and self.etag_value_for_current_download and self.etag_value_for_current_download == key.etag.strip('"\''):
            if cur_file_size > key.size:
                raise ResumableDownloadException('%s is larger (%d) than %s (%d).\nDeleting tracker file, so if you re-try this download it will start from scratch' % (
                 fp.name, cur_file_size, str(storage_uri_for_key(key)),
                 key.size), ResumableTransferDisposition.ABORT)
            elif cur_file_size == key.size:
                if key.bucket.connection.debug >= 1:
                    print('Download complete.')
                return
            if key.bucket.connection.debug >= 1:
                print('Resuming download.')
            headers = headers.copy()
            headers['Range'] = 'bytes=%d-%d' % (cur_file_size, key.size - 1)
            cb = ByteTranslatingCallbackHandler(cb, cur_file_size).call
            self.download_start_point = cur_file_size
        else:
            if key.bucket.connection.debug >= 1:
                print('Starting new resumable download.')
            self._save_tracker_info(key)
            self.download_start_point = 0
            fp.truncate(0)
        if isinstance(key, GSKey):
            key.get_file(fp, headers, cb, num_cb, torrent, version_id, override_num_retries=0, hash_algs=hash_algs)
        else:
            key.get_file(fp, headers, cb, num_cb, torrent, version_id, override_num_retries=0)
        fp.flush()

    def get_file(self, key, fp, headers, cb=None, num_cb=10, torrent=False, version_id=None, hash_algs=None):
        """
        Retrieves a file from a Key
        :type key: :class:`boto.s3.key.Key` or subclass
        :param key: The Key object from which upload is to be downloaded
        
        :type fp: file
        :param fp: File pointer into which data should be downloaded
        
        :type headers: string
        :param: headers to send when retrieving the files
        
        :type cb: function
        :param cb: (optional) a callback function that will be called to report
             progress on the download.  The callback should accept two integer
             parameters, the first representing the number of bytes that have
             been successfully transmitted from the storage service and
             the second representing the total number of bytes that need
             to be transmitted.
        
        :type num_cb: int
        :param num_cb: (optional) If a callback is specified with the cb
             parameter this parameter determines the granularity of the callback
             by defining the maximum number of times the callback will be
             called during the file transfer.
             
        :type torrent: bool
        :param torrent: Flag for whether to get a torrent for the file

        :type version_id: string
        :param version_id: The version ID (optional)

        :type hash_algs: dictionary
        :param hash_algs: (optional) Dictionary of hash algorithms and
            corresponding hashing class that implements update() and digest().
            Defaults to {'md5': hashlib/md5.md5}.

        Raises ResumableDownloadException if a problem occurs during
            the transfer.
        """
        debug = key.bucket.connection.debug
        if not headers:
            headers = {}
        if self.num_retries is None:
            self.num_retries = config.getint('Boto', 'num_retries', 6)
        progress_less_iterations = 0
        while True:
            had_file_bytes_before_attempt = get_cur_file_size(fp)
            try:
                self._attempt_resumable_download(key, fp, headers, cb, num_cb, torrent, version_id, hash_algs)
                self._remove_tracker_file()
                if debug >= 1:
                    print('Resumable download complete.')
                return
            except self.RETRYABLE_EXCEPTIONS as e:
                if debug >= 1:
                    print('Caught exception (%s)' % e.__repr__())
                if isinstance(e, IOError):
                    if e.errno == errno.EPIPE:
                        if isinstance(key, GSKey):
                            key.get_file(fp, headers, cb, num_cb, torrent, version_id, override_num_retries=0, hash_algs=hash_algs)
                        else:
                            key.get_file(fp, headers, cb, num_cb, torrent, version_id, override_num_retries=0)
            except ResumableDownloadException as e:
                if e.disposition == ResumableTransferDisposition.ABORT_CUR_PROCESS:
                    if debug >= 1:
                        print('Caught non-retryable ResumableDownloadException (%s)' % e.message)
                    raise
                else:
                    if e.disposition == ResumableTransferDisposition.ABORT:
                        if debug >= 1:
                            print('Caught non-retryable ResumableDownloadException (%s); aborting and removing tracker file' % e.message)
                        self._remove_tracker_file()
                        raise
                    elif debug >= 1:
                        print('Caught ResumableDownloadException (%s) - will retry' % e.message)

            if get_cur_file_size(fp) > had_file_bytes_before_attempt:
                progress_less_iterations = 0
            else:
                progress_less_iterations += 1
            if progress_less_iterations > self.num_retries:
                raise ResumableDownloadException('Too many resumable download attempts failed without progress. You might try this download again later', ResumableTransferDisposition.ABORT_CUR_PROCESS)
            try:
                key.close()
            except httplib.IncompleteRead:
                pass

            sleep_time_secs = 2 ** progress_less_iterations
            if debug >= 1:
                print('Got retryable failure (%d progress-less in a row).\nSleeping %d seconds before re-trying' % (
                 progress_less_iterations, sleep_time_secs))
            time.sleep(sleep_time_secs)