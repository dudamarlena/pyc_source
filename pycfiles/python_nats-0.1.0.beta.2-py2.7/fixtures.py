# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/test/fixtures.py
# Compiled at: 2014-08-31 04:18:26
import shutil, subprocess, tempfile, logging, time, hashlib, uuid
from OpenSSL import crypto

class NatsServerHelper(object):

    def __init__(self, base_directory, proc_name='nats-server'):
        self.base_directory = base_directory
        self.proc_name = proc_name
        self.daemon = None
        self.work_dir = None
        return

    def run(self, proc_args=None):
        log = logging.getLogger()
        directory = tempfile.mkdtemp(dir=self.base_directory, prefix='python-nats')
        log.debug('Created directory %s' % directory)
        daemon_args = [
         self.proc_name]
        if proc_args:
            daemon_args.extend(proc_args)
        self.daemon = subprocess.Popen(daemon_args)
        self.work_dir = directory
        log.debug('Started %d' % self.daemon.pid)
        log.debug('Params: %s' % daemon_args)
        time.sleep(2)

    def stop(self):
        log = logging.getLogger()
        dir, process = self.work_dir, self.daemon
        process.kill()
        time.sleep(2)
        log.debug('Killed nats pid:%d', process.pid)
        shutil.rmtree(dir)
        log.debug('Removed directory %s' % dir)