# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /marrow/mailer/transport/sendmail.py
# Compiled at: 2019-09-13 21:23:39
# Size of source mod 2**32: 1225 bytes
from subprocess import Popen, PIPE
from marrow.mailer.exc import MessageFailedException
__all__ = [
 'SendmailTransport']
log = __import__('logging').getLogger(__name__)

class SendmailTransport(object):
    __slots__ = ('ephemeral', 'executable')

    def __init__(self, config):
        self.executable = config.get('path', '/usr/sbin/sendmail')

    def startup(self):
        pass

    def deliver(self, message):
        args = [
         self.executable, '-t', '-i']
        if message.sendmail_f:
            log.info('sendmail_f : {}'.format(message.sendmail_f))
            args.extend(['-f', message.sendmail_f])
        proc = Popen(args, shell=False, stdin=PIPE)
        proc.communicate(bytes(message))
        proc.stdin.close()
        if proc.wait() != 0:
            raise MessageFailedException('Status code %d.' % (proc.returncode,))

    def shutdown(self):
        pass