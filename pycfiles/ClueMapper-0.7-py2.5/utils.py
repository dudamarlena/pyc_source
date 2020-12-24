# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/clue/app/utils.py
# Compiled at: 2008-06-27 12:03:50
import os, threading, logging
logger = logging.getLogger('cluemapper')

class Sleeper(object):
    """A object that can cause the current thread to sleep until the timer
    runs out or the sleep is cancelled.

      >>> sleeper = Sleeper()
      >>> class Factory(object):
      ...     def clear(self): print 'clear()'
      ...     def wait(self, seconds): print 'wait(%i)' % seconds
      ...     def set(self): print 'set()'
      >>> sleeper.event_factory = Factory
      >>> sleeper.sleep(5)
      clear()
      wait(5)
      >>> sleeper.cancel()
      set()
    """
    event_factory = threading.Event

    def __init__(self):
        self._event = None
        return

    @property
    def event(self):
        if self._event is None:
            self._event = self.event_factory()
        return self._event

    def sleep(self, seconds):
        self.event.clear()
        self.event.wait(seconds)

    def cancel(self):
        self.event.set()


def get_prjid(environ):
    """Get the active project id from environ.

      >>> get_prjid({'SCRIPT_NAME': '', 'PATH_INFO': ''}) is None
      True
      >>> get_prjid({'SCRIPT_NAME': '/pm', 'PATH_INFO': ''}) is None
      True
      >>> get_prjid({'SCRIPT_NAME': '/pm/p/foo', 'PATH_INFO': ''})
      'foo'
    """
    full = environ['SCRIPT_NAME'] + environ['PATH_INFO']
    pieces = [ x for x in full.split('/') if x ]
    try:
        pmpos = pieces.index('pm')
    except ValueError, err:
        return

    if len(pieces) - 2 > pmpos:
        return pieces[(pmpos + 2)]
    return


class AccessError(Exception):
    pass


def build_path(workingdir, p):
    if not p.startswith(os.path.sep):
        p = os.path.join(workingdir, p)
    return os.path.abspath(p)


class PathBuilder(object):

    def __init__(self, basepath):
        self.basepath = basepath

    def __call__(self, extra):
        return build_path(self.basepath, extra)


def setup_logger():
    formatter = logging.Formatter('%(asctime)s %(levelname)-5.5s [%(name)s] %(message)s')
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    handler.setLevel(logging.DEBUG)
    logger = logging.getLogger('cluemapper')
    logger.addHandler(handler)
    logger.setLevel(int(os.environ.get('cluemapper.loglevel', logging.INFO)))
    return logger