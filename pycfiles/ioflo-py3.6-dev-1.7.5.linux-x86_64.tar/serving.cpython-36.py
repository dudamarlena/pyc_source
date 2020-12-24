# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib64/python3.6/site-packages/ioflo/base/serving.py
# Compiled at: 2017-12-17 08:35:26
# Size of source mod 2**32: 9199 bytes
"""serving.py IP socket server module

"""
import sys, os, time, datetime, io
from collections import deque
from ..aid.sixing import *
from ..aid.odicting import odict
from .globaling import *
from ..aid import aiding
from ..aio.udp import PeerUdp
from . import tasking
from ..aid.consoling import getConsole
console = getConsole()

class Server(tasking.Tasker):
    __doc__ = 'Server Task Patron Registry Class for IP comms\n\n       Usage:\n    '

    def __init__(self, sha=('', 54321), dha=('localhost', 54321), prefix='./', **kw):
        """Initialize instance.

           iherited instance attributes
           .name = unique name for machine
           .store = data store

           .period = desired time in seconds between runs must be non negative, zero means asap
           .stamp = time when tasker last ran sucessfully not interrupted by exception
           .status = operational status of tasker
           .desire = desired control asked by this or other taskers
           .done = tasker completion state True or False
           .runner = generator to run tasker

           instance attributes
           .sha = (host, port) serving listen socket address
           .dha = destination address (host, port)
           .server = non blocking udp socket server object
           .prefix = log directory path prefix
           .path = log directory path
           .logPath = log file path
           .logFile = log file

        """
        (super(Server, self).__init__)(**kw)
        self.sha = sha
        self.server = PeerUdp(ha=sha)
        self.dha = dha
        self.prefix = prefix
        self.path = ''
        self.logPath = ''
        self.logFile = None

    def reinit(self, sha=None, dha=None, prefix=None, **kw):
        """Re initializes certain attributes for reuse

        """
        (super(Server, self).reinit)(**kw)
        if sha is not None:
            self.sha = sha
            if not self.server:
                self.server = PeerUdp(ha=sha, path='')
            self.server.ha = sha
        if dha is not None:
            self.dha = dha
        if prefix is not None:
            self.prefix = prefix

    def createPaths(self, prefix='./'):
        """creates log directory path
           creates physical directories on disk
        """
        dt = datetime.datetime.now()
        self.path = '{0}_{1}_{2:04d}{3:02d}{4:02d}_{5:02d}{6:02d}{7:02d}'.format(prefix, self.name, dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second)
        try:
            self.path = os.path.abspath(self.path)
            if not os.path.exists(self.path):
                os.makedirs(self.path)
        except OSError as ex:
            console.terse("Error: creating server log directory '{0}'\n".format(ex))
            return False

        console.concise("     Created Server {0} Log Directory = '{1}'\n".format(self.name, self.path))
        self.logPath = os.path.join(self.path, '{0}.txt'.format('log'))
        self.logPath = os.path.abspath(self.logPath)
        return True

    def reopen(self):
        """Closes if open then opens    """
        if not self.createPaths(prefix=(self.prefix)):
            return False
        else:
            if not self.reopenLog():
                return False
            if not self.server.reopen():
                return False
            return True

    def close(self):
        """      """
        self.server.close()
        self.closeLog()

    def reopenLog(self):
        """closes if open then reopens
        """
        self.closeLog()
        try:
            self.logFile = open(self.logPath, 'a+')
        except IOError as ex:
            console.terse("Error: creating server log file '{0}\n".format(ex))
            self.logFile = None
            return False

        console.concise('     Created Server Log file {0}\n'.format(self.logPath))
        return True

    def closeLog(self):
        """ close self.file if open except stdout
        """
        if self.logFile:
            if not self.logFile.closed:
                self.logFile.close()
                self.logFile = None

    def flush(self):
        """      """
        if self.logFile:
            if not self.logFile.closed:
                self.logFile.flush()
                os.fsync(self.logFile.fileno())

    def log(self, msg):
        """Called by runner  """
        stamp = self.store.stamp
        try:
            self.logFile.write('%0.4f\t%s\n' % (float(stamp), msg))
        except TypeError as ex:
            console.terse('{0}\n'.format(ex))
        except ValueError as ex:
            console.terse('{0}\n'.format(ex))

    def makeRunner(self):
        """generator factory function to create generator to run this monitor
        """
        console.profuse('     Making Server Task Runner {0}\n'.format(self.name))
        self.status = STOPPED
        self.desire = STOP
        self.done = True
        try:
            while True:
                control = yield self.status
                console.profuse('\n     Iterate Server {0} with control = {1} status = {2}\n'.format(self.name, ControlNames.get(control, 'Unknown'), StatusNames.get(self.status, 'Unknown')))
                if control == RUN:
                    if self.status == STARTED or self.status == RUNNING:
                        console.profuse('     Running Server {0} ...\n'.format(self.name))
                        input, sa = self.server.receive()
                        if sa:
                            shost, sport = sa
                        output = b''
                        result = self.server.send(output, self.dha)
                        self.status = RUNNING
                    else:
                        console.profuse('     Need to Start Server {0}\n'.format(self.name))
                        self.desire = START
                else:
                    if control == READY:
                        console.profuse('     Readying Server {0} ...\n'.format(self.name))
                        self.status = READIED
                        self.desire = START
                    else:
                        if control == START:
                            console.terse('     Starting Server {0} ...\n'.format(self.name))
                            if self.reopen():
                                self.desire = RUN
                                self.status = STARTED
                                self.done = False
                            else:
                                self.desire = STOP
                                self.status = STOPPED
                                self.done = True
                        else:
                            if control == STOP:
                                if self.status == RUNNING or self.status == STARTED:
                                    console.terse('     Stopping Server {0} ...\n'.format(self.name))
                                    self.close()
                                    self.desire = STOP
                                    self.status = STOPPED
                                    self.done = True
                                else:
                                    console.terse('     Server {0} not started or running.\n'.format(self.name))
                            else:
                                if control == ABORT:
                                    console.profuse('     Aborting Server {0} ...\n'.format(self.name))
                                    self.close()
                                    self.desire = ABORT
                                    self.status = ABORTED
                                else:
                                    self.desire = ABORT
                                    self.status = ABORTED
                                    console.profuse('     Aborting Server {0}, bad control = {1}\n'.format(self.name, CommandNames[control]))
                                    self.close()
                                    break
                    self.stamp = self.store.stamp

        finally:
            console.profuse('     Exception causing Abort Server {0} ...\n'.format(self.name))
            self.desire = ABORT
            self.status = ABORTED
            self.close()