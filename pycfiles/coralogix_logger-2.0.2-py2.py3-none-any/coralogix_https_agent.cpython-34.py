# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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