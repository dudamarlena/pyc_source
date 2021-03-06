# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /ampoule/main.py
# Compiled at: 2019-09-15 01:25:44
# Size of source mod 2**32: 10379 bytes
import os, sys, imp, itertools
from zope.interface import implementer
from twisted import logger
from twisted.internet import reactor, protocol, defer, error
from twisted.python import reflect
from twisted.protocols import amp
from twisted.python import runtime
from twisted.python.compat import set
from ampoule import iampoule
log = logger.Logger()
gen = itertools.count()
if runtime.platform.isWindows():
    IS_WINDOWS = True
    TO_CHILD = 0
    FROM_CHILD = 1
else:
    IS_WINDOWS = False
    TO_CHILD = 3
    FROM_CHILD = 4

class AMPConnector(protocol.ProcessProtocol):
    __doc__ = '\n    A L{ProcessProtocol} subclass that can understand and speak AMP.\n\n    @ivar amp: the children AMP process\n    @type amp: L{amp.AMP}\n\n    @ivar finished: a deferred triggered when the process dies.\n    @type finished: L{defer.Deferred}\n\n    @ivar name: Unique name for the connector, much like a pid.\n    @type name: int\n    '

    def __init__(self, proto, name=None):
        """
        @param proto: An instance or subclass of L{amp.AMP}
        @type proto: L{amp.AMP}

        @param name: optional name of the subprocess.
        @type name: int
        """
        self.finished = defer.Deferred()
        self.amp = proto
        self.name = name
        if name is None:
            self.name = next(gen)

    def signalProcess(self, signalID):
        """
        Send the signal signalID to the child process

        @param signalID: The signal ID that you want to send to the
                        corresponding child
        @type signalID: C{str} or C{int}
        """
        return self.transport.signalProcess(signalID)

    def connectionMade(self):
        log.info('Subprocess {n} started.', n=(self.name))
        self.amp.makeConnection(self)

    disconnecting = False

    def write(self, data):
        if IS_WINDOWS:
            self.transport.write(data)
        else:
            self.transport.writeToChild(TO_CHILD, data)

    def loseConnection(self):
        self.transport.closeChildFD(TO_CHILD)
        self.transport.closeChildFD(FROM_CHILD)
        self.transport.loseConnection()

    def getPeer(self):
        return ('subprocess', )

    def getHost(self):
        return ('no host', )

    def childDataReceived(self, childFD, data):
        if childFD == FROM_CHILD:
            self.amp.dataReceived(data)
            return
        self.errReceived(data)

    def errReceived(self, data):
        for line in data.strip().splitlines():
            log.error('FROM {n}: {l}', n=(self.name), l=line)

    def processEnded(self, status):
        log.info('Process: {n} ended', n=(self.name))
        self.amp.connectionLost(status)
        if status.check(error.ProcessDone):
            self.finished.callback('')
            return
        self.finished.errback(status)


BOOTSTRAP = "import sys\n\ndef main(reactor, ampChildPath):\n    from twisted.application import reactors\n    reactors.installReactor(reactor)\n\n    from twisted import logger\n    observer = logger.textFileLogObserver(sys.stderr)\n    logLevelPredicate = logger.LogLevelFilterPredicate(\n        defaultLogLevel=logger.LogLevel.info\n    )\n    filteringObserver = logger.FilteringLogObserver(\n        observer, [logLevelPredicate]\n    )\n    logger.globalLogBeginner.beginLoggingTo([filteringObserver])\n\n    from twisted.internet import reactor, stdio\n    from twisted.python import reflect, runtime\n\n    ampChild = reflect.namedAny(ampChildPath)\n    ampChildInstance = ampChild(*sys.argv[1:-2])\n    if runtime.platform.isWindows():\n        stdio.StandardIO(ampChildInstance)\n    else:\n        stdio.StandardIO(ampChildInstance, %s, %s)\n    enter = getattr(ampChildInstance, '__enter__', None)\n    if enter is not None:\n        enter()\n    try:\n        reactor.run()\n    except:\n        if enter is not None:\n            info = sys.exc_info()\n            if not ampChildInstance.__exit__(*info):\n                raise\n        else:\n            raise\n    else:\n        if enter is not None:\n            ampChildInstance.__exit__(None, None, None)\n\nmain(sys.argv[-2], sys.argv[-1])\n" % (TO_CHILD, FROM_CHILD)

@implementer(iampoule.IStarter)
class ProcessStarter(object):
    connectorFactory = AMPConnector

    def __init__(self, bootstrap=BOOTSTRAP, args=(), env={}, path=None, uid=None, gid=None, usePTY=0, packages=(), childReactor='select'):
        """
        @param bootstrap: Startup code for the child process
        @type  bootstrap: C{str}

        @param args: Arguments that should be supplied to every child
                     created.
        @type args: C{tuple} of C{str}

        @param env: Environment variables that should be present in the
                    child environment
        @type env: C{dict}

        @param path: Path in which to run the child
        @type path: C{str}

        @param uid: if defined, the uid used to run the new process.
        @type uid: C{int}

        @param gid: if defined, the gid used to run the new process.
        @type gid: C{int}

        @param usePTY: Should the child processes use PTY processes
        @type usePTY: 0 or 1

        @param packages: A tuple of packages that should be guaranteed
                         to be importable in the child processes
        @type packages: C{tuple} of C{str}

        @param childReactor: a string that sets the reactor for child
                             processes
        @type childReactor: C{str}
        """
        self.bootstrap = bootstrap
        self.args = args
        self.env = env
        self.path = path
        self.uid = uid
        self.gid = gid
        self.usePTY = usePTY
        self.packages = ('ampoule', ) + packages
        self.childReactor = childReactor

    def __repr__(self):
        """
        Represent the ProcessStarter with a string.
        """
        return 'ProcessStarter(bootstrap=%r,\n                                 args=%r,\n                                 env=%r,\n                                 path=%r,\n                                 uid=%r,\n                                 gid=%r,\n                                 usePTY=%r,\n                                 packages=%r,\n                                 childReactor=%r)' % (self.bootstrap,
         self.args,
         self.env,
         self.path,
         self.uid,
         self.gid,
         self.usePTY,
         self.packages,
         self.childReactor)

    def _checkRoundTrip(self, obj):
        """
        Make sure that an object will properly round-trip through 'qual' and
        'namedAny'.

        Raise a L{RuntimeError} if they aren't.
        """
        tripped = reflect.namedAny(reflect.qual(obj))
        if tripped is not obj:
            raise RuntimeError('importing %r is not the same as %r' % (
             reflect.qual(obj), obj))

    def startAMPProcess(self, ampChild, ampParent=None, ampChildArgs=()):
        """
        @param ampChild: a L{ampoule.child.AMPChild} subclass.
        @type ampChild: L{ampoule.child.AMPChild}

        @param ampParent: an L{amp.AMP} subclass that implements the parent
                          protocol for this process pool
        @type ampParent: L{amp.AMP}
        """
        self._checkRoundTrip(ampChild)
        fullPath = reflect.qual(ampChild)
        if ampParent is None:
            ampParent = amp.AMP
        prot = self.connectorFactory(ampParent())
        args = ampChildArgs + (self.childReactor, fullPath)
        return (self.startPythonProcess)(prot, *args)

    def startPythonProcess(self, prot, *args):
        """
        @param prot: a L{protocol.ProcessProtocol} subclass
        @type prot: L{protocol.ProcessProtocol}

        @param args: a tuple of arguments that will be added after the
                     ones in L{self.args} to start the child process.

        @return: a tuple of the child process and the deferred finished.
                 finished triggers when the subprocess dies for any reason.
        """
        spawnProcess(prot, (self.bootstrap), (self.args + args), env=(self.env), path=(self.path),
          uid=(self.uid),
          gid=(self.gid),
          usePTY=(self.usePTY),
          packages=(self.packages))
        return (
         prot.amp, prot.finished)


def spawnProcess(processProtocol, bootstrap, args=(), env={}, path=None, uid=None, gid=None, usePTY=0, packages=()):
    env = env.copy()
    pythonpath = []
    for pkg in packages:
        p = os.path.split(imp.find_module(pkg)[1])[0]
        if p.startswith(os.path.join(sys.prefix, 'lib')):
            pass
        else:
            pythonpath.append(p)

    pythonpath = list(set(pythonpath))
    pythonpath.extend(env.get('PYTHONPATH', '').split(os.pathsep))
    env['PYTHONPATH'] = os.pathsep.join(pythonpath)
    args = (sys.executable, '-c', bootstrap) + args
    if IS_WINDOWS:
        return reactor.spawnProcess(processProtocol, sys.executable, args, env, path, uid, gid, usePTY)
    else:
        return reactor.spawnProcess(processProtocol, (sys.executable), args, env,
          path, uid, gid, usePTY, childFDs={0:'w', 
         1:'r',  2:'r',  3:'w',  4:'r'})