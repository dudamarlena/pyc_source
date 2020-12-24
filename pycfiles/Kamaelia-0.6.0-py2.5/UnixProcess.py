# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/Kamaelia/File/UnixProcess.py
# Compiled at: 2008-10-19 12:19:52
"""
===========
UnixProcess
===========

Launch another unix process and communicate with it via its standard input and
output, by using the "inbox" and "outbox" of this component.

Example Usage
-------------

The purpose behind this component is to allow the following to occur::

    Pipeline(
      dataSource(),
      UnixProcess("command", *args),
      dataSink(),
    ).run()

How to use it
-------------

More specificaly, the longer term interface of this component will be:

UnixProcess:

* inbox - data recieved here is sent to the program's stdin
* outbox - data sent here is from the program's stdout
* control - at some point we'll define a mechanism for describing
  control messages - these will largely map to SIG* messages
  though. We also need to signal how we close our writing pipe.
  This can happen using the normal producerFinished message.
* signal - this will be caused by things like SIGPIPE messages. What
  this will look like is yet to be defined. (Let's see what works
  first.

Python and platform compatibility
---------------------------------

This code is only really tested on Linux.

Initially this will be python 2.4 only, but it would be nice to support
older versions of python (eg 2.2.2 - for Nokia mobiles).

For the moment I'm going to send STDERR to dev null, however things won't
stay that way.
"""
import Axon
from Kamaelia.Chassis.Pipeline import Pipeline
from Kamaelia.Util.Console import ConsoleEchoer
import Kamaelia.IPC as _ki
from Axon.Ipc import shutdown
from Kamaelia.IPC import newReader, newWriter
from Kamaelia.IPC import removeReader, removeWriter
from Kamaelia.Internet.Selector import Selector
import subprocess, fcntl, os, sys

def Chargen():
    import time
    ts = t = time.time()
    while time.time() - t < 1:
        yield 'hello\n'


def run_command(command, datasource):
    x = subprocess.Popen(command, shell=True, bufsize=1, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, close_fds=True)
    for d in datasource:
        x.stdin.write(d)

    x.stdin.close()
    print x.stdout.read()


class ChargenComponent(Axon.Component.component):

    def main(self):
        import time
        ts = t = time.time()
        b = 0
        while time.time() - t < 0.1:
            yield 1
            self.send('hello\n', 'outbox')
            b += len('hello\n')
            if time.time() - ts > 3:
                break

        self.send(Axon.Ipc.producerFinished(), 'signal')
        print 'total sent', b


def makeNonBlocking(fd):
    fl = fcntl.fcntl(fd, fcntl.F_GETFL)
    fcntl.fcntl(fd, fcntl.F_SETFL, fl | os.O_NDELAY)


class UnixProcess(Axon.Component.component):
    Inboxes = {'inbox': 'Strings containing data to send to the sub process', 
       'control': 'We receive shutdown messages here', 
       'stdinready': "We're notified here when we can write to the sub-process", 
       'stderrready': "We're notified here when we can read errors from the sub-process", 
       'stdoutready': "We're notified here when we can read from the sub-process"}
    Outboxes = {'signal': 'not used', 
       'outbox': 'data from the sub command is output here', 
       'selector': 'We send messages to the selector here, requesting it tell us when file handles can be read from/written to', 
       'selectorsignal': 'To send control messages to the selector'}

    def __init__(self, command):
        super(UnixProcess, self).__init__()
        self.command = command

    def openSubprocess(self):
        p = subprocess.Popen(self.command, shell=True, bufsize=32768, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, close_fds=True)
        makeNonBlocking(p.stdin.fileno())
        makeNonBlocking(p.stdout.fileno())
        makeNonBlocking(p.stderr.fileno())
        return p

    def main(self):
        writeBuffer = []
        shutdownMessage = False
        (selectorService, selectorShutdownService, S) = Selector.getSelectorServices(self.tracker)
        if S:
            S.activate()
        yield 1
        yield 1
        yield 1
        self.link((self, 'selector'), selectorService)
        x = self.openSubprocess()
        self.send(newWriter(self, ((self, 'stdinready'), x.stdin)), 'selector')
        self.send(newReader(self, ((self, 'stderrready'), x.stderr)), 'selector')
        self.send(newReader(self, ((self, 'stdoutready'), x.stdout)), 'selector')
        stdin_ready = 1
        stdout_ready = 1
        stderr_ready = 1
        exit_status = x.poll()
        success = 0
        while exit_status is None:
            exit_status = x.poll()
            if not self.anyReady() and not stdin_ready + stdout_ready + stderr_ready:
                self.pause()
                yield 1
                continue
            while self.dataReady('inbox'):
                d = self.recv('inbox')
                writeBuffer.append(d)

            if self.dataReady('stdinready'):
                self.recv('stdinready')
                stdin_ready = 1
            if self.dataReady('stdoutready'):
                self.recv('stdoutready')
                stdout_ready = 1
            if self.dataReady('stderrready'):
                self.recv('stderrready')
                stderr_ready = 1
            if len(writeBuffer) > 10000:
                writeBuffer = writeBuffer[-10000:]
            if stdin_ready:
                while len(writeBuffer) > 0:
                    d = writeBuffer[0]
                    try:
                        count = os.write(x.stdin.fileno(), d)
                        writeBuffer.pop(0)
                        success += 1
                    except OSError, e:
                        success -= 1
                        stdin_ready = 0
                        writeBuffer = writeBuffer[len(writeBuffer) / 2:]
                        self.send(newWriter(self, ((self, 'stdinready'), x.stdin)), 'selector')
                        break
                    except:
                        print sys.exc_info()[0]
                        break

            if stdout_ready:
                try:
                    Y = os.read(x.stdout.fileno(), 2048)
                    if len(Y) > 0:
                        self.send(Y, 'outbox')
                except OSError, e:
                    stdout_ready = 0
                    self.send(newReader(self, ((self, 'stdoutready'), x.stdout)), 'selector')
                except:
                    print sys.exc_info()[0]

            if stderr_ready:
                try:
                    Y = os.read(x.stderr.fileno(), 2048)
                except OSError, e:
                    stderr_ready = 0
                    self.send(newReader(self, ((self, 'stderrready'), x.stderr)), 'selector')
                except:
                    print sys.exc_info()[0]

            if self.dataReady('control'):
                shutdownMessage = self.recv('control')
                self.send(removeWriter(self, x.stdin), 'selector')
                yield 1
                x.stdin.close()
            yield 1

        while self.dataReady('stdoutready'):
            self.recv('stdoutready')
            try:
                Y = os.read(x.stdout.fileno(), 10)
                while Y:
                    self.send(Y, 'outbox')
                    Y = os.read(x.stdout.fileno(), 10)

            except OSError, e:
                continue
            except:
                break

            yield 1

        self.send(removeReader(self, x.stderr), 'selector')
        self.send(removeReader(self, x.stdout), 'selector')
        self.send(removeWriter(self, x.stdin), 'selector')
        if not shutdownMessage:
            self.send(Axon.Ipc.producerFinished(), 'signal')
        else:
            self.send(shutdownMessage, 'signal')
        return


__kamaelia_components__ = (
 UnixProcess,)

def Pipethrough(*args):
    print 'DEPRECATION WARNING: Pipethrough is deprecated, please use Kamaelia.File.UnixProcess.UnixProcess instead'
    return UnixProcess(*args)


if __name__ == '__main__':
    Pipeline(ChargenComponent(), UnixProcess('wc'), ConsoleEchoer(forwarder=True)).run()