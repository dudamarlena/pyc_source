# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\mad\simulation\requests.py
# Compiled at: 2016-04-27 13:32:24
# Size of source mod 2**32: 2777 bytes


class Request:
    QUERY = 0
    TRIGGER = 1
    TRANSMISSION_DELAY = 1
    PENDING = 0
    OK = 1
    ERROR = 2
    ACCEPTED = 3
    REJECTED = 4

    def __init__(self, sender, kind, operation, priority, on_accept=lambda : None, on_reject=lambda : None, on_success=lambda : None, on_error=lambda : None):
        assert sender, 'Invalid sender (found %s)' % str(sender)
        self.identifier = sender.next_request_id()
        self.sender = sender
        self.kind = kind
        self.operation = operation
        self.priority = priority
        self.on_accept = on_accept
        self.on_reject = on_reject
        self.on_success = on_success
        self.on_error = on_error
        self.status = self.PENDING
        self._response_time = None
        self._emission_time = None

    @property
    def response_time(self):
        assert self.status == self.OK, "Only successful requests expose a 'response time'"
        return self._response_time

    @property
    def is_pending(self):
        return self.status == self.PENDING

    def send_to(self, service):
        self._emission_time = self.sender.schedule.time_now
        service.schedule.after(self.TRANSMISSION_DELAY, lambda : service.process(self))

    def accept(self):
        self.sender.schedule.after(self.TRANSMISSION_DELAY, self.on_accept)

    def reject(self):
        self.sender.schedule.after(self.TRANSMISSION_DELAY, self.on_reject)

    def reply_success(self):
        if self.is_pending:
            self.status = self.OK
            assert self._response_time is None, 'Response time are updated multiple times!'
            self._response_time = self.sender.schedule.time_now - self._emission_time
            self.sender.schedule.after(self.TRANSMISSION_DELAY, self.on_success)

    def reply_error(self):
        if self.is_pending:
            self.status = self.ERROR
            self.sender.schedule.after(self.TRANSMISSION_DELAY, self.on_error)

    def discard(self):
        if self.is_pending:
            self.status = self.ERROR