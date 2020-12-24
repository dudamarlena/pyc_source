# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\supervisor\medusa\logger.py
# Compiled at: 2015-07-18 10:13:56
import supervisor.medusa.asynchat_25 as asynchat, socket, time, os, stat

class file_logger:

    def __init__(self, file, flush=1, mode='a'):
        if isinstance(file, str):
            if file == '-':
                import sys
                self.file = sys.stdout
            else:
                self.file = open(file, mode)
        else:
            self.file = file
        self.do_flush = flush

    def __repr__(self):
        return '<file logger: %s>' % self.file

    def write(self, data):
        self.file.write(data)
        self.maybe_flush()

    def writeline(self, line):
        self.file.writeline(line)
        self.maybe_flush()

    def writelines(self, lines):
        self.file.writelines(lines)
        self.maybe_flush()

    def maybe_flush(self):
        if self.do_flush:
            self.file.flush()

    def flush(self):
        self.file.flush()

    def softspace(self, *args):
        pass

    def log(self, message):
        if message[(-1)] not in ('\r', '\n'):
            self.write(message + '\n')
        else:
            self.write(message)


class rotating_file_logger(file_logger):

    def __init__(self, file, freq=None, maxsize=None, flush=1, mode='a'):
        file_logger.__init__(self, file, flush, mode)
        self.filename = file
        self.mode = mode
        self.freq = freq
        self.maxsize = maxsize
        self.rotate_when = self.next_backup(self.freq)

    def __repr__(self):
        return '<rotating-file logger: %s>' % self.file

    def next_backup(self, freq):
        yr, mo, day, hr, min, sec, wd, jday, dst = time.localtime(time.time())
        if freq == 'daily':
            return time.mktime((yr, mo, day + 1, 0, 0, 0, 0, 0, -1))
        else:
            if freq == 'weekly':
                return time.mktime((yr, mo, day - wd + 7, 0, 0, 0, 0, 0, -1))
            else:
                if freq == 'monthly':
                    return time.mktime((yr, mo + 1, 1, 0, 0, 0, 0, 0, -1))
                return

            return

    def maybe_flush(self):
        self.maybe_rotate()
        if self.do_flush:
            self.file.flush()

    def maybe_rotate(self):
        if self.freq and time.time() > self.rotate_when:
            self.rotate()
            self.rotate_when = self.next_backup(self.freq)
        elif self.maxsize:
            try:
                if os.stat(self.filename)[stat.ST_SIZE] > self.maxsize:
                    self.rotate()
            except os.error:
                self.rotate()

    def rotate(self):
        yr, mo, day, hr, min, sec, wd, jday, dst = time.localtime(time.time())
        try:
            self.file.close()
            newname = '%s.ends%04d%02d%02d' % (self.filename, yr, mo, day)
            try:
                open(newname, 'r').close()
                newname += '-%02d%02d%02d' % (hr, min, sec)
            except:
                pass

            os.rename(self.filename, newname)
            self.file = open(self.filename, self.mode)
        except:
            pass


class socket_logger(asynchat.async_chat):

    def __init__(self, address):
        asynchat.async_chat.__init__(self)
        if isinstance(address, str):
            self.create_socket(socket.AF_UNIX, socket.SOCK_STREAM)
        else:
            self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect(address)
        self.address = address

    def __repr__(self):
        return '<socket logger: address=%s>' % self.address

    def log(self, message):
        if message[-2:] != '\r\n':
            self.socket.push(message + '\r\n')
        else:
            self.socket.push(message)


class multi_logger:

    def __init__(self, loggers):
        self.loggers = loggers

    def __repr__(self):
        return '<multi logger: %s>' % repr(self.loggers)

    def log(self, message):
        for logger in self.loggers:
            logger.log(message)


class resolving_logger:
    """Feed (ip, message) combinations into this logger to get a
    resolved hostname in front of the message.  The message will not
    be logged until the PTR request finishes (or fails)."""

    def __init__(self, resolver, logger):
        self.resolver = resolver
        self.logger = logger

    class logger_thunk:

        def __init__(self, message, logger):
            self.message = message
            self.logger = logger

        def __call__(self, host, ttl, answer):
            if not answer:
                answer = host
            self.logger.log('%s:%s' % (answer, self.message))

    def log(self, ip, message):
        self.resolver.resolve_ptr(ip, self.logger_thunk(message, self.logger))


class unresolving_logger:
    """Just in case you don't want to resolve"""

    def __init__(self, logger):
        self.logger = logger

    def log(self, ip, message):
        self.logger.log('%s:%s' % (ip, message))


def strip_eol(line):
    while line and line[(-1)] in '\r\n':
        line = line[:-1]

    return line


class tail_logger:
    """Keep track of the last <size> log messages"""

    def __init__(self, logger, size=500):
        self.size = size
        self.logger = logger
        self.messages = []

    def log(self, message):
        self.messages.append(strip_eol(message))
        if len(self.messages) > self.size:
            del self.messages[0]
        self.logger.log(message)