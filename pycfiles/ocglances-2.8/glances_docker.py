# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/fraoustin/Téléchargements/ocglances/tmp/ocglances/plugins/glances_docker.py
# Compiled at: 2017-02-11 10:25:25
"""Docker plugin."""
import os, re, threading, time
from ocglances.compat import iterkeys, itervalues
from ocglances.logger import logger
from ocglances.timer import getTimeSinceLastUpdate
from ocglances.plugins.glances_plugin import GlancesPlugin
from ocglances.globals import WINDOWS
try:
    import docker, requests
except ImportError as e:
    logger.debug('Docker library not found (%s). Glances cannot grab Docker info.' % e)
    docker_tag = False
else:
    docker_tag = True

class Plugin(GlancesPlugin):
    """Glances Docker plugin.

    stats is a list
    """

    def __init__(self, args=None):
        """Init the plugin."""
        super(Plugin, self).__init__(args=args)
        self.args = args
        self.display_curse = True
        self.docker_client = False
        self.thread_list = {}
        self.reset()

    def exit(self):
        """Overwrite the exit method to close threads"""
        for t in itervalues(self.thread_list):
            t.stop()

        super(Plugin, self).exit()

    def get_key(self):
        """Return the key of the list."""
        return 'name'

    def get_export(self):
        """Overwrite the default export method.

        - Only exports containers
        - The key is the first container name
        """
        ret = []
        try:
            ret = self.stats['containers']
        except KeyError as e:
            logger.debug(('Docker export error {}').format(e))

        return ret

    def __connect_old(self, version):
        """Connect to the Docker server with the 'old school' method"""
        if hasattr(docker, 'APIClient'):
            init_docker = docker.APIClient
        else:
            if hasattr(docker, 'Client'):
                init_docker = docker.Client
            else:
                logger.error('Can not found any way to init the Docker API')
                return
            try:
                if WINDOWS:
                    url = 'npipe:////./pipe/docker_engine'
                else:
                    url = 'unix://var/run/docker.sock'
                if version is None:
                    ret = init_docker(base_url=url)
                else:
                    ret = init_docker(base_url=url, version=version)
            except NameError:
                return

        return ret

    def connect(self, version=None):
        """Connect to the Docker server."""
        if hasattr(docker, 'from_env') and version is not None:
            ret = docker.from_env()
        else:
            ret = self.__connect_old(version=version)
        try:
            ret.version()
        except requests.exceptions.ConnectionError as e:
            logger.debug("Can't connect to the Docker server (%s)" % e)
            return
        except docker.errors.APIError as e:
            if version is None:
                logger.debug('Docker API error (%s)' % e)
                version = re.search('(?:server API version|server)\\:\\ (.*)\\)".*\\)', str(e))
                if version:
                    logger.debug('Try connection with Docker API version %s' % version.group(1))
                    ret = self.connect(version=version.group(1))
                else:
                    logger.debug('Can not retreive Docker server version')
                    ret = None
            else:
                logger.error('Docker API error (%s)' % e)
                ret = None
        except Exception as e:
            logger.error("Can't connect to the Docker server (%s)" % e)
            ret = None

        if ret is None:
            logger.debug('Docker plugin is disable because an error has been detected')
        return ret

    def reset(self):
        """Reset/init the stats."""
        self.stats = {}

    @GlancesPlugin._check_decorator
    @GlancesPlugin._log_result_decorator
    def update(self):
        """Update Docker stats using the input method."""
        global docker_tag
        self.reset()
        if not self.docker_client:
            try:
                self.docker_client = self.connect()
            except Exception:
                docker_tag = False
            else:
                if self.docker_client is None:
                    docker_tag = False
        if not docker_tag:
            return self.stats
        else:
            if self.input_method == 'local':
                try:
                    self.stats['version'] = self.docker_client.version()
                except Exception as e:
                    logger.error(('{} plugin - Cannot get Docker version ({})').format(self.plugin_name, e))
                    return self.stats

                try:
                    self.stats['containers'] = self.docker_client.containers() or []
                except Exception as e:
                    logger.error(('{} plugin - Cannot get containers list ({})').format(self.plugin_name, e))
                    return self.stats

                for container in self.stats['containers']:
                    if container['Id'] not in self.thread_list:
                        logger.debug(('{} plugin - Create thread for container {}').format(self.plugin_name, container['Id'][:12]))
                        t = ThreadDockerGrabber(self.docker_client, container['Id'])
                        self.thread_list[container['Id']] = t
                        t.start()

                nonexisting_containers = set(iterkeys(self.thread_list)) - set([ c['Id'] for c in self.stats['containers'] ])
                for container_id in nonexisting_containers:
                    logger.debug(('{} plugin - Stop thread for old container {}').format(self.plugin_name, container_id[:12]))
                    self.thread_list[container_id].stop()
                    del self.thread_list[container_id]

                for container in self.stats['containers']:
                    container['key'] = self.get_key()
                    container['name'] = container['Names'][0][1:]
                    container['cpu'] = self.get_docker_cpu(container['Id'], self.thread_list[container['Id']].stats)
                    container['memory'] = self.get_docker_memory(container['Id'], self.thread_list[container['Id']].stats)
                    container['network'] = self.get_docker_network(container['Id'], self.thread_list[container['Id']].stats)
                    container['io'] = self.get_docker_io(container['Id'], self.thread_list[container['Id']].stats)

            elif self.input_method == 'snmp':
                pass
            return self.stats

    def get_docker_cpu(self, container_id, all_stats):
        """Return the container CPU usage.

        Input: id is the full container id
               all_stats is the output of the stats method of the Docker API
        Output: a dict {'total': 1.49}
        """
        cpu_new = {}
        ret = {'total': 0.0}
        try:
            cpu_new['total'] = all_stats['cpu_stats']['cpu_usage']['total_usage']
            cpu_new['system'] = all_stats['cpu_stats']['system_cpu_usage']
            cpu_new['nb_core'] = len(all_stats['cpu_stats']['cpu_usage']['percpu_usage'] or [])
        except KeyError as e:
            logger.debug(('Cannot grab CPU usage for container {} ({})').format(container_id, e))
            logger.debug(all_stats)

        if not hasattr(self, 'cpu_old'):
            self.cpu_old = {}
            try:
                self.cpu_old[container_id] = cpu_new
            except (IOError, UnboundLocalError):
                pass

        if container_id not in self.cpu_old:
            try:
                self.cpu_old[container_id] = cpu_new
            except (IOError, UnboundLocalError):
                pass

        else:
            cpu_delta = float(cpu_new['total'] - self.cpu_old[container_id]['total'])
            system_delta = float(cpu_new['system'] - self.cpu_old[container_id]['system'])
            if cpu_delta > 0.0 and system_delta > 0.0:
                ret['total'] = cpu_delta / system_delta * float(cpu_new['nb_core']) * 100
            self.cpu_old[container_id] = cpu_new
        return ret

    def get_docker_memory(self, container_id, all_stats):
        """Return the container MEMORY.

        Input: id is the full container id
               all_stats is the output of the stats method of the Docker API
        Output: a dict {'rss': 1015808, 'cache': 356352,  'usage': ..., 'max_usage': ...}
        """
        ret = {}
        try:
            ret['usage'] = all_stats['memory_stats']['usage']
            ret['limit'] = all_stats['memory_stats']['limit']
            ret['max_usage'] = all_stats['memory_stats']['max_usage']
        except (KeyError, TypeError) as e:
            logger.debug(('Cannot grab MEM usage for container {} ({})').format(container_id, e))
            logger.debug(all_stats)

        return ret

    def get_docker_network(self, container_id, all_stats):
        """Return the container network usage using the Docker API (v1.0 or higher).

        Input: id is the full container id
        Output: a dict {'time_since_update': 3000, 'rx': 10, 'tx': 65}.
        with:
            time_since_update: number of seconds elapsed between the latest grab
            rx: Number of byte received
            tx: Number of byte transmited
        """
        network_new = {}
        try:
            netcounters = all_stats['networks']
        except KeyError as e:
            logger.debug(('Cannot grab NET usage for container {} ({})').format(container_id, e))
            logger.debug(all_stats)
            return network_new

        if not hasattr(self, 'inetcounters_old'):
            self.netcounters_old = {}
            try:
                self.netcounters_old[container_id] = netcounters
            except (IOError, UnboundLocalError):
                pass

        if container_id not in self.netcounters_old:
            try:
                self.netcounters_old[container_id] = netcounters
            except (IOError, UnboundLocalError):
                pass

        else:
            try:
                network_new['time_since_update'] = getTimeSinceLastUpdate(('docker_net_{}').format(container_id))
                network_new['rx'] = netcounters['eth0']['rx_bytes'] - self.netcounters_old[container_id]['eth0']['rx_bytes']
                network_new['tx'] = netcounters['eth0']['tx_bytes'] - self.netcounters_old[container_id]['eth0']['tx_bytes']
                network_new['cumulative_rx'] = netcounters['eth0']['rx_bytes']
                network_new['cumulative_tx'] = netcounters['eth0']['tx_bytes']
            except KeyError as e:
                logger.debug(('Cannot grab network interface usage for container {} ({})').format(container_id, e))
                logger.debug(all_stats)

            self.netcounters_old[container_id] = netcounters
        return network_new

    def get_docker_io(self, container_id, all_stats):
        """Return the container IO usage using the Docker API (v1.0 or higher).

        Input: id is the full container id
        Output: a dict {'time_since_update': 3000, 'ior': 10, 'iow': 65}.
        with:
            time_since_update: number of seconds elapsed between the latest grab
            ior: Number of byte readed
            iow: Number of byte written
        """
        io_new = {}
        try:
            iocounters = all_stats['blkio_stats']
        except KeyError as e:
            logger.debug(('Cannot grab block IO usage for container {} ({})').format(container_id, e))
            logger.debug(all_stats)
            return io_new

        if not hasattr(self, 'iocounters_old'):
            self.iocounters_old = {}
            try:
                self.iocounters_old[container_id] = iocounters
            except (IOError, UnboundLocalError):
                pass

        if container_id not in self.iocounters_old:
            try:
                self.iocounters_old[container_id] = iocounters
            except (IOError, UnboundLocalError):
                pass

        else:
            try:
                ior = [ i for i in iocounters['io_service_bytes_recursive'] if i['op'] == 'Read' ][0]['value']
                iow = [ i for i in iocounters['io_service_bytes_recursive'] if i['op'] == 'Write' ][0]['value']
                ior_old = [ i for i in self.iocounters_old[container_id]['io_service_bytes_recursive'] if i['op'] == 'Read' ][0]['value']
                iow_old = [ i for i in self.iocounters_old[container_id]['io_service_bytes_recursive'] if i['op'] == 'Write' ][0]['value']
            except (IndexError, KeyError) as e:
                logger.debug(('Cannot grab block IO usage for container {} ({})').format(container_id, e))
            else:
                io_new['time_since_update'] = getTimeSinceLastUpdate(('docker_io_{}').format(container_id))
                io_new['ior'] = ior - ior_old
                io_new['iow'] = iow - iow_old
                io_new['cumulative_ior'] = ior
                io_new['cumulative_iow'] = iow
                self.iocounters_old[container_id] = iocounters

        return io_new

    def get_user_ticks(self):
        """Return the user ticks by reading the environment variable."""
        return os.sysconf(os.sysconf_names['SC_CLK_TCK'])

    def get_stats_action(self):
        """Return stats for the action
        Docker will return self.stats['containers']"""
        return self.stats['containers']

    def update_views(self):
        """Update stats views."""
        super(Plugin, self).update_views()
        if 'containers' not in self.stats:
            return False
        for i in self.stats['containers']:
            self.views[i[self.get_key()]] = {'cpu': {}, 'mem': {}}
            if 'cpu' in i and 'total' in i['cpu']:
                alert = self.get_alert(i['cpu']['total'], header=i['name'] + '_cpu', action_key=i['name'])
                if alert == 'DEFAULT':
                    alert = self.get_alert(i['cpu']['total'], header='cpu')
                self.views[i[self.get_key()]]['cpu']['decoration'] = alert
            if 'memory' in i and 'usage' in i['memory']:
                alert = self.get_alert(i['memory']['usage'], maximum=i['memory']['limit'], header=i['name'] + '_mem', action_key=i['name'])
                if alert == 'DEFAULT':
                    alert = self.get_alert(i['memory']['usage'], maximum=i['memory']['limit'], header='mem')
                self.views[i[self.get_key()]]['mem']['decoration'] = alert

        return True

    def msg_curse(self, args=None):
        """Return the dict to display in the curse interface."""
        ret = []
        if not self.stats or len(self.stats['containers']) == 0 or self.is_disable():
            return ret
        msg = ('{}').format('CONTAINERS')
        ret.append(self.curse_add_line(msg, 'TITLE'))
        msg = (' {}').format(len(self.stats['containers']))
        ret.append(self.curse_add_line(msg))
        msg = (' (served by Docker {})').format(self.stats['version']['Version'])
        ret.append(self.curse_add_line(msg))
        ret.append(self.curse_new_line())
        ret.append(self.curse_new_line())
        name_max_width = min(20, len(max(self.stats['containers'], key=lambda x: len(x['name']))['name']))
        msg = (' {:{width}}').format('Name', width=name_max_width)
        ret.append(self.curse_add_line(msg))
        msg = ('{:>26}').format('Status')
        ret.append(self.curse_add_line(msg))
        msg = ('{:>6}').format('CPU%')
        ret.append(self.curse_add_line(msg))
        msg = ('{:>7}').format('MEM')
        ret.append(self.curse_add_line(msg))
        msg = ('{:>7}').format('/MAX')
        ret.append(self.curse_add_line(msg))
        msg = ('{:>7}').format('IOR/s')
        ret.append(self.curse_add_line(msg))
        msg = ('{:>7}').format('IOW/s')
        ret.append(self.curse_add_line(msg))
        msg = ('{:>7}').format('Rx/s')
        ret.append(self.curse_add_line(msg))
        msg = ('{:>7}').format('Tx/s')
        ret.append(self.curse_add_line(msg))
        msg = (' {:8}').format('Command')
        ret.append(self.curse_add_line(msg))
        for container in self.stats['containers']:
            ret.append(self.curse_new_line())
            name = container['name']
            if len(name) > name_max_width:
                name = '_' + name[-name_max_width + 1:]
            else:
                name = name[:name_max_width]
            msg = (' {:{width}}').format(name, width=name_max_width)
            ret.append(self.curse_add_line(msg))
            status = self.container_alert(container['Status'])
            msg = container['Status'].replace('minute', 'min')
            msg = ('{:>26}').format(msg[0:25])
            ret.append(self.curse_add_line(msg, status))
            try:
                msg = ('{:>6.1f}').format(container['cpu']['total'])
            except KeyError:
                msg = ('{:>6}').format('?')

            ret.append(self.curse_add_line(msg, self.get_views(item=container['name'], key='cpu', option='decoration')))
            try:
                msg = ('{:>7}').format(self.auto_unit(container['memory']['usage']))
            except KeyError:
                msg = ('{:>7}').format('?')

            ret.append(self.curse_add_line(msg, self.get_views(item=container['name'], key='mem', option='decoration')))
            try:
                msg = ('{:>7}').format(self.auto_unit(container['memory']['limit']))
            except KeyError:
                msg = ('{:>7}').format('?')

            ret.append(self.curse_add_line(msg))
            for r in ['ior', 'iow']:
                try:
                    value = self.auto_unit(int(container['io'][r] // container['io']['time_since_update'] * 8)) + 'b'
                    msg = ('{:>7}').format(value)
                except KeyError:
                    msg = ('{:>7}').format('?')

                ret.append(self.curse_add_line(msg))

            if args.byte:
                to_bit = 1
                unit = ''
            else:
                to_bit = 8
                unit = 'b'
            for r in ['rx', 'tx']:
                try:
                    value = self.auto_unit(int(container['network'][r] // container['network']['time_since_update'] * to_bit)) + unit
                    msg = ('{:>7}').format(value)
                except KeyError:
                    msg = ('{:>7}').format('?')

                ret.append(self.curse_add_line(msg))

            msg = (' {}').format(container['Command'])
            ret.append(self.curse_add_line(msg, splittable=True))

        return ret

    def container_alert(self, status):
        """Analyse the container status."""
        if 'Paused' in status:
            return 'CAREFUL'
        else:
            return 'OK'


class ThreadDockerGrabber(threading.Thread):
    """
    Specific thread to grab docker stats.

    stats is a dict
    """

    def __init__(self, docker_client, container_id):
        """Init the class:
        docker_client: instance of Docker-py client
        container_id: Id of the container"""
        logger.debug(('docker plugin - Create thread for container {}').format(container_id[:12]))
        super(ThreadDockerGrabber, self).__init__()
        self._stopper = threading.Event()
        self._container_id = container_id
        self._stats_stream = docker_client.stats(container_id, decode=True)
        self._stats = {}

    def run(self):
        """Function called to grab stats.
        Infinite loop, should be stopped by calling the stop() method"""
        for i in self._stats_stream:
            self._stats = i
            time.sleep(0.1)
            if self.stopped():
                break

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
        logger.debug(('docker plugin - Close thread for container {}').format(self._container_id[:12]))
        self._stopper.set()

    def stopped(self):
        """Return True is the thread is stopped"""
        return self._stopper.isSet()