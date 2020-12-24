# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Dani/Documents/Projects/Golismero_2.0/src_github/plugins/ui/console.py
# Compiled at: 2014-01-14 18:58:51
__license__ = '\nGoLismero 2.0 - The web knife - Copyright (C) 2011-2013\n\nAuthors:\n  Daniel Garcia Garcia a.k.a cr0hn | cr0hn<@>cr0hn.com\n  Mario Vilas | mvilas<@>gmail.com\n\nGolismero project site: https://github.com/golismero\nGolismero project mail: golismero.project<@>gmail.com\n\nThis program is free software; you can redistribute it and/or\nmodify it under the terms of the GNU General Public License\nas published by the Free Software Foundation; either version 2\nof the License, or (at your option) any later version.\n\nThis program is distributed in the hope that it will be useful,\nbut WITHOUT ANY WARRANTY; without even the implied warranty of\nMERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the\nGNU General Public License for more details.\n\nYou should have received a copy of the GNU General Public License\nalong with this program; if not, write to the Free Software\nFoundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.\n'
from golismero.api.audit import get_audit_count
from golismero.api.config import Config
from golismero.api.data import Data
from golismero.api.plugin import UIPlugin, get_plugin_info, get_stage_display_name
from golismero.main.console import Console, colorize, colorize_traceback
from golismero.messaging.codes import MessageType, MessageCode, MessagePriority
from collections import defaultdict
from functools import partial
import warnings

class ConsoleUIPlugin(UIPlugin):
    """
    This is the console UI plugin. It provides a simple interface
    to work with GoLismero from the command line.

    This plugin has no options.
    """

    def __init__(self):
        self.already_seen_info = defaultdict(set)
        self.current_plugins = defaultdict(partial(defaultdict, dict))

    def check_params(self, options, *audits):
        if not audits:
            raise ValueError('Daemon mode not supported.')
        for audit in audits:
            if audit.is_new_audit() and not audit.targets and not audit.imports:
                raise ValueError('No targets selected for audit.')

    def recv_info(self, info):
        if Console.level < Console.STANDARD:
            return
        else:
            if info.data_type != Data.TYPE_VULNERABILITY:
                return
            if info.identity in self.already_seen_info[Config.audit_name]:
                return
            self.already_seen_info[Config.audit_name].add(info.identity)
            text = '<!> %s vulnerability dicovered by %s. Level: %s'
            text %= (
             colorize(info.display_name, info.level),
             colorize(self.get_plugin_name(info.plugin_id, None), 'blue'),
             colorize(info.level, info.level))
            Console.display(text)
            return

    def recv_msg(self, message):
        if message.message_type == MessageType.MSG_TYPE_STATUS:
            if message.message_code == MessageCode.MSG_STATUS_PLUGIN_BEGIN:
                id_dict = self.current_plugins[Config.audit_name][message.plugin_id]
                simple_id = len(id_dict)
                id_dict[message.ack_identity] = simple_id
                if Console.level >= Console.VERBOSE:
                    m_plugin_name = self.get_plugin_name(message.plugin_id, message.ack_identity)
                    m_plugin_name = colorize('[*] ' + m_plugin_name, 'informational')
                    m_text = '%s: Started.' % m_plugin_name
                    Console.display(m_text)
            elif message.message_code == MessageCode.MSG_STATUS_PLUGIN_END:
                if Console.level >= Console.VERBOSE:
                    m_plugin_name = self.get_plugin_name(message.plugin_id, message.ack_identity)
                    m_plugin_name = colorize('[*] ' + m_plugin_name, 'informational')
                    m_text = '%s: Finished.' % m_plugin_name
                    Console.display(m_text)
                try:
                    del self.current_plugins[Config.audit_name][message.plugin_id][message.ack_identity]
                except KeyError:
                    pass

            elif message.message_code == MessageCode.MSG_STATUS_PLUGIN_STEP:
                if Console.level >= Console.VERBOSE:
                    m_plugin_name = self.get_plugin_name(message.plugin_id, message.ack_identity)
                    m_plugin_name = colorize('[*] ' + m_plugin_name, 'informational')
                    m_progress = message.message_info
                    if m_progress is not None:
                        m_progress_h = int(m_progress)
                        m_progress_l = int((m_progress - float(m_progress_h)) * 100)
                        m_progress_txt = colorize('%i.%.2i%%' % (m_progress_h, m_progress_l), 'middle')
                        m_progress_txt = m_progress_txt + ' percent done...'
                    else:
                        m_progress_txt = 'Working...'
                    m_text = '%s: %s' % (m_plugin_name, m_progress_txt)
                    Console.display(m_text)
            elif message.message_code == MessageCode.MSG_STATUS_STAGE_UPDATE:
                if Console.level >= Console.VERBOSE:
                    m_stage = get_stage_display_name(message.message_info)
                    m_stage = colorize(m_stage, 'high')
                    m_plugin_name = colorize('[*] GoLismero', 'informational')
                    m_text = '%s: Current stage: %s'
                    m_text %= (m_plugin_name, m_stage)
                    Console.display(m_text)
                    if Console.level >= Console.MORE_VERBOSE and message.message_info == 'report':
                        if Config.audit_config.only_vulns:
                            m_report_type = 'Brief'
                        else:
                            m_report_type = 'Full'
                        m_report_type = colorize(m_report_type, 'yellow')
                        m_text = '%s: Report type: %s'
                        m_text %= (m_plugin_name, m_report_type)
                        Console.display(m_text)
            elif message.message_code == MessageCode.MSG_STATUS_AUDIT_ABORTED:
                audit_name, description, traceback = message.message_info
                try:
                    m_plugin_name = self.get_plugin_name(message.plugin_id, message.ack_identity)
                    m_plugin_name = colorize('[!] ' + m_plugin_name, 'critical')
                    text = '%s: Error: %s ' % (m_plugin_name, str(description))
                    traceback = colorize(traceback, 'critical')
                    Console.display_error(text)
                    Console.display_error_more_verbose(traceback)
                finally:
                    self.audit_is_dead(audit_name)

        elif message.message_type == MessageType.MSG_TYPE_CONTROL:
            if message.message_code == MessageCode.MSG_CONTROL_STOP_AUDIT:
                self.audit_is_dead(message.audit_name)
            elif message.message_code == MessageCode.MSG_CONTROL_LOG:
                text, level, is_error = message.message_info
                if Console.level >= level:
                    m_plugin_name = self.get_plugin_name(message.plugin_id, message.ack_identity)
                    if is_error:
                        text = colorize_traceback(text)
                        m_plugin_name = colorize('[!] ' + m_plugin_name, 'critical')
                        text = '%s: %s' % (m_plugin_name, text)
                        Console.display_error(text)
                    else:
                        m_plugin_name = colorize('[*] ' + m_plugin_name, 'informational')
                        text = '%s: %s' % (m_plugin_name, text)
                        Console.display(text)
            if message.message_code == MessageCode.MSG_CONTROL_ERROR:
                description, traceback = message.message_info
                m_plugin_name = self.get_plugin_name(message.plugin_id, message.ack_identity)
                m_plugin_name = colorize('[!] ' + m_plugin_name, 'critical')
                text = '%s: Error: %s ' % (m_plugin_name, str(description))
                traceback = colorize_traceback(traceback)
                Console.display_error(text)
                Console.display_error_more_verbose(traceback)
            elif message.message_code == MessageCode.MSG_CONTROL_WARNING:
                for w in message.message_info:
                    if Console.level >= Console.MORE_VERBOSE:
                        formatted = warnings.formatwarning(w.message, w.category, w.filename, w.lineno, w.line)
                        m_plugin_name = self.get_plugin_name(message.plugin_id, message.ack_identity)
                        m_plugin_name = colorize('[!] ' + m_plugin_name, 'low')
                        text = '%s: Error: %s ' % (m_plugin_name, str(formatted))
                        Console.display_error(text)

        return

    def audit_is_dead(self, audit_name):
        try:
            del self.already_seen_info[audit_name]
        except KeyError:
            pass

        try:
            del self.current_plugins[audit_name]
        except KeyError:
            pass

        if get_audit_count() <= 1:
            Config._context.send_msg(message_type=MessageType.MSG_TYPE_CONTROL, message_code=MessageCode.MSG_CONTROL_STOP, message_info=True, priority=MessagePriority.MSG_PRIORITY_LOW)

    def get_plugin_name(self, plugin_id, ack_identity):
        if not plugin_id:
            return 'GoLismero'
        if plugin_id == Config.plugin_id:
            return Config.plugin_info.display_name
        plugin_name = get_plugin_info(plugin_id).display_name
        if ack_identity:
            simple_id = self.current_plugins[Config.audit_name][plugin_id].get(ack_identity)
            if simple_id:
                plugin_name = '%s (%d)' % (plugin_name, simple_id + 1)
        return plugin_name