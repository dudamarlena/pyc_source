# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/src/__main__.py
# Compiled at: 2016-01-15 21:40:03
import os, time, coloredlogs, logging, argparse
from watchdog.observers import Observer
from src.executor import Executor
from src.monitor import Monitor
log_level = logging.DEBUG
parser = argparse.ArgumentParser(description='Restarts process when any files / directory changes')
parser.add_argument('-d', '--debug', dest='debug', help='Debug mode')
parser.add_argument('-p', '--path', default=os.getcwd(), dest='path', help='Which directory to watch for changes')
parser.add_argument('-e', '--extension', default=['.go', '.toml'], dest='file_ext', nargs='*', help='Which file extensions to listen for')
parser.add_argument('-c', '--command', required=True, dest='command', help='Command to be executed')
args = parser.parse_args()
if __name__ == '__main__':
    coloredlogs.install(level=log_level, fmt='%(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    os.chdir(args.path)
    event_handler = Monitor(args.command, args.file_ext)
    observer = Observer()
    observer.schedule(event_handler, args.path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        event_handler.executor.kill()
        observer.stop()

    observer.join()
    logging.debug('Exiting...')