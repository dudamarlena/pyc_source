# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pf3/fsmonitor.py
# Compiled at: 2014-08-15 07:47:45
# Size of source mod 2**32: 3013 bytes
__author__ = 'colin'
import sys, getopt, logging.handlers, signal
from pf3.fs.FileSystemMonitor import FileSystemMonitor
__pf3_version__ = '3.0.2'
fileSystemMonitor = None
webService = None
framework = None

def close_down(signal, frame):
    global fileSystemMonitor
    print('printflow2 is shutting down')
    if fileSystemMonitor is not None:
        fileSystemMonitor.stop()
    sys.exit(0)
    return


def main():
    global __pf3_version__
    global fileSystemMonitor
    global framework
    help_text = 'usage:\n pf3 -c <configfile> -w <workgroup> -l <logfile>\n pf3 -v'
    workgroupConfigFile = None
    configFile = None
    workgroupRunFile = None
    logFile = None
    logger = None
    framework = None
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'vhc:w:r:l:', ['version', 'configfile=', 'workgroup=', 'runfile=', 'logfile='])
    except getopt.GetoptError:
        print(help_text)
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print(help_text)
            sys.exit()
        elif opt in ('-v', '--version'):
            print(('PrintFlow 3 File System Monitor Version:', __pf3_version__))
            sys.exit()
        elif opt in ('-c', '--configfile'):
            configFile = arg
        elif opt in ('-w', '--workgroup'):
            workgroupConfigFile = arg
        elif opt in ('-r', '--runfile'):
            workgroupRunFile = arg
        elif opt in ('-l', '--logfile'):
            assert isinstance(arg, object)
            logFile = arg
            continue

    if configFile is not None and workgroupConfigFile and workgroupRunFile is not None:
        requests_log = logging.getLogger('requests')
        requests_log.setLevel(logging.WARNING)
        logging.basicConfig(level=logging.INFO)
        logger = logging.getLogger('printflow2')
        handler = logging.handlers.TimedRotatingFileHandler(logFile, when='midnight')
        handler.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        print(('Running PrintFlow 3 File System Monitor Version:', __pf3_version__))
        fileSystemMonitor = FileSystemMonitor(workgroupConfigFile, workgroupRunFile)
        if fileSystemMonitor.is_ready():
            fileSystemMonitor.scanFolders()
            fileSystemMonitor.start()
        close_down()
    else:
        print('Invalid call to PrintFlow 3 File System Monitor')
        print(help_text)
    return


signal.signal(signal.SIGINT, close_down)
signal.signal(signal.SIGTERM, close_down)
if __name__ == '__main__':
    main()
# global webService ## Warning: Unused global