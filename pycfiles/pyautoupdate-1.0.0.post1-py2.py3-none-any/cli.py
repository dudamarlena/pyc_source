# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.8-intel/egg/pyautotest/cli.py
# Compiled at: 2013-06-04 14:35:00
import argparse, logging, os, signal, time
from watchdog.observers import Observer
from pyautotest.observers import Notifier, ChangeHandler
logging.basicConfig(format='%(asctime)s (%(name)s) [%(levelname)s]: %(message)s', datefmt='%m-%d-%Y %H:%M:%S', level=logging.INFO)
logger = logging.getLogger('pyautotest')

def main():
    parser = argparse.ArgumentParser(description='Continuously run unit tests when changes detected')
    parser.add_argument('-l', '--log-level', metavar='L', default='INFO', dest='loglevel', action='store', help='set logger level')
    args = parser.parse_args()
    logger.setLevel(getattr(logging, args.loglevel.upper(), None))
    while True:
        event_handler = ChangeHandler()
        event_handler.run_tests()
        observer = Observer()
        observer.schedule(event_handler, os.getcwd(), recursive=True)
        signal.signal(signal.SIGCHLD, signal.SIG_IGN)
        observer.start()
        try:
            while True:
                time.sleep(1)

        except KeyboardInterrupt:
            observer.stop()

        observer.join()

    return


if __name__ == '__main__':
    main()