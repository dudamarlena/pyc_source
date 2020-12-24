# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/rbbz/errors.py
# Compiled at: 2014-07-11 22:40:04
from reviewboard.reviews.errors import PublishError

class InvalidBugsError(PublishError):

    def __init__(self):
        PublishError.__init__(self, 'Exactly one bug ID must be provided.')


class InvalidBugIdError(PublishError):

    def __init__(self, bug_id):
        PublishError.__init__(self, 'Invalid bug ID "%s".' % bug_id)


class ConfidentialBugError(PublishError):

    def __init__(self):
        PublishError.__init__(self, 'This bug is confidential; please attach the patch directly to the bug.')


class BugzillaError(Exception):

    def __init__(self, msg, fault_code=None):
        super(BugzillaError, self).__init__(msg)
        self.msg = msg
        self.fault_code = fault_code


class BugzillaUrlError(BugzillaError):

    def __init__(self):
        BugzillaError.__init__(self, 'No Bugzilla URL provided in rbbz configuration.')