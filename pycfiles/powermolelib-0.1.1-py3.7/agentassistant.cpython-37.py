# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/vincent/Projects/PythonPowerMole/powermolelib/powermolelib/agentassistant.py
# Compiled at: 2020-05-11 17:41:22
# Size of source mod 2**32: 20676 bytes
"""
Main code for agent assistant.

.. _Google Python Style Guide:
   http://google.github.io/styleguide/pyguide.html

"""
from abc import ABC, abstractmethod
import socket
from socket import timeout
import os.path
from os.path import basename, dirname
from urllib.error import URLError
import urllib.request, logging, json
from time import sleep
from voluptuous import Schema, Required, Any, MultipleInvalid
__author__ = 'Vincent Schouten <inquiry@intoreflection.co>'
__docformat__ = 'google'
__date__ = '10-05-2019'
__copyright__ = 'Copyright 2020, Vincent Schouten'
__credits__ = ['Vincent Schouten']
__license__ = 'MIT'
__maintainer__ = 'Vincent Schouten'
__email__ = '<inquiry@intoreflection.co>'
__status__ = 'Development'
LOGGER_BASENAME = 'machine'
LOGGER = logging.getLogger(LOGGER_BASENAME)
COMMAND_PROMPT = '[#$] '
HTTP_RESPONSE = Schema({Required('result'): Any(True, False)})

class Assistant(ABC):
    __doc__ = "Models an Assistant to interact with the agent residing on target destination host.\n\n    Note: As the agent sits on top of target destination hosts' OS, many functions can be\n    performed more effective.\n\n    "

    def __init__(self, tunnel):
        """Initializes the Assistant object."""
        logger_name = '{base}.{suffix}'.format(base=LOGGER_BASENAME, suffix=(self.__class__.__name__))
        self.host_port_proxy_server = tunnel.host_port_proxy_server
        self.host_port_heartbeat_responder = tunnel.host_port_heartbeat_responder
        self.host_port_file_server = tunnel.host_port_file_server
        self.host_port_command_server = tunnel.host_port_command_server
        self.host_port_agent = tunnel.host_port_agent
        self._logger = logging.getLogger(logger_name)
        self.host = '127.0.0.1'

    def __str__(self):
        return 'Assistant'

    def _send_instruction(self, instruction):
        json_instruction = json.dumps(instruction)
        data = json_instruction.encode('utf-8')
        try:
            with urllib.request.urlopen(f"http://{self.host}:{self.host_port_agent}", timeout=5,
              data=data) as (request_obj):
                response_string = request_obj.read().decode('utf-8')
            response_dict = json.loads(response_string)
            response = HTTP_RESPONSE(response_dict)
            result = response.get('result')
        except URLError:
            self._logger.error('agent could not be instructed. probable cause: Machine unreachable or client has not connection to the Internet')
            result = False
        except ConnectionResetError:
            self._logger.error('agent could not be instructed. probable cause: agent not bind to port')
            result = False
        except timeout:
            LOGGER.error('agent could not be instructed. probably cause: timeout exceeded for the connection attempt')
            result = False
        except json.decoder.JSONDecodeError:
            self._logger.error('response of agent could not be read, JSON document could not be deserialized')
            result = False
        except MultipleInvalid:
            self._logger.error('response of agent could not be read. data structure validating failed ("MultipleInvalid")')
            result = False

        return result

    def start_heartbeat_responder(self, machine_local_port):
        """Starts the heartbeat responder."""
        self._logger.debug('instructing the agent to start the heartbeat responder')
        result = self._send_instruction({'process':'heartbeat_responder_start',  'arguments':{'local_port': machine_local_port}})
        self._logger.debug('agent responded with: %s', result)
        return result

    def stop_heartbeat_responder(self):
        """Stops the heartbeat responder."""
        self._logger.debug('instructing the agent to stop the heartbeat responder')
        result = self._send_instruction({'process':'heartbeat_responder_stop',  'arguments':{}})
        self._logger.debug('agent responded with: %s', result)
        return result

    def stop_agent(self):
        """Starts the agent."""
        self._logger.debug('instructing agent to stop itself')
        result = self._send_instruction({'process':'stop',  'arguments':{}})
        self._logger.debug('agent responded with: %s', result)
        return result

    @abstractmethod
    def start(self):
        """Starts the necessary programs on target destination host."""
        pass

    @abstractmethod
    def stop(self):
        """Terminates the started program(s) and the agent on target destination host."""
        pass


class ForAssistant(Assistant):
    __doc__ = "Provides interaction with the agent, which resides on target destination host, to accommodate For mode.\n\n    Functions:\n    - interaction with the heartbeat responder\n    - forwards connections ('local port forwarding')\n    "

    def __init__(self, tunnel):
        """Initializes the ForAssistant object.

        Args:
            tunnel (Tunnel): An instantiated Tunnel object.

        """
        Assistant.__init__(self, tunnel)

    def start(self):
        """Starts the heartbeat responder."""
        return self.start_heartbeat_responder(machine_local_port=(self.host_port_heartbeat_responder))

    def stop(self):
        """Terminates minitoragent on target destination host."""
        return self.stop_agent()


class TorAssistant(Assistant):
    __doc__ = 'Provides interaction with the agent, which resides on target destination host, to accommodate Tor mode.\n\n    Functions:\n    - interaction with the heartbeat responder\n    - proxify internet traffic\n    '

    def __init__(self, tunnel, ip_address_e):
        """Initializes the TorAssistant object.

        Args:
            tunnel (Tunnel): An instantiated Tunnel object.
            ip_address_e (basestring): The IP address on host (on a possible different if) for outgoing connections.

        """
        Assistant.__init__(self, tunnel)
        self.ip_address_e = ip_address_e

    def start_proxy_server(self, machine_local_port, if_address_e):
        """Starts the proxy server."""
        self._logger.debug('instructing the agent to start the proxy server')
        result = self._send_instruction({'process':'proxy_server_start',  'arguments':{'local_port':machine_local_port, 
          'ip_address_e':if_address_e}})
        self._logger.debug('agent responded with: %s', result)
        return result

    def stop_proxy_server(self):
        """Stops the proxy server."""
        self._logger.debug('instructing the agent to stop the proxy server')
        result = self._send_instruction({'process':'proxy_server_stop',  'arguments':{}})
        self._logger.debug('agent responded with: %s', result)
        return result

    def start(self):
        """Starts the SOCKS proxy and heartbeat responder."""
        return all([
         self.start_proxy_server(machine_local_port=(self.host_port_proxy_server), if_address_e=(self.ip_address_e)),
         self.start_heartbeat_responder(machine_local_port=(self.host_port_heartbeat_responder))])

    def stop(self):
        """Terminates the started program(s) and the agent on target destination host."""
        return self.stop_agent()


class InteractiveAssistant(Assistant):
    __doc__ = 'Provides interaction with the agent, which resides on target destination host, to accommodate Interactive mode.\n\n    Functions:\n    - interaction with the heartbeat responder\n    - providing an interface\n    '

    def __init__(self, tunnel, local_command_port):
        """Initializes the InteractiveAssistant object.

        Args:
            tunnel (Tunnel): An instantiated Tunnel object.
            local_command_port (basestring): <>

        """
        Assistant.__init__(self, tunnel)
        self.local_command_port = local_command_port

    def start(self):
        """Performs authentication of the host and starts the heartbeat responder."""
        return all([self._start_command_server(machine_local_port=(self.host_port_command_server)),
         self.start_heartbeat_responder(machine_local_port=(self.host_port_heartbeat_responder))])

    def stop(self):
        """Terminates the started program(s) and the agent on target destination host."""
        return self.stop_agent()

    def _start_command_server(self, machine_local_port):
        """Starts the command server."""
        self._logger.debug('instructing the agent to start command server')
        result = self._send_instruction({'process':'command_server_start',  'arguments':{'local_port': machine_local_port}})
        self._logger.debug('agent responded with: %s', result)
        return result

    def _stop_command_server(self):
        """Stops the command server."""
        self._logger.debug('instructing the agent to stop command server')
        result = self._send_instruction({'process':'command_server_stop',  'arguments':{}})
        self._logger.debug('agent responded with: %s', result)
        return result

    def exec_command(self, command):
        """Executes Linux command and returns the response in a byte list."""
        if command.lower().strip() == 'exit':
            response = [
             b'ABORTED: hit control + c to end interactive mode']
            return response
        try:
            command_json = json.dumps({'command': command})
            command_byte = command_json.encode('utf-8')
            with urllib.request.urlopen(f"http://{self.host}:{self.local_command_port}", timeout=5,
              data=command_byte) as (request_obj):
                response = request_obj.read()
        except URLError:
            self._logger.error('URLError. HTTP request could not be send over forwarded connection to agent. probable cause: Machine unreachable or client has not connection to the Internet')
            response = False
        except ConnectionResetError:
            self._logger.error('ConnectionResetError. HTTP request could not be send over forwarded connection to agent. probable cause: agent not bind to port')
            response = False
        except timeout:
            LOGGER.error('HTTP request could not be send over forwarded connection to agent. timeout exceeded for the connection attempt. probable cause: Machine unreachable or client has not connection to the Internet')
            response = False

        return response


class FileAssistant(Assistant):
    __doc__ = 'Provides interaction with the agent, which resides on target destination host, to accommodate File mode.\n\n    Functions:\n    - interaction with the heartbeat responder\n    - transfer files.\n    '

    def __init__(self, tunnel, local_transfer_port):
        """Initializes the FileAssistant object.

        Args:
            tunnel (Tunnel): An instantiated Tunnel object.
            local_transfer_port (basestring): <>

        """
        Assistant.__init__(self, tunnel)
        self.metadata_files = None
        self.local_transfer_port = local_transfer_port
        self.file_client = None

    def _start_file_server(self, machine_local_port):
        """Starts the file server."""
        self._logger.debug('instructing the minitoragent to start file server')
        result = self._send_instruction({'process':'file_server_start',  'arguments':{'local_port': machine_local_port}})
        self._logger.debug('minitoragent responded with: %s', result)
        return result

    def _stop_file_server(self):
        """Stops the file server."""
        self._logger.debug('instructing the minitoragent to stop file server')
        result = self._send_instruction({'process':'file_server_stop',  'arguments':{}})
        if result:
            self._logger.debug('agent has received instruction')
        return result

    def start(self):
        """Starts the heartbeat responder and transfers files."""
        if all([self.start_heartbeat_responder(machine_local_port=(self.host_port_heartbeat_responder)),
         self._start_file_server(machine_local_port=(self.host_port_file_server))]):
            self.file_client = FileClient(local_transfer_port=(self.local_transfer_port))
            return self.file_client.start()
        return False

    def transfer(self, metadata_files):
        """Transfers files from client to target destination host."""
        for file in metadata_files:
            self.file_client.transfer(file.get('source'), file.get('destination'))

        sleep(2)
        self._logger.info('the files are successfully transferred')
        return True

    def stop(self):
        """Terminates the started program(s) and the agent on target destination host."""
        return all([self.file_client.stop(), self.stop_agent()])


class FileClient:
    __doc__ = 'Sends files to file server (ie. agent) residing on the target destination host.\n\n    Exclusively used by FileAssistant().\n\n    '

    def __init__(self, local_transfer_port):
        logger_name = '{base}.{suffix}'.format(base=LOGGER_BASENAME, suffix='FileClient')
        self._logger = logging.getLogger(logger_name)
        self.socket_ = None
        self.local_transfer_port = local_transfer_port

    def start(self):
        """Connects to file server (on Machine) and uploads data."""
        self.socket_ = socket.socket()
        host = 'localhost'
        self.socket_.connect((host, self.local_transfer_port))
        self._logger.debug('connection from client to file server established')
        return True

    def stop(self):
        """Closes socket."""
        self.socket_.close()

    def transfer(self, source, destination):
        """Opens the sockets, connects to file server (ie. agent) on Machine, and sends file(s)."""
        data_protocol = DataProtocol()
        file_name = basename(source)
        path_src = dirname(source)
        path_dst = destination
        try:
            path_dst_bin = data_protocol.path_dst(path_dst=path_dst)
            file_name_bin = data_protocol.file_name(file_name=file_name)
            file_size_bin = data_protocol.file_size(path_src=path_src, file_name=file_name)
            self._send_file(path_src=path_src, file_name=file_name,
              file_name_bin=file_name_bin,
              file_size_bin=file_size_bin,
              path_dst_bin=path_dst_bin)
            self._logger.info('file %s is transferred', source)
        except FileNotFoundError:
            self._logger.error('file or directory is requested but does not exist')

        return True

    def _send_file(self, path_src, file_name, file_name_bin, file_size_bin, path_dst_bin):
        metadata = path_dst_bin + file_name_bin + file_size_bin
        path_to_file = os.path.join(path_src, file_name)
        self._logger.debug('sending file name, file size and file content')
        data = open(path_to_file, 'rb')
        self.socket_.sendall(metadata + data.read())

    def interrupt(self):
        """Closes the socket."""
        self._logger.debug('interrupting the transfer of binary data.')
        return True


class DataProtocol:
    __doc__ = 'Encodes file metadata to a binary format.'

    def __init__(self):
        logger_name = '{base}.{suffix}'.format(base=LOGGER_BASENAME, suffix='DataProtocol')
        self._logger = logging.getLogger(logger_name)

    def path_dst(self, path_dst):
        """Encodes the destination path."""
        self._logger.debug('path to directory on remote server: %s', path_dst)
        length_path_int = len(path_dst)
        length_path_bin = bin(length_path_int)[2:].zfill(16)
        return length_path_bin.encode('utf-8') + path_dst.encode('utf-8')

    def file_name(self, file_name):
        """Encodes (only) the file name - not the directory."""
        self._logger.debug('name of file to be transferred: %s', file_name)
        length_file_int = len(file_name)
        length_file_bin = bin(length_file_int)[2:].zfill(16)
        return length_file_bin.encode('utf-8') + file_name.encode('utf-8')

    def file_size(self, path_src, file_name):
        """Encodes the file size."""
        path_to_file = os.path.join(path_src, file_name)
        size_file_int = os.path.getsize(path_to_file)
        self._logger.debug('size of file %s: %s bytes', file_name, size_file_int)
        size_file_bin = bin(size_file_int)[2:].zfill(32)
        return size_file_bin.encode('utf-8')