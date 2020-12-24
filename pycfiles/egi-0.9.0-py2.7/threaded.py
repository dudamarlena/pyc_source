# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/egi/threaded.py
# Compiled at: 2016-09-08 05:35:24
"""

    A threaded implementation of the "egi.netstation" component .

"""
import simple as internal
from socket_wrapper import Socket
Error = internal.EgiError
ms_localtime = internal.ms_localtime
from threading import Thread
from Queue import Queue
import time

class _Command:
    """
        a command is simply the name of the method to call --
        -- and a dictionary with the argument name / value pairs

    """

    def __init__(self, method_name, kwargs=None):
        if kwargs is None:
            kwargs = {}
        self._func_name = method_name
        self._kwargs = kwargs
        return

    def name(self):
        """ returns the name of the function (method, actually) to call """
        return self._func_name

    def kwargs(self):
        """ returns the key/value set of the arguments to pass to the function (ugh, "to the method", I wanted to say) """
        return self._kwargs

    @staticmethod
    def call(obj, attrname, kwargs):
        """ call the given method with the arguments specified """
        bound = getattr(obj, attrname)
        return bound(**kwargs)

    def invoke(self, obj):
        """ invoke the 'attrname' with 'kwargs' (both stored here) on the object 'obj' """
        return self.call(obj, self.name(), self.kwargs())


class _NetstationThread(Thread):
    """ Class implementing the thread instance that be sending the messages """

    def __init__(self, to_send, received):
        """
            the thread will send the strings from the 'to_send' queue,
            read the response with the read functions packed together with the strings to send,
            put the result in the 'received' queue
        """
        Thread.__init__(self)
        self.setName('Netstation Thread')
        self._netstation_object = internal.Netstation()
        self._to_send = to_send
        self._received = received

    @staticmethod
    def is_end_marker(packet):
        """ is this enry from the queue an end marker ? """
        return packet is None

    def _process(self, packet):
        """ pass the received information to internal 'netstation' object to make a method call """
        return packet.invoke(self._netstation_object)

    def run(self):
        while True:
            packet = self._to_send.get()
            if self.is_end_marker(packet):
                self._disconnect()
                break
            ret = self._process(packet)
            self._received.put(ret)

    def connect(self, str_address, port_no):
        """ "forward" this method to the inner 'netstation' object """
        return self._netstation_object.connect(str_address, port_no)

    def _disconnect(self):
        """ this method is intended to be called internally and automatically) """
        return self._netstation_object.disconnect()


class Netstation:
    """ Provides Python interface for a connection with the Netstation via a TCP/IP socket. """

    def __init__(self):
        self._to_send = Queue()
        self._to_receive = Queue()
        self._netstation_thread = _NetstationThread(self._to_send, self._to_receive)

    def _put(self, data):
        """ a shortcut to put sth in the 'to-send' queue """
        self._to_send.put(data)

    def _get(self):
        """ a shortcut to get sth from the 'to-receive' queue ; nb.: blocks ! """
        data = self._to_receive.get()
        return data

    def enumerate_responses(self):
        """ (1) check .qsize() ; (2) .get() all these elements """
        n_available = self._to_receive.qsize()
        for i in xrange(n_available):
            data = self._get()
            yield data

    def process_responces(self):
        for resp in self.enumerate_responses():
            pass

    def _ns_thread_is_running(self):
        """ returns True if our 'postman' thread is stil busy with doing something """
        return self._netstation_thread.isAlive()

    def initialize(self, str_address, port_no):
        """ open the socket /and/ start the 'Mr. Postman' thread """
        self._netstation_thread.connect(str_address, port_no)
        self._netstation_thread.start()

    def finalize(self, seconds_timeout=2):
        """ send the thread the 'Done' message and wait until it finishes """
        self._put(None)
        t_start = time.time()
        while time.time() - t_start < seconds_timeout:
            self.process_responces()

        print ' egi: stopping ... '
        return

    def BeginSession(self):
        """ say 'hi!' to the server """
        packet = _Command('BeginSession')
        self._put(packet)

    def EndSession(self):
        """ say 'bye' to the server """
        packet = _Command('EndSession')
        self._put(packet)

    def StartRecording(self):
        """ start recording to the selected (externally) file """
        packet = _Command('StartRecording')
        self._put(packet)

    def StopRecording(self):
        """ stop recording to the selected file;
            the recording can be resumed with the BeginRecording() command
            if the session is not closed yet .
        """
        packet = _Command('StopRecording')
        self._put(packet)

    def _SendAttentionCommand(self):
        """ Sends and 'Attention' command """
        packet = _Command('SendAttentionCommand')
        self._put(packet)

    def _SendLocalTime(self, ms_time=None):
        """ Send the local time (in ms) to Netstation; usually this happens after an 'Attention' command """
        packet = _Command('SendAttentionCommand', {'ms_time': ms_time})
        self._put(packet)

    def sync(self, timestamp=None):
        """ a shortcut for sending the 'attention' command and the time info """
        packet = _Command('sync', {'timestamp': timestamp})
        self._put(packet)

    def send_event(self, key, timestamp=None, label=None, description=None, table=None, pad=False):
        """
            Send an event ; note that before sending any events a sync() has to be called
            to make the sent events effective .

            Arguments:
            -- 'id' -- a four-character identifier of the event ;
            -- 'timestamp' -- the local time when event has happened, in milliseconds ;
                              note that the "clock" used to produce the timestamp should be the same
                              as for the sync() method, and, ideally,
                              should be obtained via a call to the same function ;
                              if 'timestamp' is None, a time.time() wrapper is used .
            -- 'label' -- a string with any additional information, up to 256 characters .
            -- 'description' -- more additional information can go here (same limit applies) .
            -- 'table' -- a standart Python dictionary, where keys are 4-byte identifiers,
                          not more than 256 in total ;
                          there are no special conditions on the values,
                          but the size of every value entry in bytes should not exceed 2 ^ 16 .

            Note A: due to peculiarity of the implementation, our particular version of NetStation
                    was not able to record more than 2^15 events per session .

            Note B: it is *strongly* recommended to send as less data as possible .

        """
        kwargs = {'key': key, 
           'timestamp': timestamp, 
           'label': label, 
           'description': description, 
           'table': table, 
           'pad': pad}
        packet = _Command('send_event', kwargs)
        self._put(packet)


if __name__ == '__main__':
    print __doc__
    print '\n === \n'
    print 'module dir() listing: ', dir()