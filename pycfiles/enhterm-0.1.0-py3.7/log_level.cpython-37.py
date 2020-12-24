# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\enhterm\log_level.py
# Compiled at: 2019-11-09 03:00:14
# Size of source mod 2**32: 4021 bytes
"""
Allow the user to control the level of logging.
"""
from __future__ import unicode_literals
from __future__ import print_function
import logging
from .lang import _
logger = logging.getLogger('enhterm')

class LogLevelMixin(object):
    args_set_loglevel = [
     'level', 'args']

    def __init__(self, *args, **kwargs):
        (super(LogLevelMixin, self).__init__)(*args, **kwargs)
        self.add_subcommand('set', 'loglevel')

    def sdo_set_loglevel(self, arg):
        command_format = _('The format of the command is `set loglevel LEVEL [[to] TARGET]`\nWhere LEVEL is `d[ebug]` , `i[nfo]`, `w[arning]` and `e[rror]` \nTARGET is one of `c[onsole]` or `f[ile]` (default is console)')
        console_handler = None
        file_handler = None
        for handler in logger.handlers:
            if isinstance(handler, logging.StreamHandler):
                console_handler = handler

        def get_kind(value):
            kind = value.lower()
            if kind in ('c', 'con', 'console'):
                target = (
                 console_handler, 'console')
            else:
                if kind in ('f', 'file'):
                    target = (
                     file_handler, 'file')
                else:
                    self.error(_('Invalid target argument: %s') % kind, command_format)
                    target = (None, None)
            return target

        target = None
        target_str = ''
        log_level = None
        level_str = arg['level'].lower()
        args = arg['args']
        if len(args) == 0:
            target = console_handler
            target_str = 'console'
        else:
            if len(args) == 1:
                target, target_str = get_kind(args[0])
            else:
                if len(args) == 2:
                    sugar = args[0].lower()
                    if sugar not in ('2', 'to'):
                        self.error(_('Invalid list of arguments'), command_format)
                    else:
                        target, target_str = get_kind(args[1])
                else:
                    self.error(_('Invalid list of arguments'), command_format)
        if level_str in ('d', 'debug'):
            log_level = logging.DEBUG
        else:
            if level_str in ('w', 'warn', 'warning'):
                log_level = logging.WARNING
            else:
                if level_str in ('i', 'info', 'information'):
                    log_level = logging.INFO
                else:
                    if level_str in ('e', 'err', 'error'):
                        log_level = logging.ERROR
                    else:
                        if level_str in ('c', 'crit', 'critical'):
                            log_level = logging.CRITICAL
                        else:
                            try:
                                log_level = int(level_str)
                            except ValueError:
                                self.error(_('Invalid level'), command_format)

                            if not log_level is None:
                                if not target is None:
                                    if not target[0] is None:
                                        target.setLevel(log_level)
                                        top_log = logging.getLogger('')
                                        if top_log.level > log_level:
                                            top_log.setLevel(log_level)
                                        logger.debug('New log level %s set to %s', level_str, target_str)

    def helps_set_loglevel(self):
        self.info(_('Change logging verbosity.\n\nArguments\n---------\nlevel:    new level; can be one of `d[ebug]` , `i[nfo]`, \n          `w[arning]` or `e[rror]`\nto:       this is just syntactic sugar so the sentence looks nice; \n          can be omitted;\nadapter:  the adapter(s) that should receive the words.\n\nDescription\n-----------\nThe program logs data to a file and to console. The user can control the \nverbosity by using this command.\n\nPlease note that there are two notification systems:\n- the logging system is mostly used by the library and low level commands;\n- the command system uses a separate way of printing errors only to \nthe screen.\nThis command controls the low level logging facility.\n\nExample\n-------\n$: set loglevel debug to console\n$: set loglevel debug console\n$: set loglevel d c\n$: set loglevel debug\n$: set loglevel info to file\n$: set loglevel i f\n'))