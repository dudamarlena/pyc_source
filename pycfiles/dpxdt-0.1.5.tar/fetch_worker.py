# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/danvk/github/dpxdt/dpxdt/client/fetch_worker.py
# Compiled at: 2014-07-24 14:53:43
"""Workers for driving screen captures, perceptual diffs, and related work."""
import Queue, base64, json, logging, shutil, socket, ssl, time, urllib, urllib2, gflags
FLAGS = gflags.FLAGS
import poster.encode, poster.streaminghttp
poster.streaminghttp.register_openers()
from dpxdt.client import workers
gflags.DEFINE_float('fetch_frequency', 1.0, 'Maximum number of fetches to make per second per thread.')
gflags.DEFINE_integer('fetch_threads', 1, 'Number of fetch threads to run')

class FetchItem(workers.WorkItem):
    """Work item that is handled by fetching a URL."""

    def __init__(self, url, post=None, timeout_seconds=30, result_path=None, username=None, password=None):
        """Initializer.

        Args:
            url: URL to fetch.
            post: Optional. Dictionary of post parameters to include in the
                request, with keys and values coerced to strings. If any
                values are open file handles, the post data will be formatted
                as multipart/form-data.
            timeout_seconds: Optional. How long until the fetch should timeout.
            result_path: When supplied, the output of the fetch should be
                streamed to a file on disk with the given path. Use this
                to prevent many fetches from causing memory problems.
            username: Optional. Username to use for the request, for
                HTTP basic authentication.
            password: Optional. Password to use for the request, for
                HTTP basic authentication.
        """
        workers.WorkItem.__init__(self)
        self.url = url
        self.post = post
        self.username = username
        self.password = password
        self.timeout_seconds = timeout_seconds
        self.result_path = result_path
        self.status_code = None
        self.data = None
        self.headers = None
        self._data_json = None
        return

    def _get_dict_for_repr(self):
        result = self.__dict__.copy()
        if result.get('password'):
            result['password'] = 'ELIDED'
        return result

    @property
    def json(self):
        """Returns de-JSONed data or None if it's a different content type."""
        if self._data_json:
            return self._data_json
        else:
            if not self.data or self.headers.gettype() != 'application/json':
                return None
            self._data_json = json.loads(self.data)
            return self._data_json


class FetchThread(workers.WorkerThread):
    """Worker thread for fetching URLs."""

    def handle_item(self, item):
        start_time = time.time()
        if item.post is not None:
            adjusted_data = {}
            use_form_data = False
            for key, value in item.post.iteritems():
                if value is None:
                    continue
                if isinstance(value, file):
                    use_form_data = True
                adjusted_data[key] = value

            if use_form_data:
                datagen, headers = poster.encode.multipart_encode(adjusted_data)
                request = urllib2.Request(item.url, datagen, headers)
            else:
                request = urllib2.Request(item.url, urllib.urlencode(adjusted_data))
        else:
            request = urllib2.Request(item.url)
        if item.username:
            credentials = base64.b64encode('%s:%s' % (item.username, item.password))
            request.add_header('Authorization', 'Basic %s' % credentials)
        try:
            try:
                conn = urllib2.urlopen(request, timeout=item.timeout_seconds)
            except urllib2.HTTPError as e:
                conn = e
            except (urllib2.URLError, ssl.SSLError) as e:
                item.status_code = 400
                return item

            try:
                try:
                    item.status_code = conn.getcode()
                    item.headers = conn.info()
                    if item.result_path:
                        with open(item.result_path, 'wb') as (result_file):
                            shutil.copyfileobj(conn, result_file)
                    else:
                        item.data = conn.read()
                except socket.timeout as e:
                    item.status_code = 400
                    return item

            finally:
                conn.close()

            return item
        finally:
            end_time = time.time()
            wait_duration = 1.0 / FLAGS.fetch_frequency - (end_time - start_time)
            if wait_duration > 0:
                logging.debug('Rate limiting URL fetch for %f seconds', wait_duration)
                time.sleep(wait_duration)

        return


def register(coordinator):
    """Registers this module as a worker with the given coordinator."""
    fetch_queue = Queue.Queue()
    coordinator.register(FetchItem, fetch_queue)
    for i in xrange(FLAGS.fetch_threads):
        coordinator.worker_threads.append(FetchThread(fetch_queue, coordinator.input_queue))