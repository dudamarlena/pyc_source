# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /marrow/mailer/transport/maildir.py
# Compiled at: 2019-09-13 21:23:39
# Size of source mod 2**32: 1614 bytes
import mailbox
__all__ = [
 'MaildirTransport']
log = __import__('logging').getLogger(__name__)

class MaildirTransport(object):
    __doc__ = 'A modern UNIX maildir on-disk file delivery transport.'
    __slots__ = ('ephemeral', 'box', 'directory', 'folder', 'create', 'separator')

    def __init__(self, config):
        self.box = None
        self.directory = config.get('directory', None)
        self.folder = config.get('folder', None)
        self.create = config.get('create', False)
        self.separator = config.get('separator', '!')
        if not self.directory:
            raise ValueError('You must specify the path to a maildir tree to write messages to.')

    def startup(self):
        self.box = mailbox.Maildir(self.directory)
        if self.folder:
            try:
                folder = self.box.get_folder(self.folder)
            except mailbox.NoSuchMailboxError:
                if not self.create:
                    raise
                folder = self.box.add_folder(self.folder)

            self.box = folder
        self.box.colon = self.separator

    def deliver(self, message):
        self.box.add(mailbox.MaildirMessage(str(message)))

    def shutdown(self):
        self.box = None