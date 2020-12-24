# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sparked/tap.py
# Compiled at: 2011-05-10 16:24:41
"""
Twisted Application Persistence package for the startup of the twisted sparked plugin.
"""
import signal, tempfile, warnings
from zope.interface import implements
from twisted.python import usage
from twisted.python import log
from twisted.python.filepath import FilePath
from twisted.python.logfile import LogFile
from sparked import launcher, application

class Options(usage.Options):

    def parseOptions(self, o):
        (sparkedOpts, self.appName, appOpts) = launcher.splitOptions(o)
        self.opts = launcher.Options()
        self.opts.parseOptions(sparkedOpts)
        if not self.appName:
            self.opts.opt_help()
        (self.module, self.appName) = launcher.loadModule(self.appName)
        if hasattr(self.module, 'Options'):
            self.appOpts = self.module.Options()
        else:
            self.appOpts = application.Options()
        self.appOpts.parseOptions(appOpts)


class RotatableFileLogObserver(object):
    """A log observer that uses a log file and reopens it on SIGUSR1."""
    implements(log.ILogObserver)

    def __init__(self, logfilename):
        if logfilename is None:
            logFile = sys.stdout
        else:
            logFile = LogFile.fromFullPath(logfilename, rotateLength=None)
            if not signal.getsignal(signal.SIGUSR1):

                def signalHandler(signal, frame):
                    from twisted.internet import reactor
                    reactor.callFromThread(logFile.reopen)

                signal.signal(signal.SIGUSR1, signalHandler)
        self.observer = log.FileLogObserver(logFile)
        return

    def __call__(self, eventDict):
        self.observer.emit(eventDict)


def makeService(config):
    from twisted.internet import reactor
    from twisted.internet.base import BlockingResolver
    reactor.installResolver(BlockingResolver())
    try:
        import dbus.mainloop.glib
        dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
    except ImportError:
        warnings.warn('Failed to import the dbus module, some functionality might not work.')

    if not hasattr(config.module, 'Application'):
        raise usage.UsageError('Invalid application module: ' + config.appName)
    s = config.module.Application(config.appName, config.opts, config.appOpts)
    s.quitFlag = launcher.QuitFlag(s.path('temp').child('quitflag'))
    s.setName(config.appName)
    for kind in ['temp', 'db']:
        path = s.path(kind)
        if not path.exists():
            path.createDirectory()

    logFile = s.path('logfile')
    if not logFile.parent().exists():
        logFile.parent().createDirectory()
    filename = s.path('logfile').path
    if config.opts['no-logrotate']:
        observer = RotatableFileLogObserver(filename)
    else:
        logFile = LogFile.fromFullPath(filename, maxRotatedFiles=9)
        observer = log.FileLogObserver(logFile).emit
    log.addObserver(observer)
    return s