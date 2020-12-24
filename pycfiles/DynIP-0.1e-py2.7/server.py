# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dynip/server.py
# Compiled at: 2011-11-30 01:05:44
"""
DynIP Server

A embarrisingly-simple server which listens for UDP packets and logs
the data, the source IP address and time.
"""
import socket, json, logging, sys, datetime, traceback, os, argparse, ConfigParser, return_codes as rc
logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.WARNING)
CONFIG_SECTION = 'DynIP:Server'
DEFAULT_SERVER_IP = '*'
DEFAULT_SERVER_PORT = 28630
DEFAULT_CLIENT_LOG_PATH = 'dynip.json'
DATA_SIZE_MAX = 256
argparser = argparse.ArgumentParser(description='')
argparser.add_argument('-v', '--verbose', help='Enable verbose (INFO-level) logging', action='store_const', default=logging.WARNING, const=logging.INFO)
argparser.add_argument('--debug', help='Enable debug (DEBUG-level) logging', action='store_const', default=logging.WARNING, const=logging.DEBUG)
argparser.add_argument('config', help='Configuration .conf file', type=str, nargs=1)

def main():
    """
    Listen for UDP packets and save the remote IP address and data
    to the file specified in ``client_log_path`` in the configuration file

    Notes: This reads the entire JSON file in on each packet, so
    this is not suitable for any significant load or anything but
    a trivial number of clients.
    """
    args = argparser.parse_args()
    log.setLevel(min(args.verbose, args.debug))
    try:
        config = ConfigParser.ConfigParser({CONFIG_SECTION: {'server_ip': DEFAULT_SERVER_IP, 'server_port': DEFAULT_SERVER_PORT, 
                            'client_log_path': DEFAULT_CLIENT_LOG_PATH}})
        config.read(args.config)
        server_ip = config.get(CONFIG_SECTION, 'server_ip')
        server_port = config.getint(CONFIG_SECTION, 'server_port')
        client_log_path = config.get(CONFIG_SECTION, 'client_log_path')
    except:
        log.fatal(('ERROR: Could not read configuration file {0}').format(args.config))
        return rc.CANNOT_READ_CONFIG

    log.info('Starting server...')
    if os.path.exists(client_log_path) == False:
        client_data = {}
    else:
        try:
            log.info(('Opening file at client_log_path: {0}').format(client_log_path))
            client_log_fh = open(client_log_path, 'r')
        except:
            log.fatal(('ERROR: Could not open {0}').format(client_log_path))
            return rc.CANNOT_OPEN_CLIENT_LOG_PATH

        log.info(('Opened client_log_path successfully').format(client_log_path))
        try:
            log.info('Importing json data from client_log_path')
            client_data = json.load(client_log_fh)
            if isinstance(client_data, dict) == False:
                client_data = {}
        except:
            log.debug(traceback.format_exc())
            log.info('Improper format of client_log_path file found.  Starting from scratch.')
            client_data = {}

        log.debug(client_data)
        client_log_fh.close()
    log.info('Opening UDP socket')
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    if server_ip == '*':
        log.info('Discovering IP address')
        server_ip = socket.gethostbyname(socket.gethostname())
    sock.bind((server_ip, server_port))
    log.info(('Listening on {0}:{1}').format(server_ip, server_port))
    if listen_loop(sock, client_data, client_log_path) != True:
        log.error('The listen_loop did not exit gracefully.')
    log.info('Shutting down the server')
    sock.close()
    log.info('Server stopped')
    return rc.OK


def listen_loop(sock, client_data, client_log_path):
    """
    A blocking loop that listens for UDP packets, logs them, and then waits for the next one.
    Exits when a KeyboardInterrupt is caught.

    :param sock: The bound socket.socketobject
    :type sock: socket.socketobject
    :param client_data: The in-memory client data dict that is written out to the ``client_log_path`` on receipt of each packet.
    :type client_data: dict
    :param client_log_path: The filepath to the JSON-encoded client log file
    :type client_log_path: str
    """
    try:
        while True:
            log.debug('Waiting for the next packet')
            data, addr = sock.recvfrom(1024)
            now = datetime.datetime.now().isoformat(' ')
            log.debug(('{now} Received packet from {addr} | Data: {data}').format(addr=addr, data=data, now=now))
            client_data[data[:DATA_SIZE_MAX]] = [
             addr[0],
             now]
            log.info('Saving data')
            client_log_fh = open(client_log_path, 'w')
            json.dump(client_data, client_log_fh)
            client_log_fh.close()

    except KeyboardInterrupt:
        log.info('Caught KeyboardInterrupt.  Exiting gracefully')
        if client_log_fh is not None and client_log_fh.closed is False:
            client_log_fh.close()

    return True


def usage():
    """Print usage information"""
    argparser.print_help()


if __name__ == '__main__':
    sys.exit(main())