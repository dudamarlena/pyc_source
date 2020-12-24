# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/zmq_rpc/client.py
# Compiled at: 2016-12-27 13:29:54
import logging, os, random, struct, time, zmq
from zmq_rpc.base import ZmqRpcConnector
from zmq_rpc.errors import ZmqRpcError
logger = logging.getLogger(__name__)
log = logger.debug

class ZmqRpcClient(ZmqRpcConnector):
    """zmq-rpc client implementation with pyzmq.
    """
    REQ_PREFIX = struct.Struct('=HH')
    REQ_SUFFIX = struct.Struct('=Ld')
    RESP = struct.Struct('=HHLd?')

    def __init__(self, url, timeout=None):
        """Initialize the connector.
        :param url: URL to the aiozmq server.
        :param timeout: Timeout when waiting for the server before throwing an
        exception (in milliseconds - use "None" for no timeout).
        """
        super(ZmqRpcClient, self).__init__()
        self.counter = 0
        self.prefix = self.REQ_PREFIX.pack(os.getpid() % 65536, random.randrange(65536))
        self.context = zmq.Context().instance()
        if timeout is not None:
            self.context.RCVTIMEO = timeout
        self.socket = self.context.socket(zmq.DEALER)
        self.socket.connect(url)
        return

    def __getattr__(self, name):
        """Allow directly calling RPC functions.
        """
        return lambda *args, **kwargs: self.callFunction(name, args, kwargs)

    def callFunction(self, func_name, func_args, func_kwargs):
        """Call the specified RPC-exposed function and return its result
        (blocking).

        :param func_name: The name of the RPC function exposed by the server.
        :type func_name: String.

        :param func_args: The positional arguments to send the RPC function.
        :type func_args: List.

        :param func_kwargs: The named arguments to send the RPC function.
        :type func_kwargs: Dictionary.

        :raise zmq_rpc.errors.ZmqRpcError.

        :return: Result of the RPC function call.
        """
        data = [
         self._newHeader(),
         func_name.encode('utf-8'),
         self.packer.pack(func_args),
         self.packer.pack(func_kwargs)]
        self.send(data)
        log('sent data: %s', data)
        data = self.receive()
        log('received data: %s', data)
        header, answer = data
        pid, rnd, req_id, timestamp, is_error = self.RESP.unpack(header)
        answer = self.packer.unpack(answer)
        if is_error:
            raise ZmqRpcError(answer[2])
        return answer

    def close(self):
        """Close the connection.
        """
        self.socket.close()

    def _newHeader(self):
        self.counter += 1
        if self.counter > 4294967295:
            self.counter = 0
        return self.prefix + self.REQ_SUFFIX.pack(self.counter, time.time())


def main():
    """Start a test client.
    """
    logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.DEBUG)
    log('start')

    def runClient():
        zmq_rpc_client = ZmqRpcClient('tcp://127.0.0.1:2678', timeout=1000)
        call_result = zmq_rpc_client.test_func(1, 2, zmq_rpc_client.packer.pack('abc'))
        log('result of the test_func call: %s', call_result)
        zmq_rpc_client.close()
        log('closed')

    import threading
    thread = threading.Thread(target=runClient)
    thread.start()
    thread.join()
    log('done')


if __name__ == '__main__':
    main()