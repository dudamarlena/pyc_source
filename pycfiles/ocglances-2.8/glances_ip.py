# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/fraoustin/Téléchargements/ocglances/tmp/ocglances/plugins/glances_ip.py
# Compiled at: 2017-02-11 10:25:25
"""IP plugin."""
import threading
from json import loads
from ocglances.compat import iterkeys, urlopen, queue
from ocglances.globals import BSD
from ocglances.logger import logger
from ocglances.timer import Timer
from ocglances.plugins.glances_plugin import GlancesPlugin
if not BSD:
    try:
        import netifaces
        netifaces_tag = True
    except ImportError:
        netifaces_tag = False

else:
    netifaces_tag = False
urls = [
 (
  'http://ip.42.pl/raw', False, None),
 (
  'http://httpbin.org/ip', True, 'origin'),
 (
  'http://jsonip.com', True, 'ip'),
 (
  'https://api.ipify.org/?format=json', True, 'ip')]

class Plugin(GlancesPlugin):
    """Glances IP Plugin.

    stats is a dict
    """

    def __init__(self, args=None):
        """Init the plugin."""
        super(Plugin, self).__init__(args=args)
        self.display_curse = True
        self.public_address = PublicIpAddress().get()
        self.reset()

    def reset(self):
        """Reset/init the stats."""
        self.stats = {}

    @GlancesPlugin._check_decorator
    @GlancesPlugin._log_result_decorator
    def update(self):
        """Update IP stats using the input method.

        Stats is dict
        """
        self.reset()
        if self.input_method == 'local' and netifaces_tag:
            try:
                default_gw = netifaces.gateways()['default'][netifaces.AF_INET]
            except (KeyError, AttributeError) as e:
                logger.debug(('Cannot grab the default gateway ({})').format(e))
            else:
                try:
                    self.stats['address'] = netifaces.ifaddresses(default_gw[1])[netifaces.AF_INET][0]['addr']
                    self.stats['mask'] = netifaces.ifaddresses(default_gw[1])[netifaces.AF_INET][0]['netmask']
                    self.stats['mask_cidr'] = self.ip_to_cidr(self.stats['mask'])
                    self.stats['gateway'] = netifaces.gateways()['default'][netifaces.AF_INET][0]
                    self.stats['public_address'] = self.public_address
                except (KeyError, AttributeError) as e:
                    logger.debug(('Cannot grab IP information: {}').format(e))

        elif self.input_method == 'snmp':
            pass
        return self.stats

    def update_views(self):
        """Update stats views."""
        super(Plugin, self).update_views()
        for key in iterkeys(self.stats):
            self.views[key]['optional'] = True

    def msg_curse(self, args=None):
        """Return the dict to display in the curse interface."""
        ret = []
        if not self.stats or self.is_disable():
            return ret
        msg = ' - '
        ret.append(self.curse_add_line(msg))
        msg = 'IP '
        ret.append(self.curse_add_line(msg, 'TITLE'))
        msg = ('{}').format(self.stats['address'])
        ret.append(self.curse_add_line(msg))
        if 'mask_cidr' in self.stats:
            msg = ('/{}').format(self.stats['mask_cidr'])
            ret.append(self.curse_add_line(msg))
        try:
            msg_pub = ('{}').format(self.stats['public_address'])
        except UnicodeEncodeError:
            pass

        if self.stats['public_address'] is not None:
            msg = ' Pub '
            ret.append(self.curse_add_line(msg, 'TITLE'))
            ret.append(self.curse_add_line(msg_pub))
        return ret

    @staticmethod
    def ip_to_cidr(ip):
        """Convert IP address to CIDR.

        Example: '255.255.255.0' will return 24
        """
        return sum([ int(x) << 8 for x in ip.split('.') ]) // 8128


class PublicIpAddress(object):
    """Get public IP address from online services"""

    def __init__(self, timeout=2):
        self.timeout = timeout

    def get(self):
        """Get the first public IP address returned by one of the online services"""
        q = queue.Queue()
        for u, j, k in urls:
            t = threading.Thread(target=self._get_ip_public, args=(q, u, j, k))
            t.daemon = True
            t.start()

        timer = Timer(self.timeout)
        ip = None
        while not timer.finished() and ip is None:
            if q.qsize() > 0:
                ip = q.get()

        return ip

    def _get_ip_public(self, queue_target, url, json=False, key=None):
        """Request the url service and put the result in the queue_target"""
        try:
            response = urlopen(url, timeout=self.timeout).read().decode('utf-8')
        except Exception as e:
            logger.debug(('IP plugin - Cannot open URL {} ({})').format(url, e))
            queue_target.put(None)
        else:
            try:
                if not json:
                    queue_target.put(response)
                else:
                    queue_target.put(loads(response)[key])
            except ValueError:
                queue_target.put(None)

        return