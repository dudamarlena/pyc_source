# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/flowproc/flowprocd.py
# Compiled at: 2019-07-06 23:08:34
# Size of source mod 2**32: 3639 bytes
"""
The flow collector daemon
"""
import argparse, logging, socketserver, sys
from flowproc import process
from flowproc import __version__
__author__ = 'Tobias Frei'
__copyright__ = 'Tobias Frei'
__license__ = 'mit'
logger = logging.getLogger(__name__)

def parse_args(args):
    """Parse command line parameters

    Args:
      args ([str]): command line parameters as list of strings

    Returns:
      :obj:`argparse.Namespace`: command line parameters namespace
    """
    parser = argparse.ArgumentParser(description='Flow collector daemon command line interface',
      formatter_class=(argparse.ArgumentDefaultsHelpFormatter))
    parser.add_argument(dest='socket',
      choices=[
     'udp', 'tcp'],
      default='udp',
      help='select server socket type (future should bring sctp)')
    parser.add_argument('--host',
      default='0.0.0.0',
      help='set address to listen on',
      action='store',
      metavar='ipaddr')
    parser.add_argument('-p',
      '--port',
      default=2055,
      help='set port to listen on',
      type=int,
      action='store',
      metavar='int')
    parser.add_argument('--logfile',
      default='stderr',
      help='set file to log to',
      action='store',
      metavar='path')
    parser.add_argument('-v',
      dest='loglevel',
      help='set loglevel INFO',
      action='store_const',
      const=(logging.INFO))
    parser.add_argument('-vv',
      dest='loglevel',
      help='set loglevel DEBUG',
      action='store_const',
      const=(logging.DEBUG))
    parser.add_argument('-V',
      '--version',
      help='print version and exit',
      action='version',
      version='flowproc {ver}'.format(ver=__version__))
    return parser.parse_args(args)


class _NetFlowUDPHandler(socketserver.DatagramRequestHandler):

    def handle(self):
        client_addr = self.client_address[0]
        export_packet = self.request[0]
        process(client_addr, export_packet, None)


def start_listener(socket_type, addr):
    """Start socketserver
    Args:
        socket_Type     `str`       for the time being just UDP
        addr            `str`,`int` tuple (host, port)
    """
    if socket_type.upper() == 'UDP':
        s = socketserver.UDPServer(addr, _NetFlowUDPHandler)
        s.serve_forever()
    else:
        logger.error("There's no TCP without IPFIX support, exiting...")


def setup_logging(loglevel):
    """Setup basic logging

    Args:
      loglevel (int): minimum loglevel for emitting messages
    """
    logformat = '[%(asctime)s] %(levelname)-9s %(name)s: %(message)s'
    logging.basicConfig(level=loglevel,
      stream=(sys.stdout),
      format=logformat,
      datefmt='%b %d %Y %H:%M:%S')


def main(args):
    """Main entry point allowing external calls

    Args:
      args ([str]): command line parameter list
    """
    args = parse_args(args)
    setup_logging(args.loglevel)
    logger.info('Starting version {}'.format(__version__))
    logger.info('Args {}'.format(vars(args)))
    try:
        start_listener(args.socket, (args.host, args.port))
    except KeyboardInterrupt:
        logger.info('Shutting down...')


def run():
    """Entry point for console_scripts
    """
    main(sys.argv[1:])


if __name__ == '__main__':
    run()