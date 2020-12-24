# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/chibiegg/.pyenv/versions/cloudbackup/lib/python3.4/site-packages/cloudbackup/drivers/s3/writer.py
# Compiled at: 2014-12-28 14:20:28
# Size of source mod 2**32: 4179 bytes
from _io import BytesIO
import logging
from queue import Empty
from queue import Queue
import threading, time, traceback
from boto.glacier.writer import _Partitioner
logger = logging.getLogger('cloudbackup.drivers.s3')
_END_SENTINEL = None
logger.setLevel(logging.DEBUG)

class PartUploadThread(threading.Thread):

    def __init__(self, mp, worker_queue, result_queue, retry_count=5):
        super(PartUploadThread, self).__init__()
        self.mp = mp
        self.worker_queue = worker_queue
        self.result_queue = result_queue
        self.retry_count = retry_count
        self.daemon = True

    def run(self):
        while True:
            part_data = self.worker_queue.get()
            if part_data == _END_SENTINEL:
                logger.debug('Exit upload thread : %s', self)
                return
            for trycount in range(self.retry_count):
                logger.debug('Start upload part %d', part_data['number'])
                try:
                    part_data['mp'].upload_part_from_file(part_data['data'], part_data['number'])
                except Exception as e:
                    logger.warn(traceback.format_exc())
                    logger.warn('Retry to upload part %d', part_data['number'])
                else:
                    logger.debug('Finished upload part %d', part_data['number'])
                break
            else:
                self.result_queue.put(e)
                return

            self.result_queue.put(None)


class MultiPartUploader(object):
    counter = 0

    def __init__(self, bucket, keyname, part_size=104857600, num_threads=10):
        self.bucket = bucket
        self._part_size = part_size
        self._num_threads = num_threads
        self.part_count = 0
        self.partitioner = _Partitioner(part_size, self._upload_part)
        self.worker_queue = Queue(2)
        self.result_queue = Queue()
        self.mp = self.bucket.initiate_multipart_upload(keyname)
        logger.debug('Multipart Uplaod ID : %s', self.mp.id)
        self._start_upload_threads()

    def _start_upload_threads(self):
        self._threads = []
        logger.debug('Starting threads.')
        for _ in range(self._num_threads):
            thread = PartUploadThread(self.mp, self.worker_queue, self.result_queue)
            thread.start()
            self._threads.append(thread)

    def _shutdown_threads(self):
        self.worker_queue.clear()
        for i in range(self._num_threads):
            self.worker_queue.put(_END_SENTINEL)

        for t in self._threads:
            t.join()

    def _upload_part(self, data):
        self.part_count += 1
        start = self._part_size * self.part_count
        logger.debug('Adding work items to queue (%d).', self.part_count)
        self.worker_queue.put({'mp': self.mp, 
         'number': self.part_count, 
         'range': (
                   start, start + len(data) - 1), 
         'data': BytesIO(data)})

    def _poll(self, block=False):
        try:
            result = self.result_queue.get(block=block)
        except Empty:
            return

        if isinstance(result, Exception):
            self._shutdown_threads()
            raise result

    def _wait_for_upload_threads(self):
        logger.debug('Waiting for finish uploading all parts.')
        while 1:
            running = False
            for t in self._threads:
                if t.is_alive():
                    running = True
                    break

            self._poll(block=False)
            time.sleep(1)
            if not running:
                return

    def write(self, data):
        self._poll()
        self.partitioner.write(data)

    def close(self):
        self.partitioner.flush()
        for i in range(self._num_threads):
            self.worker_queue.put(_END_SENTINEL)

        self._wait_for_upload_threads()
        self.mp.complete_upload()