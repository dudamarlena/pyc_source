# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/indra/ipc/saranwrap.py
# Compiled at: 2008-07-28 17:15:44
"""@file saranwrap.py
@author Phoenix
@date 2007-07-13
@brief A simple, pickle based rpc mechanism which reflects python
objects and callables.

$LicenseInfo:firstyear=2007&license=mit$

Copyright (c) 2007-2008, Linden Research, Inc.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
$/LicenseInfo$

This file provides classes and exceptions used for simple python level
remote procedure calls. This is achieved by intercepting the basic
getattr and setattr calls in a client proxy, which commnicates those
down to the server which will dispatch them to objects in it's process
space.

The basic protocol to get and set attributes is for the client proxy
to issue the command:

getattr $id $name
setattr $id $name $value

getitem $id $item
setitem $id $item $value
eq $id $rhs
del $id

When the get returns a callable, the client proxy will provide a
callable proxy which will invoke a remote procedure call. The command
issued from the callable proxy to server is:

call $id $name $args $kwargs

If the client supplies an id of None, then the get/set/call is applied
to the object(s) exported from the server.

The server will parse the get/set/call, take the action indicated, and
return back to the caller one of:

value $val
callable
object $id
exception $excp

To handle object expiration, the proxy will instruct the rpc server to
discard objects which are no longer in use. This is handled by
catching proxy deletion and sending the command:

del $id

The server will handle this by removing clearing it's own internal
references. This does not mean that the object will necessarily be
cleaned from the server, but no artificial references will remain
after successfully completing. On completion, the server will return
one of:

value None
exception $excp

The server also accepts a special command for debugging purposes:

status

Which will be intercepted by the server to write back:

status {...}

The wire protocol is to pickle the Request class in this file. The
request class is basically an action and a map of parameters'
"""
import os, cPickle, struct, sys
try:
    set = set
    frozenset = frozenset
except NameError:
    from sets import Set as set, ImmutableSet as frozenset

from eventlet.processes import Process
from eventlet import api
_g_debug_mode = False
if _g_debug_mode:
    import traceback

def pythonpath_sync():
    """
@brief apply the current sys.path to the environment variable PYTHONPATH, so that child processes have the same paths as the caller does.
"""
    pypath = os.pathsep.join(sys.path)
    os.environ['PYTHONPATH'] = pypath


def wrap(obj, dead_callback=None):
    """
@brief wrap in object in another process through a saranwrap proxy
@param object The object to wrap.
@param dead_callback A callable to invoke if the process exits."""
    if type(obj).__name__ == 'module':
        return wrap_module(obj.__name__, dead_callback)
    pythonpath_sync()
    p = Process('python', [__file__, '--child'], dead_callback)
    prox = Proxy(p, p)
    prox.obj = obj
    return prox.obj


def wrap_module(fqname, dead_callback=None):
    """
@brief wrap a module in another process through a saranwrap proxy
@param fqname The fully qualified name of the module.
@param dead_callback A callable to invoke if the process exits."""
    global _g_debug_mode
    pythonpath_sync()
    if _g_debug_mode:
        p = Process('python', [__file__, '--module', fqname, '--logfile', '/tmp/saranwrap.log'], dead_callback)
    else:
        p = Process('python', [__file__, '--module', fqname], dead_callback)
    prox = Proxy(p, p)
    return prox


def status(proxy):
    """
@brief get the status from the server through a proxy
@param proxy a saranwrap.Proxy object connected to a server."""
    _write_request(Request('status', {}), proxy.__local_dict['_out'])
    return _read_response(None, None, proxy.__local_dict['_in'], proxy.__local_dict['_out'], None)


class BadResponse(Exception):
    """"This exception is raised by an saranwrap client when it could
    parse but cannot understand the response from the server."""
    __module__ = __name__


class BadRequest(Exception):
    """"This exception is raised by a saranwrap server when it could parse
    but cannot understand the response from the server."""
    __module__ = __name__


class UnrecoverableError(Exception):
    __module__ = __name__


class Request(object):
    """@brief A wrapper class for proxy requests to the server."""
    __module__ = __name__

    def __init__(self, action, param):
        self._action = action
        self._param = param

    def __str__(self):
        return 'Request `' + self._action + '` ' + str(self._param)

    def __getitem__(self, name):
        return self._param[name]

    def action(self):
        return self._action


def _read_lp_hunk(stream):
    len_bytes = stream.read(4)
    length = struct.unpack('I', len_bytes)[0]
    body = stream.read(length)
    return body


def _read_response(id, attribute, input, output, dead_list):
    """@brief local helper method to read respones from the rpc server."""
    try:
        str = _read_lp_hunk(input)
        _prnt(`str`)
        response = cPickle.loads(str)
    except AttributeError, e:
        raise UnrecoverableError(e)

    _prnt('response: %s' % response)
    if response[0] == 'value':
        return response[1]
    elif response[0] == 'callable':
        return CallableProxy(id, attribute, input, output, dead_list)
    elif response[0] == 'object':
        return ObjectProxy(input, output, response[1], dead_list)
    elif response[0] == 'exception':
        exp = response[1]
        raise exp
    else:
        raise BadResponse(response[0])


def _write_lp_hunk(stream, hunk):
    write_length = struct.pack('I', len(hunk))
    stream.write(write_length + hunk)
    if hasattr(stream, 'flush'):
        stream.flush()


def _write_request(param, output):
    _prnt('request: %s' % param)
    str = cPickle.dumps(param)
    _write_lp_hunk(output, str)


def _is_local(attribute):
    """Return true if the attribute should be handled locally"""
    if '__local_dict' in attribute:
        return True
    return False


def _prnt(message):
    if _g_debug_mode:
        print message


_g_logfile = None

def _log(message):
    global _g_logfile
    if _g_logfile:
        _g_logfile.write(str(os.getpid()) + ' ' + message)
        _g_logfile.write('\n')
        _g_logfile.flush()


def _unmunge_attr_name(name):
    """ Sometimes attribute names come in with classname prepended, not sure why.
    This function removes said classname, because we're huge hackers and we didn't
    find out what the true right thing to do is.  *FIX: find out. """
    if name.startswith('_Proxy'):
        name = name[len('_Proxy'):]
    if name.startswith('_ObjectProxy'):
        name = name[len('_ObjectProxy'):]
    return name


class Proxy(object):
    """@class Proxy
@brief This class wraps a remote python process, presumably available
in an instance of an Server.

This is the class you will typically use as a client to a child
process. Simply instantiate one around a file-like interface and start
calling methods on the thing that is exported. The dir() builtin is
not supported, so you have to know what has been exported.
"""
    __module__ = __name__

    def __init__(self, input, output, dead_list=None):
        """@param input a file-like object which supports read().
@param output a file-like object which supports write() and flush().
@param id an identifier for the remote object. humans do not provide this.
"""
        if dead_list is None:
            dead_list = set()
        self.__local_dict = dict(_in=input, _out=output, _dead_list=dead_list, _id=None)
        return

    def __getattribute__(self, attribute):
        if _is_local(attribute):
            attribute = _unmunge_attr_name(attribute)
            return super(Proxy, self).__getattribute__(attribute)
        else:
            my_in = self.__local_dict['_in']
            my_out = self.__local_dict['_out']
            my_id = self.__local_dict['_id']
            _dead_list = self.__local_dict['_dead_list']
            for dead_object in _dead_list.copy():
                request = Request('del', {'id': dead_object})
                _write_request(request, my_out)
                response = _read_response(my_id, attribute, my_in, my_out, _dead_list)
                _dead_list.remove(dead_object)

            request = Request('getattr', {'id': my_id, 'attribute': attribute})
            _write_request(request, my_out)
            return _read_response(my_id, attribute, my_in, my_out, _dead_list)

    def __setattr__(self, attribute, value):
        if _is_local(attribute):
            attribute = _unmunge_attr_name(attribute)
            super(Proxy, self).__getattribute__('__dict__')[attribute] = value
        else:
            my_in = self.__local_dict['_in']
            my_out = self.__local_dict['_out']
            my_id = self.__local_dict['_id']
            _dead_list = self.__local_dict['_dead_list']
            request = Request('setattr', {'id': my_id, 'attribute': attribute, 'value': value})
            _write_request(request, my_out)
            return _read_response(my_id, attribute, my_in, my_out, _dead_list)


class ObjectProxy(Proxy):
    """@class ObjectProxy
@brief This class wraps a remote object in the Server

This class will be created during normal operation, and users should
not need to deal with this class directly."""
    __module__ = __name__

    def __init__(self, input, output, id, dead_list):
        """@param input a file-like object which supports read().
@param output a file-like object which supports write() and flush().
@param id an identifier for the remote object. humans do not provide this.
"""
        Proxy.__init__(self, input, output, dead_list)
        self.__local_dict['_id'] = id

    def __del__(self):
        my_id = self.__local_dict['_id']
        _prnt('ObjectProxy::__del__ %s' % my_id)
        self.__local_dict['_dead_list'].add(my_id)

    def __getitem__(self, key):
        my_in = self.__local_dict['_in']
        my_out = self.__local_dict['_out']
        my_id = self.__local_dict['_id']
        _dead_list = self.__local_dict['_dead_list']
        request = Request('getitem', {'id': my_id, 'key': key})
        _write_request(request, my_out)
        return _read_response(my_id, key, my_in, my_out, _dead_list)

    def __setitem__(self, key, value):
        my_in = self.__local_dict['_in']
        my_out = self.__local_dict['_out']
        my_id = self.__local_dict['_id']
        _dead_list = self.__local_dict['_dead_list']
        request = Request('setitem', {'id': my_id, 'key': key, 'value': value})
        _write_request(request, my_out)
        return _read_response(my_id, key, my_in, my_out, _dead_list)

    def __eq__(self, rhs):
        my_in = self.__local_dict['_in']
        my_out = self.__local_dict['_out']
        my_id = self.__local_dict['_id']
        _dead_list = self.__local_dict['_dead_list']
        request = Request('eq', {'id': my_id, 'rhs': rhs.__local_dict['_id']})
        _write_request(request, my_out)
        return _read_response(my_id, None, my_in, my_out, _dead_list)

    def __repr__(self):
        val = self.__repr__()
        return 'saran:%s' % val

    def __str__(self):
        return self.__str__()

    def __len__(self):
        return self.__len__()


def proxied_type(self):
    if type(self) is not ObjectProxy:
        return type(self)
    my_in = self.__local_dict['_in']
    my_out = self.__local_dict['_out']
    my_id = self.__local_dict['_id']
    request = Request('type', {'id': my_id})
    _write_request(request, my_out)
    return _read_response(my_id, None, my_in, my_out, None)


class CallableProxy(object):
    """@class CallableProxy
@brief This class wraps a remote function in the Server

This class will be created by an Proxy during normal operation,
and users should not need to deal with this class directly."""
    __module__ = __name__

    def __init__(self, object_id, name, input, output, dead_list):
        self._object_id = object_id
        self._name = name
        self._in = input
        self._out = output
        self._dead_list = dead_list

    def __call__(self, *args, **kwargs):
        request = Request('call', {'id': self._object_id, 'name': self._name, 'args': args, 'kwargs': kwargs})
        _write_request(request, self._out)
        return _read_response(self._object_id, self._name, self._in, self._out, self._dead_list)


class Server(object):
    __module__ = __name__

    def __init__(self, input, output, export):
        """@param input a file-like object which supports read().
@param output a file-like object which supports write() and flush().
@param export an object, function, or map which is exported to clients
when the id is None."""
        self._in = input
        self._out = output
        self._export = export
        self._next_id = 1
        self._objects = {}

    def handle_status(self, object, req):
        return {'object_count': len(self._objects), 'next_id': self._next_id, 'pid': os.getpid()}

    def handle_getattr(self, object, req):
        try:
            return getattr(object, req['attribute'])
        except AttributeError, e:
            if hasattr(object, '__getitem__'):
                return object[req['attribute']]
            else:
                raise e

    def handle_setattr(self, object, req):
        try:
            return setattr(object, req['attribute'], req['value'])
        except AttributeError, e:
            if hasattr(object, '__setitem__'):
                return object.__setitem__(req['attribute'], req['value'])
            else:
                raise e

    def handle_getitem(self, object, req):
        return object[req['key']]

    def handle_setitem(self, object, req):
        object[req['key']] = req['value']
        return

    def handle_eq(self, object, req):
        rhs = None
        try:
            rhs = self._objects[req['rhs']]
        except KeyError, e:
            return False

        return object == rhs

    def handle_call(self, object, req):
        try:
            fn = getattr(object, req['name'])
        except AttributeError, e:
            if hasattr(object, '__setitem__'):
                fn = object[req['name']]
            else:
                raise e

        return fn(*req['args'], **req['kwargs'])

    def handle_del(self, object, req):
        id = req['id']
        _log('del %s from %s' % (id, self._objects))
        del self._objects[id]
        return

    def handle_type(self, object, req):
        return type(object)

    def loop(self):
        """@brief Loop forever and respond to all requests."""
        _log('Server::loop')
        while True:
            try:
                try:
                    str = _read_lp_hunk(self._in)
                except EOFError:
                    sys.exit(0)

                request = cPickle.loads(str)
                _log('request: %s (%s)' % (request, self._objects))
                req = request
                id = None
                object = None
                try:
                    id = req['id']
                    if id:
                        id = int(id)
                        object = self._objects[id]
                except Exception, e:
                    pass

                if object is None or id is None:
                    id = None
                    object = self._export
                handler_name = 'handle_%s' % request.action()
                try:
                    handler = getattr(self, handler_name)
                except AttributeError:
                    raise BadRequest, request.action()

                response = handler(object, request)
                if request.action() in ['status', 'type']:
                    self.respond(['value', response])
                elif callable(response):
                    self.respond(['callable'])
                elif self.is_value(response):
                    self.respond(['value', response])
                else:
                    self._objects[self._next_id] = response
                    self.respond(['object', self._next_id])
                    self._next_id += 1
            except SystemExit, e:
                raise e
            except Exception, e:
                self.write_exception(e)
            except:
                self.write_exception(sys.exc_info()[0])

        return

    def is_value(self, value):
        """@brief Test if value should be serialized as a simple dataset.
@param value The value to test.
@return Returns true if value is a simple serializeable set of data.
"""
        return type(value) in (str, unicode, int, float, long, bool, type(None))

    def respond(self, body):
        _log('responding with: %s' % body)
        s = cPickle.dumps(body)
        _log(`s`)
        str = _write_lp_hunk(self._out, s)

    def write_exception(self, e):
        """@brief Helper method to respond with an exception."""
        self.respond(['exception', e])
        if _g_debug_mode:
            _log('traceback: %s' % traceback.format_tb(sys.exc_info()[2]))


def raise_a_weird_error():
    raise 'oh noes you can raise a string'


def raise_an_unpicklable_error():

    class Unpicklable(Exception):
        __module__ = __name__

    raise Unpicklable()


def raise_standard_error():
    raise FloatingPointError()


def print_string(str):
    print str


def err_string(str):
    print >> sys.stderr, str


def main():
    global _g_logfile
    import optparse
    parser = optparse.OptionParser(usage='usage: %prog [options]', description='Simple saranwrap.Server wrapper')
    parser.add_option('-c', '--child', default=False, action='store_true', help='Wrap an object serialed via setattr.')
    parser.add_option('-m', '--module', type='string', dest='module', default=None, help='a module to load and export.')
    parser.add_option('-l', '--logfile', type='string', dest='logfile', default=None, help='file to log to.')
    (options, args) = parser.parse_args()
    if options.logfile:
        _g_logfile = open(options.logfile, 'a')
    if options.module:
        export = api.named(options.module)
        server = Server(sys.stdin, sys.stdout, export)
    elif options.child:
        server = Server(sys.stdin, sys.stdout, {})

    class NullSTDOut(object):
        __module__ = __name__

        def write(a, b):
            pass

    sys.stderr = NullSTDOut()
    sys.stdout = NullSTDOut()
    server.loop()
    if _g_logfile:
        _g_logfile.close()
    return


if __name__ == '__main__':
    main()