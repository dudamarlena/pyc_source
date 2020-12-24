# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/benchexec/filehierarchylimit.py
# Compiled at: 2020-05-07 05:52:35
from __future__ import absolute_import, division, print_function, unicode_literals
import logging, os, threading
from benchexec import container
from benchexec import util
_CHECK_INTERVAL_SECONDS = 60
_DURATION_WARNING_THRESHOLD = 1

class FileHierarchyLimitThread(threading.Thread):
    """
    Thread that periodically checks whether a given file hierarchy exceeds some limits.
    After this happens, the process is terminated.
    """

    def __init__(self, path, files_count_limit, files_size_limit, pid_to_kill, callbackFn=lambda reason: None):
        super(FileHierarchyLimitThread, self).__init__()
        self.name = b'FileHierarchyLimitThread-' + self.name
        assert os.path.isdir(path)
        self._path = path
        self._files_count_limit = files_count_limit
        self._files_size_limit = files_size_limit
        self._pid_to_kill = pid_to_kill
        self._callback = callbackFn
        self._finished = threading.Event()

    def _check_limit(self, files_count, files_size):
        if self._files_count_limit and files_count > self._files_count_limit:
            reason = b'files-count'
        elif self._files_size_limit and files_size > self._files_size_limit:
            reason = b'files-size'
        else:
            return
        self._callback(reason)
        logging.debug(b'Killing process %d due to %s limit (%d files with %d bytes).', self._pid_to_kill, reason, files_count, files_size)
        util.kill_process(self._pid_to_kill)
        return reason

    def run(self):
        while not self._finished.is_set():
            self._finished.wait(_CHECK_INTERVAL_SECONDS)
            files_count = 0
            files_size = 0
            start_time = util.read_monotonic_time()
            for current_dir, dirs, files in os.walk(self._path):
                for file in files:
                    abs_file = os.path.join(current_dir, file)
                    file = b'/' + os.path.relpath(file, self._path)
                    if not container.is_container_system_config_file(file) and os.path.isfile(abs_file) and not os.path.islink(abs_file):
                        files_count += 1
                        if self._files_size_limit:
                            try:
                                files_size += os.path.getsize(abs_file)
                            except OSError:
                                pass

            if self._check_limit(files_count, files_size):
                return
            duration = util.read_monotonic_time() - start_time
            logging.debug(b'FileHierarchyLimitThread for process %d: files count: %d, files size: %d, scan duration %fs', self._pid_to_kill, files_count, files_size, duration)
            if duration > _DURATION_WARNING_THRESHOLD:
                logging.warning(b'Scanning file hierarchy for enforcement of limits took %ds.', duration)

    def cancel(self):
        self._finished.set()