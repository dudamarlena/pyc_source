# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\mad\log.py
# Compiled at: 2016-04-11 03:21:40
# Size of source mod 2**32: 1505 bytes


class Event:
    __doc__ = '\n    An entry in the log\n    '

    def __init__(self, time, context, message):
        self.time = time
        self.context = context
        self.message = message

    def __repr__(self):
        return '%4d %-20s %-40s' % (self.time, self.context, self.message)


class Log:
    __doc__ = '\n    The history of message logged recorded during a simulation\n    '

    def record(self, time, context, message):
        pass


class FileLog(Log):
    __doc__ = '\n    Dump the event into the given stream using the given format\n    '

    def __init__(self, output, format):
        super().__init__()
        self.format = format
        self.output = output

    def record(self, time, context, message):
        self.output.write(self.format % (time, context, message))