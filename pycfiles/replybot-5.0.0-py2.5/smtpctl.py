# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/botlib/testing/smtpctl.py
# Compiled at: 2008-08-09 12:39:34
__metaclass__ = type
__all__ = [
 'Controller']
import os, sys, time, random, shutil, signal, socket, mailbox, datetime, tempfile
from email import message_from_file
from pkg_resources import resource_filename

class Controller:
    """Manage an SMTP server child process."""

    def __init__(self):
        self._tempdir = tempfile.mkdtemp()
        self._maildir = os.path.join(self._tempdir, 'mailbox')
        self._mailbox = mailbox.Maildir(self._maildir, message_from_file)
        self._pid = None
        self.port = random.randint(10000, 20000)
        return

    def _command(self, command):
        s = socket.socket()
        s.connect(('localhost', self.port))
        s.setblocking(0)
        s.send(command + '\r\n')
        s.close()

    def start(self):
        """Start the child process listening for SMTP."""
        self._pid = pid = os.fork()
        if pid == 0:
            os.execl(sys.executable, sys.executable, resource_filename('botlib.testing', 'smtpsrv.py'), '--host', 'localhost', '--port', str(self.port), '--mbox', self._maildir)
            os._exit(1)
        until = datetime.datetime.now() + datetime.timedelta(seconds=5)
        while datetime.datetime.now() < until:
            try:
                self._command('QUIT')
                return
            except socket.error:
                time.sleep(0.5)

        raise RuntimeError('no smtp listener')

    def stop(self):
        """Stop the child process."""
        os.kill(self._pid, signal.SIGTERM)
        os.waitpid(self._pid, 0)
        shutil.rmtree(self._tempdir, True)

    def reset(self):
        self._mailbox.clear()

    @property
    def messages(self):
        return [ message for message in self._mailbox ]