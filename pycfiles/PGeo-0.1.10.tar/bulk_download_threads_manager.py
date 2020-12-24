# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/kalimaha/Development/git-repositories/Geobricks/pgeo/pgeo/thread/bulk_download_threads_manager.py
# Compiled at: 2014-09-02 09:47:46
from ftplib import FTP
from threading import Thread
from threading import Lock
import Queue, os, time
from threading import Timer
from pgeo.utils import log
from pgeo.utils.filesystem import create_filesystem
log = log.logger('bulk_download_threads_manager.py')
progress_map = {}
exit_flags = {}

class BulkDownloadThread(Thread):
    bulk_download_object = None
    total_files = 0
    downloaded_files = 0

    def __init__(self, thread_name, queue, queue_lock, tab_id, target_folder):
        Thread.__init__(self)
        self.thread_name = thread_name
        self.queue = queue
        self.queue_lock = queue_lock
        self.tab_id = tab_id
        self.target_folder = target_folder
        progress_map[self.tab_id] = {}
        progress_map[self.tab_id]['status'] = 'WAITING'

    def run(self):
        while not exit_flags[self.tab_id]:
            self.queue_lock.acquire()
            if not self.queue.empty():
                self.bulk_download_object = self.queue.get()
                self.total_files = len(self.bulk_download_object['file_list'])
                progress_map[self.tab_id]['total_files'] = self.total_files
                progress_map[self.tab_id]['downloaded_files'] = 0
                progress_map[self.tab_id]['status'] = 'START'
                progress_map[self.tab_id]['progress'] = 0
                self.queue_lock.release()
                ftp = FTP(self.bulk_download_object['ftp_base_url'])
                try:
                    ftp.login()
                except Exception as e:
                    progress_map[self.tab_id]['status'] = 'ERROR'
                    exit_flags[self.tab_id] = 1
                    continue

                ftp.cwd(self.bulk_download_object['ftp_data_dir'])
                remote_files = ftp.nlst()
                for file_name in self.bulk_download_object['file_list']:
                    if file_name in remote_files:
                        ftp.sendcmd('TYPE i')
                        file_obj = file_name
                        local_file = os.path.join(self.target_folder, file_obj)
                        progress_map[self.tab_id]['status'] = 'ONGOING'
                        if not os.path.isfile(local_file):
                            with open(local_file, 'w') as (f):

                                def callback(chunk):
                                    f.write(chunk)

                                ftp.retrbinary('RETR %s' % file_obj, callback)
                                self.downloaded_files += 1
                                progress_map[self.tab_id]['status'] = 'COMPLETE'
                                progress_map[self.tab_id]['progress'] = self.percent_done()
                                log.info(progress_map[self.tab_id]['progress'])
                        else:
                            self.downloaded_files += 1
                            progress_map[self.tab_id]['status'] = 'COMPLETE'
                            progress_map[self.tab_id]['progress'] = self.percent_done()
                            log.info(progress_map[self.tab_id]['progress'])

                ftp.quit()
            else:
                self.queue_lock.release()
            time.sleep(1)

    def percent_done(self):
        return float(('{0:.2f}').format(float(self.downloaded_files) / float(self.total_files) * 100))


class BulkDownloadManager(Thread):

    def __init__(self, source, filesystem_structure, bulk_download_objects, tab_id):
        Thread.__init__(self)
        self.bulk_download_objects = bulk_download_objects
        self.tab_id = tab_id
        self.source = source
        self.filesystem_structure = filesystem_structure
        self.target_folder = create_filesystem(self.source, self.filesystem_structure)

    def run(self):
        t = Timer(1, self.start_manager)
        t.start()
        return self.target_folder

    def start_manager(self):
        exit_flags[self.tab_id] = 0
        log.info('START | Bulk Download Manager')
        thread_list = [
         'Alpha']
        queue_lock = Lock()
        work_queue = Queue.Queue(len(self.bulk_download_objects))
        threads = []
        for thread_name in thread_list:
            thread = BulkDownloadThread(thread_name, work_queue, queue_lock, self.tab_id, self.target_folder)
            thread.start()
            threads.append(thread)

        queue_lock.acquire()
        for obj in self.bulk_download_objects:
            work_queue.put(obj)

        queue_lock.release()
        while not work_queue.empty():
            pass

        exit_flags[self.tab_id] = 1
        for t in threads:
            t.join()

        log.info('END   | Bulk Download Manager')


class BulkDownloadObject:
    ftp_base_url = None
    ftp_data_dir = None
    file_list = []

    def __init__(self, ftp_base_url, ftp_data_dir, file_list):
        self.ftp_base_url = ftp_base_url
        self.ftp_data_dir = ftp_data_dir
        self.file_list = file_list

    def __str__(self):
        s = ''
        s += str(self.ftp_base_url) + '\n'
        s += str(self.ftp_data_dir) + '\n'
        s += str(self.file_list)
        return s