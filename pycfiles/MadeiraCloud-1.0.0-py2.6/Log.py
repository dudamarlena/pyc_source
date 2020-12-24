# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/madeiracloud/Log.py
# Compiled at: 2011-12-16 02:01:38
import sys, time, logging
try:
    import curses
except ImportError:
    curses = None

class LogFormatter(logging.Formatter):

    def __init__(self, console, *args, **kwargs):
        logging.Formatter.__init__(self, '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        color = False
        if console:
            if curses and sys.stderr.isatty():
                try:
                    curses.setupterm()
                    if curses.tigetnum('colors') > 0:
                        color = True
                except Exception:
                    pass

        self._color = color
        if color:
            fg_color = unicode(curses.tigetstr('setaf') or curses.tigetstr('setf') or '', 'ascii')
            self._colors = {logging.DEBUG: unicode(curses.tparm(fg_color, 4), 'ascii'), 
               logging.INFO: unicode(curses.tparm(fg_color, 2), 'ascii'), 
               logging.WARNING: unicode(curses.tparm(fg_color, 3), 'ascii'), 
               logging.ERROR: unicode(curses.tparm(fg_color, 1), 'ascii')}
            self._normal = unicode(curses.tigetstr('sgr0'), 'ascii')

    def format(self, record):
        try:
            record.message = record.getMessage()
        except Exception, e:
            record.message = 'Bad message (%r): %r' % (e, record.__dict__)

        record.asctime = time.strftime('%Y-%m-%d %H:%M:%S', self.converter(record.created))
        prefix = '[%(asctime)s - %(levelname)s - %(module)s:%(lineno)d]' % record.__dict__
        if self._color:
            prefix = self._colors.get(record.levelno, self._normal) + prefix + self._normal
        formatted = prefix + ' ' + record.message
        if record.exc_info:
            if not record.exc_text:
                record.exc_text = self.formatException(record.exc_info)
        if record.exc_text:
            formatted = formatted.rstrip() + '\n' + record.exc_text
        return formatted.replace('\n', '\n    ')