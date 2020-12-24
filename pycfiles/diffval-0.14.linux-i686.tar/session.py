# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.6/dist-packages/diffval/session.py
# Compiled at: 2010-09-30 21:09:41
import os, signal, subprocess, sys, tempfile

class session:

    def __init__(self, executable, log=None, env=None):
        self._code = None
        self._stdout = []
        self._stderr = []
        self._log = log
        if self._log:
            self._log.openElement('session', {'program': executable})
        signal.signal(signal.SIGTERM, self.cancel)
        try:
            windows = sys.platform == 'win32' or sys.platform == 'cygwin'
            self._session = subprocess.Popen(['env', executable] + self._args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=windows, close_fds=not windows, env=env)
            input = None
            if self._input:
                input = ('\n').join(self._input)
            try:
                (out, err) = self._session.communicate(input=input)
                if out:
                    self._stdout += out.split('\n')
                if err:
                    self._stderr += err.split('\n')
            except ValueError:
                pass
            except OSError:
                self._stderr.append('<< Session terminated unexpectedly >>')

        except KeyboardInterrupt:
            self.cancel()

        if self._log:
            self._log.closeElement('session')
        return

    def slurp(self):
        try:
            while self._session:
                (out, err) = self._session.communicate()
                if out:
                    self._stdout += out.split('\n')
                if err:
                    self._stderr += err.split('\n')

        except ValueError:
            pass
        except OSError:
            self._stderr.append('<< Session terminated unexpectedly >>')

        if self._session.returncode is not None:
            self._code = self._session.returncode
        return

    def cancel(self):
        try:
            if self._session:
                os.kill(self._session.pid, signal.SIGTERM)
        except:
            pass

    def output(self):
        self.slurp()
        out = self._stdout
        self._stdout = []
        return out

    def errors(self):
        self.slurp()
        err = self._stderr
        self._stderr = []
        return err