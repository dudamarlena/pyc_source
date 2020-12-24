# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\coralogix\coralogix_https_agent.py
# Compiled at: 2016-01-03 04:46:21
# Size of source mod 2**32: 490 bytes
from coralogix import CoralogixHTTPSHandler

class spider(object):

    def get_files(self):
        pass

    def weave(self):
        processes = list()
        for file in self.get_files():
            process = Process(target=self.spawn, args=(f,))
            processes.append(process)
            process.start()

    def spawn(self, filename):
        logger.info()
        tailer = Tailer(filename)
        tailor.watch()


if __name__ == '__main__':
    pass