# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win-amd64\egg\apsitemap\utility.py
# Compiled at: 2017-10-12 21:55:38
# Size of source mod 2**32: 2613 bytes
import logging, sys, logging.handlers
try:
    import colorama
except ImportError:
    colorama = None

try:
    import curses
except ImportError:
    curses = None

def _stderr_supports_color():
    try:
        if hasattr(sys.stderr, 'isatty'):
            if sys.stderr.isatty():
                if curses:
                    curses.setupterm()
                    if curses.tigetnum('colors') > 0:
                        return True
                elif colorama:
                    if sys.stderr is getattr(colorama.initialise, 'wrapped_stderr', object()):
                        return True
    except Exception:
        pass

    return False


class ColoredFormatter(logging.Formatter):
    DEFAULT_FORMAT = '%(color)s[%(levelname)-8.8s %(asctime)s %(module)s:%(lineno)d]%(end_color)s %(message)s'
    DEFAULT_DATE_FORMAT = '%Y/%m/%d %H:%M:%S'
    DEFAULT_COLORS = {logging.DEBUG: 34, 
     logging.INFO: 32, 
     logging.WARNING: 33, 
     logging.ERROR: 31, 
     logging.CRITICAL: 35}

    def __init__(self, fmt=DEFAULT_FORMAT, datefmt=DEFAULT_DATE_FORMAT, style='%', color=True, colors=DEFAULT_COLORS):
        logging.Formatter.__init__(self, datefmt=datefmt)
        self._fmt = fmt
        self.style = style
        self._colors = {}
        if color:
            if _stderr_supports_color():
                for levelno, code in colors.items():
                    self._colors[levelno] = '\x1b[2;%dm' % code

                self._normal = '\x1b[0m'
        else:
            self._normal = ''

    def format(self, record):
        record.message = record.getMessage()
        record.asctime = self.formatTime(record, self.datefmt)
        if record.levelno in self._colors:
            record.color = self._colors[record.levelno]
            record.end_color = self._normal
        else:
            record.color = record.end_color = ''
        return self._fmt % record.__dict__


def standardize_url(url: str, scheme='http://'):
    if url.startswith('http://') or url.startswith('https://'):
        return url
    else:
        return scheme + url


def _get_logger():
    """generate logger"""
    logger = logging.Logger('sitemap')
    handler = logging.StreamHandler(stream=(sys.stdout))
    formatter = ColoredFormatter()
    handler.setFormatter(fmt=formatter)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)
    return logger


sitemap_log = _get_logger()