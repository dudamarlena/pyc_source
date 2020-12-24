# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/prompt_tool_kit/eventloop/inputhook.py
# Compiled at: 2019-08-15 23:53:38
# Size of source mod 2**32: 3566 bytes
__doc__ = "\nSimilar to `PyOS_InputHook` of the Python API. Some eventloops can have an\ninputhook to allow easy integration with other event loops.\n\nWhen the eventloop of prompt-toolkit is idle, it can call such a hook. This\nhook can call another eventloop that runs for a short while, for instance to\nkeep a graphical user interface responsive.\n\nIt's the responsibility of this hook to exit when there is input ready.\nThere are two ways to detect when input is ready:\n\n- Call the `input_is_ready` method periodically. Quit when this returns `True`.\n\n- Add the `fileno` as a watch to the external eventloop. Quit when file descriptor\n  becomes readable. (But don't read from it.)\n\n  Note that this is not the same as checking for `sys.stdin.fileno()`. The\n  eventloop of prompt-toolkit allows thread-based executors, for example for\n  asynchronous autocompletion. When the completion for instance is ready, we\n  also want prompt-toolkit to gain control again in order to display that.\n\nAn alternative to using input hooks, is to create a custom `EventLoop` class that\ncontrols everything.\n"
from __future__ import unicode_literals
import os, threading
from prompt_tool_kit.utils import is_windows
from .select import select_fds
__all__ = ('InputHookContext', )

class InputHookContext(object):
    """InputHookContext"""

    def __init__(self, inputhook):
        assert callable(inputhook)
        self.inputhook = inputhook
        self._input_is_ready = None
        self._r, self._w = os.pipe()

    def input_is_ready(self):
        """
        Return True when the input is ready.
        """
        return self._input_is_ready(wait=False)

    def fileno(self):
        """
        File descriptor that will become ready when the event loop needs to go on.
        """
        return self._r

    def call_inputhook(self, input_is_ready_func):
        """
        Call the inputhook. (Called by a prompt-toolkit eventloop.)
        """
        self._input_is_ready = input_is_ready_func

        def thread():
            input_is_ready_func(wait=True)
            os.write(self._w, 'x')

        threading.Thread(target=thread).start()
        self.inputhook(self)
        try:
            if not is_windows():
                select_fds([self._r], timeout=None)
            os.read(self._r, 1024)
        except OSError:
            pass

        self._input_is_ready = None

    def close(self):
        """
        Clean up resources.
        """
        if self._r:
            os.close(self._r)
            os.close(self._w)
        self._r = self._w = None