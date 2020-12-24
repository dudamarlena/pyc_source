# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/Toolserver/select_trigger.py
# Compiled at: 2010-03-01 05:38:51
VERSION_STRING = '$Id: select_trigger.py 5 2004-02-05 13:07:15Z gb $'
import asyncore, asynchat, os, socket, string, thread
if os.name == 'posix':

    class trigger(asyncore.file_dispatcher):
        """Wake up a call to select() running in the main thread"""

        def __init__(self):
            (r, w) = os.pipe()
            self.trigger = w
            asyncore.file_dispatcher.__init__(self, r)
            self.lock = thread.allocate_lock()
            self.thunks = []

        def __repr__(self):
            return '<select-trigger (pipe) at %x>' % id(self)

        def readable(self):
            return 1

        def writable(self):
            return 0

        def handle_connect(self):
            pass

        def pull_trigger(self, thunk=None):
            if thunk:
                try:
                    self.lock.acquire()
                    self.thunks.append(thunk)
                finally:
                    self.lock.release()

            os.write(self.trigger, 'x')

        def handle_read(self):
            self.recv(8192)
            try:
                self.lock.acquire()
                for thunk in self.thunks:
                    try:
                        thunk()
                    except:
                        ((file, fun, line), t, v, tbinfo) = asyncore.compact_traceback()
                        print 'exception in trigger thunk: (%s:%s %s)' % (t, v, tbinfo)

                self.thunks = []
            finally:
                self.lock.release()


else:

    class trigger(asyncore.dispatcher):
        address = ('127.9.9.9', 19999)

        def __init__(self):
            a = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            w = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            w.setsockopt(socket.IPPROTO_TCP, 1, 1)
            host = '127.0.0.1'
            port = 19999
            while 1:
                try:
                    self.address = (
                     host, port)
                    a.bind(self.address)
                    break
                except:
                    if port <= 19950:
                        raise 'Bind Error', 'Cannot bind trigger!'
                    port = port - 1

            a.listen(1)
            w.setblocking(0)
            try:
                w.connect(self.address)
            except:
                pass

            (r, addr) = a.accept()
            a.close()
            w.setblocking(1)
            self.trigger = w
            asyncore.dispatcher.__init__(self, r)
            self.lock = thread.allocate_lock()
            self.thunks = []
            self._trigger_connected = 0

        def __repr__(self):
            return '<select-trigger (loopback) at %x>' % id(self)

        def readable(self):
            return 1

        def writable(self):
            return 0

        def handle_connect(self):
            pass

        def pull_trigger(self, thunk=None):
            if thunk:
                try:
                    self.lock.acquire()
                    self.thunks.append(thunk)
                finally:
                    self.lock.release()

            self.trigger.send('x')

        def handle_read(self):
            self.recv(8192)
            try:
                self.lock.acquire()
                for thunk in self.thunks:
                    try:
                        thunk()
                    except:
                        ((file, fun, line), t, v, tbinfo) = asyncore.compact_traceback()
                        print 'exception in trigger thunk: (%s:%s %s)' % (t, v, tbinfo)

                self.thunks = []
            finally:
                self.lock.release()


the_trigger = None

class trigger_file:
    """A 'triggered' file object"""
    buffer_size = 4096

    def __init__(self, parent):
        global the_trigger
        if the_trigger is None:
            the_trigger = trigger()
        self.parent = parent
        self.buffer = ''
        return

    def write(self, data):
        self.buffer = self.buffer + data
        if len(self.buffer) > self.buffer_size:
            d, self.buffer = self.buffer, ''
            the_trigger.pull_trigger(lambda d=d, p=self.parent: p.push(d))

    def writeline(self, line):
        self.write(line + '\r\n')

    def writelines(self, lines):
        self.write(string.joinfields(lines, '\r\n') + '\r\n')

    def flush(self):
        if self.buffer:
            d, self.buffer = self.buffer, ''
            the_trigger.pull_trigger(lambda p=self.parent, d=d: p.push(d))

    def softspace(self, *args):
        pass

    def close(self):
        self.flush()
        self.parent = None
        return

    def trigger_close(self):
        d, self.buffer = self.buffer, ''
        p, self.parent = self.parent, None
        the_trigger.pull_trigger(lambda p=p, d=d: (p.push(d), p.close_when_done()))
        return


if __name__ == '__main__':
    import time

    def thread_function(output_file, i, n):
        print 'entering thread_function'
        while n:
            time.sleep(5)
            output_file.write('%2d.%2d %s\r\n' % (i, n, output_file))
            output_file.flush()
            n = n - 1

        output_file.close()
        print 'exiting thread_function'


    class thread_parent(asynchat.async_chat):

        def __init__(self, conn, addr):
            self.addr = addr
            asynchat.async_chat.__init__(self, conn)
            self.set_terminator('\r\n')
            self.buffer = ''
            self.count = 0

        def collect_incoming_data(self, data):
            self.buffer = self.buffer + data

        def found_terminator(self):
            data, self.buffer = self.buffer, ''
            if not data:
                asyncore.close_all()
                print 'done'
                return
            n = string.atoi(string.split(data)[0])
            tf = trigger_file(self)
            self.count = self.count + 1
            thread.start_new_thread(thread_function, (tf, self.count, n))


    class thread_server(asyncore.dispatcher):

        def __init__(self, family=socket.AF_INET, address=('', 9003)):
            asyncore.dispatcher.__init__(self)
            self.create_socket(family, socket.SOCK_STREAM)
            self.set_reuse_addr()
            self.bind(address)
            self.listen(5)

        def handle_accept(self):
            (conn, addr) = self.accept()
            tp = thread_parent(conn, addr)


    thread_server()
    try:
        asyncore.loop()
    except:
        asyncore.close_all()