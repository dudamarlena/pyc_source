# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/dyntftpd/cli.py
# Compiled at: 2015-04-13 06:26:22
import argparse, logging, logging.config
from .server import TFTPServer

def arguments_parser():
    parser = argparse.ArgumentParser(description='Extendable TFTP server, implemented in Python')
    parser.add_argument('--host', '-H', default='')
    parser.add_argument('--port', '-p', default=69, type=int)
    parser.add_argument('--root', '-r', default='/var/lib/tftpboot/', help='TFTP root folder')
    return parser


def main():
    parser = arguments_parser()
    parser.add_argument('-v', dest='verbose', action='count', default=0, help='Verbose mode')
    args = parser.parse_args()
    log_level = logging.DEBUG if args.verbose else logging.INFO
    logging.config.dictConfig({'version': 1, 
       'disable_existing_loggers': False, 
       'formatters': {'with_client_ip': {'format': '[%(asctime)-15s] %(levelname)s %(client_ip)s: %(message)s'}}, 
       'handlers': {'console': {'class': 'logging.StreamHandler'}, 
                    'console_with_client_ip': {'class': 'logging.StreamHandler', 
                                               'formatter': 'with_client_ip'}}, 
       'loggers': {'': {'handlers': [
                                   'console'], 
                        'level': log_level}, 
                   'dyntftpd': {'handlers': [
                                           'console_with_client_ip'], 
                                'propagate': False, 
                                'level': log_level}}})
    tftp_server = TFTPServer(args.host, args.port, root=args.root)
    tftp_server.serve_forever()