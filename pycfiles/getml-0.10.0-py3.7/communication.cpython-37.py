# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/getml/communication.py
# Compiled at: 2020-03-16 07:21:38
# Size of source mod 2**32: 20839 bytes
"""
Handles the communication for the getml library
"""
import json, socket, sys, numbers, numpy as np, getml

class _Encoding(object):
    __doc__ = '\n    Maps strings to integers, so we can speed up the sending\n    of string columns. \n    '

    def __init__(self):
        self.map = dict()
        self.vec = []

    def __getitem__(self, key):
        if key in self.map:
            return self.map[key]
        val = len(self.vec)
        self.map[key] = val
        self.vec.append(key)
        return val


class _GetmlEncoder(json.JSONEncoder):
    __doc__ = 'Enables a custom serialization of the getML classes.\n    '

    def default(self, obj):
        """Checks for the particular type of the provided object and
        deserializes it into an escaped string.

        To ensure the getML can handle all keys, we have to add a
        trailing underscore.

        Args:
            obj: Any of the classes defined in the getml package.

        Returns:
            string:
                Encoded JSON.

        Examples:
            Create a :class:`~getml.predictors.LinearRegression`,
            serialize it, and deserialize it again.

            .. code-block:: python

                p = getml.predictors.LinearRegression()
                p_serialized = json.dumps(p, cls = getml.communication._GetmlEncoder)
                p2 = json.loads(p_serialized, object_hook = getml.helpers.predictors._decode_predictor)
                p == p2

        """
        if hasattr(obj, '_getml_deserialize'):
            return obj._getml_deserialize()
        return json.JSONEncoder.default(self, obj)


def engine_exception_handler(msg, fallback=''):
    """Looks at the error message thrown by the engine and decides whether
    to throw a corresponding Exception using the same string or
    altering the message first.

    In either way, this function will always throw some sort of Exception.

    Args:

        msg (str): Error message returned by the getML engine.
        fallback (str):

            If not empty, the default Exception will carry this
            string.

    Raises:

        IOError: In any case.

    """
    if not fallback:
        fallback = msg
    elif msg == 'You have not set a project!':
        raise IOError('You have not set a project yet! See `help(getml.engine.set_project)` for further information.')
    else:
        raise IOError(fallback)


def recv_data(sock, size):
    """Receives data (of any type) sent by the getml engine.

    Raises:
        TypeError: If `sock` is not of type :py:class:`socket.socket`
            or `size` is not a number.
        RuntimeError: If no data could be received from the engine.
    """
    if type(sock) is not socket.socket:
        raise TypeError("'sock' must be a socket.")
    if not isinstance(size, numbers.Real):
        raise TypeError("'size' must be a number.")
    data = []
    bytes_received = np.uint64(0)
    max_chunk_size = np.uint64(2048)
    while bytes_received < size:
        current_chunk_size = int(min(size - bytes_received, max_chunk_size))
        chunk = sock.recv(current_chunk_size)
        if chunk == '':
            raise RuntimeError('Connection to getml engine broken')
        data.append(chunk)
        bytes_received += np.uint64(len(chunk))

    return ''.encode().join(data)


def recv_boolean_matrix(sock):
    """Receives a matrix (type boolean) from the getml engine.

    Raises:
        TypeError: If `sock` is not of type :py:class:`socket.socket`.
    """
    if type(sock) is not socket.socket:
        raise TypeError("'sock' must be a socket.")
    elif sys.byteorder == 'little':
        shape = np.frombuffer((sock.recv(np.nbytes[np.int32] * 2)),
          dtype=(np.int32)).byteswap().astype(np.uint64)
        size = shape[0] * shape[1] * np.uint64(np.nbytes[np.int32])
        matrix = recv_data(sock, size)
        matrix = np.frombuffer(matrix,
          dtype=(np.int32)).byteswap()
        matrix = matrix.reshape(shape[0], shape[1])
    else:
        shape = np.frombuffer((sock.recv(np.nbytes[np.int32] * 2)),
          dtype=(np.int32)).astype(np.uint64)
        size = shape[0] * shape[1] * np.uint64(np.nbytes[np.int32])
        matrix = recv_data(sock, size)
        matrix = np.frombuffer(matrix,
          dtype=(np.int32))
        matrix = matrix.reshape(shape[0], shape[1])
    return matrix == 1


def recv_matrix(sock):
    """
    Receives a matrix (type np.float64) from the getml engine.

    Raises:
        TypeError: If `sock` is not of type :py:class:`socket.socket`.
    """
    if type(sock) is not socket.socket:
        raise TypeError("'sock' must be a socket.")
    elif sys.byteorder == 'little':
        shape = np.frombuffer((sock.recv(np.nbytes[np.int32] * 2)),
          dtype=(np.int32)).byteswap().astype(np.uint64)
        size = shape[0] * shape[1] * np.uint64(np.nbytes[np.float64])
        matrix = recv_data(sock, size)
        matrix = np.frombuffer(matrix,
          dtype=(np.float64)).byteswap()
        matrix = matrix.reshape(shape[0], shape[1])
    else:
        shape = np.frombuffer((sock.recv(np.nbytes[np.int32] * 2)),
          dtype=(np.int32)).astype(np.uint64)
        size = shape[0] * shape[1] * np.uint64(np.nbytes[np.float64])
        matrix = recv_data(sock, size)
        matrix = np.frombuffer(matrix,
          dtype=(np.float64))
        matrix = matrix.reshape(shape[0], shape[1])
    return matrix


def recv_string(sock):
    """
    Receives a string from the getml engine
    (an actual string, not a bytestring).

    Raises:
        TypeError: If `sock` is not of type :py:class:`socket.socket`.
    """
    if type(sock) is not socket.socket:
        raise TypeError("'sock' must be a socket.")
    if sys.byteorder == 'little':
        try:
            size = np.frombuffer((sock.recv(np.nbytes[np.int32])),
              dtype=(np.int32)).byteswap()[0]
        except IndexError:
            raise IOError("The getML engine died unexpectedly. If this wasn't done on purpose, please get in contact with our support or file a bug report.")

    else:
        try:
            size = np.frombuffer((sock.recv(np.nbytes[np.int32])),
              dtype=(np.int32))[0]
        except IndexError:
            raise IOError("The getML engine died unexpectedly. If this wasn't done on purpose, please get in contact with our support or file a bug report.")

        string = recv_data(sock, size).decode()
        return string


def recv_categorical_matrix(sock):
    """
    Receives a matrix of type string from the getml engine

    Raises:
        TypeError: If `sock` is not of type :py:class:`socket.socket`.
    """
    if type(sock) is not socket.socket:
        raise TypeError("'sock' must be a socket.")
    elif sys.byteorder == 'little':
        shape = np.frombuffer((sock.recv(np.nbytes[np.int32] * 2)),
          dtype=(np.int32)).byteswap().astype(np.uint64)
        size = shape[0] * shape[1]
    else:
        shape = np.frombuffer((sock.recv(np.nbytes[np.int32] * 2)),
          dtype=(np.int32)).astype(np.uint64)
        size = shape[0] * shape[1]
    mat = []
    for i in range(size):
        mat.append(recv_string(sock))

    mat = np.asarray(mat)
    return mat.reshape(shape[0], shape[1])


def send(cmd):
    """Sends a command to the getml engine and closes the established
    connection.

    Creates a socket and sends a command to the getML engine using the
    module-wide variable :py:const:`~getml.port`.

    A message (string) from the :py:class:`socket.socket` will be
    received using :py:func:`~getml.recv_string` and the socket will
    be closed. If the message is "Success!", everything work
    properly. Else, an Exception will be thrown containing the
    message.

    In case another message is supposed to be send by the engine,
    :py:func:`~getml.communication.send_and_receive_socket` has to be used
    and the calling function must handle the message itself!

    Please be very careful when altering the routing/calling behavior
    of the socket communication! The engine might react in a quite
    sensible and freezing way.

    Arg:
        cmd (dict): A dictionary specifying the command the engine is
            supposed to execute. It _must_ contain at least two string
            values with the corresponding keys being named "name_" and
            "type_".

    Raises:
        Exception: If the message received from the engine is not
            "Success!
        TypeError: If `cmd` is not a dict.
        ConnectionRefusedError: If the getML is unreachable.

    """
    if type(cmd) is not dict:
        raise TypeError("'cmd' must be a dict.")
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect(('localhost', getml.port))
    except ConnectionRefusedError:
        raise ConnectionRefusedError("\n        Cannot connect to getML engine. \n        Make sure the engine is on port '" + str(getml.port) + "' and you are logged in. \n        See `help(getml.engine)`.")

    msg = json.dumps(cmd, cls=_GetmlEncoder)
    send_string(sock, msg)
    msg = recv_string(sock)
    sock.close()
    if msg != 'Success!':
        engine_exception_handler(msg)


def send_and_receive_socket(cmd):
    """Sends a command to the getml engine and returns the established
    connection.

    Creates a socket and sends a command to the getML engine using the
    module-wide variable :py:const:`~getml.port`.

    The function will return the socket it opened and the calling
    function is free to receive whatever data is desires over it. But
    the latter has also to take care of closing the socket afterwards
    itself!

    Please be very careful when altering the routing/calling behavior
    of the socket communication! The engine might react in a quite
    sensible and freezing way. Especially implemented handling of
    socket sessions (their passing from function to function) must not
    be altered or separated in distinct calls to the
    :py:func:`~getml.communication.send` function! Some commands have
    to be send via the same socket or the engine will not be able to
    handle them and might block.

    Arg:
        cmd (dict): A dictionary specifying the command the engine is
            supposed to execute. It _must_ contain at least two string
            values with the corresponding keys being named "name_" and
            "type_"."

    Returns:
        :py:class:`socket.socket`: A socket using which the Python API
            can communicate with the getML engine.

    Raises:
        TypeError: If `cmd` is not a dict.
        ConnectionRefusedError: If the getML is unreachable.

    """
    if type(cmd) is not dict:
        raise TypeError("'cmd' must be a dict.")
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect(('localhost', getml.port))
    except ConnectionRefusedError:
        raise ConnectionRefusedError("\n        Cannot connect to getML engine.\n        Make sure the engine is running on port '" + str(getml.port) + "' and you are logged in. \n        See `help(getml.engine)`.")

    msg = json.dumps(cmd, cls=_GetmlEncoder)
    send_string(sock, msg)
    return sock


def send_categorical_matrix(sock, categorical_matrix):
    """Sends a list of strings to the getml engine
    (an actual string, not a bytestring).

    Raises:
        TypeError: If the input is not of proper type.
        Exception: If the dimension of `categorical_matrix` is larger
            than two.
    """
    if type(sock) is not socket.socket:
        raise TypeError("'sock' must be a socket.")
    else:
        if type(categorical_matrix) is not np.ndarray:
            raise TypeError("'categorical_matrix' must be a numpy.ndarray.")
        elif len(categorical_matrix.shape) > 2 or len(categorical_matrix.shape) == 0:
            raise Exception('Numpy array must be one-dimensional or two-dimensional!')
        else:
            if len(categorical_matrix.shape) == 2:
                if categorical_matrix.shape[1] != 1:
                    raise Exception('Numpy array must be single column!')
        encoding = _Encoding()
        integers = [encoding[string.encode('utf-8')] for string in categorical_matrix.astype(str).flatten()]
        integers = np.asarray(integers).astype(np.int32)
        if sys.byteorder == 'little':
            shape = [integers.shape[0], 1]
            sock.sendall(np.asarray(shape).astype(np.int32).byteswap().tostring())
            sock.sendall(integers.byteswap().tostring())
            raw_data = ''.encode().join([np.asarray(len(elem)).astype(np.int32).byteswap().tostring() + elem for elem in encoding.vec])
            shape = [
             len(encoding.vec),
             len(raw_data)]
            sock.sendall(np.asarray(shape).astype(np.int32).byteswap().tostring())
            sock.sendall(raw_data)
        else:
            shape = [integers.shape[0], 1]
            sock.sendall(np.asarray(shape).astype(np.int32).tostring())
            sock.sendall(integers.tostring())
            raw_data = ''.encode().join([np.asarray(len(elem)).astype(np.int32).tostring() + elem for elem in encoding.vec])
            shape = [
             len(encoding.vec),
             len(raw_data)]
            sock.sendall(np.asarray(shape).astype(np.int32).tostring())
            sock.sendall(raw_data)


def send_matrix(sock, matrix):
    """Sends a matrix (type np.float64) to the getml engine.

    Raises:
        TypeError: If the input is not of proper type.
        Exception: If the dimension of `matrix` is larger than two.
    """
    if type(sock) is not socket.socket:
        raise TypeError("'sock' must be a socket.")
    else:
        if type(matrix) is not np.ndarray:
            raise TypeError("'matrix' must be a numpy.ndarray.")
        elif len(matrix.shape) == 1:
            shape = [
             matrix.shape[0], 1]
        else:
            if len(matrix.shape) > 2:
                raise Exception('Numpy array must be one-dimensional or two-dimensional!')
            else:
                shape = matrix.shape
        if sys.byteorder == 'little':
            sock.sendall(np.asarray(shape).astype(np.int32).byteswap().tostring())
            sock.sendall(matrix.astype(np.float64).byteswap().tostring())
        else:
            sock.sendall(np.asarray(shape).astype(np.int32).tostring())
            sock.sendall(matrix.astype(np.float64).tostring())


def send_string(sock, string):
    """
    Sends a string to the getml engine
    (an actual string, not a bytestring).

    Raises:
        TypeError: If the input is not of proper type.
    """
    if type(sock) is not socket.socket:
        raise TypeError("'sock' must be a socket.")
    else:
        if type(string) is not str:
            raise TypeError("'string' must be a str.")
        encoded = string.encode('utf-8')
        size = len(encoded)
        if sys.byteorder == 'little':
            sock.sendall(np.asarray([size]).astype(np.int32).byteswap().tostring())
        else:
            sock.sendall(np.asarray([size]).astype(np.int32).tostring())
    sock.sendall(encoded)