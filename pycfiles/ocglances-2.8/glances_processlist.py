# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/fraoustin/Téléchargements/ocglances/tmp/ocglances/plugins/glances_processlist.py
# Compiled at: 2017-02-11 10:25:25
"""Process list plugin."""
import os
from datetime import timedelta
from ocglances.compat import iteritems
from ocglances.globals import LINUX, WINDOWS
from ocglances.logger import logger
from ocglances.processes import glances_processes, sort_stats
from ocglances.plugins.glances_core import Plugin as CorePlugin
from ocglances.plugins.glances_plugin import GlancesPlugin

def convert_timedelta(delta):
    """Convert timedelta to human-readable time."""
    days, total_seconds = delta.days, delta.seconds
    hours = days * 24 + total_seconds // 3600
    minutes = total_seconds % 3600 // 60
    seconds = str(total_seconds % 60).zfill(2)
    microseconds = str(delta.microseconds)[:2].zfill(2)
    return (
     hours, minutes, seconds, microseconds)


def split_cmdline(cmdline):
    """Return path, cmd and arguments for a process cmdline."""
    path, cmd = os.path.split(cmdline[0])
    arguments = (' ').join(cmdline[1:]).replace('\n', ' ')
    if LINUX and any(x in cmdline[0] for x in ('chrome', 'chromium')):
        try:
            exe, arguments = cmdline[0].split(' ', 1)
            path, cmd = os.path.split(exe)
        except ValueError:
            arguments = None

    return (
     path, cmd, arguments)


class Plugin(GlancesPlugin):
    """Glances' processes plugin.

    stats is a list
    """

    def __init__(self, args=None):
        """Init the plugin."""
        super(Plugin, self).__init__(args=args)
        self.display_curse = True
        self.tag_proc_time = True
        try:
            self.nb_log_core = CorePlugin(args=self.args).update()['log']
        except Exception:
            self.nb_log_core = 0

        self.max_values = glances_processes.max_values()
        self.pid_max = glances_processes.pid_max

    def get_key(self):
        """Return the key of the list."""
        return 'pid'

    def reset(self):
        """Reset/init the stats."""
        self.stats = []

    def update(self):
        """Update processes stats using the input method."""
        self.reset()
        if self.input_method == 'local':
            if glances_processes.is_tree_enabled():
                self.stats = glances_processes.gettree()
            else:
                self.stats = glances_processes.getlist()
            self.max_values = glances_processes.max_values()
        elif self.input_method == 'snmp':
            pass
        return self.stats

    def get_process_tree_curses_data(self, node, args, first_level=True, max_node_count=None):
        """Get curses data to display for a process tree."""
        ret = []
        node_count = 0
        if not node.is_root and (max_node_count is None or max_node_count > 0):
            node_data = self.get_process_curses_data(node.stats, False, args)
            node_count += 1
            ret.extend(node_data)
        for child in node.iter_children():
            if max_node_count is not None and node_count >= max_node_count:
                break
            if max_node_count is None:
                children_max_node_count = None
            else:
                children_max_node_count = max_node_count - node_count
            child_data = self.get_process_tree_curses_data(child, args, first_level=node.is_root, max_node_count=children_max_node_count)
            if max_node_count is None:
                node_count += len(child)
            else:
                node_count += min(children_max_node_count, len(child))
            if not node.is_root:
                child_data = self.add_tree_decoration(child_data, child is node.children[(-1)], first_level)
            ret.extend(child_data)

        return ret

    def add_tree_decoration(self, child_data, is_last_child, first_level):
        """Add tree curses decoration and indentation to a subtree."""
        pos = []
        for i, m in enumerate(child_data):
            if m.get('_tree_decoration', False):
                del m['_tree_decoration']
                pos.append(i)

        new_child_data = []
        new_pos = []
        for i, m in enumerate(child_data):
            if i in pos:
                new_pos.append(len(new_child_data))
                new_child_data.append(self.curse_add_line(''))
                new_child_data[(-1)]['_tree_decoration'] = True
            new_child_data.append(m)

        child_data = new_child_data
        pos = new_pos
        if pos:
            if is_last_child:
                prefix = '└─'
            else:
                prefix = '├─'
            child_data[pos[0]]['msg'] = prefix
            for i in pos:
                spacing = 2
                if first_level:
                    spacing = 1
                elif is_last_child and i is not pos[0]:
                    spacing = 3
                child_data[i]['msg'] = '%s%s' % (' ' * spacing, child_data[i]['msg'])

            if not is_last_child:
                for i in pos[1:]:
                    old_str = child_data[i]['msg']
                    if first_level:
                        child_data[i]['msg'] = ' │' + old_str[2:]
                    else:
                        child_data[i]['msg'] = old_str[:2] + '│' + old_str[3:]

        return child_data

    def get_process_curses_data(self, p, first, args):
        """Get curses data to display for a process.
        - p is the process to display
        - first is a tag=True if the process is the first on the list
        """
        ret = [
         self.curse_new_line()]
        if 'cpu_percent' in p and p['cpu_percent'] is not None and p['cpu_percent'] != '':
            if args.disable_irix and self.nb_log_core != 0:
                msg = ('{:>6.1f}').format(p['cpu_percent'] / float(self.nb_log_core))
            else:
                msg = ('{:>6.1f}').format(p['cpu_percent'])
            alert = self.get_alert(p['cpu_percent'], highlight_zero=False, is_max=p['cpu_percent'] == self.max_values['cpu_percent'], header='cpu')
            ret.append(self.curse_add_line(msg, alert))
        else:
            msg = ('{:>6}').format('?')
            ret.append(self.curse_add_line(msg))
        if 'memory_percent' in p and p['memory_percent'] is not None and p['memory_percent'] != '':
            msg = ('{:>6.1f}').format(p['memory_percent'])
            alert = self.get_alert(p['memory_percent'], highlight_zero=False, is_max=p['memory_percent'] == self.max_values['memory_percent'], header='mem')
            ret.append(self.curse_add_line(msg, alert))
        else:
            msg = ('{:>6}').format('?')
            ret.append(self.curse_add_line(msg))
        if 'memory_info' in p and p['memory_info'] is not None and p['memory_info'] != '':
            msg = ('{:>6}').format(self.auto_unit(p['memory_info'][1], low_precision=False))
            ret.append(self.curse_add_line(msg, optional=True))
            msg = ('{:>6}').format(self.auto_unit(p['memory_info'][0], low_precision=False))
            ret.append(self.curse_add_line(msg, optional=True))
        else:
            msg = ('{:>6}').format('?')
            ret.append(self.curse_add_line(msg))
            ret.append(self.curse_add_line(msg))
        msg = ('{:>{width}}').format(p['pid'], width=self.__max_pid_size() + 1)
        ret.append(self.curse_add_line(msg))
        if 'username' in p:
            msg = (' {:9}').format(str(p['username'])[:9])
            ret.append(self.curse_add_line(msg))
        else:
            msg = (' {:9}').format('?')
            ret.append(self.curse_add_line(msg))
        if 'nice' in p:
            nice = p['nice']
            if nice is None:
                nice = '?'
            msg = ('{:>5}').format(nice)
            if isinstance(nice, int) and (WINDOWS and nice != 32 or not WINDOWS and nice != 0):
                ret.append(self.curse_add_line(msg, decoration='NICE'))
            else:
                ret.append(self.curse_add_line(msg))
        else:
            msg = ('{:>5}').format('?')
            ret.append(self.curse_add_line(msg))
        if 'status' in p:
            status = p['status']
            msg = ('{:>2}').format(status)
            if status == 'R':
                ret.append(self.curse_add_line(msg, decoration='STATUS'))
            else:
                ret.append(self.curse_add_line(msg))
        else:
            msg = ('{:>2}').format('?')
            ret.append(self.curse_add_line(msg))
        if self.tag_proc_time:
            try:
                delta = timedelta(seconds=sum(p['cpu_times']))
            except (OverflowError, TypeError) as e:
                logger.debug(('Cannot get TIME+ ({})').format(e))
                self.tag_proc_time = False
            else:
                hours, minutes, seconds, microseconds = convert_timedelta(delta)
                if hours:
                    msg = ('{:>4}h').format(hours)
                    ret.append(self.curse_add_line(msg, decoration='CPU_TIME', optional=True))
                    msg = ('{}:{}').format(str(minutes).zfill(2), seconds)
                else:
                    msg = ('{:>4}:{}.{}').format(minutes, seconds, microseconds)
        else:
            msg = ('{:>10}').format('?')
        ret.append(self.curse_add_line(msg, optional=True))
        if 'io_counters' in p:
            io_rs = int((p['io_counters'][0] - p['io_counters'][2]) / p['time_since_update'])
            if io_rs == 0:
                msg = ('{:>6}').format('0')
            else:
                msg = ('{:>6}').format(self.auto_unit(io_rs, low_precision=True))
            ret.append(self.curse_add_line(msg, optional=True, additional=True))
            io_ws = int((p['io_counters'][1] - p['io_counters'][3]) / p['time_since_update'])
            if io_ws == 0:
                msg = ('{:>6}').format('0')
            else:
                msg = ('{:>6}').format(self.auto_unit(io_ws, low_precision=True))
            ret.append(self.curse_add_line(msg, optional=True, additional=True))
        else:
            msg = ('{:>6}').format('?')
            ret.append(self.curse_add_line(msg, optional=True, additional=True))
            ret.append(self.curse_add_line(msg, optional=True, additional=True))
        cmdline = p['cmdline']
        try:
            if cmdline and cmdline != ['']:
                path, cmd, arguments = split_cmdline(cmdline)
                if os.path.isdir(path) and not args.process_short_name:
                    msg = (' {}').format(path) + os.sep
                    ret.append(self.curse_add_line(msg, splittable=True))
                    if glances_processes.is_tree_enabled():
                        ret[(-1)]['_tree_decoration'] = True
                    ret.append(self.curse_add_line(cmd, decoration='PROCESS', splittable=True))
                else:
                    msg = (' {}').format(cmd)
                    ret.append(self.curse_add_line(msg, decoration='PROCESS', splittable=True))
                    if glances_processes.is_tree_enabled():
                        ret[(-1)]['_tree_decoration'] = True
                if arguments:
                    msg = (' {}').format(arguments)
                    ret.append(self.curse_add_line(msg, splittable=True))
            else:
                msg = (' {}').format(p['name'])
                ret.append(self.curse_add_line(msg, splittable=True))
        except UnicodeEncodeError:
            ret.append(self.curse_add_line('', splittable=True))

        if first and 'extended_stats' in p:
            xpad = '             '
            if 'cpu_affinity' in p and p['cpu_affinity'] is not None:
                ret.append(self.curse_new_line())
                msg = xpad + 'CPU affinity: ' + str(len(p['cpu_affinity'])) + ' cores'
                ret.append(self.curse_add_line(msg, splittable=True))
            if 'memory_info' in p and p['memory_info'] is not None:
                ret.append(self.curse_new_line())
                msg = xpad + 'Memory info: '
                for k, v in iteritems(p['memory_info']._asdict()):
                    if k not in ('rss', 'vms') and v is not None:
                        msg += k + ' ' + self.auto_unit(v, low_precision=False) + ' '

                if 'memory_swap' in p and p['memory_swap'] is not None:
                    msg += 'swap ' + self.auto_unit(p['memory_swap'], low_precision=False)
                ret.append(self.curse_add_line(msg, splittable=True))
            msg = ''
            if 'num_threads' in p and p['num_threads'] is not None:
                msg += 'threads ' + str(p['num_threads']) + ' '
            if 'num_fds' in p and p['num_fds'] is not None:
                msg += 'files ' + str(p['num_fds']) + ' '
            if 'num_handles' in p and p['num_handles'] is not None:
                msg += 'handles ' + str(p['num_handles']) + ' '
            if 'tcp' in p and p['tcp'] is not None:
                msg += 'TCP ' + str(p['tcp']) + ' '
            if 'udp' in p and p['udp'] is not None:
                msg += 'UDP ' + str(p['udp']) + ' '
            if msg != '':
                ret.append(self.curse_new_line())
                msg = xpad + 'Open: ' + msg
                ret.append(self.curse_add_line(msg, splittable=True))
            if 'ionice' in p and p['ionice'] is not None:
                ret.append(self.curse_new_line())
                msg = xpad + 'IO nice: '
                k = 'Class is '
                v = p['ionice'].ioclass
                if WINDOWS:
                    if v == 0:
                        msg += k + 'Very Low'
                    elif v == 1:
                        msg += k + 'Low'
                    elif v == 2:
                        msg += 'No specific I/O priority'
                    else:
                        msg += k + str(v)
                elif v == 0:
                    msg += 'No specific I/O priority'
                elif v == 1:
                    msg += k + 'Real Time'
                elif v == 2:
                    msg += k + 'Best Effort'
                elif v == 3:
                    msg += k + 'IDLE'
                else:
                    msg += k + str(v)
                if hasattr(p['ionice'], 'value') and p['ionice'].value != 0:
                    msg += ' (value %s/7)' % str(p['ionice'].value)
                ret.append(self.curse_add_line(msg, splittable=True))
        return ret

    def msg_curse(self, args=None):
        """Return the dict to display in the curse interface."""
        ret = []
        if not self.stats or args.disable_process:
            return ret
        process_sort_key = glances_processes.sort_key
        self.__msg_curse_header(ret, process_sort_key, args)
        if glances_processes.is_tree_enabled():
            ret.extend(self.get_process_tree_curses_data(self.__sort_stats(process_sort_key), args, first_level=True, max_node_count=glances_processes.max_processes))
        else:
            first = True
            for p in self.__sort_stats(process_sort_key):
                ret.extend(self.get_process_curses_data(p, first, args))
                first = False

        if glances_processes.process_filter is not None:
            if args.reset_minmax_tag:
                args.reset_minmax_tag = not args.reset_minmax_tag
                self.__mmm_reset()
            self.__msg_curse_sum(ret, args=args)
            self.__msg_curse_sum(ret, mmm='min', args=args)
            self.__msg_curse_sum(ret, mmm='max', args=args)
        return ret

    def __msg_curse_header(self, ret, process_sort_key, args=None):
        """
        Build the header and add it to the ret dict
        """
        sort_style = 'SORT'
        if args.disable_irix and 0 < self.nb_log_core < 10:
            msg = ('{:>6}').format('CPU%/' + str(self.nb_log_core))
        elif args.disable_irix and self.nb_log_core != 0:
            msg = ('{:>6}').format('CPU%/C')
        else:
            msg = ('{:>6}').format('CPU%')
        ret.append(self.curse_add_line(msg, sort_style if process_sort_key == 'cpu_percent' else 'DEFAULT'))
        msg = ('{:>6}').format('MEM%')
        ret.append(self.curse_add_line(msg, sort_style if process_sort_key == 'memory_percent' else 'DEFAULT'))
        msg = ('{:>6}').format('VIRT')
        ret.append(self.curse_add_line(msg, optional=True))
        msg = ('{:>6}').format('RES')
        ret.append(self.curse_add_line(msg, optional=True))
        msg = ('{:>{width}}').format('PID', width=self.__max_pid_size() + 1)
        ret.append(self.curse_add_line(msg))
        msg = (' {:10}').format('USER')
        ret.append(self.curse_add_line(msg, sort_style if process_sort_key == 'username' else 'DEFAULT'))
        msg = ('{:>4}').format('NI')
        ret.append(self.curse_add_line(msg))
        msg = ('{:>2}').format('S')
        ret.append(self.curse_add_line(msg))
        msg = ('{:>10}').format('TIME+')
        ret.append(self.curse_add_line(msg, sort_style if process_sort_key == 'cpu_times' else 'DEFAULT', optional=True))
        msg = ('{:>6}').format('R/s')
        ret.append(self.curse_add_line(msg, sort_style if process_sort_key == 'io_counters' else 'DEFAULT', optional=True, additional=True))
        msg = ('{:>6}').format('W/s')
        ret.append(self.curse_add_line(msg, sort_style if process_sort_key == 'io_counters' else 'DEFAULT', optional=True, additional=True))
        msg = (' {:8}').format('Command')
        ret.append(self.curse_add_line(msg, sort_style if process_sort_key == 'name' else 'DEFAULT'))

    def __msg_curse_sum(self, ret, sep_char='_', mmm=None, args=None):
        """
        Build the sum message (only when filter is on) and add it to the ret dict
        * ret: list of string where the message is added
        * sep_char: define the line separation char
        * mmm: display min, max, mean or current (if mmm=None)
        * args: Glances args
        """
        ret.append(self.curse_new_line())
        if mmm is None:
            ret.append(self.curse_add_line(sep_char * 69))
            ret.append(self.curse_new_line())
        msg = ('{:>6.1f}').format(self.__sum_stats('cpu_percent', mmm=mmm))
        ret.append(self.curse_add_line(msg, decoration=self.__mmm_deco(mmm)))
        msg = ('{:>6.1f}').format(self.__sum_stats('memory_percent', mmm=mmm))
        ret.append(self.curse_add_line(msg, decoration=self.__mmm_deco(mmm)))
        if 'memory_info' in self.stats[0] and self.stats[0]['memory_info'] is not None and self.stats[0]['memory_info'] != '':
            msg = ('{:>6}').format(self.auto_unit(self.__sum_stats('memory_info', indice=1, mmm=mmm), low_precision=False))
            ret.append(self.curse_add_line(msg, decoration=self.__mmm_deco(mmm), optional=True))
            msg = ('{:>6}').format(self.auto_unit(self.__sum_stats('memory_info', indice=0, mmm=mmm), low_precision=False))
            ret.append(self.curse_add_line(msg, decoration=self.__mmm_deco(mmm), optional=True))
        else:
            msg = ('{:>6}').format('')
            ret.append(self.curse_add_line(msg))
            ret.append(self.curse_add_line(msg))
        msg = ('{:>6}').format('')
        ret.append(self.curse_add_line(msg))
        msg = (' {:9}').format('')
        ret.append(self.curse_add_line(msg))
        msg = ('{:>5}').format('')
        ret.append(self.curse_add_line(msg))
        msg = ('{:>2}').format('')
        ret.append(self.curse_add_line(msg))
        msg = ('{:>10}').format('')
        ret.append(self.curse_add_line(msg, optional=True))
        if 'io_counters' in self.stats[0] and mmm is None:
            io_rs = int((self.__sum_stats('io_counters', 0) - self.__sum_stats('io_counters', indice=2, mmm=mmm)) / self.stats[0]['time_since_update'])
            if io_rs == 0:
                msg = ('{:>6}').format('0')
            else:
                msg = ('{:>6}').format(self.auto_unit(io_rs, low_precision=True))
            ret.append(self.curse_add_line(msg, decoration=self.__mmm_deco(mmm), optional=True, additional=True))
            io_ws = int((self.__sum_stats('io_counters', 1) - self.__sum_stats('io_counters', indice=3, mmm=mmm)) / self.stats[0]['time_since_update'])
            if io_ws == 0:
                msg = ('{:>6}').format('0')
            else:
                msg = ('{:>6}').format(self.auto_unit(io_ws, low_precision=True))
            ret.append(self.curse_add_line(msg, decoration=self.__mmm_deco(mmm), optional=True, additional=True))
        else:
            msg = ('{:>6}').format('')
            ret.append(self.curse_add_line(msg, optional=True, additional=True))
            ret.append(self.curse_add_line(msg, optional=True, additional=True))
        if mmm is None:
            msg = (' < {}').format('current')
            ret.append(self.curse_add_line(msg, optional=True))
        else:
            msg = (' < {}').format(mmm)
            ret.append(self.curse_add_line(msg, optional=True))
            msg = " ('M' to reset)"
            ret.append(self.curse_add_line(msg, optional=True))
        return

    def __mmm_deco(self, mmm):
        """
        Return the decoration string for the current mmm status
        """
        if mmm is not None:
            return 'DEFAULT'
        else:
            return 'FILTER'
            return

    def __mmm_reset(self):
        """
        Reset the MMM stats
        """
        self.mmm_min = {}
        self.mmm_max = {}

    def __sum_stats(self, key, indice=None, mmm=None):
        """
        Return the sum of the stats value for the given key
        * indice: If indice is set, get the p[key][indice]
        * mmm: display min, max, mean or current (if mmm=None)
        """
        ret = 0
        for p in self.stats:
            if indice is None:
                ret += p[key]
            else:
                ret += p[key][indice]

        mmm_key = self.__mmm_key(key, indice)
        if mmm == 'min':
            try:
                if self.mmm_min[mmm_key] > ret:
                    self.mmm_min[mmm_key] = ret
            except AttributeError:
                self.mmm_min = {}
                return 0
            except KeyError:
                self.mmm_min[mmm_key] = ret

            ret = self.mmm_min[mmm_key]
        elif mmm == 'max':
            try:
                if self.mmm_max[mmm_key] < ret:
                    self.mmm_max[mmm_key] = ret
            except AttributeError:
                self.mmm_max = {}
                return 0
            except KeyError:
                self.mmm_max[mmm_key] = ret

            ret = self.mmm_max[mmm_key]
        return ret

    def __mmm_key(self, key, indice):
        ret = key
        if indice is not None:
            ret += str(indice)
        return ret

    def __sort_stats(self, sortedby=None):
        """Return the stats (dict) sorted by (sortedby)"""
        return sort_stats(self.stats, sortedby, tree=glances_processes.is_tree_enabled(), reverse=glances_processes.sort_reverse)

    def __max_pid_size(self):
        """Return the maximum PID size in number of char"""
        if self.pid_max is not None:
            return len(str(self.pid_max))
        else:
            return 5
            return