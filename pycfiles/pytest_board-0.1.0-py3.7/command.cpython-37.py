# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/pytest_board/command.py
# Compiled at: 2018-12-29 09:38:09
# Size of source mod 2**32: 1088 bytes
from .watcher import Watcher
from .server import WebServer
from .testrunner import TestRunner
import pytest, os, sys
from multiprocessing import Process
import gevent

def main():
    web_server = WebServer()
    test_runner = TestRunner(before_run=(web_server.notify_test_executing),
      on_completed=(web_server.notify_test_completed))
    web_server.set_test_runner(test_runner.notify)
    watcher = Watcher(directories=[
     os.getcwd()],
      on_changed=(test_runner.notify))
    workers = [
     Process(target=(web_server.run)),
     Process(target=(test_runner.run)),
     Process(target=(watcher.run))]
    try:
        test_runner.notify('first')
        for worker in workers:
            worker.start()

        for worker in workers:
            worker.join()

    except:
        print('killing child process...')
        for worker in workers:
            worker.terminate()

        for worker in workers:
            worker.join()


if __name__ == '__main__':
    main()