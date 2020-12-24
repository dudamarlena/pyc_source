# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/fraoustin/Téléchargements/ocglances/tmp/ocglances/plugins/glances_ports.py
# Compiled at: 2017-02-11 10:25:25
"""Ports scanner plugin."""
import os, subprocess, threading, socket, time
from ocglances.globals import WINDOWS
from ocglances.ports_list import GlancesPortsList
from ocglances.timer import Timer, Counter
from ocglances.compat import bool_type
from ocglances.logger import logger
from ocglances.plugins.glances_plugin import GlancesPlugin

class Plugin(GlancesPlugin):
    """Glances ports scanner plugin."""

    def __init__(self, args=None, config=None):
        """Init the plugin."""
        super(Plugin, self).__init__(args=args)
        self.args = args
        self.config = config
        self.display_curse = True
        self.stats = GlancesPortsList(config=config, args=args).get_ports_list()
        self.timer_ports = Timer(0)
        self._thread = None
        return

    def exit(self):
        """Overwrite the exit method to close threads"""
        if self._thread is not None:
            self._thread.stop()
        super(Plugin, self).exit()
        return

    def reset(self):
        """Reset/init the stats."""
        self.stats = []

    @GlancesPlugin._log_result_decorator
    def update(self):
        """Update the ports list."""
        if self.input_method == 'local':
            if self._thread is None:
                thread_is_running = False
            else:
                thread_is_running = self._thread.isAlive()
            if self.timer_ports.finished() and not thread_is_running:
                self._thread = ThreadScanner(self.stats)
                self._thread.start()
                if len(self.stats) > 0:
                    self.timer_ports = Timer(self.stats[0]['refresh'])
                else:
                    self.timer_ports = Timer(0)
        return self.stats

    def get_alert(self, port, header='', log=False):
        """Return the alert status relative to the port scan return value."""
        if port['status'] is None:
            return 'CAREFUL'
        else:
            if port['status'] == 0:
                return 'CRITICAL'
            if isinstance(port['status'], (float, int)) and port['rtt_warning'] is not None and port['status'] > port['rtt_warning']:
                return 'WARNING'
            return 'OK'

    def msg_curse(self, args=None):
        """Return the dict to display in the curse interface."""
        ret = []
        if not self.stats or args.disable_ports:
            return ret
        for p in self.stats:
            if p['status'] is None:
                status = 'Scanning'
            elif isinstance(p['status'], bool_type) and p['status'] is True:
                status = 'Open'
            elif p['status'] == 0:
                status = 'Timeout'
            else:
                status = ('{0:.0f}ms').format(p['status'] * 1000.0)
            msg = ('{:14.14} ').format(p['description'])
            ret.append(self.curse_add_line(msg))
            msg = ('{:>8}').format(status)
            ret.append(self.curse_add_line(msg, self.get_alert(p)))
            ret.append(self.curse_new_line())

        try:
            ret.pop()
        except IndexError:
            pass

        return ret

    def _port_scan_all(self, stats):
        """Scan all host/port of the given stats"""
        for p in stats:
            self._port_scan(p)
            time.sleep(1)


class ThreadScanner(threading.Thread):
    """
    Specific thread for the port scanner.

    stats is a list of dict
    """

    def __init__(self, stats):
        """Init the class"""
        logger.debug(('ports plugin - Create thread for scan list {}').format(stats))
        super(ThreadScanner, self).__init__()
        self._stopper = threading.Event()
        self._stats = stats
        self.plugin_name = 'ports'

    def run(self):
        """Function called to grab stats.
        Infinite loop, should be stopped by calling the stop() method"""
        for p in self._stats:
            self._port_scan(p)
            if self.stopped():
                break
            time.sleep(1)

    @property
    def stats(self):
        """Stats getter"""
        return self._stats

    @stats.setter
    def stats(self, value):
        """Stats setter"""
        self._stats = value

    def stop(self, timeout=None):
        """Stop the thread"""
        logger.debug(('ports plugin - Close thread for scan list {}').format(self._stats))
        self._stopper.set()

    def stopped(self):
        """Return True is the thread is stopped"""
        return self._stopper.isSet()

    def _port_scan(self, port):
        """Scan the port structure (dict) and update the status key"""
        if int(port['port']) == 0:
            return self._port_scan_icmp(port)
        else:
            return self._port_scan_tcp(port)

    def _resolv_name(self, hostname):
        """Convert hostname to IP address"""
        ip = hostname
        try:
            ip = socket.gethostbyname(hostname)
        except Exception as e:
            logger.debug(('{}: Cannot convert {} to IP address ({})').format(self.plugin_name, hostname, e))

        return ip

    def _port_scan_icmp(self, port):
        """Scan the (ICMP) port structure (dict) and update the status key"""
        ret = None
        cmd = [
         'ping', '-n' if WINDOWS else '-c', '1', self._resolv_name(port['host'])]
        fnull = open(os.devnull, 'w')
        try:
            counter = Counter()
            ret = subprocess.check_call(cmd, stdout=fnull, stderr=fnull, close_fds=True)
            if ret == 0:
                port['status'] = counter.get()
            else:
                port['status'] = False
        except Exception as e:
            logger.debug(('{}: Error while pinging host {} ({})').format(self.plugin_name, port['host'], e))

        return ret

    def _port_scan_tcp(self, port):
        """Scan the (TCP) port structure (dict) and update the status key"""
        ret = None
        try:
            socket.setdefaulttimeout(port['timeout'])
            _socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except Exception as e:
            logger.debug(('{}: Error while creating scanning socket').format(self.plugin_name))

        ip = self._resolv_name(port['host'])
        counter = Counter()
        try:
            try:
                ret = _socket.connect_ex((ip, int(port['port'])))
            except Exception as e:
                logger.debug(('{}: Error while scanning port {} ({})').format(self.plugin_name, port, e))

            if ret == 0:
                port['status'] = counter.get()
            else:
                port['status'] = False
        finally:
            _socket.close()

        return ret