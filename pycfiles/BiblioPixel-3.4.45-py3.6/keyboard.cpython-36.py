# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bibliopixel/control/keyboard.py
# Compiled at: 2019-08-11 12:22:47
# Size of source mod 2**32: 1583 bytes
import getpass, platform, sys, threading
from ..util import log
from .control import ExtractedControl
DARWIN_ROOT_WARNING = '\nIn MacOS, pynput must to be running as root in order to get keystrokes.\n\nTry running your program like this:\n\n    sudo %s <your commands here>\n'
INSTALL_ERROR = '\nPlease install the pynput library with\n\n    $ pip install pynput\n\n'
try:
    import pynput
except ImportError:
    pynput = Listener = None
else:

    class Listener(pynput.keyboard.Listener):

        def join(self, timeout=None):
            self._queue.put(None)
            return super().join(timeout)


def keyname(key):
    return getattr(key, 'name', None) or getattr(key, 'char')


class Keyboard(ExtractedControl):
    EXTRACTOR = {'keys_by_type':{'press':[
       'type', 'key'], 
      'release':[
       'type', 'key']}, 
     'normalizers':{'key': keyname}}

    def _press(self, key):
        self.receive({'type':'press',  'key':key})

    def _release(self, key):
        self.receive({'type':'release',  'key':key})

    def _make_thread(self):
        if not pynput:
            raise ValueError(INSTALL_ERROR)
        if platform.platform().startswith('Darwin'):
            if getpass.getuser() != 'root':
                log.warning(DARWIN_ROOT_WARNING, sys.argv[0])
        log.info('Starting to listen for keyboard input')
        return Listener(self._press, self._release)