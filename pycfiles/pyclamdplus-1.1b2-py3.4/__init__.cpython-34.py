# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyclamdplus/__init__.py
# Compiled at: 2015-11-13 06:52:04
# Size of source mod 2**32: 12049 bytes
"""
Pythonic interface to the Clamav daemon.

"""
import socket
from os import path
from six import string_types
__all__ = ('ClamdNetworkConnection', 'ClamdUNIXConnection', 'PyclamdplusException',
           'ConnectionError', 'RequestError', 'BadTargetError')

class ClamdConnection(object):
    __doc__ = '\n    Base class for Clamd connections.\n    \n    '

    def __init__(self):
        """
        Init the socket.
        
        :raises pyclamdplus.exc.ConnectionError: If it could not connect to
            the server.
        
        """
        self._socket = None
        self.ping()

    def disconnect(self):
        """
        End connection with the Clamd server.
        
        :raises pyclamdplus.exc.ConnectionError: If it could not disconnect.
        
        """
        try:
            self._init_socket()
            self._socket.shutdown(socket.SHUT_RDWR)
            self._socket.close()
        except socket.error as exc:
            raise ConnectionError('Could not disconnect from Clamd server: %s' % exc)

    def shutdown(self):
        """
        Force Clamd to shutdown and finally close the connection.
        
        :raises pyclamdplus.exc.RequestError: If the server did not shut itself
            down.
        :raises pyclamdplus.exc.ConnectionError: If it could not disconnect
            after the server was shut down.
        
        """
        response = self._send_data('SHUTDOWN')
        if response:
            raise RequestError('Clamd ignored shutdown command: %s' % response)

    def ping(self):
        """
        Send a PING to the Clamav server, which should reply by a PONG.
        
        :raises pyclamdplus.ConnectionError: If there was a connection problem.
        :raises pyclamdplus.exc.ConnectionError: If it as not successful.
        
        """
        response = self._send_data('PING')
        if response != 'PONG':
            raise ConnectionError('Wrong PING response: %s' % response)

    def reload(self):
        """
        Force Clamd to reload signature database.
        
        :raises pyclamdplus.ConnectionError: If there was a connection problem.
        :raises pyclamdplus.RequestError: If the server did not reload its
            signature database.
        
        """
        response = self._send_data('RELOAD')
        if response != 'RELOADING':
            raise RequestError('The signature database was not reloaded: %s' % response)

    def get_version(self):
        """
        Get Clamscan version.
        
        :raises pyclamdplus.ConnectionError: If there was a connection problem.
        :return: The Clamscan version.
        
        """
        response = self._send_data('VERSION')
        return response

    def _init_socket(self):
        """
        Initialise the socket.
        
        To be implemented by the actual connections.
        
        """
        raise NotImplementedError('Clamd connections must define their initialization routines')

    def _send_data(self, data, auto_close=True):
        """
        Send ``data`` to the socket and get its response.
        
        :param data: The data to be sent to the socket.
        :type data: str
        :param auto_close: Whether the socket should be closed after retrieving
            the data.
        :type auto_close: bool
        :raises pyclamdplus.ConnectionError: If there was a problem.
        :return: The response.
        :rtype: str
        
        """
        data_encoded = data.encode()
        try:
            self._init_socket()
            self._socket.send(data_encoded)
            result = self._retrieve_data(auto_close=auto_close)
        except socket.error as exc:
            raise ConnectionError('Could not send data "%s" to the Clamd server: %s' % (
             data, exc))

        return result

    def _retrieve_data(self, auto_close=True):
        """
        Retrieve data from the socket.
        
        :param auto_close: Whether the socket should be closed after retrieving
            the data.
        :type auto_close: bool
        
        """
        response = self._socket.recv(20000).strip()
        if auto_close:
            self._socket.close()
        return response.decode()

    def scan_file(self, file):
        """
        Check if the ``file`` is infected and if so return the virus name.
        
        :param file: The path to the file to be scanned.
        :type file: str
        :raises BadTargetError: If ``file`` is not an existing regular file.
        :raises RequestError: If the ``file`` could not be scanned.
        :return: The name of the virus.
        :rtype: ``bool`` or ``None``
        
        """
        _target_must_exist(file)
        if not path.isfile(file):
            raise BadTargetError('Target %s is not a file' % file)
        result = self._scan(file)
        if result:
            return list(result.items())[0][1]
        else:
            return

    def scan_directory(self, directory):
        """
        Find the infected files in ``directory``.
        
        :param directory: The directory to be scanned.
        :type directory: str
        :raises BadTargetError: If ``directory`` is not an existing directory.
        :raises RequestError: If the ``directory`` could not be scanned.
        :return: The infected files.
        :rtype: dict
        
        The result will be a dictionary whose keys are the file paths and the
        items are the viruses detected.
        
        The dictionary will be empty if no files were infected.
        
        """
        _target_must_exist(directory)
        if not path.isdir(directory):
            raise BadTargetError('Target %s is not a directory' % directory)
        return self._scan(directory, contscan=True)

    def _scan(self, file, contscan=False):
        """
        Scan a file or directory given by filename and stop on virus.
        
        :param file: The path to the file/directory to be scanned; must be
            an absolute path.
        :type file: str
        :param contscan: Whether to scan using the "CONTSCAN" method instead
            of "SCAN".
        :type contscan: bool
        :raises RequestError: If a file/directory could not be scanned.
        :return: The infected files.
        :rtype: dict
        
        The result will be a dictionary whose keys are the file paths and the
        items are the viruses detected.
        
        """
        if contscan:
            method = 'CONTSCAN'
        else:
            method = 'SCAN'
        result = self._send_data('%s %s' % (method, file), auto_close=False)
        infected_files = {}
        try:
            while len(result) > 0:
                result_parts = result.split(':')
                filename = ' '.join(result_parts[:-1])
                virusname = result_parts[(-1)].strip()
                if virusname[-5:] == 'ERROR':
                    raise RequestError('Could not scan %s: %s' % (filename,
                     virusname))
                elif virusname[-5:] == 'FOUND':
                    infected_files[filename] = virusname[:-6]
                result = self._retrieve_data(auto_close=False)

        finally:
            self._socket.close()

        return infected_files


class ClamdNetworkConnection(ClamdConnection):
    __doc__ = '\n    Clamd network socket connection.\n    \n    '

    def __init__(self, host='127.0.0.1', port=3310):
        """
        Init pyclamd to use Clamd network socket.
        
        :param host: The clamd server address.
        :type host: str
        :param port: The clamd server port.
        :type port: int
        :raises pyclamdplus.exc.ConnectionError: If the parameters were not
            correct or if we could not connect to the server for another
            reason.
        
        """
        if not isinstance(host, string_types):
            raise ConnectionError('Host should be a string, not %s' % repr(host))
        if not isinstance(port, int):
            raise ConnectionError('Port should be an integer, not %s' % repr(port))
        self.host = host
        self.port = port
        super(ClamdNetworkConnection, self).__init__()

    def _init_socket(self):
        """
        Initialize the network socket.
        
        :raises pyclamdplus.exc.ConnectionError: If we could not connect to the
            server.
        
        """
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.connect((self.host, self.port))
        except socket.error as exc:
            s.close()
            raise ConnectionError('Could not reach Clamd server on %s:%s: %s' % (
             self.host, self.port, exc))
        else:
            self._socket = s


class ClamdUNIXConnection(ClamdConnection):
    __doc__ = '\n    Clamd UNIX file socket connections.\n    \n    '

    def __init__(self, filename='/var/run/clamd'):
        """
        Init pyclamd to use Clamd network socket.
        
        :param filename: The clamd file for local UNIX socket.
        :type filename: str
        :raises pyclamdplus.exc.ConnectionError: If the parameters were not
            correct or if we could not connect to the server for another
            reason.
        
        """
        if not isinstance(filename, string_types):
            raise ConnectionError('The filename should be a string, not %s' % repr(filename))
        self.filename = filename
        super(ClamdUNIXConnection, self).__init__()

    def _init_socket(self):
        """
        Initialize the UNIX socket.
        
        :raises pyclamdplus.exc.ConnectionError: If we could not reach the UNIX
            socket file.
        
        """
        s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        try:
            s.connect(self.filename)
        except socket.error as exc:
            s.close()
            raise ConnectionError('Could not reach Clamd UNIX socket %s: %s' % (
             self.filename, exc))
        else:
            self._socket = s


def _target_must_exist(path_):
    """
    Make sure ``path_`` exists.
    
    :raises BadTargetError: If it doesn't exist.
    
    """
    if not path.exists(path_):
        raise BadTargetError('Target %s does not exist or is not accessible' % path_)


from pyclamdplus.exc import PyclamdplusException, ConnectionError, RequestError, BadTargetError