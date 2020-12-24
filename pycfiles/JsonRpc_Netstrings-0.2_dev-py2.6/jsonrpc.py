# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/jsonrpc_netstrings/jsonrpc.py
# Compiled at: 2011-03-25 22:50:48
import socket, json, time, math, traceback
timeout = 60

class ConnectionLost(Exception):
    pass


class JsonRpcError(Exception):
    pass


class JsonRpcProxy:
    retries = 0

    def __init__(self, host, port, version='2.0'):
        self.host = host
        self.port = port
        self._version = version
        self.connect()

    def connect(self):
        try:
            self.retries += 1
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.settimeout(timeout)
            self.socket.connect((self.host, self.port))
            self._incrementor = 1
            self.retries = 0
        except Exception, e:
            print e
            sleep_time = math.log(self.retries)
            print "Couldn't Connect, sleeping for %s seconds and retrying... (retry #%s)" % (sleep_time, self.retries)
            time.sleep(sleep_time)
            return self.connect()

    def close(self):
        self.socket.close()

    def call_remote(self, method, params={}, retries=0):
        if retries > 10:
            raise JsonRpcError('Too many retries: %s' % retries)
        self._incrementor += 1
        jsonrpc_request = {'jsonrpc': self._version, 'id': self._incrementor, 'method': method, 'params': params}
        string = json.dumps(jsonrpc_request)
        jsonrpc = str(len(string)) + ':' + string + ','
        try:
            print 'Sending message: %s' % jsonrpc
            self.socket.send(jsonrpc)
            byte_length = self.socket.recv(1, socket.MSG_WAITALL)
            if not byte_length:
                raise ConnectionLost()
            while byte_length[(-1)] != ':':
                print 'Receiving byte length (next char)...'
                byte_length += self.socket.recv(1)

            byte_length = int(byte_length[:-1])
            print 'Got byte length:', byte_length
            response_string = ''
            while len(response_string) < byte_length:
                print 'Receiving bytedata bytes...'
                response_string += str(self.socket.recv(byte_length - len(response_string)))

            response = json.loads(response_string)
        except Exception, e:
            traceback_string = traceback.format_exc()
            print traceback_string
            self.connect()
            return self.call_remote(method, params)
        else:
            if not response['id'] == self._incrementor:
                return self.call_remote(method, params, retries)
            last_char = self.socket.recv(1)
            if last_char != ',':
                raise JsonRpcError('Expected a comma as a jsonrpc terminator!')
            if 'result' in response:
                return response['result']
            if 'error' in response:
                raise JsonRpcError(response['error'])
            raise JsonRpcError('Unknow error. Response: %s' % response)