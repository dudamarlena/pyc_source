# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\PyTrinamic\connections\ConnectionManager.py
# Compiled at: 2020-01-29 04:36:38
# Size of source mod 2**32: 12522 bytes
"""
Created on 28.05.2019

@author: LH
"""
import sys, argparse
import PyTrinamic.connections.dummy_tmcl_interface as dummy_tmcl_interface
import PyTrinamic.connections.pcan_tmcl_interface as pcan_tmcl_interface
import PyTrinamic.connections.socketcan_tmcl_interface as socketcan_tmcl_interface
import PyTrinamic.connections.serial_tmcl_interface as serial_tmcl_interface
import PyTrinamic.connections.uart_ic_interface as uart_ic_interface
import PyTrinamic.connections.usb_tmcl_interface as usb_tmcl_interface

class ConnectionManager:
    __doc__ = '\n    This class provides a centralized way of extracting connection-specific\n    arguments out of a scripts command line arguments and using these to\n    initiate connections.\n\n    The constructor takes the list of commandline arguments as a list of\n    strings. This allows to directly pass the sys.argv parameter list. If no\n    list is passed sys.argv is used as default.\n\n    The resulting filters for connections are stored in the instance of this\n    class which allows repeated connect() and disconnect() calls.\n\n    Supported commandline arguments:\n        --interface <interface>\n            Select an interface to use for connections. The possible values for\n            this can be retrieved using the static function\n                ConnectionManager.showInterfaces()\n            which returns a list of interface strings.\n\n            Default value: usb_tmcl\n\n        --port <port>\n            The port to use for connecting. The <port> value can be:\n            - A number:\n                Uses the n-th available port. Starts from 0, supports negative\n                values to start counting from the end of the list of ports.\n            - "any":\n                Use any available port (the first one). Equivalent to using the\n                number 0.\n            - "interactive":\n                Shows an interactive dialoge for selecting the port to use.\n            - Any other string:\n                Attempt to use the provided string to connect with the selected\n                interface directly. E.g. for a serial connection you can use\n                "COM3" on windows or "/dev/tty3" on linux.\n\n            Default value: "any"\n\n        --no-port <no-port>\n            Ports to exclude when choosing a connection. This parameter can be\n            added multiple times. E.g. "COM1" prevents the connection manager to\n            select the port "COM1" for connections when using "any",\n            "interactive" or a number as the --port argument.\n\n        --data-rate <data-rate>\n            The data rate to use for the connection. How this value is\n            interpreted depends on the interface used. E.g. the serial\n            connection uses this value as the baud rate.\n\n            Default value: 115200\n\n        --host-id <host-id>\n            The host id to use with a TMCL connection.\n\n            Default value: 2\n\n        --module-id <module-id>\n            The module id to use with a TMCL connection.\n\n            Default value: 1\n    '
    _INTERFACES = [
     (
      'dummy_tmcl', dummy_tmcl_interface, 0),
     (
      'pcan_tmcl', pcan_tmcl_interface, 1000000),
     (
      'socketcan_tmcl', socketcan_tmcl_interface, 1000000),
     (
      'serial_tmcl', serial_tmcl_interface, 9600),
     (
      'uart_ic', uart_ic_interface, 9600),
     (
      'usb_tmcl', usb_tmcl_interface, 115200)]

    def __init__(self, argList=None, debug=False):
        parser = argparse.ArgumentParser(description='ConnectionManager to setup connections dynamically and interactively')
        parser.add_argument('--interface', dest='interface', action='store', nargs=1, type=str, choices=['dummy_tmcl', 'pcan_tmcl', 'socketcan_tmcl', 'serial_tmcl', 'uart_ic', 'usb_tmcl'], default=['usb_tmcl'], help='Connection interface (default: %(default)s)')
        parser.add_argument('--port', dest='port', action='store', nargs=1, type=str, default=['any'], help='Connection port (default: %(default)s, n: Use n-th available port, "any": Use any available port, "interactive": Interactive dialogue for port selection, String: Attempt to use the provided string - e.g. COM6 or /dev/tty3)')
        parser.add_argument('--no-port', dest='exclude', action='append', nargs='*', type=str, default=[], help='Exclude ports')
        parser.add_argument('--data-rate', dest='data_rate', action='store', nargs=1, type=int, help='Connection data-rate (default: %(default)s)')
        parser.add_argument('--host-id', dest='host_id', action='store', nargs=1, type=int, default=[2], help='TMCL host-id (default: %(default)s)')
        parser.add_argument('--module-id', dest='module_id', action='store', nargs=1, type=int, default=[1], help='TMCL module-id (default: %(default)s)')
        if not argList:
            argList = sys.argv
        args = parser.parse_known_args(argList)[0]
        self._ConnectionManager__debug = debug
        self._ConnectionManager__interface = usb_tmcl_interface
        self._ConnectionManager__port = 'any'
        self._ConnectionManager__no_port = []
        self._ConnectionManager__data_rate = 115200
        self._ConnectionManager__host_id = 2
        self._ConnectionManager__module_id = 1
        if self._ConnectionManager__debug:
            print('Commandline argument list: {0:s}'.format(str(self._ConnectionManager__argList)))
            print('Parsing {0:d} commandline arguments:'.format(len(self._ConnectionManager__argList)))
        if self._ConnectionManager__debug:
            print()
        for interface in self._INTERFACES:
            if args.interface[0] == interface[0]:
                self._ConnectionManager__interface = interface[1]
                self._ConnectionManager__data_rate = interface[2]
                break
        else:
            raise ValueError('Invalid interface: {0:s}'.format(args.interface[0]))

        self._ConnectionManager__port = args.port[0]
        for port in args.exclude:
            if port in ('any', 'interactive'):
                raise ValueError('Port blacklist (no-port) cannot use the special port: ' + port)

        try:
            self._ConnectionManager__data_rate = int(args.data_rate[0])
        except ValueError:
            raise ValueError('Invalid data rate: ' + args.data_rate[0])
        except TypeError:
            pass

        try:
            self._ConnectionManager__host_id = int(args.host_id[0])
        except ValueError:
            raise ValueError('Invalid host id: ' + args.host_id[0])

        try:
            self._ConnectionManager__module_id = int(args.module_id[0])
        except ValueError:
            raise ValueError('Invalid module id: ' + args.module_id[0])

        if self._ConnectionManager__debug:
            print('Connection parameters:')
            print('\tInterface:  ' + self._ConnectionManager__interface.__qualname__)
            print('\tPort:       ' + self._ConnectionManager__port)
            print('\tBlacklist:  ' + str(self._ConnectionManager__no_port))
            print('\tData rate:  ' + str(self._ConnectionManager__data_rate))
            print('\tHost ID:    ' + str(self._ConnectionManager__host_id))
            print('\tModule ID:  ' + str(self._ConnectionManager__module_id))
            print()

    def connect(self):
        """
        Attempt to connect to a module with the stored connection parameters.

        Returns a connection instance of a class based on the tmcl_interface.
        Which class type gets returned depends on the interface used.

        If no connections are available or a connection attempt fails, a
        ConnectionError exception is raised

        """
        portList = self.listConnections()
        if len(portList) == 0:
            raise ConnectionError('No connections available')
        if self._ConnectionManager__port == 'interactive':
            port = self._ConnectionManager__interactivePortSelection()
        else:
            if self._ConnectionManager__port == 'any':
                port = portList[0]
            else:
                try:
                    tmp = int(self._ConnectionManager__port)
                    try:
                        port = portList[tmp]
                    except IndexError:
                        raise ConnectionError("Couldn't connect to Port Number " + self._ConnectionManager__port + '. Only ' + str(len(portList)) + ' ports available')

                except ValueError:
                    port = self._ConnectionManager__port

                try:
                    if self._ConnectionManager__interface.supportsTMCL():
                        self._ConnectionManager__connection = self._ConnectionManager__interface(port, (self._ConnectionManager__data_rate), (self._ConnectionManager__host_id), (self._ConnectionManager__module_id), debug=(self._ConnectionManager__debug))
                    else:
                        self._ConnectionManager__connection = self._ConnectionManager__interface(port, (self._ConnectionManager__data_rate), debug=(self._ConnectionManager__debug))
                except ConnectionError as e:
                    try:
                        raise ConnectionError("Couldn't connect to port " + port + '. Connection failed.') from e
                    finally:
                        e = None
                        del e

                return self._ConnectionManager__connection

    def disconnect(self):
        self._ConnectionManager__connection.close()

    def listConnections(self):
        portList = self._ConnectionManager__interface.list()
        portList = [port for port in portList if port not in self._ConnectionManager__no_port]
        return portList

    def __interactivePortSelection(self):
        while 1:
            portList = self.listConnections()
            print('Available options:')
            for i, entry in enumerate(portList, 1):
                print('\t{0:2d}: {1:s}'.format(i, entry))

            print('\t x: Abort selection')
            print('\t r: Refresh list')
            while True:
                selection = input('Enter your selection: ')
                print()
                if selection == 'r':
                    break
                elif selection == 'x':
                    raise ConnectionError('Port selection aborted by user')
                else:
                    try:
                        selection = int(selection)
                        if not 1 <= selection <= len(portList):
                            raise ValueError
                        return portList[(selection - 1)]
                    except ValueError:
                        continue

    @staticmethod
    def listInterfaces():
        return [x[0] for x in ConnectionManager._INTERFACES]


if __name__ == '__main__':
    print('Verifying interfaces list...\n')
    for interface in ConnectionManager._INTERFACES:
        if not hasattr(interface[1], 'supportsTMCL'):
            raise NotImplementedError('Interface ' + interface[0] + ' is missing the supportsTMCL() function')
        if not hasattr(interface[1], 'close'):
            raise NotImplementedError('Interface ' + interface[0] + ' is missing the close() function')
        if not hasattr(interface[1], 'list'):
            raise NotImplementedError('Interface ' + interface[0] + ' is missing the list() function')

    print('List of interfaces: ' + str(ConnectionManager.listInterfaces()) + '\n')
    print('Performing test run...\n')
    connectionManager = ConnectionManager()
    try:
        connection = connectionManager.connect()
        connectionManager.disconnect()
    except RuntimeError:
        print("Couldn't connect to the specified port(s)")

    print('Test run complete')