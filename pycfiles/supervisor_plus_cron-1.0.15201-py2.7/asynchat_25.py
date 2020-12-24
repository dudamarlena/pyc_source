# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\supervisor\medusa\asynchat_25.py
# Compiled at: 2015-07-18 10:13:56
r"""A class supporting chat-style (command/response) protocols.

This class adds support for 'chat' style protocols - where one side
sends a 'command', and the other sends a response (examples would be
the common internet protocols - smtp, nntp, ftp, etc..).

The handle_read() method looks at the input stream for the current
'terminator' (usually '\r\n' for single-line responses, '\r\n.\r\n'
for multi-line output), calling self.found_terminator() on its
receipt.

for example:
Say you build an async nntp client using this class.  At the start
of the connection, you'll have self.terminator set to '\r\n', in
order to process the single-line greeting.  Just before issuing a
'LIST' command you'll set it to '\r\n.\r\n'.  The output of the LIST
command will be accumulated (using your own 'collect_incoming_data'
method) up to the terminator, and then control will be returned to
you - by calling your self.found_terminator() method.
"""
import socket
from supervisor.medusa import asyncore_25 as asyncore
from supervisor.compat import long

class async_chat(asyncore.dispatcher):
    """This is an abstract class.  You must derive from this class, and add
    the two methods collect_incoming_data() and found_terminator()"""
    ac_in_buffer_size = 4096
    ac_out_buffer_size = 4096

    def __init__(self, conn=None, map=None):
        self.ac_in_buffer = ''
        self.ac_out_buffer = ''
        self.producer_fifo = fifo()
        asyncore.dispatcher.__init__(self, conn, map)

    def collect_incoming_data(self, data):
        raise NotImplementedError('must be implemented in subclass')

    def found_terminator(self):
        raise NotImplementedError('must be implemented in subclass')

    def set_terminator(self, term):
        """Set the input delimiter.  Can be a fixed string of any length, an integer, or None"""
        self.terminator = term

    def get_terminator(self):
        return self.terminator

    def handle_read(self):
        try:
            data = self.recv(self.ac_in_buffer_size)
        except socket.error:
            self.handle_error()
            return

        self.ac_in_buffer += data
        while self.ac_in_buffer:
            lb = len(self.ac_in_buffer)
            terminator = self.get_terminator()
            if not terminator:
                self.collect_incoming_data(self.ac_in_buffer)
                self.ac_in_buffer = ''
            elif isinstance(terminator, int) or isinstance(terminator, long):
                n = terminator
                if lb < n:
                    self.collect_incoming_data(self.ac_in_buffer)
                    self.ac_in_buffer = ''
                    self.terminator -= lb
                else:
                    self.collect_incoming_data(self.ac_in_buffer[:n])
                    self.ac_in_buffer = self.ac_in_buffer[n:]
                    self.terminator = 0
                    self.found_terminator()
            else:
                terminator_len = len(terminator)
                index = self.ac_in_buffer.find(terminator)
                if index != -1:
                    if index > 0:
                        self.collect_incoming_data(self.ac_in_buffer[:index])
                    self.ac_in_buffer = self.ac_in_buffer[index + terminator_len:]
                    self.found_terminator()
                else:
                    index = find_prefix_at_end(self.ac_in_buffer, terminator)
                    if index:
                        if index != lb:
                            self.collect_incoming_data(self.ac_in_buffer[:-index])
                            self.ac_in_buffer = self.ac_in_buffer[-index:]
                        break
                    else:
                        self.collect_incoming_data(self.ac_in_buffer)
                        self.ac_in_buffer = ''

    def handle_write(self):
        self.initiate_send()

    def handle_close(self):
        self.close()

    def push(self, data):
        self.producer_fifo.push(simple_producer(data))
        self.initiate_send()

    def push_with_producer(self, producer):
        self.producer_fifo.push(producer)
        self.initiate_send()

    def readable(self):
        """predicate for inclusion in the readable for select()"""
        return len(self.ac_in_buffer) <= self.ac_in_buffer_size

    def writable(self):
        """predicate for inclusion in the writable for select()"""
        return not (self.ac_out_buffer == '' and self.producer_fifo.is_empty() and self.connected)

    def close_when_done(self):
        """automatically close this channel once the outgoing queue is empty"""
        self.producer_fifo.push(None)
        return

    def refill_buffer(self):
        while 1:
            if len(self.producer_fifo):
                p = self.producer_fifo.first()
                if p is None:
                    if not self.ac_out_buffer:
                        self.producer_fifo.pop()
                        self.close()
                    return
                if isinstance(p, str):
                    self.producer_fifo.pop()
                    self.ac_out_buffer += p
                    return
                data = p.more()
                if data:
                    self.ac_out_buffer = self.ac_out_buffer + data
                    return
                self.producer_fifo.pop()
            else:
                return

        return

    def initiate_send(self):
        obs = self.ac_out_buffer_size
        if len(self.ac_out_buffer) < obs:
            self.refill_buffer()
        if self.ac_out_buffer and self.connected:
            try:
                num_sent = self.send(self.ac_out_buffer[:obs])
                if num_sent:
                    self.ac_out_buffer = self.ac_out_buffer[num_sent:]
            except socket.error:
                self.handle_error()
                return

    def discard_buffers(self):
        self.ac_in_buffer = ''
        self.ac_out_buffer = ''
        while self.producer_fifo:
            self.producer_fifo.pop()


class simple_producer:

    def __init__(self, data, buffer_size=512):
        self.data = data
        self.buffer_size = buffer_size

    def more(self):
        if len(self.data) > self.buffer_size:
            result = self.data[:self.buffer_size]
            self.data = self.data[self.buffer_size:]
            return result
        else:
            result = self.data
            self.data = ''
            return result


class fifo:

    def __init__(self, list=None):
        if not list:
            self.list = []
        else:
            self.list = list

    def __len__(self):
        return len(self.list)

    def is_empty(self):
        return self.list == []

    def first(self):
        return self.list[0]

    def push(self, data):
        self.list.append(data)

    def pop(self):
        if self.list:
            return (1, self.list.pop(0))
        else:
            return (0, None)
            return


def find_prefix_at_end(haystack, needle):
    l = len(needle) - 1
    while l and not haystack.endswith(needle[:l]):
        l -= 1

    return l