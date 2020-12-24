# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/beantop/arguments.py
# Compiled at: 2013-06-04 05:02:18
DEFAULT_HOST = 'localhost'
DEFAULT_PORT = 11300

class Arguments:

    def __init__(self, system, getopt):
        self._system = system
        self._getopt = getopt

    def process(self, argv):
        try:
            return self._process_arguments(argv)
        except self._getopt.GetoptError:
            self._exception_when_processing(argv)

    def _process_arguments(self, argv):
        opts, _ = self._getopt.getopt(argv, 'h:p:', [])
        host = DEFAULT_HOST
        port = DEFAULT_PORT
        for opt, arg in opts:
            if opt == '-h':
                host = arg
            if opt == '-p':
                port = arg

        return (
         host, port)

    def _exception_when_processing(self, argv):
        self._system.stdout.write(argv[0] + ' -h <host> -p <port>')
        self._system.exit(2)