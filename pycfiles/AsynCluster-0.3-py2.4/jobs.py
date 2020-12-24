# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/asyncluster/master/jobs.py
# Compiled at: 2007-11-29 12:08:54
"""
Running jobs via the Master's UNIX socket PB interface.
"""
import os.path, textwrap
from zope.interface import implements
from twisted.internet import defer, reactor
from twisted.spread import pb
from asynqueue import workers, TaskQueue

class JobClient(object):
    """
    I connect to the master TCP server via a UNIX socket and provide an
    interface for running jobs defined by a Python code file.

    @ivar root: A remote reference to the root object provided by the server.
    
    """
    __module__ = __name__
    root = None

    def __init__(self, socket, codePath=None, codeString=None):
        if not os.path.exists(socket):
            raise RuntimeError("No UNIX socket available at '%s'" % socket)
        self.socket = socket
        if codeString is None and codePath is None:
            raise RuntimeError('You must specify either a file or a string containing ' + 'Python source for the job.')
        if codeString is None:
            if not os.path.exists(codePath):
                raise RuntimeError("No code file available at '%s'" % codePath)
            fh = open(codePath)
            codeString = fh.read()
            fh.close()
        self.jobCode = textwrap.dedent(codeString)
        return

    def startup(self):
        """
        Makes the UNIX socket connection, storing a remote reference to the
        server's control root object if the connection is successful. Returns a
        deferred that fires C{True} if so, and I am thus ready to accept
        commands as a result, or C{False} otherwise.
        """

        def gotAnswer(answer):
            if pb.IUnjellyable.providedBy(answer):
                self.root = answer
                d = self.root.callRemote('newJob', self.jobCode)
                d.addCallback(gotID)
                return d
            return False

        def gotID(jobID):
            if jobID:
                self.jobID = jobID
                return True
            return False

        def gotFinalStatus(success):
            if not success:
                self.client.disconnect()
            return success

        factory = pb.PBClientFactory()
        self.connector = reactor.connectUNIX(self.socket, factory)
        d = factory.getRootObject()
        d.addBoth(gotAnswer)
        d.addCallback(gotFinalStatus)
        return d

    def shutdown(self):
        """
        Disconnects from the master TCP server, returning a deferred that fires
        when the disconnection is complete. Before the TCP disconnection
        occurs, any jobs that are running are allowed to finish and any active
        session is ended.
        """

        def doneCanceling(null):
            self.root = None
            self.connector.disconnect()
            return

        jobID = getattr(self, 'jobID', None)
        if jobID is None:
            d = defer.succeed(None)
        else:
            d = self.root.callRemote('cancelJob', jobID)
            d.addCallback(doneCanceling)
        return d

    def update(self, cmd, *args, **kw):
        """
        Arranges for a job update to be done on all present and future nodes
        before they next run a job. Note that the update will apply to any jobs
        currently queued up, too!

        The update is done via the specified I{cmd} with any args and keywords
        supplied.
        """
        if hasattr(self, 'jobID'):
            return self.root.callRemote('updateJob', self.jobID, cmd, *args, **kw)
        raise Exception('No job registered!')

    def registerClasses(self, *args):
        """
        Instructs the controller to register the classes specified by the
        argument(s) as self-unjellyable and allowable past PB security, and to
        arrange an update to have its nodes do the same.

        The classes are specified by their string representations::
        
            <package(s).module.class>

        Use judiciously!
        """
        return self.root.callRemote('registerClasses', *args)

    def run(self, cmd, *args, **kw):
        """
        Does a job run on the next available node with any args supplied.
        """
        if hasattr(self, 'jobID'):
            return self.root.callRemote('runJob', self.jobID, cmd, *args, **kw)
        raise Exception('No job registered!')


class JobWorker(workers.RemoteCallWorker):
    """
    Instantiate me with a started instance of L{JobClient} and I'll use its
    root reference and job runner.
    """
    __module__ = __name__
    N = 30

    def __init__(self, jobClient):
        if not hasattr(jobClient, 'jobID'):
            raise Exception('Supplied job client not started!')
        self.client = jobClient
        self.iQualified = [jobClient.jobID]
        self.startup(jobClient.root)

    def runNow(self, null, task):
        (cmd, args, kw) = task.callTuple
        d = self.client.run(cmd, *args, **kw)
        job = (task, d)
        self.jobs.append(job)
        d.addCallback(self.doneTrying, job)
        d.addErrback(self.oops)

    def stop(self):
        d = workers.RemoteCallWorker.stop(self)
        d.addCallback(lambda _: self.client.shutdown())
        return d