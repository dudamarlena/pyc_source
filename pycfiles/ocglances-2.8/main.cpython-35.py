# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\faoustin\Downloads\ocglances\ocglances\main.py
# Compiled at: 2017-02-13 10:56:38
# Size of source mod 2**32: 24518 bytes
"""Glances main class."""
import argparse, os, sys, tempfile
from ocglances import __version__, psutil_version
from ocglances.compat import input
from ocglances.config import Config
from ocglances.globals import LINUX, WINDOWS
from ocglances.logger import logger

class GlancesMain(object):
    __doc__ = 'Main class to manage Glances instance.'
    refresh_time = 3
    cached_time = 1
    client_tag = False
    server_port = 61209
    web_server_port = 61208
    username = 'glances'
    password = ''
    example_of_use = 'Examples of use:\n\nMonitor local machine (standalone mode):\n  $ glances\n\nMonitor local machine with the Web interface (Web UI):\n  $ glances -w\n  Glances web server started on http://0.0.0.0:61208/\n\nMonitor local machine and export stats to a CSV file (standalone mode):\n  $ glances --export-csv /tmp/glances.csv\n\nMonitor local machine and export stats to a InfluxDB server with 5s refresh time (standalone mode):\n  $ glances -t 5 --export-influxdb\n\nStart a Glances server (server mode):\n  $ glances -s\n\nConnect Glances to a Glances server (client mode):\n  $ glances -c <ip_server>\n\nConnect Glances to a Glances server and export stats to a StatsD server (client mode):\n  $ glances -c <ip_server> --export-statsd\n\nStart the client browser (browser mode):\n  $ glances --browser\n    '
    example_of_use = '\nExamples of use:\n\nConnect Glances to a Glances server (client mode):\n  $ glances -c <ip_server>\n\nConnect Glances to a Glances server and export stats to a StatsD server (client mode):\n  $ glances -c <ip_server> --export-statsd\n'

    def __init__(self):
        """Manage the command line arguments."""
        self.args = self.parse_args()

    def init_args(self):
        """Init all the command line arguments."""
        version = 'OCGlances v' + __version__
        parser = argparse.ArgumentParser(prog='glances', conflict_handler='resolve', formatter_class=argparse.RawDescriptionHelpFormatter, epilog=self.example_of_use)
        parser.add_argument('-V', '--version', action='version', version=version)
        parser.add_argument('-d', '--debug', action='store_true', default=False, dest='debug', help='enable debug mode')
        parser.add_argument('-C', '--config', dest='conf_file', help='path to the configuration file')
        parser.add_argument('--disable-alert', action='store_true', default=False, dest='disable_alert', help='disable alert module')
        parser.add_argument('--disable-amps', action='store_true', default=False, dest='disable_amps', help='disable applications monitoring process (AMP) module')
        parser.add_argument('--disable-cpu', action='store_true', default=False, dest='disable_cpu', help='disable CPU module')
        parser.add_argument('--disable-diskio', action='store_true', default=False, dest='disable_diskio', help='disable disk I/O module')
        parser.add_argument('--disable-docker', action='store_true', default=False, dest='disable_docker', help='disable Docker module')
        parser.add_argument('--disable-folders', action='store_true', default=False, dest='disable_folders', help='disable folder module')
        parser.add_argument('--disable-fs', action='store_true', default=False, dest='disable_fs', help='disable filesystem module')
        parser.add_argument('--disable-gpu', action='store_true', default=False, dest='disable_gpu', help='disable GPU module')
        parser.add_argument('--disable-hddtemp', action='store_true', default=False, dest='disable_hddtemp', help='disable HD temperature module')
        parser.add_argument('--disable-ip', action='store_true', default=False, dest='disable_ip', help='disable IP module')
        parser.add_argument('--disable-load', action='store_true', default=False, dest='disable_load', help='disable load module')
        parser.add_argument('--disable-mem', action='store_true', default=False, dest='disable_mem', help='disable memory module')
        parser.add_argument('--disable-memswap', action='store_true', default=False, dest='disable_memswap', help='disable memory swap module')
        parser.add_argument('--disable-network', action='store_true', default=False, dest='disable_network', help='disable network module')
        parser.add_argument('--disable-now', action='store_true', default=False, dest='disable_now', help='disable current time module')
        parser.add_argument('--disable-ports', action='store_true', default=False, dest='disable_ports', help='disable ports scanner module')
        parser.add_argument('--disable-process', action='store_true', default=False, dest='disable_process', help='disable process module')
        parser.add_argument('--disable-raid', action='store_true', default=False, dest='disable_raid', help='disable RAID module')
        parser.add_argument('--disable-sensors', action='store_true', default=False, dest='disable_sensors', help='disable sensors module')
        parser.add_argument('--disable-wifi', action='store_true', default=False, dest='disable_wifi', help='disable wifi module')
        parser.add_argument('-0', '--disable-irix', action='store_true', default=False, dest='disable_irix', help="task's cpu usage will be divided by the total number of CPUs")
        parser.add_argument('-1', '--percpu', action='store_true', default=False, dest='percpu', help='start Glances in per CPU mode')
        parser.add_argument('-2', '--disable-left-sidebar', action='store_true', default=False, dest='disable_left_sidebar', help='disable network, disk I/O, FS and sensors modules')
        parser.add_argument('-3', '--disable-quicklook', action='store_true', default=False, dest='disable_quicklook', help='disable quick look module')
        parser.add_argument('-4', '--full-quicklook', action='store_true', default=False, dest='full_quicklook', help='disable all but quick look and load')
        parser.add_argument('-5', '--disable-top', action='store_true', default=False, dest='disable_top', help='disable top menu (QL, CPU, MEM, SWAP and LOAD)')
        parser.add_argument('-6', '--meangpu', action='store_true', default=False, dest='meangpu', help='start Glances in mean GPU mode')
        parser.add_argument('--disable-history', action='store_true', default=False, dest='disable_history', help='disable stats history')
        parser.add_argument('--disable-bold', action='store_true', default=False, dest='disable_bold', help='disable bold mode in the terminal')
        parser.add_argument('--disable-bg', action='store_true', default=False, dest='disable_bg', help='disable background colors in the terminal')
        (
         parser.add_argument('--enable-irq', action='store_true', default=False, dest='enable_irq', help='enable IRQ module'),)
        parser.add_argument('--enable-process-extended', action='store_true', default=False, dest='enable_process_extended', help='enable extended stats on top process')
        parser.add_argument('--export-graph', action='store_true', default=None, dest='export_graph', help='export stats to graphs')
        parser.add_argument('--path-graph', default=tempfile.gettempdir(), dest='path_graph', help='set the export path for graphs (default is {})'.format(tempfile.gettempdir()))
        parser.add_argument('--export-csv', default=None, dest='export_csv', help='export stats to a CSV file')
        parser.add_argument('--export-influxdb', action='store_true', default=False, dest='export_influxdb', help='export stats to an InfluxDB server (influxdb lib needed)')
        parser.add_argument('--export-cassandra', action='store_true', default=False, dest='export_cassandra', help='export stats to a Cassandra or Scylla server (cassandra lib needed)')
        parser.add_argument('--export-opentsdb', action='store_true', default=False, dest='export_opentsdb', help='export stats to an OpenTSDB server (potsdb lib needed)')
        parser.add_argument('--export-statsd', action='store_true', default=False, dest='export_statsd', help='export stats to a StatsD server (statsd lib needed)')
        parser.add_argument('--export-elasticsearch', action='store_true', default=False, dest='export_elasticsearch', help='export stats to an ElasticSearch server (elasticsearch lib needed)')
        parser.add_argument('--export-rabbitmq', action='store_true', default=False, dest='export_rabbitmq', help='export stats to rabbitmq broker (pika lib needed)')
        parser.add_argument('--export-riemann', action='store_true', default=False, dest='export_riemann', help='export stats to riemann broker (bernhard lib needed)')
        parser.add_argument('--export-couchdb', action='store_true', default=False, dest='export_couchdb', help='export stats to a CouchDB server (couch lib needed)')
        parser.add_argument('--export-zeromq', action='store_true', default=False, dest='export_zeromq', help='export stats to a ZeroMQ server (pyzmq lib needed)')
        parser.add_argument('-c', '--client', dest='client', default='127.0.0.1', help='connect to a Glances server by IPv4/IPv6 address or hostname')
        parser.add_argument('-p', '--port', default=None, type=int, dest='port', help='define the client/server TCP port [default: {}]'.format(self.server_port))
        parser.add_argument('--username', action='store_true', default=False, dest='username_prompt', help='define a client/server username')
        parser.add_argument('--password', action='store_true', default=False, dest='password_prompt', help='define a client/server password')
        parser.add_argument('--snmp-community', default='public', dest='snmp_community', help='SNMP community')
        parser.add_argument('--snmp-port', default=161, type=int, dest='snmp_port', help='SNMP port')
        parser.add_argument('--snmp-version', default='2c', dest='snmp_version', help='SNMP version (1, 2c or 3)')
        parser.add_argument('--snmp-user', default='private', dest='snmp_user', help='SNMP username (only for SNMPv3)')
        parser.add_argument('--snmp-auth', default='password', dest='snmp_auth', help='SNMP authentication key (only for SNMPv3)')
        parser.add_argument('--snmp-force', action='store_true', default=False, dest='snmp_force', help='force SNMP mode')
        parser.add_argument('-t', '--time', default=self.refresh_time, type=float, dest='time', help='set refresh time in seconds [default: {} sec]'.format(self.refresh_time))
        parser.add_argument('-q', '--quiet', default=False, action='store_true', dest='quiet', help='do not display the curses interface')
        parser.add_argument('-f', '--process-filter', default=None, type=str, dest='process_filter', help='set the process filter pattern (regular expression)')
        parser.add_argument('--process-short-name', action='store_true', default=False, dest='process_short_name', help='force short name for processes name')
        if not WINDOWS:
            parser.add_argument('--hide-kernel-threads', action='store_true', default=False, dest='no_kernel_threads', help='hide kernel threads in process list')
        if LINUX:
            parser.add_argument('--tree', action='store_true', default=False, dest='process_tree', help='display processes as a tree')
        parser.add_argument('-b', '--byte', action='store_true', default=False, dest='byte', help='display network rate in byte per second')
        parser.add_argument('--diskio-show-ramfs', action='store_true', default=False, dest='diskio_show_ramfs', help='show RAM Fs in the DiskIO plugin')
        parser.add_argument('--diskio-iops', action='store_true', default=False, dest='diskio_iops', help='show IO per second in the DiskIO plugin')
        parser.add_argument('--fahrenheit', action='store_true', default=False, dest='fahrenheit', help='display temperature in Fahrenheit (default is Celsius)')
        parser.add_argument('--fs-free-space', action='store_true', default=False, dest='fs_free_space', help='display FS free space instead of used')
        parser.add_argument('--theme-white', action='store_true', default=False, dest='theme_white', help='optimize display colors for white background')
        parser.add_argument('--disable-check-update', action='store_true', default=False, dest='disable_check_update', help='disable online Glances version ckeck')
        return parser

    def parse_args(self):
        """Parse command line arguments."""
        args = self.init_args().parse_args()
        args.server = False
        args.webserver = False
        args.bind_address = '0.0.0.0'
        args.browser = False
        args.disable_autodiscover = False
        args.open_web_browser = False
        args.cached_time = 1
        self.config = Config(args.conf_file)
        if args.debug:
            from logging import DEBUG
            logger.setLevel(DEBUG)
        if args.port is None:
            if args.webserver:
                args.port = self.web_server_port
        else:
            args.port = self.server_port
        if args.disable_autodiscover:
            logger.info('Auto discover mode is disabled')
        if args.webserver:
            args.process_short_name = True
        if args.username_prompt:
            args.password_prompt = True
            if args.server:
                args.username = self._GlancesMain__get_username(description='Define the Glances server username: ')
            else:
                if args.webserver:
                    args.username = self._GlancesMain__get_username(description='Define the Glances webserver username: ')
                elif args.client:
                    args.username = self._GlancesMain__get_username(description='Enter the Glances server username: ')
        else:
            args.username = self.username
        if args.password_prompt:
            if args.server:
                args.password = self._GlancesMain__get_password(description='Define the Glances server password ({} username): '.format(args.username), confirm=True, username=args.username)
            else:
                if args.webserver:
                    args.password = self._GlancesMain__get_password(description='Define the Glances webserver password ({} username): '.format(args.username), confirm=True, username=args.username)
                elif args.client:
                    args.password = self._GlancesMain__get_password(description='Enter the Glances server password ({} username): '.format(args.username), clear=True, username=args.username)
        else:
            args.password = self.password
        args.help_tag = False
        args.network_sum = False
        args.network_cumul = False
        if args.full_quicklook:
            logger.info('Disable QuickLook menu')
            args.disable_quicklook = False
            args.disable_cpu = True
            args.disable_mem = True
            args.disable_memswap = True
            args.disable_load = False
        if args.disable_top:
            logger.info('Disable top menu')
            args.disable_quicklook = True
            args.disable_cpu = True
            args.disable_mem = True
            args.disable_memswap = True
            args.disable_load = True
        self.args = args
        export_tag = args.export_csv or args.export_elasticsearch or args.export_statsd or args.export_influxdb or args.export_cassandra or args.export_opentsdb or args.export_rabbitmq or args.export_couchdb
        if not (self.is_standalone() or self.is_client()) and export_tag:
            logger.critical('Export is only available in standalone or client mode')
            sys.exit(2)
        if args.process_filter is not None and not self.is_standalone():
            logger.critical('Process filter is only available in standalone mode')
            sys.exit(2)
        if args.export_graph and args.path_graph is not None:
            if not os.access(args.path_graph, os.W_OK):
                logger.critical("Graphs output path {} doesn't exist or is not writable".format(args.path_graph))
                sys.exit(2)
            logger.debug('Graphs output path is set to {}'.format(args.path_graph))
        if args.export_graph and args.disable_history:
            logger.critical('Can not export graph if history is disabled')
            sys.exit(2)
        if args.disable_sensors:
            args.disable_hddtemp = True
            logger.debug('Sensors and HDDTemp are disabled')
        return args

    def __get_username(self, description=''):
        """Read a username from the command line.
        """
        return input(description)

    def __get_password(self, description='', confirm=False, clear=False, username='glances'):
        """Read a password from the command line.

        - if confirm = True, with confirmation
        - if clear = True, plain (clear password)
        """
        from ocglances.password import GlancesPassword
        password = GlancesPassword(username=username)
        return password.get_password(description, confirm, clear)

    def is_standalone(self):
        """Return True if Glances is running in standalone mode."""
        return not self.args.client and not self.args.browser and not self.args.server and not self.args.webserver

    def is_client(self):
        """Return True if Glances is running in client mode."""
        return (self.args.client or self.args.browser) and not self.args.server

    def is_client_browser(self):
        """Return True if Glances is running in client browser mode."""
        return self.args.browser and not self.args.server

    def is_server(self):
        """Return True if Glances is running in server mode."""
        return not self.args.client and self.args.server

    def is_webserver(self):
        """Return True if Glances is running in Web server mode."""
        return not self.args.client and self.args.webserver

    def get_config(self):
        """Return configuration file object."""
        return self.config

    def get_args(self):
        """Return the arguments."""
        return self.args