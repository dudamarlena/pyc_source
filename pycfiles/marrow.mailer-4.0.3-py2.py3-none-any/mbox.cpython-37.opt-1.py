# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /marrow/mailer/transport/mbox.py
# Compiled at: 2019-09-13 21:23:39
# Size of source mod 2**32: 1015 bytes
import mailbox
__all__ = [
 'MailboxTransport']
log = __import__('logging').getLogger(__name__)

class MailboxTransport(object):
    __doc__ = 'A classic UNIX mailbox on-disk file delivery transport.\n    \n    Due to the file locking inherent in this format, using a background\n    delivery mechanism (such as a Futures thread pool) makes no sense.\n    '
    __slots__ = ('ephemeral', 'box', 'filename')

    def __init__(self, config):
        self.box = None
        self.filename = config.get('file', None)
        if not self.filename:
            raise ValueError('You must specify an mbox file name to write messages to.')

    def startup(self):
        self.box = mailbox.mbox(self.filename)

    def deliver(self, message):
        self.box.lock()
        self.box.add(mailbox.mboxMessage(str(message)))
        self.box.unlock()

    def shutdown(self):
        if self.box is None:
            return
        self.box.close()
        self.box = None