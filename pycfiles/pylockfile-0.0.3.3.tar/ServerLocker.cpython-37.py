# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Library/Frameworks/Python.framework/Versions/3.7/lib/python3.7/site-packages/pylocker/ServerLocker.py
# Compiled at: 2020-01-14 15:04:22
# Size of source mod 2**32: 88210 bytes
from __future__ import print_function
import os, sys, time, atexit, signal, uuid, traceback, socket, threading
from multiprocessing.connection import Listener, Client
IS2 = True
if sys.version_info.major == 3:
    assert sys.version_info.major != 2, 'Only python 2 or 3 are supported. %s is used instead' % (sys.version_info.major,)
    IS2 = False
elif IS2:
    str = str
    unicode = unicode
    bytes = str
    long = long
    basestring = basestring
    xrange = xrange
    range = range
    maxint = sys.maxint
else:
    str = str
    long = int
    unicode = str
    bytes = bytes
    basestring = (str, bytes)
    xrange = range
    range = lambda *args: list(xrange(*args))
    maxint = sys.maxsize

def _full_stack():
    try:
        exc = sys.exc_info()[0]
        stack = traceback.extract_stack()[:-1]
        if exc is not None:
            del stack[-1]
        trc = 'Traceback (most recent call last):\n'
        stackstr = trc + ''.join(traceback.format_list(stack))
        if exc is not None:
            stackstr += '  ' + traceback.format_exc().lstrip(trc)
    except Exception as err:
        try:
            stackstr = 'Unable to pull full stack (%s)' % str(err)
            try:
                _stack = traceback.extract_stack()[:-1]
                stackstr = '%s\n%s' % (stackstr, ''.join(traceback.format_list(_stack)))
            except:
                pass

        finally:
            err = None
            del err

    return stackstr


class _LockerThread(threading.Thread):

    def __init__(self, locker, target, args=(), kwargs={}, name=None, daemon=True):
        threading.Thread.__init__(self, group=None, target=None, name=name)
        self.locker_ = locker
        self.running_ = False
        self.started_ = False
        self.failed_ = False
        self.result_ = None
        self.error_ = None
        self.stack_ = None
        self.stop_ = False
        self._LockerThread__target = target
        self._LockerThread__args = args
        self._LockerThread__kwargs = kwargs
        self.setDaemon(daemon)

    def run(self):
        self.started_ = True
        self.running_ = True
        try:
            self.result_ = (self._LockerThread__target)(*self._LockerThread__args, **self._LockerThread__kwargs)
        except Exception as err:
            try:
                self.failed_ = True
                self.error_ = err
                self.result_ = None
                try:
                    self.stack_ = _full_stack()
                except:
                    self.stack_ = None

                self.locker_._error((str(self.error_)), stack=(self.stack_))
            finally:
                err = None
                del err

        self.running_ = False


def _reconnect_server(method):
    """Internally used wrapper function"""

    def wrapper(self, *args, **kwargs):
        with self._reconnectCounterLock:
            self._reconnectCounter += 1
        try:
            result = method(self, *args, **kwargs)
        except Exception as err:
            try:
                result = None
                self._error((str(err)), stack=(_full_stack()))
            finally:
                err = None
                del err

        with self._reconnectCounterLock:
            self._reconnectCounter -= 1
        self._stop_server(reconnect=True)
        return result

    return wrapper


def _reconnect_client(method):
    """Internally used wrapper function"""

    def wrapper(self, *args, **kwargs):
        with self._reconnectCounterLock:
            self._reconnectCounter += 1
        try:
            result = method(self, *args, **kwargs)
        except Exception as err:
            try:
                result = None
                self._error((str(err)), stack=(_full_stack()))
            finally:
                err = None
                del err

        with self._reconnectCounterLock:
            self._reconnectCounter -= 1
        self._stop_client(reconnect=True)
        return result

    return wrapper


def _to_bytes(input, encode='utf-8', errors='ignore'):
    if not isinstance(input, bytes):
        input = input.encode(encode, errors=errors)
    return input


def _to_unicode(input, decode='utf-8', errors='ignore'):
    if not isinstance(input, unicode):
        input = input.decode(decode, errors=errors)
    return input


class ServerLocker(object):
    """ServerLocker"""

    def __init__(self, password, name=None, serverFile=True, defaultTimeout=20, maxLockTime=120, port=3000, allowServing=True, autoconnect=True, reconnect=False, connectTimeout=20, logger=False, blocking=False, debugMode=False):
        self.debugMode = debugMode
        assert isinstance(autoconnect, bool), 'locker autoconnect must be boolean'
        self._ServerLocker__uniqueName = _to_unicode(str(uuid.uuid1()))
        if name is None:
            name = self._ServerLocker__uniqueName
        else:
            assert isinstance(name, basestring), 'locker server name must be None or a string'
            name = _to_unicode(name)
        assert ':' not in name, "':' not allowed in ServerLocker name"
        self._ServerLocker__name = name
        assert isinstance(blocking, bool), 'locker blocking must be boolean'
        self._ServerLocker__blocking = blocking
        assert isinstance(password, basestring), 'locker password must be a string'
        if not isinstance(password, bytes):
            password = _to_bytes(password)
        else:
            self._ServerLocker__password = password
            try:
                self._ServerLocker__pid = os.getpid()
            except:
                self._ServerLocker__pid = 0

            self.set_maximum_lock_time(maxLockTime)
            self.set_default_timeout(defaultTimeout)
            self._ServerLocker__address = self._ServerLocker__get_ip_address()
            if not isinstance(reconnect, bool):
                assert isinstance(reconnect, int), 'reconnect must be boolean or integer'
                if not reconnect >= 0:
                    raise AssertionError('reconnect must be >=0')
            elif reconnect is False:
                reconnect = 0
        self._ServerLocker__reconnect = False
        assert isinstance(connectTimeout, int), 'connectTimeout must be integer'
        assert connectTimeout > 0, 'connectTimeout must ber >0'
        self._ServerLocker__connectTimeout = connectTimeout
        assert isinstance(port, int), 'port must be integer'
        assert 1 <= port <= 65535, 'port must be 1<=port<=65535'
        self._ServerLocker__port = port
        assert isinstance(allowServing, bool), 'allowServing must be boolean'
        self._ServerLocker__allowServing = allowServing
        self.reset(raiseError=True)
        self.set_server_file(serverFile)
        atexit.register(self._on_atexit)
        if autoconnect:
            self._ServerLocker__serve_or_connect()
            if not self.isServer:
                if not self.isClient:
                    self._warn('locker is not a serving nor connected as client yet autoconnect is set to True')

    def __getstate__(self):
        current = {}
        current.update(self.__dict__)
        _serverFile = self.__dict__.pop('_ServerLocker__serverFile')
        self.reset()
        state = {}
        state.update(self.__dict__)
        state['_ServerLocker__serverFile'] = _serverFile
        for k in state:
            if k.endswith('Lock'):
                state[k] = None
            if k.endswith('Event'):
                state[k] = None

        self.__dict__ = current
        return state

    def __setstate__(self, state):
        self.__dict__ = state
        _serverFile = self.__dict__.pop('_ServerLocker__serverFile')
        self.reset()
        self.__dict__['_ServerLocker__serverFile'] = _serverFile

    def _critical(self, message, force=False, stack=None):
        if self._ServerLocker__debugMode:
            print('%s - CRITICAL - %s' % (self.__class__.__name__, message))
            if stack is not None:
                print(stack)
        return message

    def _error(self, message, force=False, stack=None):
        if self._ServerLocker__debugMode:
            print('%s - ERROR - %s' % (self.__class__.__name__, message))
            if stack is not None:
                print(stack)
        return message

    def _warn(self, message, force=False, stack=None):
        if self._ServerLocker__debugMode:
            print('%s - WARNING - %s' % (self.__class__.__name__, message))
            if stack is not None:
                print(stack)
        return message

    def _info(self, message, force=False, stack=None):
        if self._ServerLocker__debugMode:
            print('%s - INFO - %s' % (self.__class__.__name__, message))
            if stack is not None:
                print(stack)
        return message

    @property
    def _clientsLUT(self):
        return self._ServerLocker__clientsLUT

    @property
    def _pathsLUT(self):
        return self._ServerLocker__pathsLUT

    @property
    def _clientsQueue(self):
        return self._ServerLocker__clientsQueue

    @property
    def _ownRequests(self):
        return self._ServerLocker__ownRequests

    @property
    def _ownAcquired(self):
        return self._ServerLocker__ownAcquired

    @property
    def _publications(self):
        return self._ServerLocker__publications

    def _on_atexit(self, *args, **kwargs):
        try:
            uniqueName, timestamp, address, port, pid = self.get_running_server_fingerprint(serverFile=(self._ServerLocker__serverFile), raiseNotFound=False, raiseError=False)
            if uniqueName == self._ServerLocker__uniqueName:
                with self._ServerLocker__serverFileLock:
                    open(self._ServerLocker__serverFile, 'w').close()
        except:
            pass

        self.stop()

    def _stop_server(self, reconnect=False):
        try:
            if not self._stopServing:
                self._stopServing = True
                uniqueName, timestamp, address, port, pid = self.get_running_server_fingerprint(serverFile=(self._ServerLocker__serverFile), raiseNotFound=False, raiseError=False)
                if uniqueName == self._ServerLocker__uniqueName:
                    with self._ServerLocker__serverFileLock:
                        open(self._ServerLocker__serverFile, 'w').close()
        except:
            pass

        try:
            try:
                self._stopServing = True
                if self._ServerLocker__server is not None:
                    self._ServerLocker__server.close()
            except Exception as err:
                try:
                    self._warn('Unable to stop locker server (%s)' % err)
                finally:
                    err = None
                    del err

        finally:
            self._ServerLocker__server = None

        try:
            with self._ServerLocker__clientsLUTLock:
                if self._ServerLocker__clientsLUT is not None:
                    for cname in list(self._ServerLocker__clientsLUT):
                        try:
                            self._ServerLocker__clientsLUT.pop(cname)['connection'].close()
                        except Exception as err:
                            try:
                                self._warn("Unable to close clocker client '%s' connection (%s)" % (cname, err))
                            finally:
                                err = None
                                del err

                        else:
                            self._warn("locker closed connection to '%s'" % cname)

                self._ServerLocker__clientsLUT = None
        except Exception as err:
            try:
                self._warn('Unable to close locker clients connection (%s)' % err)
            finally:
                err = None
                del err

        self._ServerLocker__deadLockEvent.set()
        self._ServerLocker__deadLockEvent.clear()
        self._ServerLocker__clientsQueueEvent.set()
        self._ServerLocker__clientsQueueEvent.clear()
        if self._reconnectCounter == 0 and reconnect:
            if not self._killSignal:
                if self._ServerLocker__reconnect is True or self._ServerLocker__reconnect > 0:
                    if self._ServerLocker__reconnect is not True:
                        self._ServerLocker__reconnect -= 1
                    self._warn('locker server stopped! Trying to reconnect')
                    self._ServerLocker__serve_or_connect()
                else:
                    raise Exception('locker server stopped! Aborting')

    def _stop_client(self, reconnect=False):
        try:
            try:
                self._ServerLocker__connection.close()
            except:
                pass

        finally:
            self._ServerLocker__connection = None

        self._ServerLocker__serverUniqueName = None
        self._ServerLocker__serverName = None
        self._ServerLocker__serverAddress = None
        self._ServerLocker__serverPort = None
        if self._reconnectCounter == 0:
            if reconnect:
                if not self._killSignal:
                    if self._ServerLocker__reconnect is True or self._ServerLocker__reconnect > 0:
                        if self._ServerLocker__reconnect is not True:
                            self._ServerLocker__reconnect -= 1
                        self._warn('locker client connection stopped! Trying to reconnect')
                        self._ServerLocker__serve_or_connect()
                    else:
                        raise Exception('locker client connection stopped! Aborting')

    def __process_server_response(self, received):
        if isinstance(received, dict):
            received = [
             received]
        assert isinstance(received, (list, set, tuple)), 'received data must be a list'
        assert len(received), 'received list is emtpy'
        for response in received:
            assert isinstance(response, dict), 'received list items must be dictionaries'
            assert 'action' in response, "received dict items must have 'action' key"
            assert 'request_unique_id' in response, "received dict items must have 'request_unique_id' key"
            if response['action'] == 'publish':
                assert 'message' in response, "received action '%s' must have 'message' key" % response['action']
                message = response['message']
                if not isinstance(message, basestring):
                    raise AssertionError("received action '%s' message must be a string" % response['action'])
                else:
                    assert response['action'] in ('acquired', 'released', 'exceeded_maximum_lock_time'), "received dict items dict 'action' key value is not recognized"
                    assert 'path' in response, "received action '%s' must have 'path' key" % response['action']
                    path = response['path']
                    if isinstance(path, basestring):
                        path = [
                         path]
                    assert isinstance(path, (list, set, tuple)), "received dict 'path' value must be a list"
                    assert len(path), "received dict 'path' value list must be not empty"
                    assert all([isinstance(p, basestring) for p in path]), "received dict 'path' list items must be all strings. %s is given" % path

        with self._ServerLocker__ownRequestsLock:
            utctimestamp = time.time()
            for response in received:
                _action = response['action']
                _ruid = response['request_unique_id']
                if _action == 'acquired':
                    _req = self._ServerLocker__ownRequests.pop(_ruid, {'acquired_event': None})
                    if _req['acquired_event'] is not None:
                        _req['acquired_event'].set()
                    _req['acquired_utctime'] = utctimestamp
                    self._ServerLocker__ownAcquired[_ruid] = _req
                elif _action == 'released':
                    self._warn("action 'released' received at client !!! This is meaningless")
                elif _action == 'exceeded_maximum_lock_time':
                    if self._ServerLocker__ownAcquired.pop(_ruid, None) is not None:
                        _cname = response['client_name']
                        _cuname = response['client_unique_name']
                        self._warn("Lock '%s' requested by client %s:%s for all '%s' is released by server because maximum lock time is exceed and the lock is required by another client" % (_ruid, _cname, _cuname, response['path']))
                    else:
                        if _action == 'publish':
                            self._ServerLocker__add_publication(request=response)
                else:
                    raise Exception("Unkown 'action' '%s'. PLEASE REPORT" % (_action,))

    def __process_client_request(self, request, connection):
        ruid = request['request_unique_id']
        cname = request['client_name']
        cuname = request['client_unique_name']
        action = request['action']
        if action == 'release':
            with self._ServerLocker__pathsLUTLock:
                path = request['path']
                self._warn('releasing request: %s' % request)
                for p in path:
                    if p not in self._ServerLocker__pathsLUT:
                        self._warn("requesting to release unlocked path '%s'" % (path,))
                    elif self._ServerLocker__pathsLUT[p]['client_unique_name'] == cuname and self._ServerLocker__pathsLUT[p]['request_unique_id'] == ruid:
                        self._ServerLocker__pathsLUT.pop(p, None)
                    else:
                        self._warn("requesting to release path '%s' locked by different locker" % (path,))

        elif action == 'acquire':
            with self._ServerLocker__clientsQueueLock:
                req = {'connection': connection}
                req.update(request)
                self._ServerLocker__clientsQueue.append(req)
        elif action == 'publish':
            with self._ServerLocker__clientsLUTLock:
                receivers = request['receivers']
                if receivers is None:
                    receivers = [
                     self._ServerLocker__uniqueName] + list(self._ServerLocker__clientsLUT)
                for r in receivers:
                    if r == request['client_unique_name']:
                        continue
                    if r == self._ServerLocker__uniqueName:
                        self._ServerLocker__add_publication(request=request)
                    else:
                        conn = self._ServerLocker__clientsLUT[r]['connection']
                        conn.send(request)

        else:
            raise Exception("Unkown request id '%s' action '%s' from client '%s' (%s)" % (ruid, action, cname, cuname))
        with self._ServerLocker__clientsQueueLock:
            self._ServerLocker__clientsQueueEvent.set()
            self._ServerLocker__clientsQueueEvent.clear()
        with self._ServerLocker__pathsLUTLock:
            self._ServerLocker__deadLockEvent.set()
            self._ServerLocker__deadLockEvent.clear()

    def __serve_client(self, connection, clientName, clientUniqueName):
        self._warn("Client '%s:%s' connected to server" % (clientName, clientUniqueName))
        while not self._stopServing:
            if not self._killSignal:
                lastTimeout = None
                try:
                    received = connection.recv()
                except socket.timeout as err:
                    try:
                        if lastTimeout is None:
                            lastTimeout = time.time()
                        elif time.time() - lastTimeout < 1:
                            self._critical("Connection to locker client '%s:%s' has encountered unsuspected successive timeouts within 1 second." % (clientName, clientUniqueName))
                            break
                        self._error("Connection timeout to locker client '%s:%s' this should have no effect on the locker if otherwise please report (%s)" % (clientName, clientUniqueName, err))
                        continue
                    finally:
                        err = None
                        del err

                except Exception as err:
                    try:
                        self._critical("Connection error to locker client '%s:%s' (%s)" % (clientName, clientUniqueName, err))
                        break
                    finally:
                        err = None
                        del err

                try:
                    lastTimeout = None
                    assert isinstance(received, dict), 'received data must be a dict. PLEASE REPORT'
                    assert 'request_unique_id' in received, "received dict must have 'request_unique_id' key"
                    assert isinstance(received['request_unique_id'], basestring), "received 'resquest_unique_id' value must be a string"
                    assert 'client_unique_name' in received, "received dict must have 'client_unique_name' key"
                    assert received['client_unique_name'] == clientUniqueName, "received dict 'client_name' key value '%s' does not match registered clientUniqueName '%s'" % (received['client_unique_name'], clientUniqueName)
                    assert 'client_name' in received, "received dict must have 'client_name' key"
                    assert received['client_name'] == clientName, "received dict 'client_name' key value '%s' does not match registered clientName '%s'" % (received['client_unique_name'], clientName)
                    assert 'action' in received, "received dict must have 'action' key"
                    if received['action'] == 'publish':
                        assert 'message' in received, "received action '%s' must have 'message' key" % response['action']
                        message = received['message']
                        if not isinstance(message, basestring):
                            raise AssertionError("received action '%s' message must be a string" % response['action'])
                    else:
                        assert received['action'] in ('acquire', 'release', 'publish'), "received dict must have 'action' key value must be either 'acquire', 'release' or 'publish'"
                        assert 'path' in received, "received dict must have 'path' key"
                    path = received['path']
                    if isinstance(path, basestring):
                        path = [
                         path]
                        assert isinstance(path, (list, set, tuple)), "received dict must have 'path' key value must be either a string or a list"
                        assert all([isinstance(p, basestring) for p in path]), 'received dict path list items must be all strings'
                        path = tuple(set(path))
                    if received['action'] == 'acquire':
                        assert 'request_utctime' in received, "received dict must have 'requestUTCTime' key"
                        received['request_utctime'] = float(received['request_utctime'])
                        received['received_utctime'] = time.time()
                        assert received['received_utctime'] > received['request_utctime'], 'request utctime is set before it is being received at server! PLEASE REPORT'
                        assert 'timeout' in received, "received dict must have 'timeout' key"
                        received['timeout'] = float(received['timeout'])
                        assert received['timeout'] > 0, 'request timeout must be >0'
                    self._ServerLocker__process_client_request(request=received, connection=connection)
                except Exception as err:
                    try:
                        self._error('Unable to serve locker client request (%s)' % err)
                        continue
                    finally:
                        err = None
                        del err

        try:
            with self._ServerLocker__pathsLUTLock:
                if self._ServerLocker__pathsLUT is not None:
                    for p in list(self._ServerLocker__pathsLUT):
                        if self._ServerLocker__pathsLUT[p]['client_unique_name'] == clientUniqueName:
                            self._warn(("Lock on path '%s' is released. Server no more serving client '%s:%s'" % (path, clientName, clientUniqueName)), force=True)
                            self._ServerLocker__pathsLUT.pop(p)

        except Exception as err:
            try:
                self._error("Unable to clean locks after locker client '%s:%s' (%s)" % (clientName, clientUniqueName, err))
            finally:
                err = None
                del err

        try:
            with self._ServerLocker__clientsQueueLock:
                queue = []
                for req in self._ServerLocker__clientsQueue:
                    if req['client_unique_name'] == clientUniqueName:
                        self._warn(("Queued request to lock path '%s' is removed. locker server no more serving locker client '%s:%s'" % (path, clientName, clientUniqueName)), force=True)
                    else:
                        queue.append(q)

                self._ServerLocker__clientsQueue = queue
                self._ServerLocker__clientsQueueEvent.set()
        except Exception as err:
            try:
                self._error("Unable to clean queue after locker client '%s:%s' (%s)" % (clientName, clientUniqueName, err))
            finally:
                err = None
                del err

        try:
            with self._ServerLocker__clientsLUTLock:
                if self._ServerLocker__clientsLUT is not None:
                    client = self._ServerLocker__clientsLUT.pop(clientUniqueName, None)
                    if client is not None:
                        client['connection'].close()
        except Exception as err:
            try:
                self._error("Unable to clean after locker client '%s:%s' (%s)" % (clientName, clientUniqueName, err))
            finally:
                err = None
                del err

    @_reconnect_client
    def __listen_to_server(self):
        assert self._ServerLocker__connection is not None, 'connection must not be None. PLEASE REPORT'
        self._ServerLocker__wasClient = True
        error = None
        while not self._killSignal:
            try:
                received = self._ServerLocker__connection.recv()
            except EOFError as err:
                try:
                    error = 'Connection end of file encountered (%s)' % err
                    break
                finally:
                    err = None
                    del err

            except IOError as err:
                try:
                    error = 'Connection IO Error encountered (%s)' % err
                    break
                finally:
                    err = None
                    del err

            except Exception as err:
                try:
                    error = 'Connection recv Error encountered (%s)' % err
                    break
                finally:
                    err = None
                    del err

            try:
                self._ServerLocker__process_server_response(received)
            except Exception as err:
                try:
                    self._error('Received from locker server is not accepted (%s)' % err)
                    continue
                finally:
                    err = None
                    del err

        if error is not None:
            self._critical(error)
        self._stop_client()

    @_reconnect_server
    def __wait_for_clients(self):
        self._stopServing = False
        self._ServerLocker__pathsLUT = {}
        self._ServerLocker__clientsLUT = {}
        while not self._stopServing:
            if not self._killSignal:
                try:
                    connection = self._ServerLocker__server.accept()
                    if connection is None:
                        continue
                    try:
                        information = connection.recv()
                    except Exception as err:
                        try:
                            self._critical('Unable to receive locker client name. Connection refused (%s)' % (err,))
                            connection.close()
                            continue
                        finally:
                            err = None
                            del err

                    if not isinstance(information, dict):
                        self._critical("locker client information must be a dictionary, '%s' is given. Connection refused" % (information,))
                        connection.close()
                        continue
                    clientName = information.get('name', None)
                    if not isinstance(clientName, basestring):
                        self._critical('locker client name must be given')
                        connection.close()
                        continue
                    clientUniqueName = information.get('unique_name', None)
                    if not isinstance(clientUniqueName, basestring):
                        self._critical('Client unique name must be given')
                        connection.close()
                        continue
                    try:
                        connection.send({'server_file':self._ServerLocker__serverFile,  'server_name':self._ServerLocker__name,  'server_unique_name':self._ServerLocker__uniqueName,  'lock_maximum_acquired_time':self._ServerLocker__maxLockTime})
                    except Exception as err:
                        try:
                            self._critical("Unable to send locker client '%s:%s' the locker server unique name (%s). Connection refused" % (clientName, clientUniqueName, err))
                            connection.close()
                            continue
                        finally:
                            err = None
                            del err

                    with self._ServerLocker__clientsLUTLock:
                        if clientUniqueName in self._ServerLocker__clientsLUT:
                            self._critical("locker client name '%s:%s' is already registered. Connection refused" % (clientName, clientUniqueName))
                            connection.close()
                            continue
                        clientUTCTime = time.time()
                        trd = _LockerThread(locker=self, target=(self._ServerLocker__serve_client), args=[connection, clientName, clientUniqueName], name=('serve_client_%s' % clientUTCTime))
                        self._ServerLocker__clientsLUT[clientUniqueName] = {'connection':connection,  'thread':trd,  'client_accepted_utctime':clientUTCTime,  'client_name':clientName,  'client_unique_name':clientUniqueName}
                        trd.start()
                except socket.timeout as err:
                    try:
                        self._error("Connection timeout '%s' this should have no effect on the locker if otherwise please report" % (err,))
                        continue
                    finally:
                        err = None
                        del err

                except Exception as err:
                    try:
                        self._critical('locker server is down (%s)' % err)
                        break
                    finally:
                        err = None
                        del err

    @_reconnect_server
    def __acquired_locks_max_time_monitor(self):
        while not self._stopServing:
            if not self._killSignal:
                expired = {}
                minimum = None
                with self._ServerLocker__pathsLUTLock:
                    self._ServerLocker__deadLockEvent.set()
                    self._ServerLocker__deadLockEvent.clear()
                    if self._ServerLocker__pathsLUT is None:
                        self._warn('pathsLUT is found None, server is down!')
                        break
                    exceeded = {}
                    for key in list(self._ServerLocker__pathsLUT):
                        pldata = self._ServerLocker__pathsLUT[key]
                        remain = self._ServerLocker__maxLockTime - (time.time() - pldata['acquired_utctime'])
                        if remain <= 0:
                            _ = self._ServerLocker__pathsLUT.pop(key)
                            d = exceeded.setdefault(pldata['client_unique_name'], {'client_name':pldata['client_name'],  'connection':pldata['connection'],  'ruid':{}})
                            _ = d['ruid'].setdefault(pldata['request_unique_id'], pldata['path'])
                        elif minimum is None:
                            minimum = (
                             remain, pldata)
                        elif minimum[0] > remain:
                            minimum = (
                             remain, pldata)

                    for _cuname in exceeded:
                        _cname = exceeded[_cuname]['client_name']
                        responses = []
                        for _reqId in exceeded[_cuname]['ruid']:
                            responses.append({'action':'exceeded_maximum_lock_time',  'path':exceeded[_cuname]['ruid'][_reqId], 
                             'client_unique_name':_cuname, 
                             'client_name':_cname, 
                             'request_unique_id':_reqId})

                        _connection = exceeded[_cuname]['connection']
                        try:
                            if _connection is None:
                                self._ServerLocker__process_server_response(responses)
                            else:
                                _connection.send(responses)
                        except Exception as err:
                            try:
                                self._critical("Unable to inform client '%s:%s' about releasing locks %s because it has been acquired longer than maximum locking time '%s'" % (_cname, _cuname, exceeded[_cuname]['request_unique_id'], self._ServerLocker__maxLockTime))
                            finally:
                                err = None
                                del err

                        else:
                            _luids = [i['request_unique_id'] for i in responses]
                            _paths = [i['path'] for i in responses]
                            self._warn('Locks %s requested by client %s:%s for all paths %s are released by server because maximum lock time is exceed and the lock is required by another client' % (_luids, _cname, _cuname, _paths))

                if minimum is None:
                    self._warn('WATING for 100 sec. FOR NEW EVENT.')
                    minimum = (100, None)
                else:
                    self._warn('WATING FOR %s secs. for %s' % (minimum[0], minimum[1]))
                with self._ServerLocker__clientsQueueLock:
                    self._ServerLocker__clientsQueueEvent.set()
                    self._ServerLocker__clientsQueueEvent.clear()
                self._ServerLocker__deadLockEvent.wait(minimum[0])

    @_reconnect_server
    def __launch_queue_monitor(self):
        while not self._stopServing:
            if not self._killSignal:
                self._ServerLocker__clientsQueueEvent.wait(100)
                with self._ServerLocker__clientsQueueLock:
                    self._ServerLocker__clientsQueueEvent.set()
                    self._ServerLocker__clientsQueueEvent.clear()
                    queueRemaining = []
                    for request in self._ServerLocker__clientsQueue:
                        requestCName = request['client_name']
                        requestCUName = request['client_unique_name']
                        requestRuid = request['request_unique_id']
                        requestPath = request['path']
                        if time.time() - request['request_utctime'] >= request['timeout']:
                            self._warn("Request id '%s' from client '%s:%s' timeout has expired. Lock is not acquired and request is removed from the queue" % (requestRuid, requestCName, requestCUName))
                            continue
                        with self._ServerLocker__pathsLUTLock:
                            canLock = True
                            for p in requestPath:
                                if p in self._ServerLocker__pathsLUT:
                                    canLock = False

                            if not canLock:
                                queueRemaining.append(request)
                                continue
                            else:
                                acquiredUTCTime = time.time()
                                for p in requestPath:
                                    _pathLockDict = {'lock_of_path':p,  'acquired_utctime':acquiredUTCTime}
                                    _pathLockDict.update(request)
                                    self._ServerLocker__pathsLUT[p] = _pathLockDict

                            try:
                                request['action'] = 'acquired'
                                connection = request.pop('connection')
                                if connection is None:
                                    self._ServerLocker__process_server_response(received=[request])
                                else:
                                    connection.send(request)
                            except Exception as err:
                                try:
                                    for p in requestPath:
                                        _ = self._ServerLocker__pathsLUT.pop(p)

                                    self._error("Unable to inform client '%s:%s' about lock id '%s' locking %s being acquired (%s)" % (requestCName, requestCUName, requestRuid, requestPath, err))
                                finally:
                                    err = None
                                    del err

                            else:
                                self._info("Client '%s:%s' acquired lock '%s' locking for all %s" % (requestCName, requestCUName, requestRuid, requestPath))

                    self._ServerLocker__clientsQueue = queueRemaining

    @_reconnect_server
    def __update_severfile_fingerprint--- This code section failed: ---

 L. 839         0  LOAD_FAST                'self'
                2  LOAD_ATTR                fingerprint
                4  STORE_FAST               'fingerprint'

 L. 840         6  LOAD_FAST                'self'
                8  LOAD_ATTR                _ServerLocker__serverFile
               10  STORE_FAST               'serverFile'

 L. 841        12  LOAD_CONST               None
               14  STORE_FAST               'now'

 L. 842        16  LOAD_FAST                'self'
               18  LOAD_ATTR                _ServerLocker__server
               20  STORE_FAST               'server'

 L. 844        22  LOAD_CONST               True
               24  LOAD_FAST                'self'
               26  STORE_ATTR               _ServerLocker__wasServer

 L. 845        28  LOAD_FAST                'self'
               30  LOAD_METHOD              _warn
               32  LOAD_STR                 'Starting as a server @%s:%s'
               34  LOAD_FAST                'self'
               36  LOAD_ATTR                _ServerLocker__address
               38  LOAD_FAST                'self'
               40  LOAD_ATTR                _ServerLocker__port
               42  BUILD_TUPLE_2         2 
               44  BINARY_MODULO    
               46  CALL_METHOD_1         1  ''
               48  POP_TOP          

 L. 846     50_52  SETUP_LOOP          350  'to 350'
               54  LOAD_FAST                'self'
               56  LOAD_ATTR                _stopServing
            58_60  POP_JUMP_IF_TRUE    348  'to 348'
               62  LOAD_FAST                'self'
               64  LOAD_ATTR                _killSignal
            66_68  POP_JUMP_IF_TRUE    348  'to 348'

 L. 847        70  SETUP_EXCEPT        292  'to 292'

 L. 848        72  LOAD_FAST                'self'
               74  LOAD_ATTR                _ServerLocker__server
               76  LOAD_CONST               None
               78  COMPARE_OP               is
               80  POP_JUMP_IF_FALSE    84  'to 84'

 L. 849        82  BREAK_LOOP       
             84_0  COME_FROM            80  '80'

 L. 850        84  LOAD_FAST                'self'
               86  LOAD_ATTR                _ServerLocker__server
               88  LOAD_ATTR                _listener
               90  LOAD_CONST               None
               92  COMPARE_OP               is
               94  POP_JUMP_IF_FALSE    98  'to 98'

 L. 851        96  BREAK_LOOP       
             98_0  COME_FROM            94  '94'

 L. 852        98  LOAD_FAST                'now'
              100  LOAD_CONST               None
              102  COMPARE_OP               is-not
              104  POP_JUMP_IF_FALSE   200  'to 200'

 L. 853       106  LOAD_FAST                'self'
              108  LOAD_ATTR                get_running_server_fingerprint
              110  LOAD_FAST                'serverFile'
              112  LOAD_CONST               False
              114  LOAD_CONST               ('serverFile', 'raiseNotFound')
              116  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              118  UNPACK_SEQUENCE_5     5 
              120  STORE_FAST               'uniqueName'
              122  STORE_FAST               'timestamp'
              124  STORE_FAST               'address'
              126  STORE_FAST               'port'
              128  STORE_FAST               'pid'

 L. 854       130  LOAD_FAST                'uniqueName'
              132  LOAD_FAST                'self'
              134  LOAD_ATTR                uniqueName
              136  COMPARE_OP               !=
              138  POP_JUMP_IF_TRUE    186  'to 186'
              140  LOAD_FAST                'address'
              142  LOAD_FAST                'self'
              144  LOAD_ATTR                _ServerLocker__address
              146  COMPARE_OP               !=
              148  POP_JUMP_IF_TRUE    186  'to 186'
              150  LOAD_FAST                'port'
              152  LOAD_GLOBAL              str
              154  LOAD_FAST                'self'
              156  LOAD_ATTR                _ServerLocker__port
              158  CALL_FUNCTION_1       1  ''
              160  COMPARE_OP               !=
              162  POP_JUMP_IF_TRUE    186  'to 186'
              164  LOAD_FAST                'pid'
              166  LOAD_GLOBAL              str
              168  LOAD_FAST                'self'
              170  LOAD_ATTR                _ServerLocker__pid
              172  CALL_FUNCTION_1       1  ''
              174  COMPARE_OP               !=
              176  POP_JUMP_IF_TRUE    186  'to 186'
              178  LOAD_FAST                'timestamp'
              180  LOAD_FAST                'now'
              182  COMPARE_OP               !=
              184  POP_JUMP_IF_FALSE   200  'to 200'
            186_0  COME_FROM           176  '176'
            186_1  COME_FROM           162  '162'
            186_2  COME_FROM           148  '148'
            186_3  COME_FROM           138  '138'

 L. 855       186  LOAD_GLOBAL              Exception
              188  LOAD_STR                 "server fingerprint has changed. This shouldn't have happened unless you or another process mistakenly changed '%s'. PLEASE REPORT"
              190  LOAD_FAST                'serverFile'
              192  BUILD_TUPLE_1         1 
              194  BINARY_MODULO    
              196  CALL_FUNCTION_1       1  ''
              198  RAISE_VARARGS_1       1  ''
            200_0  COME_FROM           184  '184'
            200_1  COME_FROM           104  '104'

 L. 856       200  LOAD_FAST                'self'
              202  LOAD_ATTR                _ServerLocker__serverFileLock
              204  SETUP_WITH          272  'to 272'
              206  POP_TOP          

 L. 857       208  LOAD_GLOBAL              open
              210  LOAD_FAST                'serverFile'
              212  LOAD_STR                 'w'
              214  CALL_FUNCTION_2       2  ''
              216  SETUP_WITH          262  'to 262'
              218  STORE_FAST               'fd'

 L. 858       220  LOAD_GLOBAL              str
              222  LOAD_GLOBAL              time
              224  LOAD_METHOD              time
              226  CALL_METHOD_0         0  ''
              228  CALL_FUNCTION_1       1  ''
              230  STORE_FAST               'now'

 L. 859       232  LOAD_FAST                'fd'
              234  LOAD_METHOD              write
              236  LOAD_FAST                'fingerprint'
              238  LOAD_ATTR                format
              240  LOAD_FAST                'now'
              242  LOAD_GLOBAL              str
              244  LOAD_FAST                'self'
              246  LOAD_ATTR                _ServerLocker__port
              248  CALL_FUNCTION_1       1  ''
              250  LOAD_CONST               ('now', 'port')
              252  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              254  CALL_METHOD_1         1  ''
              256  POP_TOP          
              258  POP_BLOCK        
              260  LOAD_CONST               None
            262_0  COME_FROM_WITH      216  '216'
              262  WITH_CLEANUP_START
              264  WITH_CLEANUP_FINISH
              266  END_FINALLY      
              268  POP_BLOCK        
              270  LOAD_CONST               None
            272_0  COME_FROM_WITH      204  '204'
              272  WITH_CLEANUP_START
              274  WITH_CLEANUP_FINISH
              276  END_FINALLY      

 L. 861       278  LOAD_GLOBAL              time
              280  LOAD_METHOD              sleep
              282  LOAD_CONST               2
              284  CALL_METHOD_1         1  ''
              286  POP_TOP          
              288  POP_BLOCK        
              290  JUMP_BACK            54  'to 54'
            292_0  COME_FROM_EXCEPT     70  '70'

 L. 862       292  DUP_TOP          
              294  LOAD_GLOBAL              Exception
              296  COMPARE_OP               exception-match
          298_300  POP_JUMP_IF_FALSE   344  'to 344'
              302  POP_TOP          
              304  STORE_FAST               'err'
              306  POP_TOP          
              308  SETUP_FINALLY       332  'to 332'

 L. 863       310  LOAD_FAST                'self'
              312  LOAD_METHOD              _critical
              314  LOAD_STR                 'Unable to update serverfile fingerprint (%s)'
              316  LOAD_FAST                'err'
              318  BUILD_TUPLE_1         1 
              320  BINARY_MODULO    
              322  CALL_METHOD_1         1  ''
              324  POP_TOP          

 L. 864       326  BREAK_LOOP       
              328  POP_BLOCK        
              330  LOAD_CONST               None
            332_0  COME_FROM_FINALLY   308  '308'
              332  LOAD_CONST               None
              334  STORE_FAST               'err'
              336  DELETE_FAST              'err'
              338  END_FINALLY      
              340  POP_EXCEPT       
              342  JUMP_BACK            54  'to 54'
            344_0  COME_FROM           298  '298'
              344  END_FINALLY      
              346  JUMP_BACK            54  'to 54'
            348_0  COME_FROM            66  '66'
            348_1  COME_FROM            58  '58'
              348  POP_BLOCK        
            350_0  COME_FROM_LOOP       50  '50'

Parse error at or near `COME_FROM' instruction at offset 200_0

    def __serve_or_connect(self, ntrials=3):
        if self._ServerLocker__wasServer:
            self._warn('Re-connecting previous server is not allowed.')
            return
            if not self.canServe:
                assert self._ServerLocker__server is None, 'This locker instance is not allowed to serve but server is not None. PLEASE REPORT'
                if self._ServerLocker__serverFile is None:
                    self._warn('Unable to serve nor to connect. serverFile is not defined', force=True)
                    return
        elif not self._ServerLocker__pathsLUT is None:
            raise AssertionError('paths look up table must be not defined')
        assert isinstance(ntrials, int), 'LockerServer ntrials must be integer'
        assert ntrials > 0, 'LockerServer ntrials must be >0'
        self._stop_server()
        fingerprint = self.fingerprint
        serverFile = self._ServerLocker__serverFile
        connectStart = None
        nowTimestamp = None
        nowPort = None
        serverTrials = ntrials
        clientTrials = ntrials
        while 1:
            uniqueName, timestamp, address, port, pid = self.get_running_server_fingerprint(serverFile=serverFile, raiseNotFound=False, raiseError=False)
            try:
                diff = time.time() - float(timestamp)
            except:
                diff = 10

            if self.canServe and not uniqueName is None:
                if not address is None:
                    if not uniqueName != self._ServerLocker__uniqueName or diff >= 2:
                        connectStart = None
                        with self._ServerLocker__serverFileLock:
                            with open(serverFile, 'w') as (fd):
                                fd.write(fingerprint.format(now='TIMESTAMP', port='PORT'))
                        time.sleep(0.001)
                        continue
                elif self.canServe:
                    if uniqueName == self._ServerLocker__uniqueName:
                        connectStart = None
                        if address == self._ServerLocker__address or address is None:
                            if not pid == str(self._ServerLocker__pid):
                                if not pid is None:
                                    raise AssertionError('LockerServer uniqueName clash encountered')
                            if timestamp == 'TIMESTAMP' or timestamp is None:
                                assert nowTimestamp is None, 'locker timestamp is assigned before initial serverFile is wrote. PLEASE REPORT'
                                nowTimestamp = time.time()
                                with self._ServerLocker__serverFileLock:
                                    with open(serverFile, 'w') as (fd):
                                        fd.write(fingerprint.format(now=(str(nowTimestamp)), port='PORT'))
                                time.sleep(0.001)
                                continue
                        elif port == 'PORT':
                            assert nowPort is None, 'locker timestamp is assigned before port write to servefFile. PLEASE REPORT'
                            assert timestamp == str(nowTimestamp), "locker timestamp '%s' not matching registered one '%s'. PLEASE REPORT" % (str(timestamp), nowTimestamp)
                            port = self._ServerLocker__port
                            while serverTrials:
                                serverTrials -= 1
                                try:
                                    port = self._ServerLocker__get_first_available_port(address='', start=port, end=65535, step=1)
                                    self._ServerLocker__server = Listener((self._ServerLocker__address, port), family='AF_INET', authkey=(self._ServerLocker__password))
                                except Exception as err:
                                    try:
                                        if serverTrials:
                                            self._warn('Unable to launch server @address:%s @port:%s (%s)' % (self._ServerLocker__address, port, err))
                                            continue
                                        else:
                                            self._warn('Unable to launch server (%s)' % err)
                                            return
                                    finally:
                                        err = None
                                        del err

                                break

                            nowPort = time.time()
                            with self._ServerLocker__serverFileLock:
                                with open(serverFile, 'w') as (fd):
                                    fd.write(fingerprint.format(now=nowPort, port=(str(port))))
                            self._ServerLocker__port = port
                            self._stopServing = False
                            trd = _LockerThread(locker=self, target=(self._ServerLocker__wait_for_clients), name='wait_for_clients')
                            trd.start()
                            time.sleep(0.001)
                            continue
                        else:
                            if port == str(self._ServerLocker__port):
                                assert timestamp == str(nowPort), "locker timestamp '%s' for port not matching registered one '%s'. PLEASE REPORT" % (str(nowPort), timestamp)
                                trd = _LockerThread(locker=self, target=(self._ServerLocker__launch_queue_monitor), name='launch_queue_monitor')
                                trd.start()
                                trd = _LockerThread(locker=self, target=(self._ServerLocker__acquired_locks_max_time_monitor), name='acquired_locks_max_time_monitor')
                                trd.start()
                                self._ServerLocker__serverMaxLockTime = self._ServerLocker__maxLockTime
                                if self._ServerLocker__blocking:
                                    self._ServerLocker__update_severfile_fingerprint()
                                else:
                                    trd = _LockerThread(locker=self, target=(self._ServerLocker__update_severfile_fingerprint), name='update_severfile_fingerprint')
                                    trd.start()
                                return
                            self._stop_server()
                            raise Exception("locker port has changed! This shouldn't have happened!! PLEASE REPORT")
                if clientTrials > 0:
                    if self._ServerLocker__server is not None:
                        self._stop_server()
                    elif connectStart is None:
                        connectStart = time.time()
                    elif not time.time() - connectStart <= self._ServerLocker__connectTimeout:
                        raise AssertionError('locker exceeding allowed trying to connect timeout (%s)' % (self._ServerLocker__connectTimeout,))
                    else:
                        if not timestamp in ('TIMESTAMP', None):
                            if port in ('PORT', None) or address is None:
                                time.sleep(0.01)
                                continue
                        else:
                            connected = False
                            try:
                                clientTrials -= 1
                                connected = self.connect(address=address, port=(int(port)), ntrials=ntrials)
                            except Exception as err:
                                try:
                                    self._error('Unable to connect to server (%s)' % err)
                                finally:
                                    err = None
                                    del err

                        if connected:
                            break
                        else:
                            continue
                else:
                    break

    def __get_ip_address(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.connect(('10.255.255.255', 1))
            IP = s.getsockname()[0]
        except:
            IP = '127.0.0.1'
        else:
            s.shutdown(socket.SHUT_RDWR)
            s.close()
        return IP

    def __is_port_open(self, address='', port=5555):
        isOpen = False
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            try:
                s.bind((address, port))
            except:
                isOpen = False
            else:
                isOpen = True
        finally:
            s.close()

        return isOpen

    def __get_first_available_port(self, address='', start=10000, end=65535, step=1):
        isOpen = False
        port = start - step
        while not isOpen:
            port += step
            if port > end:
                break
            isOpen = self._ServerLocker__is_port_open(address=address, port=port)

        if not isOpen:
            port = None
        return port

    @property
    def debugMode(self):
        """debug mode flag"""
        return self._ServerLocker__debugMode

    @debugMode.setter
    def debugMode(self, value):
        assert isinstance(value, bool), 'debugMode value must be boolean'
        self._ServerLocker__debugMode = value

    @property
    def name(self):
        """locker user given name"""
        return self._ServerLocker__name

    @property
    def fingerprint(self):
        """server locker fingerprint"""
        return '%s({now})@%s:{port}[%s]' % (self._ServerLocker__uniqueName, self._ServerLocker__address, self._ServerLocker__pid)

    @property
    def canServe(self):
        """whether this instance can serve"""
        return self._ServerLocker__allowServing and self._ServerLocker__serverFile is not None and not self._ServerLocker__wasClient

    @property
    def uniqueName(self):
        """locker unique name"""
        return self._ServerLocker__uniqueName

    @property
    def serverFile(self):
        """serverlocker server file"""
        return self._ServerLocker__serverFile

    @property
    def pid(self):
        """python process pid"""
        return self._ServerLocker__pid

    @property
    def serverAddress(self):
        """this instance machine address"""
        return self._ServerLocker__serverAddress

    @property
    def serverPort(self):
        """this instance machine port"""
        return self._ServerLocker__serverPort

    @property
    def serverUniqueName(self):
        """server unique name"""
        return self._ServerLocker__serverUniqueName

    @property
    def serverName(self):
        """server user given name"""
        return self._ServerLocker__serverName

    @property
    def serverMaxLockTime(self):
        """server maximum allowed lock time"""
        return self._ServerLocker__serverMaxLockTime

    @property
    def address(self):
        """locker instance machine address"""
        return self._ServerLocker__address

    @property
    def port(self):
        """locker instance port"""
        return self._ServerLocker__port

    @property
    def password(self):
        """locker password"""
        return self._ServerLocker__password

    @property
    def defaultTimeout(self):
        """locker timeout in seconds"""
        return self._ServerLocker__defaultTimeout

    @property
    def maxLockTime(self):
        """locker maximum locking time in seconds"""
        return self._ServerLocker__maxLockTime

    @property
    def isServer(self):
        """Whether this instance is being the lock server or a client"""
        return self._ServerLocker__server is not None

    @property
    def isClient(self):
        """Whether this instance is being the lock client to a running server"""
        return self._ServerLocker__connection is not None

    @property
    def messages(self):
        """get list of received published messages"""
        return list(self._ServerLocker__publications)

    @property
    def lockedPaths(self):
        """dictionary copy of currently acquired locks by all clients including
        self. This will return None if this locker is not the locker server.
        Keys are paths and values are a dictionary of locks id and client
        name and client unique name"""
        locks = None
        with self._ServerLocker__pathsLUTLock:
            if self._ServerLocker__pathsLUT is not None:
                locks = {}
                for p in self._ServerLocker__pathsLUT:
                    pl = self._ServerLocker__pathsLUT[p]
                    locks[p] = {'lock_unique_id':pl['request_unique_id'],  'client_name':pl['client_name'], 
                     'client_unique_name':pl['client_unique_name']}

        return locks

    @property
    def ownedLocks(self):
        """dictionary copy of currently acquired locks by this locker.
        keys are locks unique ids and value are path list"""
        with self._ServerLocker__ownRequestsLock:
            locks = dict([(lid, self._ServerLocker__ownAcquired[lid]['path']) for lid in self._ServerLocker__ownAcquired])
        return locks

    @property
    def clientLocks(self):
        """dictionary copy of currently acquired locks by all clients including
        self This will return None if this locker is not the locker server.
        keys are unique locks id and values are the list of paths"""
        locks = None
        with self._ServerLocker__pathsLUTLock:
            if self._ServerLocker__pathsLUT is not None:
                locks = {}
                for p in self._ServerLocker__pathsLUT:
                    pl = self._ServerLocker__pathsLUT[p]
                    ps = locks.setdefault(pl['request_unique_id'], {'client_name':pl['client_name'],  'client_unique_name':pl['client_unique_name'],  'path':[]})['path']
                    ps.append(p)

        return locks

    def _parse_fingerprint(self, fingerprint):
        """parse server fingerprint information"""
        uniqueName, s = fingerprint.split('(')
        timestamp, s = s.split(')')
        address, s = s[1:].split(':')
        port, s = s.split('[')
        pid = s.split(']')[0]
        return (
         uniqueName, timestamp, address, port, pid)

    def get_running_server_fingerprint(self, serverFile=None, raiseNotFound=False, raiseError=True):
        """get running server fingerprint information

        :Parameters:
           #. serverFile (None, string): Path to the locker server file. If
              None is given, this instance serverFile will be used unless it's
              not defined then an error will be raised
           #. raiseNotFound (boolean): Whether to raise an error if file was
              not found
           #. raiseError (boolean): Whether to raise an error upon reading
              and parsing the server file data

        :Returns:
           #. uniqueName (string): the running server unique name
           #. timestamp (string): the running server last saved utc timestamp.
              this must be float castable
           #. address (string): the ip address of the running locker server
           #. port (string): the running server port number. This must be integer
              castable
           #. pid (int): the running server process identification number

        **N.B All returned information can be None if serverFile was not found or if an error parsing the information occured**
        """
        if serverFile is None:
            serverFile = self._ServerLocker__serverFile
        else:
            assert serverFile is not None, 'given serverFile is None while object serverFile is not defined'
            uniqueName = timestamp = address = port = pid = None
            if os.path.isfile(serverFile):
                try:
                    with self._ServerLocker__serverFileLock:
                        with open(serverFile, 'r') as (fd):
                            fingerprint = fd.readlines()[0].strip()
                    uniqueName, timestamp, address, port, pid = self._parse_fingerprint(fingerprint)
                except Exception as err:
                    try:
                        if raiseError:
                            raise AssertionError(str(err))
                    finally:
                        err = None
                        del err

            elif raiseNotFound:
                raise Exception("Given serverFile '%s' is not found on disk" % serverFile)
        return (
         uniqueName, timestamp, address, port, pid)

    def set_maximum_lock_time(self, maxLockTime):
        """
        Set maximum allowed time for a lock to be acquired

        :Parameters:
            #. maxLockTime (number): The maximum number of seconds allowed for
               any lock to be acquired
        """
        try:
            maxLockTime = float(maxLockTime)
            assert maxLockTime > 0
        except:
            raise Exception('maxLockTime must be a positive number')

        self._ServerLocker__maxLockTime = maxLockTime

    def set_default_timeout(self, defaultTimeout):
        """
        Set default timeout to acquire a lock

        :Parameters:
            #. maxLockTime (number): the default timeout in seconds for a lock
               to be acquired
        """
        try:
            defaultTimeout = float(defaultTimeout)
            assert defaultTimeout > 0
        except:
            raise Exception('defaultTimeout must be a positive number')

        self._ServerLocker__defaultTimeout = defaultTimeout

    def set_server_file(self, serverFile):
        """set server file path

        :Parameters:
           #. serverFile (boolean, string): If True it will be set to
              '.pylocker.serverlocker' in user's home directory. If False, this
              instance will never serve. If string is given, it's the path to the
              serving locker file if existing. When given whether as a string
              or as True, and if this instance is allowed to serve then whenever
              'start' is called, this instance will try to become the serving
              locker unless another instance is serving already then it will
              try to connect.
        """
        if self.isServer or self.isClient:
            raise AssertionError('not allowed to set serverFile when instance is a server or a client')
        if serverFile is True:
            serverFile = os.path.join(os.path.expanduser('~'), '.pylocker.serverlocker')
        elif serverFile is False:
            serverFile = None
        else:
            assert isinstance(serverFile, basestring), 'serverFile must be boolean or a string'
            directory = os.path.dirname(serverFile)
            if not os.path.exists(directory):
                os.makedirs(directory)
        self._ServerLocker__serverFile = serverFile

    def stop(self):
        """Stop server and client connections"""
        self._killSignal = True
        self._stop_server(reconnect=False)
        self._stop_client(reconnect=False)

    def start(self, address=None, port=None, password=None, ntrials=3):
        """start locker as server (if allowed) or a client in case there
        is running server. If both, address and port are None and no server
        is found in the server file, the this instance is going to be the
        server

        :Parameters:
           #. address (None, string): ip address of server to connect to
           #. port (None, integer): port used by the server socket
           #. password (None, string): in case both address and port are not
              None, password is the server password. If None is given, the
              instanciation password is provided.
        """
        if self.isServer:
            self._warn("locker '%s:%s' is already a running server" % (self._ServerLocker__name, self._ServerLocker__uniqueName))
        elif self.isClient:
            self._warn("locker '%s' is already a client to the running server '%s:%s'" % (self._ServerLocker__uniqueName, self._ServerLocker__serverName, self._ServerLocker__serverUniqueName))
        else:
            self.reset()
            if address is not None or port is not None:
                if not (address is not None and port is not None):
                    raise AssertionError('locker address and port can be either both None or both given')
                self.connect(address=adress, port=port, password=password, ntrials=ntrials)
            else:
                self._ServerLocker__serve_or_connect(ntrials=ntrials)

    def connect(self, address, port, password=None, ntrials=3):
        """connect to a serving locker whether it's local or remote

        :Parameters:
            #. address (string): serving locker ip address
            #. port (integer): serving locker connection port
            #. password (None, string): serving locker password. If None,
               this instance password will be used. If given, this instance
               password will be updated
            #. ntrials (integer): number of trials to connect

        :Returns:
            #. result (boolean): whether connection was successful
        """
        if not self._ServerLocker__connection is None:
            raise AssertionError("locker unable to connect to server, logger is connected to server '%s:%s'" % (self._ServerLocker__serverName, self._ServerLocker__serverUniqueName))
        else:
            if password is None:
                password = self._ServerLocker__password
            if not isinstance(password, bytes):
                assert isinstance(password, str), 'locker password must be string or bytes'
                password = _to_bytes(password)
            assert isinstance(port, int), 'locker port must be integer'
            success = False
            while ntrials:
                ntrials -= 1
                try:
                    _start = time.time()
                    connection = Client((address, port), authkey=(self._ServerLocker__password))
                    connection.send({'name':self._ServerLocker__name,  'unique_name':self._ServerLocker__uniqueName})
                    params = connection.recv()
                    assert isinstance(params, dict), 'locker received server params must be a dictionary'
                    assert 'server_name' in params, "locker received server params must have 'server_name' key"
                    serverName = params['server_name']
                    assert 'server_unique_name' in params, "locker received server params must have 'server_unique_name' key"
                    serverUniqueName = params['server_unique_name']
                    assert 'lock_maximum_acquired_time' in params, "locker received server params must have 'lock_maximum_acquired_time' key"
                    serverMaxLockTime = params['lock_maximum_acquired_time']
                    assert isinstance(serverName, basestring), 'locker received serverName must be a string'
                    assert isinstance(serverMaxLockTime, (float, int)), 'locker received serverMaxLockTime must be a number'
                    assert serverMaxLockTime > 0, 'locker received serverMaxLockTime must be >0'
                    assert 'server_file' in params, "locker received server params must have 'server_file' key"
                    serverFile = params['server_file']
                    assert isinstance(serverFile, basestring), 'locker received serverFile must be a string'
                    serverMaxLockTime = float(serverMaxLockTime)
                    serverName = _to_unicode(serverName)
                    serverUniqueName = _to_unicode(serverUniqueName)
                    if self._ServerLocker__maxLockTime != serverMaxLockTime:
                        self._warn("Server maximum allowed lock time is '%s' is different than this locker '%s'" % (serverMaxLockTime, self._ServerLocker__maxLockTime))
                    if self._ServerLocker__address == address:
                        if serverFile != self._ServerLocker__serverFile:
                            if self._ServerLocker__serverFile is not None:
                                self._warn("locker serverFile is updated from '%s' to '%s' after connecting to server %s:%s" % (self._ServerLocker__serverFile, serverFile, serverName, serverUniqueName))
                                self._ServerLocker__serverFile = serverFile
                except Exception as err:
                    try:
                        _dt = time.time() - _start
                        success = False
                        self._error(err, stack=(_full_stack()))
                        self._warn('locker launch client failed in %.4f sec. %i trials remaining (%s)' % (_dt, ntrials, str(err)))
                        continue
                    finally:
                        err = None
                        del err

                else:
                    success = True
                    break

            if not success:
                return False
                self._ServerLocker__connection = connection
                self._ServerLocker__password = password
                self._ServerLocker__serverUniqueName = serverUniqueName
                self._ServerLocker__serverName = serverName
                self._ServerLocker__serverMaxLockTime = serverMaxLockTime
                self._ServerLocker__serverAddress = address
                self._ServerLocker__serverPort = port
                self._warn("locker connecting as a client to '%s' @%s:%s" % (serverName, address, port))
                if self._ServerLocker__blocking:
                    self._ServerLocker__listen_to_server()
            else:
                trd = _LockerThread(locker=self, target=(self._ServerLocker__listen_to_server), args=(), name='__listen_to_server')
                trd.start()
        return True

    def reset(self, raiseError=False):
        """Used to recycle a disconnected client or serving locker that was
        shut down. Calling reset will insure resetting the state of the locker
        to a freshly new one. If Locker is still serving or still connected
        to a serving locker calling reset will be raise an error if raiseError
        is set to True.

        :Parameters:
            #. raiseError (boolean): whether to raise error if recyling is not
               possible

        :Returns:
            #. success (boolean): whether reset was successful
            #. error (None, string): reason why it failed.
        """
        if not isinstance(raiseError, bool):
            raise AssertionError('raiseError must be boolean')
        else:
            self._killSignal = hasattr(self, '_ServerLocker__serverFile') or False
            self._stopServing = False
            self._ServerLocker__server = None
            self._ServerLocker__connection = None
            self._ServerLocker__serverUniqueName = None
            self._ServerLocker__serverName = None
            self._ServerLocker__serverAddress = None
            self._ServerLocker__serverPort = None
            self._ServerLocker__serverMaxLockTime = None
            self._ServerLocker__transferLock = threading.Lock()
            self._ServerLocker__serverFileLock = threading.Lock()
            self._ServerLocker__wasServer = False
            self._ServerLocker__wasClient = False
            self._ServerLocker__clientsLUTLock = threading.Lock()
            self._ServerLocker__clientsLUT = None
            self._ServerLocker__pathsLUTLock = threading.Lock()
            self._ServerLocker__pathsLUT = None
            self._ServerLocker__clientsQueueLock = threading.Lock()
            self._ServerLocker__clientsQueue = []
            self._ServerLocker__clientsQueueEvent = threading.Event()
            self._ServerLocker__ownRequestsLock = threading.Lock()
            self._ServerLocker__ownRequests = {}
            self._ServerLocker__ownAcquired = {}
            self._ServerLocker__publicationsLock = threading.Lock()
            self._ServerLocker__publications = {}
            self._reconnectCounterLock = threading.Lock()
            self._reconnectCounter = 0
            self._ServerLocker__deadLockEvent = threading.Event()
            return (True, None)
        if self.isServer or self.isClient:
            message = 'Not allowed to recycle a client or a serving locker'
            if raiseError:
                raise AssertionError(message)
            return (
             False, message)
        self._killSignal = False
        self._stopServing = False
        self._ServerLocker__server = None
        self._ServerLocker__connection = None
        self._ServerLocker__serverUniqueName = None
        self._ServerLocker__serverName = None
        self._ServerLocker__serverAddress = None
        self._ServerLocker__serverPort = None
        self._ServerLocker__serverMaxLockTime = None
        if self._ServerLocker__transferLock.locked():
            self._ServerLocker__transferLock.release()
        if self._ServerLocker__serverFileLock.locked():
            self._ServerLocker__serverFileLock.release()
        self._ServerLocker__wasServer = False
        self._ServerLocker__wasClient = False
        if self._ServerLocker__clientsLUTLock.locked():
            self._ServerLocker__clientsLUTLock.release()
        self._ServerLocker__clientsLUT = None
        if self._ServerLocker__pathsLUTLock.locked():
            self._ServerLocker__pathsLUTLock.release()
        self._ServerLocker__pathsLUT = None
        if self._ServerLocker__clientsQueueLock.locked():
            self._ServerLocker__clientsQueueLock.release()
        self._ServerLocker__clientsQueue = []
        self._ServerLocker__clientsQueueEvent.set()
        self._ServerLocker__clientsQueueEvent.clear()
        if self._ServerLocker__ownRequestsLock.locked():
            self._ServerLocker__ownRequestsLock.release()
        self._ServerLocker__ownRequests = {}
        self._ServerLocker__ownAcquired = {}
        if self._reconnectCounterLock.locked():
            self._reconnectCounterLock.release()
        self._reconnectCounter = 0
        self._ServerLocker__deadLockEvent.set()
        self._ServerLocker__deadLockEvent.clear()
        return (True, None)

    def __monitor_publication_timeout(request):
        ruuid = request['request_unique_id']
        message = request['message']
        remaining = request['timeout'] - time.time() + request['request_utctime']
        if remaining > 0:
            time.sleep(remaining)
        with self._ServerLocker__publicationsLock:
            if message not in self._ServerLocker__publications:
                self._warn("monitored published message '%s' not found!" % message)
            else:
                reqList = [r for r in self._ServerLocker__publications[message] if r['request_unique_id'] != ruuid]
                if len(reqList) == len(self._ServerLocker__publications[message]):
                    self._warn("monitored published message '%s' from sender '%s' not found! Is it removed seperately by calling 'remove_published_message'?" % (message, ruuid))
                elif not len(reqList):
                    self._ServerLocker__publications.pop(message, None)
                else:
                    self._ServerLocker__publications[message] = reqList

    def __add_publication(self, request):
        message = request['message']
        unique = request['unique']
        replace = request['replace']
        timeout = request['timeout']
        with self._ServerLocker__publicationsLock:
            if unique:
                assert message not in self._ServerLocker__publications, "Given message '%s' to publish already exist" % message
            elif replace:
                self._ServerLocker__publications[message] = [
                 request]
            else:
                self._ServerLocker__publications.setdefault(message, []).append(request)
        if timeout is not None:
            trd = _LockerThread(locker=self, target=(self._ServerLocker__monitor_publication_timeout), args=(request,), name='__monitor_publication_timeout')
            trd.start()

    def remove_published_message(self, message, senders=None):
        """ Remove published message

        :Parameters:
            #. message (string): published message
            #. senders (None, list): list of senders of the message to remove
               publication from a particular sender. If None, published message
               from all senders will be removed
        """
        assert isinstance(message, basestring), 'published message must be a string'
        if senders is not None:
            assert isinstance(senders, (list, set, tuple)), 'senders must be None or a list of receivers unique name'
            assert all([isinstance(r, basestring) for r in senders]), 'senders list items must be all strings'
            senders = dict([(s, True) for s in senders])
        with self._ServerLocker__publicationsLock:
            if message not in self._ServerLocker__publications:
                self._warn("published message '%s' not found!" % message)
            else:
                reqList = self._ServerLocker__publications[message]
                if senders is None:
                    reqList = []
                else:
                    reqDict = {}
                    remList = []
                    for r in reqList:
                        reqDict.setdefault(r['request_unique_id'], []).append(r)

                    for s in senders:
                        if s not in reqDict:
                            self._warn("published message '%s' from sender '%s' not found!" % (message, s))
                            remList.extend(reqDict.pop(s))
                        else:
                            _ = reqDict.pop(s)

                    reqList = remList
                if not len(reqList):
                    self._ServerLocker__publications.pop(message, None)
                else:
                    self._ServerLocker__publications[message] = reqList

    def remove_message(self, *args, **kwargs):
        """alias to remove_published_message"""
        return (self.remove_published_message)(*args, **kwargs)

    def has_message(self, message):
        """ Get whether a message exists in list of received published messages

        :Parameters:
            #. message (string): published message

        :Returns:
            #. exist (boolean): whether message exist
        """
        return message in self._ServerLocker__publications

    def get_message(self, message):
        """get message from received published messages

        :Parameters:
            #. message (string): published message to get

        :Returns:
            #. publication (None,m dict): the message publication dictionary.
               If message does not exit, None is returned
        """
        return self._ServerLocker__publications.get(message, None)

    def pop_message(self, message):
        """pop message from received published messages

        :Parameters:
            #. message (string): published message to pop

        :Returns:
            #. publication (None,m dict): the message publication dictionary.
               If message does not exit, None is returned
        """
        return self._ServerLocker__publications.pop(message, None)

    def publish_message(self, message, receivers=None, timeout=None, toSelf=True, unique=False, replace=True):
        """publish a message to connected ServerLocker instances. This method
        makes pylocker.ServerLocker more than a locking server but a message
        passing server between threads and processes.

        :Parameters:
            #. message (string): Any message to publish
            #. receivers (None, list): List of ServerLocker instances unique name
               to publish message to. If None, all connected ServerLocker instances
               to this server or to this client server will receive the message
            #. timeout (None, number): message timeout on the receiver side.
               If timeout exceeds, receiver will automatically remove the message
               from the list of publications
            #. toSelf (boolean): whether to also publish to self
            #. unique (boolean): whether message is allowed to exist in the list
               of remaining published message of every and each receiver
               seperately
            #. replace (boolean): whether to replace existing message at
               every and each receiver

        :Returns:
            #. success (boolean): whether publishing was successful
            #. publicationUniqueId (str, int): The publication unique Id.
               If success is False, this become the integer failure code

                *  1: Connection to serving locker is unexpectedly not found.
                *  2: This ServerLocker instance is neither a client nor a server.
                *  string: any other error message.
        """
        if not isinstance(unique, bool):
            raise AssertionError('unique must be a boolean')
        elif not isinstance(toSelf, bool):
            raise AssertionError('toSelf must be a boolean')
        else:
            if not isinstance(replace, bool):
                raise AssertionError('replace must be a boolean')
            else:
                if receivers is not None:
                    assert isinstance(receivers, (list, set, tuple)), 'receivers must be None or a list of receivers unique name'
                    assert all([isinstance(r, basestring) for r in receivers]), 'receivers list items must be all strings'
                    toSelf = toSelf or 
                assert isinstance(message, basestring), 'publishing message must be a string'
                if timeout is not None:
                    assert isinstance(timeout, (int, float)), 'timeout must be a number'
                    if not timeout > 0:
                        raise AssertionError('timeout must be >0')
            utcTime = time.time()
            ruuid = str(uuid.uuid1())
            request = {'request_unique_id':ruuid,  'action':'publish', 
             'message':message, 
             'timeout':timeout, 
             'unique':unique, 
             'replace':replace, 
             'receivers':receivers, 
             'to_self':toSelf, 
             'client_unique_name':self._ServerLocker__uniqueName, 
             'client_name':self._ServerLocker__name, 
             'request_utctime':utcTime}
            if toSelf:
                self._ServerLocker__add_publication(request=request)
            try:
                if self.isServer:
                    self._ServerLocker__process_client_request(request=request, connection=None)
                elif self.isClient:
                    with self._ServerLocker__transferLock:
                        assert self._ServerLocker__connection is not None, '1'
                        self._ServerLocker__connection.send(request)
                else:
                    raise Exception('2')
            except Exception as err:
                try:
                    code = str(err)
                    try:
                        code = int(code)
                    except:
                        pass

                    return (
                     False, code)
                finally:
                    err = None
                    del err

        return (
         True, ruuid)

    def publish(self, *args, **kwargs):
        """alias to publish_message"""
        return (self.publish_message)(*args, **kwargs)

    def acquire_lock(self, path, timeout=None, lockGlobal=False):
        """ Acquire a lock for given path or list of paths. Each time the
        method a called a new lock will be acquired. This method is blocking,
        If lock on path is already acquired even from the same process the
        function will block. If lockGlobal is True, then acquiring the
        lock on a locked path by the same process won't block and will
        return successfully by all threads trying to acquire it.

        :Parameters:
            #. path (string, list): string path of list of strings to lock
            #. timeout (None, integer): timeout limit to acquire the lock. If
               None, defaultTimeout will be used
            #. lockGlobal (boolean): whether to make the acquire global to
               all threads of the same process. If True, until the lock
               expires, any thread of the same process can request the
               exact same lock path and acquire it without being blocked.
               THIS IS NOT IMPLEMENTED YET

        :Returns:
            #. success (boolean): whether locking was successful
            #. lockUniqueId (str, int): The lock unique Id. If success is False,
               this become the integer failure code

                *  0: Lock was not successfully set before timeout.
                *  1: Connection to serving locker is unexpectedly not found.
                *  2: This ServerLocker instance is neither a client nor a server.
                *  string: any other error message.
        """
        if isinstance(path, basestring):
            path = [
             path]
        elif not len(path):
            raise AssertionError('path must be given')
        else:
            assert all([isinstance(p, basestring) for p in path]), 'path must be a string or a list of string'
            path = [_to_bytes(p) for p in path]
            if timeout is None:
                timeout = self._ServerLocker__defaultTimeout
            assert isinstance(timeout, (int, float)), 'timeout must be a number'
            assert timeout > 0, 'timeout must be >0'
            utcTime = time.time()
            ruuid = str(uuid.uuid1())
            request = {'request_unique_id':ruuid,  'action':'acquire', 
             'path':path, 
             'timeout':timeout, 
             'client_unique_name':self._ServerLocker__uniqueName, 
             'client_name':self._ServerLocker__name, 
             'request_utctime':utcTime}
            with self._ServerLocker__ownRequestsLock:
                event = threading.Event()
                ownReq = {'acquired_event': event}
                ownReq.update(request)
                self._ServerLocker__ownRequests[ruuid] = ownReq
            try:
                if self.isServer:
                    self._ServerLocker__process_client_request(request=request, connection=None)
                elif self.isClient:
                    with self._ServerLocker__transferLock:
                        assert self._ServerLocker__connection is not None, '1'
                        self._ServerLocker__connection.send(request)
                else:
                    event.set()
                    with self._ServerLocker__ownRequestsLock:
                        self._ServerLocker__ownRequests.pop(ruuid, None)
                    raise Exception('2')
            except Exception as err:
                try:
                    code = str(err)
                    try:
                        code = int(code)
                    except:
                        pass

                    return (
                     False, code)
                finally:
                    err = None
                    del err

        isAcquired = event.wait(timeout)
        with self._ServerLocker__ownRequestsLock:
            self._ServerLocker__ownRequests.pop(ruuid, None)
            isAcquired = ruuid in self._ServerLocker__ownAcquired
            if not isAcquired:
                ruuid = 0
        return (isAcquired, ruuid)

    def acquire(self, *args, **kwargs):
        """alias to acquire"""
        return (self.acquire_lock)(*args, **kwargs)

    def release_lock(self, lockId):
        """ release acquired lock given its id

        :Parameters:
            #. lockId (string): Lock id as returned from acquire_lock method

        :Returns:
            #. success (boolean): whether lock is released
            #. code (int, string): reason for graceful release or failing to
               release code.

               *  0: Lock is not found, therefore successfully released
               *  1: Lock is found owned by this locker and successfully released
               *  2: Connection to serving locker is unexpectedly not found.
               *  3: Locker is neither a client nor a server
               *  string: any other error message

        """
        with self._ServerLocker__ownRequestsLock:
            request = self._ServerLocker__ownAcquired.pop(lockId, None)
            if request is None:
                return (True, 0)
            request['action'] = 'release'
            _ = request.pop('acquired_event', None)
        try:
            if self.isServer:
                self._ServerLocker__process_client_request(request=request, connection=None)
            elif self.isClient:
                with self._ServerLocker__transferLock:
                    assert self._ServerLocker__connection is not None, '2'
                    self._ServerLocker__connection.send(request)
            else:
                raise Exception('3')
        except Exception as err:
            try:
                code = str(err)
                try:
                    code = int(code)
                except:
                    pass

                return (
                 False, code)
            finally:
                err = None
                del err

        return (True, 1)

    def release(self, *args, **kwargs):
        """alias to release"""
        return (self.release_lock)(*args, **kwargs)


class SingleLocker(ServerLocker):
    """SingleLocker"""
    _SingleLocker__thisInstance = None

    def __new__(cls, *args, **kwds):
        if cls._SingleLocker__thisInstance is None:
            cls._SingleLocker__thisInstance = super(ServerLocker, cls).__new__(cls)
            cls._SingleLocker__thisInstance._isInitialized = False
        return cls._SingleLocker__thisInstance

    def __init__(self, *args, **kwargs):
        if self._isInitialized:
            return
        (super(SingleLocker, self).__init__)(*args, **kwargs)
        self._isInitialized = True


class LockersFactory(object):
    """LockersFactory"""
    _LockersFactory__thisInstance = None

    def __new__(cls, *args, **kwds):
        if cls._LockersFactory__thisInstance is None:
            cls._LockersFactory__thisInstance = super(LockersFactory, cls).__new__(cls)
            cls._LockersFactory__thisInstance._isInitialized = False
        return cls._LockersFactory__thisInstance

    def __init__(self):
        if self._isInitialized:
            return
        self._isInitialized = True
        self._LockersFactory__lut = {}

    def __call__(self, key, *args, **kwargs):
        return (self.get)(args, key=key, **kwargs)

    def get(self, key, *args, **kwargs):
        """get locker instance given a key.
        If locker is not found by key then it's created
        using *args and **kwargs and returned

        :Parameters:
            #. key (string): locker key. Usually it should be the serverFile path

        :Returns:
            #. locker (ServerLocker): the locker instance
        """
        assert isinstance(key, basestring), 'key must be a string'
        key = _to_unicode(key)
        if key not in self._LockersFactory__lut:
            self._LockersFactory__lut[key] = ServerLocker(*args, **kwargs)
        return self._LockersFactory__lut[key]


FACTORY = LockersFactory()