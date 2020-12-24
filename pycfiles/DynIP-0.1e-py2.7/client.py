# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dynip/client.py
# Compiled at: 2011-11-30 01:06:30
"""
DynIP Client

A embarrisingly-simple client with sends UDP packets to the DynIP server.
"""
import socket, sys, logging, argparse, ConfigParser, traceback, return_codes as rc
CONFIG_SECTION = 'DynIP:Client'
DEFAULT_SERVER_HOSTNAME = 'localhost'
DEFAULT_SERVER_PORT = 28630
logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.WARNING)
argparser = argparse.ArgumentParser(description='Sends a single packet to the DynIP server.')
argparser.add_argument('-v', '--verbose', help='Enable verbose (INFO-level) logging', action='store_const', default=logging.WARNING, const=logging.INFO)
argparser.add_argument('--debug', help='Enable debug (DEBUG-level) logging', action='store_const', default=logging.WARNING, const=logging.DEBUG)
argparser.add_argument('config', help='Configuration .conf file', type=str, nargs=1)

def main():
    """
    Send a single UDP datagram to the server
    """
    args = argparser.parse_args()
    log.setLevel(min(args.verbose, args.debug))
    try:
        config = ConfigParser.ConfigParser({CONFIG_SECTION: {'server_hostname': DEFAULT_SERVER_HOSTNAME, 'server_port': DEFAULT_SERVER_PORT}})
        config.read(args.config)
        server_hostname = config.get(CONFIG_SECTION, 'server_hostname')
        server_port = config.get(CONFIG_SECTION, 'server_port')
    except:
        log.fatal(('ERROR: Could not read configuration file {0}').format(args.config))
        return rc.CANNOT_READ_CONFIG

    if server_hostname == '':
        log.fatal('ERROR: server_hostname is required')
        return rc.SERVER_HOSTNAME_MISSING
    else:
        log.debug('Looking up hostname')
        server_ip = socket.gethostbyname(server_hostname)
        if send_packet(server_ip, server_port) == True:
            return rc.OK
        return rc.PACKET_SEND_FAILED


def send_packet(destination_ip, destination_port):
    """
    Send a single UDP packet to the target server.

    :param destination_ip: IP address of the server
    :type desination_ip: str
    :param destination_port: Port number of the server
    :type destination_port: int
    """
    try:
        import socket
        log.debug('Preparing message')
        message = socket.gethostname()
        log.debug('Preparing socket')
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        log.debug(('Sending UDP datagram to {0}:{1}').format(destination_ip, destination_port))
        sock.sendto(message, (destination_ip, int(destination_port)))
        return True
    except:
        log.warning('Packet should not be sent to the destination')
        log.warning(traceback.format_exc())
        return False


def usage():
    """Print usage information"""
    argparser.print_help()


if __name__ == '__main__':
    sys.exit(main())