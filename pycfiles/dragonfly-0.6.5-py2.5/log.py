# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\dragonfly\log.py
# Compiled at: 2009-01-29 08:32:46
"""
    This file implements Dragonfly's internal logging system.
"""
import sys, os.path, logging, logging.handlers, win32gui
from win32com.shell import shell, shellcon
log_handlers = [
 'stdout', 'file']
log_names = {'': (
      logging.WARNING, logging.WARNING), 
   'engine': (
            logging.WARNING, logging.INFO), 
   'engine.compiler': (
                     logging.WARNING, logging.INFO), 
   'grammar': (
             logging.WARNING, logging.INFO), 
   'grammar.load': (
                  logging.WARNING, logging.INFO), 
   'grammar.begin': (
                   logging.WARNING, logging.INFO), 
   'grammar.results': (
                     logging.WARNING, logging.WARNING), 
   'grammar.decode': (
                    logging.WARNING, logging.INFO), 
   'grammar.eval': (
                  logging.WARNING, logging.WARNING), 
   'grammar.process': (
                     logging.WARNING, logging.WARNING), 
   'compound.parse': (
                    logging.WARNING, logging.INFO), 
   'dictation.formatter': (
                         logging.WARNING, logging.WARNING), 
   'action': (
            logging.WARNING, logging.WARNING), 
   'action.init': (
                 logging.WARNING, logging.WARNING), 
   'action.exec': (
                 logging.WARNING, logging.WARNING), 
   'context': (
             logging.WARNING, logging.INFO), 
   'context.match': (
                   logging.WARNING, logging.INFO), 
   'rule': (
          logging.WARNING, logging.INFO), 
   'config': (
            logging.WARNING, logging.INFO), 
   'monitor.init': (
                  logging.WARNING, logging.INFO)}
mydocs_pidl = shell.SHGetFolderLocation(0, shellcon.CSIDL_PERSONAL, 0, 0)
mydocs_path = shell.SHGetPathFromIDList(mydocs_pidl)
log_file_path = os.path.join(mydocs_path, 'dragonfly.txt')
log_file_size = 131072
log_file_count = 9
_log_cache = {}

def get_log(name):
    global _log_cache
    global log_names
    global root_logger
    if name in _log_cache:
        return _log_cache[name]
    if name in log_names:
        log_levels = log_names[name]
        if not log_levels or not [ True for l in log_levels if l is not None ]:
            _log_cache[name] = None
            return
        else:
            log = logging.getLogger(name)
            minimum_level = min([ l for l in log_levels if l is not None ])
            log.setLevel(minimum_level)
            log.propagate = False
            for (handler, level) in zip(log_handlers, log_levels):
                if level is not None:
                    handler.addFilter(NameLevelFilter(name, level))
                    log.addHandler(handler)

            _log_cache[name] = log
            return log
    else:
        root_logger.error("Request for unknown log name: '%s'" % name)
        _log_cache[name] = logging.getLogger('UNKNOWN')
        return _log_cache[name]
    return


class NameLevelFilter(logging.Filter):

    def __init__(self, name, level):
        self._name = name
        self._level = level

    def filter(self, record):
        if record.name == self._name:
            if record.levelno >= self._level:
                return True
            else:
                return False
        else:
            return True


root_logger = logging.getLogger('')
root_logger.setLevel(logging.DEBUG)

class _OutputStream(object):

    def __init__(self, write):
        self.write = write

    def flush(self):
        pass


handler = logging.StreamHandler(_OutputStream(sys.stdout.write))
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(name)s: %(message)s')
handler.setFormatter(formatter)
log_handlers[log_handlers.index('stdout')] = handler
root_logger.addHandler(handler)
handler = logging.FileHandler(log_file_path)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s %(name)s (%(levelname)s): %(message)s')
handler.setFormatter(formatter)
log_handlers[log_handlers.index('file')] = handler
root_logger.addHandler(handler)