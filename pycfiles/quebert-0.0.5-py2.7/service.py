# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/quebert/service.py
# Compiled at: 2009-08-21 14:12:20
from twisted.application import service
from twisted.python import log
try:
    import syslog

    class SyslogObserver:

        def __init__(self, prefix):
            self.prefix = prefix
            syslog.openlog(prefix, 0, syslog.LOG_LOCAL1)

        def emit(self, eventDict):
            edm = eventDict['message']
            if not edm:
                if eventDict['isError'] and eventDict.has_key('failure'):
                    text = eventDict['failure'].getTraceback()
                elif eventDict.has_key('format'):
                    text = eventDict['format'] % eventDict
                else:
                    return
            else:
                text = (' ').join(map(str, edm))
            lines = text.split('\n')
            while lines[-1:] == ['']:
                lines.pop()

            firstLine = 1
            for line in lines:
                if firstLine:
                    firstLine = 0
                else:
                    line = '\t%s' % line
                syslog.syslog(syslog.LOG_INFO, '[%s] %s' % (self.prefix, line))


    def startLogging(prefix='Twisted', setStdout=1):
        obs = SyslogObserver(prefix)
        log.startLoggingWithObserver(obs.emit, setStdout=setStdout)


except:
    syslog = None

def makeService(options):
    """
    Create the service for the application
    """
    return QuebertService(options)


def makeExecutorService(options):
    """
    Create the executor service
    """
    return QuExecutorService(options)


class QuebertService(service.Service):
    """
    I am the service responsible for starting up a Quebert Mediator
    instance with a command line given configuration file.
    """

    def __init__(self, options):
        self.configFunction = options['config']
        self.syslog_prefix = options['with_syslog_prefix']
        self.options = options
        self.closeFunction = None
        return

    def startService(self):
        """
        Before reactor.run() is called we setup the system.
        """
        service.Service.startService(self)
        try:
            if self.syslog_prefix and syslog:
                startLogging(self.syslog_prefix)
            log.msg('Calling user configuration function...')
            self.closeFunction = self.configFunction(self.options)
            log.msg('done')
        except:
            import traceback
            print traceback.format_exc()
            raise

    def stopService(self):
        if self.closeFunction:
            return self.closeFunction()


class QuExecutorService(service.Service):
    """
    I am the service responsible for starting up a Quebert Executor
    instance with a command line given configuration file.
    """

    def __init__(self, options):
        self.configFunction = options['function']
        self.options = options
        self.syslog_prefix = options['with_syslog_prefix']
        self.closeFunction = None
        return

    def startService(self):
        """
        Before reactor.run() is called we setup the system.
        """
        service.Service.startService(self)
        try:
            if self.syslog_prefix and syslog:
                startLogging(self.syslog_prefix)
            log.msg('Creating the executor...')
            self.closeFunction = self.configFunction(self.options)
            log.msg('done')
        except:
            import traceback
            print traceback.format_exc()
            raise

    def stopService(self):
        if self.closeFunction:
            return self.closeFunction()