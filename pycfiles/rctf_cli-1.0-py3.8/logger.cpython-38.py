# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/rctf-cli/rctf/logger.py
# Compiled at: 2020-03-23 01:47:18
# Size of source mod 2**32: 3103 bytes
import logging

class ColorLog(object):

    def __init__(self, logger):
        self._log = logger

    def _log_msg(self, name, *args, **kwargs):
        return getattr(self._log, 'fatal' if name == 'exception' else name)((self._format_msg)(name, *args, **kwargs))

    def _format_msg(self, name, *args, **kwargs):
        exc_info = kwargs.get('exc_info', False)
        if name == 'exception':
            name = 'fatal'
            exc_info = True
        else:
            if name == 'warn':
                name = 'warning'
            else:
                if name == 'critical':
                    name = 'fatal'
        _colored = colored if kwargs.get('use_ansi', True) else (lambda s, x: s)
        prompt = prompts[name] + ' ' if not kwargs.get('prompt') else kwargs.get('prompt')
        message = _colored(prompt, colormap[name]) + ''.join([_colored(x, colormap[name]) for x in args])
        if exc_info:
            exception = traceback.format_exc().strip()
            prompt = '... ' if not kwargs.get('prompt') else kwargs.get('prompt')
            message += '\n' + '\n'.join([prompt + _colored(x, colormap['exception']) for x in exception.split('\n')])
        return message

    def __getattr__(self, name):
        if name in ('debug', 'info', 'warn', 'warning', 'error', 'critical', 'fatal',
                    'exception'):
            return lambda *args, **kwargs: (self._log_msg)(name, *args, **kwargs)
        return getattr(self._log, name)


colored = lambda message, attrs=[]: colors['reset'] + ''.join([colors[x] for x in attrs]) + str(message) + colors['reset']
colored_command = lambda message: colors['bold'] + colors['underline'] + str(message) + colors['reset']
colormap = {'debug':[
  'italics', 'gray'], 
 'info':[
  'blue'], 
 'warning':[
  'bold', 'darkorange'], 
 'error':[
  'bold', 'lightred'], 
 'fatal':[
  'bg_red', 'bold_white'], 
 'exception':[
  'italics', 'darkred']}
prompts = {'debug':' * ', 
 'info':'[*]', 
 'warn':'[!]', 
 'warning':'[!]', 
 'error':'[-]', 
 'fatal':'[-]'}
log_levels = {'debug':logging.DEBUG, 
 'info':logging.INFO, 
 'warn':logging.WARNING, 
 'warning':logging.WARNING, 
 'error':logging.ERROR, 
 'critical':logging.CRITICAL, 
 'fatal':logging.FATAL}
colors = {'lightgray':'\x1b[37m', 
 'darkgray':'\x1b[90m', 
 'gray':'\x1b[2m', 
 'blue':'\x1b[34m', 
 'green':'\x1b[32m', 
 'cyan':'\x1b[36m', 
 'darkorange':'\x1b[33m', 
 'darkred':'\x1b[31m', 
 'lightred':'\x1b[91m', 
 'red':'\x1b[91m', 
 'yellow':'\x1b[33m', 
 'lightyellow':'\x1b[93m', 
 'lightgreen':'\x1b[92m', 
 'bold_white':'\x1b[1;37m', 
 'bg_red':'\x1b[41m', 
 'italics':'\x1b[3m', 
 'bold':'\x1b[01m', 
 'underline':'\x1b[04m', 
 'reset':'\x1b[0m'}
LOG_LEVEL = logging.DEBUG
log = ColorLog(logging.getLogger(__name__))
log.setLevel(LOG_LEVEL)
stdout = logging.StreamHandler()
log.addHandler(stdout)
stdout.setLevel(LOG_LEVEL)
logging = log