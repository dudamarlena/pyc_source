# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/egi/threaded_alt.py
# Compiled at: 2016-09-08 05:35:24
"""

    A threaded implementation of the "egi.netstation" component .

    (This variant of the threaded implementation is a bit more complicated,
      and a bit more messy -- but may be easier to support, as the method names
      from the " internal EGI.Netstation class " are wrapped automatically
      in the local Netstation wrapper class definition . )

"""
import simple as internal
from socket_wrapper import Socket
Error = internal.EgiError
ms_localtime = internal.ms_localtime
import types
from StringIO import StringIO
from threading import Thread
from Queue import Queue
import time

class _Command():
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


class Netstation():
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

    def process_responses(self):
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
            self.process_responses()

        print ' egi: stopping ... '
        return

    local_names = locals().keys()
    from fwhelper import FunctionWrappingHelper as FWH
    _NS = internal.Netstation
    for name in _NS.__dict__.iterkeys():
        value = getattr(_NS, name)
        if name.startswith('_'):
            continue
        if not callable(value):
            continue
        if name in local_names:
            continue
        fwh = FWH(value)
        header = StringIO()
        header.write('def %s(' % (name,))
        for entry in fwh.enum_argentries(b_all=True):
            header.write('%s, ' % (entry,))

        header.write('):\n')
        header.write('\n')
        header = header.getvalue()
        helpstr = getattr(value, '__doc__', None)
        call = StringIO()
        if helpstr:
            call.write('"""%s"""\n\n' % (helpstr,))
        if fwh.nargs() > 1:
            call.write('kwargs = {')
            for entry in fwh.enum_argentries(b_no_default_values=True, b_all=False):
                if entry == 'self':
                    continue
                call.write("'%s': %s, " % (entry, entry))

            call.write(' }\n')
            call.write('\n')
            call.write("packet = _Command('%s', kwargs)\n" % name)
        else:
            call.write("packet = _Command('%s')\n" % name)
        call.write('self._put(packet) \n')
        call.write('\n')
        call.seek(0)
        call_ = StringIO()
        for line in call.readlines():
            call_.write('\t' + line)

        call_.write('\n')
        call_ = call_.getvalue()
        code = header + call_
        exec code
        local_names.append(name)

    extended_ = locals().keys()
    delete_ = [ v for v in extended_ if v not in local_names ]
    for v in delete_:
        exec 'del %s' % (v,)

    del delete_
    del v


if __name__ == '__main__':
    print __doc__
    print '\n === \n'
    print 'module dir() listing: ', dir()