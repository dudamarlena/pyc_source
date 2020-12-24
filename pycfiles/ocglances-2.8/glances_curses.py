# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/fraoustin/Téléchargements/ocglances/tmp/ocglances/outputs/glances_curses.py
# Compiled at: 2017-02-11 10:25:25
"""Curses interface class."""
import re, sys
from ocglances.compat import u, itervalues
from ocglances.globals import MACOS, WINDOWS
from ocglances.logger import logger
from ocglances.logs import glances_logs
from ocglances.processes import glances_processes
from ocglances.timer import Timer
if not WINDOWS:
    try:
        import curses, curses.panel
        from curses.textpad import Textbox
    except ImportError:
        logger.critical('Curses module not found. Glances cannot start in standalone mode.')
        sys.exit(1)

class _GlancesCurses(object):
    """This class manages the curses display (and key pressed).

    Note: It is a private class, use GlancesCursesClient or GlancesCursesBrowser.
    """
    _hotkeys = {'0': {'switch': 'disable_irix'}, '1': {'switch': 'percpu'}, '2': {'switch': 'disable_left_sidebar'}, '3': {'switch': 'disable_quicklook'}, '6': {'switch': 'meangpu'}, '/': {'switch': 'process_short_name'}, 'd': {'switch': 'disable_diskio'}, 'A': {'switch': 'disable_amps'}, 'b': {'switch': 'byte'}, 'B': {'switch': 'diskio_iops'}, 'D': {'switch': 'disable_docker'}, 'F': {'switch': 'fs_free_space'}, 'G': {'switch': 'disable_gpu'}, 'h': {'switch': 'help_tag'}, 'I': {'switch': 'disable_ip'}, 'l': {'switch': 'disable_alert'}, 'M': {'switch': 'reset_minmax_tag'}, 'n': {'switch': 'disable_network'}, 'N': {'switch': 'disable_now'}, 'P': {'switch': 'disable_ports'}, 'Q': {'switch': 'enable_irq'}, 'R': {'switch': 'disable_raid'}, 's': {'switch': 'disable_sensors'}, 'T': {'switch': 'network_sum'}, 'U': {'switch': 'network_cumul'}, 'W': {'switch': 'disable_wifi'}, 'a': {'auto_sort': True, 'sort_key': 'cpu_percent'}, 'c': {'auto_sort': False, 'sort_key': 'cpu_percent'}, 'i': {'auto_sort': False, 'sort_key': 'io_counters'}, 'm': {'auto_sort': False, 'sort_key': 'memory_percent'}, 'p': {'auto_sort': False, 'sort_key': 'name'}, 't': {'auto_sort': False, 'sort_key': 'cpu_times'}, 'u': {'auto_sort': False, 'sort_key': 'username'}}

    def __init__(self, config=None, args=None):
        self.config = config
        self.args = args
        self.term_w = 80
        self.term_h = 24
        self.space_between_column = 3
        self.space_between_line = 2
        self.screen = curses.initscr()
        if not self.screen:
            logger.critical('Cannot init the curses library.\n')
            sys.exit(1)
        self.theme = {'name': 'black'}
        self.load_config(config)
        self._init_cursor()
        self._init_colors()
        self.term_window = self.screen.subwin(0, 0)
        self.__refresh_time = args.time
        self.edit_filter = False
        self.args.reset_minmax_tag = False
        self.no_flash_cursor()
        self.term_window.nodelay(1)
        self.pressedkey = -1
        self._init_history()

    def load_config(self, config):
        """Load the outputs section of the configuration file."""
        if config is not None and config.has_section('outputs'):
            logger.debug('Read the outputs section in the configuration file')
            self.theme['name'] = config.get_value('outputs', 'curse_theme', default='black')
            logger.debug(('Theme for the curse interface: {}').format(self.theme['name']))
        return

    def is_theme(self, name):
        """Return True if the theme *name* should be used."""
        return getattr(self.args, 'theme_' + name) or self.theme['name'] == name

    def _init_history(self):
        """Init the history option."""
        self.reset_history_tag = False
        self.graph_tag = False
        if self.args.export_graph:
            logger.info('Export graphs function enabled with output path %s' % self.args.path_graph)
            from ocglances.exports.graph import GlancesGraph
            self.glances_graph = GlancesGraph(self.args.path_graph)
            if not self.glances_graph.graph_enabled():
                self.args.export_graph = False
                logger.error('Export graphs disabled')

    def _init_cursor(self):
        """Init cursors."""
        if hasattr(curses, 'noecho'):
            curses.noecho()
        if hasattr(curses, 'cbreak'):
            curses.cbreak()
        self.set_cursor(0)

    def _init_colors(self):
        """Init the Curses color layout."""
        if hasattr(curses, 'start_color'):
            curses.start_color()
        if hasattr(curses, 'use_default_colors'):
            curses.use_default_colors()
        if self.args.disable_bold:
            A_BOLD = 0
            self.args.disable_bg = True
        else:
            A_BOLD = curses.A_BOLD
        self.title_color = A_BOLD
        self.title_underline_color = A_BOLD | curses.A_UNDERLINE
        self.help_color = A_BOLD
        if curses.has_colors():
            if self.is_theme('white'):
                curses.init_pair(1, curses.COLOR_BLACK, -1)
            else:
                curses.init_pair(1, curses.COLOR_WHITE, -1)
            if self.args.disable_bg:
                curses.init_pair(2, curses.COLOR_RED, -1)
                curses.init_pair(3, curses.COLOR_GREEN, -1)
                curses.init_pair(4, curses.COLOR_BLUE, -1)
                curses.init_pair(5, curses.COLOR_MAGENTA, -1)
            else:
                curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_RED)
                curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_GREEN)
                curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_BLUE)
                curses.init_pair(5, curses.COLOR_WHITE, curses.COLOR_MAGENTA)
            curses.init_pair(6, curses.COLOR_RED, -1)
            curses.init_pair(7, curses.COLOR_GREEN, -1)
            curses.init_pair(8, curses.COLOR_BLUE, -1)
            if curses.COLOR_PAIRS > 8:
                try:
                    curses.init_pair(9, curses.COLOR_MAGENTA, -1)
                except Exception:
                    if self.is_theme('white'):
                        curses.init_pair(9, curses.COLOR_BLACK, -1)
                    else:
                        curses.init_pair(9, curses.COLOR_WHITE, -1)

                try:
                    curses.init_pair(10, curses.COLOR_CYAN, -1)
                except Exception:
                    if self.is_theme('white'):
                        curses.init_pair(10, curses.COLOR_BLACK, -1)
                    else:
                        curses.init_pair(10, curses.COLOR_WHITE, -1)

                self.ifWARNING_color2 = curses.color_pair(9) | A_BOLD
                self.ifCRITICAL_color2 = curses.color_pair(6) | A_BOLD
                self.filter_color = curses.color_pair(10) | A_BOLD
            self.no_color = curses.color_pair(1)
            self.default_color = curses.color_pair(3) | A_BOLD
            self.nice_color = curses.color_pair(9)
            self.cpu_time_color = curses.color_pair(9)
            self.ifCAREFUL_color = curses.color_pair(4) | A_BOLD
            self.ifWARNING_color = curses.color_pair(5) | A_BOLD
            self.ifCRITICAL_color = curses.color_pair(2) | A_BOLD
            self.default_color2 = curses.color_pair(7)
            self.ifCAREFUL_color2 = curses.color_pair(8) | A_BOLD
        else:
            self.no_color = curses.A_NORMAL
            self.default_color = curses.A_NORMAL
            self.nice_color = A_BOLD
            self.cpu_time_color = A_BOLD
            self.ifCAREFUL_color = curses.A_UNDERLINE
            self.ifWARNING_color = A_BOLD
            self.ifCRITICAL_color = curses.A_REVERSE
            self.default_color2 = curses.A_NORMAL
            self.ifCAREFUL_color2 = curses.A_UNDERLINE
            self.ifWARNING_color2 = A_BOLD
            self.ifCRITICAL_color2 = curses.A_REVERSE
            self.filter_color = A_BOLD
        self.colors_list = {'DEFAULT': self.no_color, 
           'UNDERLINE': curses.A_UNDERLINE, 
           'BOLD': A_BOLD, 
           'SORT': A_BOLD, 
           'OK': self.default_color2, 
           'MAX': self.default_color2 | curses.A_BOLD, 
           'FILTER': self.filter_color, 
           'TITLE': self.title_color, 
           'PROCESS': self.default_color2, 
           'STATUS': self.default_color2, 
           'NICE': self.nice_color, 
           'CPU_TIME': self.cpu_time_color, 
           'CAREFUL': self.ifCAREFUL_color2, 
           'WARNING': self.ifWARNING_color2, 
           'CRITICAL': self.ifCRITICAL_color2, 
           'OK_LOG': self.default_color, 
           'CAREFUL_LOG': self.ifCAREFUL_color, 
           'WARNING_LOG': self.ifWARNING_color, 
           'CRITICAL_LOG': self.ifCRITICAL_color, 
           'PASSWORD': curses.A_PROTECT}

    def flash_cursor(self):
        self.term_window.keypad(1)

    def no_flash_cursor(self):
        self.term_window.keypad(0)

    def set_cursor(self, value):
        """Configure the curse cursor apparence.

        0: invisible
        1: visible
        2: very visible
        """
        if hasattr(curses, 'curs_set'):
            try:
                curses.curs_set(value)
            except Exception:
                pass

    def get_key(self, window):
        keycode = [
         0, 0]
        keycode[0] = window.getch()
        keycode[1] = window.getch()
        if keycode != [-1, -1]:
            logger.debug('Keypressed (code: %s)' % keycode)
        if keycode[0] == 27 and keycode[1] != -1:
            return -1
        else:
            return keycode[0]

    def __catch_key(self, return_to_browser=False):
        self.pressedkey = self.get_key(self.term_window)
        for hotkey in self._hotkeys:
            if self.pressedkey == ord(hotkey) and 'switch' in self._hotkeys[hotkey]:
                setattr(self.args, self._hotkeys[hotkey]['switch'], not getattr(self.args, self._hotkeys[hotkey]['switch']))
            if self.pressedkey == ord(hotkey) and 'auto_sort' in self._hotkeys[hotkey]:
                setattr(glances_processes, 'auto_sort', self._hotkeys[hotkey]['auto_sort'])
            if self.pressedkey == ord(hotkey) and 'sort_key' in self._hotkeys[hotkey]:
                setattr(glances_processes, 'sort_key', self._hotkeys[hotkey]['sort_key'])

        if self.pressedkey == ord('\x1b') or self.pressedkey == ord('q'):
            if return_to_browser:
                logger.info('Stop Glances client and return to the browser')
            else:
                self.end()
                logger.info('Stop Glances')
                sys.exit(0)
        elif self.pressedkey == ord('\n'):
            self.edit_filter = not self.edit_filter
        elif self.pressedkey == ord('4'):
            self.args.full_quicklook = not self.args.full_quicklook
            if self.args.full_quicklook:
                self.enable_fullquicklook()
            else:
                self.disable_fullquicklook()
        elif self.pressedkey == ord('5'):
            self.args.disable_top = not self.args.disable_top
            if self.args.disable_top:
                self.disable_top()
            else:
                self.enable_top()
        elif self.pressedkey == ord('e'):
            self.args.enable_process_extended = not self.args.enable_process_extended
            if not self.args.enable_process_extended:
                glances_processes.disable_extended()
            else:
                glances_processes.enable_extended()
        elif self.pressedkey == ord('E'):
            glances_processes.process_filter = None
        elif self.pressedkey == ord('f'):
            self.args.disable_fs = not self.args.disable_fs
            self.args.disable_folders = not self.args.disable_folders
        elif self.pressedkey == ord('g'):
            self.graph_tag = not self.graph_tag
        elif self.pressedkey == ord('r'):
            self.reset_history_tag = not self.reset_history_tag
        elif self.pressedkey == ord('w'):
            glances_logs.clean()
        elif self.pressedkey == ord('x'):
            glances_logs.clean(critical=True)
        elif self.pressedkey == ord('z'):
            self.args.disable_process = not self.args.disable_process
            if self.args.disable_process:
                glances_processes.disable()
            else:
                glances_processes.enable()
        return self.pressedkey

    def disable_top(self):
        """Disable the top panel"""
        for p in ['quicklook', 'cpu', 'gpu', 'mem', 'memswap', 'load']:
            setattr(self.args, 'disable_' + p, True)

    def enable_top(self):
        """Enable the top panel"""
        for p in ['quicklook', 'cpu', 'gpu', 'mem', 'memswap', 'load']:
            setattr(self.args, 'disable_' + p, False)

    def disable_fullquicklook(self):
        """Disable the full quicklook mode"""
        for p in ['quicklook', 'cpu', 'gpu', 'mem', 'memswap']:
            setattr(self.args, 'disable_' + p, False)

    def enable_fullquicklook(self):
        """Disable the full quicklook mode"""
        self.args.disable_quicklook = False
        for p in ['cpu', 'gpu', 'mem', 'memswap']:
            setattr(self.args, 'disable_' + p, True)

    def end(self):
        """Shutdown the curses window."""
        if hasattr(curses, 'echo'):
            curses.echo()
        if hasattr(curses, 'nocbreak'):
            curses.nocbreak()
        if hasattr(curses, 'curs_set'):
            try:
                curses.curs_set(1)
            except Exception:
                pass

        curses.endwin()

    def init_line_column(self):
        """Init the line and column position for the curses interface."""
        self.init_line()
        self.init_column()

    def init_line(self):
        """Init the line position for the curses interface."""
        self.line = 0
        self.next_line = 0

    def init_column(self):
        """Init the column position for the curses interface."""
        self.column = 0
        self.next_column = 0

    def new_line(self):
        """New line in the curses interface."""
        self.line = self.next_line

    def new_column(self):
        """New column in the curses interface."""
        self.column = self.next_column

    def __get_stat_display(self, stats, plugin_max_width):
        """Return a dict of dict with all the stats display
        * key: plugin name
        * value: dict returned by the get_stats_display Plugin method

        :returns: dict of dict
        """
        ret = {}
        for p in stats.getAllPlugins(enable=False):
            if p in ('network', 'wifi', 'irq', 'fs', 'folders'):
                ret[p] = stats.get_plugin(p).get_stats_display(args=self.args, max_width=plugin_max_width)
            elif p in ('quicklook', ):
                continue
            else:
                try:
                    ret[p] = stats.get_plugin(p).get_stats_display(args=self.args)
                except AttributeError:
                    ret[p] = None

        if self.args.percpu:
            ret['cpu'] = ret['percpu']
        return ret

    def display(self, stats, cs_status=None):
        """Display stats on the screen.

        stats: Stats database to display
        cs_status:
            "None": standalone or server mode
            "Connected": Client is connected to a Glances server
            "SNMP": Client is connected to a SNMP server
            "Disconnected": Client is disconnected from the server

        Return:
            True if the stats have been displayed
            False if the help have been displayed
        """
        self.init_line_column()
        if cs_status == 'SNMP':
            plugin_max_width = 43
        else:
            plugin_max_width = None
        self.args.cs_status = cs_status
        __stat_display = self.__get_stat_display(stats, plugin_max_width)
        max_processes_displayed = self.screen.getmaxyx()[0] - 11 - self.get_stats_display_height(__stat_display['alert']) - self.get_stats_display_height(__stat_display['docker'])
        try:
            if self.args.enable_process_extended and not self.args.process_tree:
                max_processes_displayed -= 4
        except AttributeError:
            pass

        if max_processes_displayed < 0:
            max_processes_displayed = 0
        if glances_processes.max_processes is None or glances_processes.max_processes != max_processes_displayed:
            logger.debug(('Set number of displayed processes to {}').format(max_processes_displayed))
            glances_processes.max_processes = max_processes_displayed
        __stat_display['processlist'] = stats.get_plugin('processlist').get_stats_display(args=self.args)
        if self.args.help_tag:
            self.display_plugin(stats.get_plugin('help').get_stats_display(args=self.args))
            return False
        else:
            self.__display_firstline(__stat_display)
            self.__display_secondline(__stat_display, stats)
            self.__display_left(__stat_display)
            self.__display_right(__stat_display)
            if self.graph_tag and self.args.export_graph:
                self.display_popup(('Generate graphs history in {}\nPlease wait...').format(self.glances_graph.get_output_folder()))
                self.display_popup(('Generate graphs history in {}\nDone: {} graphs generated').format(self.glances_graph.get_output_folder(), self.glances_graph.generate_graph(stats)))
            elif self.reset_history_tag and self.args.export_graph:
                self.display_popup('Reset graph history')
                self.glances_graph.reset(stats)
            elif (self.graph_tag or self.reset_history_tag) and not self.args.export_graph:
                try:
                    self.glances_graph.graph_enabled()
                except Exception:
                    self.display_popup('Graph disabled\nEnable it using --export-graph')
                else:
                    self.display_popup('Graph disabled')

            self.graph_tag = False
            self.reset_history_tag = False
            if self.edit_filter and cs_status is None:
                new_filter = self.display_popup('Process filter pattern: \n\n' + 'Examples:\n' + '- python\n' + '- .*python.*\n' + '- \\/usr\\/lib.*\n' + '- name:.*nautilus.*\n' + '- cmdline:.*glances.*\n' + '- username:nicolargo\n' + '- username:^root        ', is_input=True, input_value=glances_processes.process_filter_input)
                glances_processes.process_filter = new_filter
            elif self.edit_filter and cs_status is not None:
                self.display_popup('Process filter only available in standalone mode')
            self.edit_filter = False
            return True

    def __display_firstline(self, stat_display):
        """Display the first line in the Curses interface.

        system + ip + uptime
        """
        self.space_between_column = 0
        self.new_line()
        l_uptime = self.get_stats_display_width(stat_display['system']) + self.space_between_column + self.get_stats_display_width(stat_display['ip']) + 3 + self.get_stats_display_width(stat_display['uptime'])
        self.display_plugin(stat_display['system'], display_optional=self.screen.getmaxyx()[1] >= l_uptime)
        self.new_column()
        self.display_plugin(stat_display['ip'])
        self.space_between_column = 3
        self.new_column()
        self.display_plugin(stat_display['uptime'])

    def __display_secondline(self, stat_display, stats):
        """Display the second line in the Curses interface.

        <QUICKLOOK> + CPU|PERCPU + <GPU> + MEM + SWAP + LOAD
        """
        self.init_column()
        self.new_line()
        stat_display['quicklook'] = {'msgdict': []}
        plugin_widths = {'quicklook': 0}
        for p in ['cpu', 'gpu', 'mem', 'memswap', 'load']:
            plugin_widths[p] = self.get_stats_display_width(stat_display[p]) if hasattr(self.args, 'disable_' + p) and p in stat_display else 0

        stats_width = sum(itervalues(plugin_widths))
        stats_number = int(not self.args.disable_cpu and stat_display['cpu']['msgdict'] != []) + int(not self.args.disable_gpu and stat_display['gpu']['msgdict'] != []) + int(not self.args.disable_mem and stat_display['mem']['msgdict'] != []) + int(not self.args.disable_memswap and stat_display['memswap']['msgdict'] != []) + int(not self.args.disable_load and stat_display['load']['msgdict'] != [])
        if not self.args.disable_quicklook:
            if self.args.full_quicklook:
                quicklook_width = self.screen.getmaxyx()[1] - (stats_width + 8 + stats_number * self.space_between_column)
            else:
                quicklook_width = min(self.screen.getmaxyx()[1] - (stats_width + 8 + stats_number * self.space_between_column), 79)
            try:
                stat_display['quicklook'] = stats.get_plugin('quicklook').get_stats_display(max_width=quicklook_width, args=self.args)
            except AttributeError as e:
                logger.debug('Quicklook plugin not available (%s)' % e)
            else:
                plugin_widths['quicklook'] = self.get_stats_display_width(stat_display['quicklook'])
                stats_width = sum(itervalues(plugin_widths)) + 1

            self.space_between_column = 1
            self.display_plugin(stat_display['quicklook'])
            self.new_column()
        plugin_display_optional = {}
        for p in ['cpu', 'gpu', 'mem', 'memswap', 'load']:
            plugin_display_optional[p] = True

        if stats_number > 1:
            self.space_between_column = max(1, int((self.screen.getmaxyx()[1] - stats_width) / (stats_number - 1)))
            for p in ['mem', 'cpu']:
                if self.space_between_column < 3:
                    plugin_display_optional[p] = False
                    plugin_widths[p] = self.get_stats_display_width(stat_display[p], without_option=True) if hasattr(self.args, 'disable_' + p) else 0
                    stats_width = sum(itervalues(plugin_widths)) + 1
                    self.space_between_column = max(1, int((self.screen.getmaxyx()[1] - stats_width) / (stats_number - 1)))

        else:
            self.space_between_column = 0
        for p in ['cpu', 'gpu', 'mem', 'memswap', 'load']:
            if p in stat_display:
                self.display_plugin(stat_display[p], display_optional=plugin_display_optional[p])
            if p is not 'load':
                self.new_column()

        self.space_between_column = 3
        self.saved_line = self.next_line

    def __display_left(self, stat_display):
        """Display the left sidebar in the Curses interface.

        network+wifi+ports+diskio+fs+irq+folders+raid+sensors+now
        """
        self.init_column()
        if not self.args.disable_left_sidebar:
            for s in ['network', 'wifi', 'ports', 'diskio', 'fs', 'irq', 'folders', 'raid', 'sensors', 'now']:
                if (hasattr(self.args, 'enable_' + s) or hasattr(self.args, 'disable_' + s)) and s in stat_display:
                    self.new_line()
                    self.display_plugin(stat_display[s])

    def __display_right(self, stat_display):
        """Display the right sidebar in the Curses interface.

        docker + processcount + amps + processlist + alert
        """
        if self.screen.getmaxyx()[1] > 52:
            self.next_line = self.saved_line
            self.new_column()
            self.new_line()
            self.display_plugin(stat_display['docker'])
            self.new_line()
            self.display_plugin(stat_display['processcount'])
            self.new_line()
            self.display_plugin(stat_display['amps'])
            self.new_line()
            self.display_plugin(stat_display['processlist'], display_optional=self.screen.getmaxyx()[1] > 102, display_additional=not MACOS, max_y=self.screen.getmaxyx()[0] - self.get_stats_display_height(stat_display['alert']) - 2)
            self.new_line()
            self.display_plugin(stat_display['alert'])

    def display_popup(self, message, size_x=None, size_y=None, duration=3, is_input=False, input_size=30, input_value=None):
        """
        Display a centered popup.

        If is_input is False:
         Display a centered popup with the given message during duration seconds
         If size_x and size_y: set the popup size
         else set it automatically
         Return True if the popup could be displayed

        If is_input is True:
         Display a centered popup with the given message and a input field
         If size_x and size_y: set the popup size
         else set it automatically
         Return the input string or None if the field is empty
        """
        sentence_list = message.split('\n')
        if size_x is None:
            size_x = len(max(sentence_list, key=len)) + 4
            if is_input:
                size_x += input_size
        if size_y is None:
            size_y = len(sentence_list) + 4
        screen_x = self.screen.getmaxyx()[1]
        screen_y = self.screen.getmaxyx()[0]
        if size_x > screen_x or size_y > screen_y:
            return False
        pos_x = int((screen_x - size_x) / 2)
        pos_y = int((screen_y - size_y) / 2)
        popup = curses.newwin(size_y, size_x, pos_y, pos_x)
        popup.border()
        for y, m in enumerate(message.split('\n')):
            popup.addnstr(2 + y, 2, m, len(m))

        if is_input and not WINDOWS:
            subpop = popup.derwin(1, input_size, 2, 2 + len(m))
            subpop.attron(self.colors_list['FILTER'])
            if input_value is not None:
                subpop.addnstr(0, 0, input_value, len(input_value))
            popup.refresh()
            subpop.refresh()
            self.set_cursor(2)
            self.flash_cursor()
            textbox = GlancesTextbox(subpop, insert_mode=False)
            textbox.edit()
            self.set_cursor(0)
            self.no_flash_cursor()
            if textbox.gather() != '':
                logger.debug('User enters the following string: %s' % textbox.gather())
                return textbox.gather()[:-1]
            logger.debug('User centers an empty string')
            return
        else:
            popup.refresh()
            self.wait(duration * 1000)
            return True
        return

    def display_plugin(self, plugin_stats, display_optional=True, display_additional=True, max_y=65535):
        """Display the plugin_stats on the screen.

        If display_optional=True display the optional stats
        If display_additional=True display additionnal stats
        max_y do not display line > max_y
        """
        if plugin_stats is None or not plugin_stats['msgdict'] or not plugin_stats['display']:
            return 0
        screen_x = self.screen.getmaxyx()[1]
        screen_y = self.screen.getmaxyx()[0]
        if plugin_stats['align'] == 'right':
            display_x = screen_x - self.get_stats_display_width(plugin_stats)
        else:
            display_x = self.column
        if plugin_stats['align'] == 'bottom':
            display_y = screen_y - self.get_stats_display_height(plugin_stats)
        else:
            display_y = self.line
        x = display_x
        x_max = x
        y = display_y
        for m in plugin_stats['msgdict']:
            if m['msg'].startswith('\n'):
                y += 1
                x = display_x
                continue
            if x < 0:
                continue
            if not m['splittable'] and x + len(m['msg']) > screen_x:
                continue
            if y < 0 or y + 1 > screen_y or y > max_y:
                break
            if not display_optional and m['optional']:
                continue
            if not display_additional and m['additional']:
                continue
            try:
                self.term_window.addnstr(y, x, m['msg'], screen_x - x, self.colors_list[m['decoration']])
            except Exception:
                pass
            else:
                try:
                    x += len(u(m['msg']))
                except UnicodeDecodeError:
                    pass

                if x > x_max:
                    x_max = x

        self.next_column = max(self.next_column, x_max + self.space_between_column)
        self.next_line = max(self.next_line, y + self.space_between_line)
        return

    def erase(self):
        """Erase the content of the screen."""
        self.term_window.erase()

    def flush(self, stats, cs_status=None):
        """Clear and update the screen.

        stats: Stats database to display
        cs_status:
            "None": standalone or server mode
            "Connected": Client is connected to the server
            "Disconnected": Client is disconnected from the server
        """
        self.erase()
        self.display(stats, cs_status=cs_status)

    def update(self, stats, cs_status=None, return_to_browser=False):
        """Update the screen.

        Wait for __refresh_time sec / catch key every 100 ms.

        INPUT
        stats: Stats database to display
        cs_status:
            "None": standalone or server mode
            "Connected": Client is connected to the server
            "Disconnected": Client is disconnected from the server
        return_to_browser:
            True: Do not exist, return to the browser list
            False: Exit and return to the shell

        OUPUT
        True: Exit key has been pressed
        False: Others cases...
        """
        self.flush(stats, cs_status=cs_status)
        exitkey = False
        countdown = Timer(self.__refresh_time)
        while not countdown.finished() and not exitkey:
            pressedkey = self.__catch_key(return_to_browser=return_to_browser)
            exitkey = pressedkey == ord('\x1b') or pressedkey == ord('q')
            if not exitkey and pressedkey > -1:
                self.flush(stats, cs_status=cs_status)
            self.wait()

        return exitkey

    def wait(self, delay=100):
        """Wait delay in ms"""
        curses.napms(100)

    def get_stats_display_width(self, curse_msg, without_option=False):
        """Return the width of the formatted curses message.

        The height is defined by the maximum line.
        """
        try:
            if without_option:
                c = len(max(('').join([ (i['optional'] or re.sub)('[^\\x00-\\x7F]+', ' ', i['msg']) if 1 else '' for i in curse_msg['msgdict']
                                      ]).split('\n'), key=len))
            else:
                c = len(max(('').join([ re.sub('[^\\x00-\\x7F]+', ' ', i['msg']) for i in curse_msg['msgdict']
                                      ]).split('\n'), key=len))
        except Exception:
            return 0

        return c

    def get_stats_display_height(self, curse_msg):
        r"""Return the height of the formatted curses message.

        The height is defined by the number of '\n' (new line).
        """
        try:
            c = [ i['msg'] for i in curse_msg['msgdict'] ].count('\n')
        except Exception:
            return 0

        return c + 1


class GlancesCursesStandalone(_GlancesCurses):
    """Class for the Glances curse standalone."""
    pass


class GlancesCursesClient(_GlancesCurses):
    """Class for the Glances curse client."""
    pass


if not WINDOWS:

    class GlancesTextbox(Textbox, object):

        def __init__(self, *args, **kwargs):
            super(GlancesTextbox, self).__init__(*args, **kwargs)

        def do_command(self, ch):
            if ch == 10:
                return 0
            if ch == 127:
                return 8
            return super(GlancesTextbox, self).do_command(ch)