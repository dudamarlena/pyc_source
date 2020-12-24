# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/minideblib/GPGSigVerifier.py
# Compiled at: 2007-11-06 15:08:00
import os, string, commands

class GPGSigVerifierException(Exception):

    def __init__(self, value):
        self._value = value

    def __str__(self):
        return `(self._value)`


class GPGSigVerificationFailure(Exception):

    def __init__(self, value, output):
        self._value = value
        self._output = output

    def __str__(self):
        return `(self._value)`

    def getOutput(self):
        return self._output


class GPGSigVerifier:

    def __init__(self, keyrings, gpgv=None):
        self._keyrings = keyrings
        if gpgv is None:
            gpgv = '/usr/bin/gpgv'
        if not os.access(gpgv, os.X_OK):
            raise GPGSigVerifierException('Couldn\'t execute "%s"' % (gpgv,))
        self._gpgv = gpgv
        return

    def verify(self, filename, sigfilename=None):
        args = []
        for keyring in self._keyrings:
            args.append('--keyring')
            args.append(keyring)

        if sigfilename:
            args.append(sigfilename)
        args = [
         self._gpgv] + args + [filename]
        (status, output) = commands.getstatusoutput(string.join(args))
        if not (status is None or os.WIFEXITED(status) and os.WEXITSTATUS(status) == 0):
            if os.WIFEXITED(status):
                msg = 'gpgv exited with error code %d' % (os.WEXITSTATUS(status),)
            elif os.WIFSTOPPED(status):
                msg = 'gpgv stopped unexpectedly with signal %d' % (os.WSTOPSIG(status),)
            elif os.WIFSIGNALED(status):
                msg = 'gpgv died with signal %d' % (os.WTERMSIG(status),)
            raise GPGSigVerificationFailure(msg, output)
        return output.splitlines()