# uncompyle6 version 3.7.4
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/net6mon/logger.py
# Compiled at: 2006-05-17 03:21:59
import logging, sys

class Logger(object):
    """ 
        Cette classe est utilisée pour logger des messages           
    """
    __module__ = __name__

    def __init__(self, name='', logfile='', loglevel=logging.DEBUG, logtostd=0):
        self.logger = logging.getLogger(name)
        self.loglevel = loglevel
        self.logger.setLevel(loglevel)
        if logfile != '':
            self.add_file_handler(logfile)
        if logtostd:
            self.add_stream_handler(loglevel)

    def add_stream_handler(self):
        """
            Ajoute un '''stream handler''', c'est a dire configure le logger
            pour envoyer vers la sortie ''stdout''
        """
        self.streamHandler = logging.StreamHandler()
        self.streamHandler.setLevel(self.loglevel)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.streamHandler.setFormatter(formatter)
        self.logger.addHandler(self.streamHandler)

    def add_file_handler(self, logfile):
        """
                Ajoute un '''file handler''', c'est a dire configure le logger pour envoyer 
                vers un fichier 
        
                @type logfile: string
                @param logfile: nom de fichier du fichier de log

        """
        self.fileHandler = logging.FileHandler(logfile)
        self.fileHandler.setLevel(self.loglevel)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.fileHandler.setFormatter(formatter)
        self.logger.addHandler(self.fileHandler)


def logger_factory(logtype='syslog', logfile=None, level='DEBUG', logid='net6mon', stdlog=None):
    try:
        import logging, logging.handlers
        logger = logging.getLogger(logid)
        logtype = logtype.lower()
        if logtype == 'file':
            hdlr = logging.FileHandler(logfile)
        elif logtype in ['winlog', 'eventlog', 'nteventlog']:
            hdlr = logging.handlers.NTEventLogHandler(logid, logtype='Application')
        elif logtype in ['syslog', 'unix']:
            hdlr = logging.handlers.SysLogHandler('/dev/log')
        elif logtype in ['stderr']:
            hdlr = logging.StreamHandler(sys.stderr)
        else:
            raise ValueError
        format = 'Net6mon[%(module)s] %(levelname)s: %(message)s'
        if logtype == 'file':
            format = '%(asctime)s ' + format
        datefmt = ''
        level = level.upper()
        if level in ['DEBUG', 'ALL']:
            logger.setLevel(logging.DEBUG)
            datefmt = '%X'
        elif level == 'INFO':
            logger.setLevel(logging.INFO)
        elif level == 'ERROR':
            logger.setLevel(logging.ERROR)
        elif level == 'CRITICAL':
            logger.setLevel(logging.CRITICAL)
        else:
            logger.setLevel(logging.WARNING)
        formatter = logging.Formatter(format, datefmt)
        hdlr.setFormatter(formatter)
        logger.addHandler(hdlr)
        if stdlog == 'yes':
            stdhdlr = logging.StreamHandler(sys.stderr)
            logger.addHandler(stdhdlr)
    except (ImportError, ValueError):

        class DummyLogger:
            """The world's most fake logger."""
            __module__ = __name__

            def __noop(self, *args, **kwargs):
                pass

            debug = info = warning = error = critical = log = exception = __noop
            warn = fatal = __noop
            getEffectiveLevel = lambda self: 0
            isEnabledFor = lambda self, level: 0

        logger = DummyLogger()

    return logger