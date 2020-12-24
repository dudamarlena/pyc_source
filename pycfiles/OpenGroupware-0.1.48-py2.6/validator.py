# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/logic/foundation/services/validator.py
# Compiled at: 2012-10-12 07:02:39
from time import time
from sqlalchemy import *
from sqlalchemy.orm import *
from coils.core import *

class ManagerService(Service):
    __service__ = 'coils.validator'
    __TimeOut__ = 60

    def __init__(self):
        Service.__init__(self)

    def prepare(self):
        Service.prepare(self)
        self._enabled = True
        self._ctx = AdministrativeContext({}, broker=self._broker)
        self._last_time = time()

    def work(self):
        if self._enabled:
            if time() - self._last_time > 360:
                self.log.debug('Running validator processes')
                self._scan_running_processes()
                self._start_queued_processes()
                self._last_time = time()

    def _generate_checksum(self):
        db = self._ctx.db_session()
        blobs = db.query(DocumentVersion).filter(DocumentVersion.checksum is None).limit(10)
        for blob in blobs:
            pass

        return

    def _verify_checksum(self, handle):
        pass