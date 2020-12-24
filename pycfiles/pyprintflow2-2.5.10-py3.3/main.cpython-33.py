# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/main.py
# Compiled at: 2014-04-03 03:33:52
# Size of source mod 2**32: 3124 bytes
"""
Created on Sep 7, 2013

@author: "Colin Manning"
"""
import sys, getopt, logging, logging.handlers, signal
from printflow2.FileSystemMonitor import FileSystemMonitor
from printflow2.NooshMonitor import NooshMonitor
__printflow2_version__ = '0.4.4'
fileSystemMonitor = None
nooshMonitor = None
webService = None

def close_down(signal, frame):
    global fileSystemMonitor
    global nooshMonitor
    print('printflow2 is shutting down')
    if fileSystemMonitor is not None:
        fileSystemMonitor.stop()
    if nooshMonitor is not None:
        nooshMonitor.stop()
    sys.exit(0)
    return


def main():
    global __printflow2_version__
    global fileSystemMonitor
    global nooshMonitor
    help_text = 'usage:\n printflow2 -c <configfile> -w <workgroup> -l <logfile>\n printflow2 -v'
    workgroupId = None
    configFile = None
    logFile = None
    logger = None
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'vhc:w:l:', ['version', 'configfile=', 'workgroup=', 'logfile='])
    except getopt.GetoptError:
        print(help_text)
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print(help_text)
            sys.exit()
        elif opt in ('-v', '--version'):
            print(('printflow2 version:', __printflow2_version__))
            sys.exit()
        elif opt in ('-c', '--configfile'):
            configFile = arg
        elif opt in ('-w', '--workgroup'):
            workgroupId = arg
        elif opt in ('-l', '--logfile'):
            logFile = arg
            continue

    if configFile is not None and workgroupId is not None:
        requests_log = logging.getLogger('requests')
        requests_log.setLevel(logging.WARNING)
        logging.basicConfig(level=logging.INFO)
        logger = logging.getLogger('printflow2')
        handler = logging.handlers.TimedRotatingFileHandler(logFile, when='midnight')
        handler.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        print(('running printflow2 version:', __printflow2_version__))
        fileSystemMonitor = FileSystemMonitor(configFile, workgroupId)
        nooshMonitor = NooshMonitor(configFile, workgroupId, fileSystemMonitor)
        if fileSystemMonitor.is_ready():
            fileSystemMonitor.scanFolders()
            fileSystemMonitor.start()
        if nooshMonitor.is_ready():
            nooshMonitor.start()
        close_down()
    else:
        print('Invalid call to printflow2')
        print(help_text)
    return


signal.signal(signal.SIGINT, close_down)
signal.signal(signal.SIGTERM, close_down)
if __name__ == '__main__':
    main()
# global webService ## Warning: Unused global