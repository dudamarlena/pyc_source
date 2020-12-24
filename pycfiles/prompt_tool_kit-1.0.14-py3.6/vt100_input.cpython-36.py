# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/prompt_tool_kit/terminal/vt100_input.py
# Compiled at: 2019-08-15 23:53:38
# Size of source mod 2**32: 18429 bytes
"""
Parser for VT100 input stream.
"""
from __future__ import unicode_literals
import os, re, six, termios, tty
from six.moves import range
from ..keys import Keys
from ..key_binding.input_processor import KeyPress
__all__ = ('InputStream', 'raw_mode', 'cooked_mode')
_DEBUG_RENDERER_INPUT = False
_DEBUG_RENDERER_INPUT_FILENAME = 'prompt-toolkit-render-input.log'
_cpr_response_re = re.compile('^' + re.escape('\x1b[') + '\\d+;\\d+R\\Z')
_mouse_event_re = re.compile('^' + re.escape('\x1b[') + '(<?[\\d;]+[mM]|M...)\\Z')
_cpr_response_prefix_re = re.compile('^' + re.escape('\x1b[') + '[\\d;]*\\Z')
_mouse_event_prefix_re = re.compile('^' + re.escape('\x1b[') + '(<?[\\d;]*|M.{0,2})\\Z')

class _Flush(object):
    __doc__ = ' Helper object to indicate flush operation to the parser. '


ANSI_SEQUENCES = {'\x1b':Keys.Escape, 
 '\x00':Keys.ControlSpace, 
 '\x01':Keys.ControlA, 
 '\x02':Keys.ControlB, 
 '\x03':Keys.ControlC, 
 '\x04':Keys.ControlD, 
 '\x05':Keys.ControlE, 
 '\x06':Keys.ControlF, 
 '\x07':Keys.ControlG, 
 '\x08':Keys.ControlH, 
 '\t':Keys.ControlI, 
 '\n':Keys.ControlJ, 
 '\x0b':Keys.ControlK, 
 '\x0c':Keys.ControlL, 
 '\r':Keys.ControlM, 
 '\x0e':Keys.ControlN, 
 '\x0f':Keys.ControlO, 
 '\x10':Keys.ControlP, 
 '\x11':Keys.ControlQ, 
 '\x12':Keys.ControlR, 
 '\x13':Keys.ControlS, 
 '\x14':Keys.ControlT, 
 '\x15':Keys.ControlU, 
 '\x16':Keys.ControlV, 
 '\x17':Keys.ControlW, 
 '\x18':Keys.ControlX, 
 '\x19':Keys.ControlY, 
 '\x1a':Keys.ControlZ, 
 '\x1c':Keys.ControlBackslash, 
 '\x1d':Keys.ControlSquareClose, 
 '\x1e':Keys.ControlCircumflex, 
 '\x1f':Keys.ControlUnderscore, 
 '\x7f':Keys.Backspace, 
 '\x1b[A':Keys.Up, 
 '\x1b[B':Keys.Down, 
 '\x1b[C':Keys.Right, 
 '\x1b[D':Keys.Left, 
 '\x1b[H':Keys.Home, 
 '\x1bOH':Keys.Home, 
 '\x1b[F':Keys.End, 
 '\x1bOF':Keys.End, 
 '\x1b[3~':Keys.Delete, 
 '\x1b[3;2~':Keys.ShiftDelete, 
 '\x1b[3;5~':Keys.ControlDelete, 
 '\x1b[1~':Keys.Home, 
 '\x1b[4~':Keys.End, 
 '\x1b[5~':Keys.PageUp, 
 '\x1b[6~':Keys.PageDown, 
 '\x1b[7~':Keys.Home, 
 '\x1b[8~':Keys.End, 
 '\x1b[Z':Keys.BackTab, 
 '\x1b[2~':Keys.Insert, 
 '\x1bOP':Keys.F1, 
 '\x1bOQ':Keys.F2, 
 '\x1bOR':Keys.F3, 
 '\x1bOS':Keys.F4, 
 '\x1b[[A':Keys.F1, 
 '\x1b[[B':Keys.F2, 
 '\x1b[[C':Keys.F3, 
 '\x1b[[D':Keys.F4, 
 '\x1b[[E':Keys.F5, 
 '\x1b[11~':Keys.F1, 
 '\x1b[12~':Keys.F2, 
 '\x1b[13~':Keys.F3, 
 '\x1b[14~':Keys.F4, 
 '\x1b[15~':Keys.F5, 
 '\x1b[17~':Keys.F6, 
 '\x1b[18~':Keys.F7, 
 '\x1b[19~':Keys.F8, 
 '\x1b[20~':Keys.F9, 
 '\x1b[21~':Keys.F10, 
 '\x1b[23~':Keys.F11, 
 '\x1b[24~':Keys.F12, 
 '\x1b[25~':Keys.F13, 
 '\x1b[26~':Keys.F14, 
 '\x1b[28~':Keys.F15, 
 '\x1b[29~':Keys.F16, 
 '\x1b[31~':Keys.F17, 
 '\x1b[32~':Keys.F18, 
 '\x1b[33~':Keys.F19, 
 '\x1b[34~':Keys.F20, 
 '\x1b[1;2P':Keys.F13, 
 '\x1b[1;2Q':Keys.F14, 
 '\x1b[1;2S':Keys.F16, 
 '\x1b[15;2~':Keys.F17, 
 '\x1b[17;2~':Keys.F18, 
 '\x1b[18;2~':Keys.F19, 
 '\x1b[19;2~':Keys.F20, 
 '\x1b[20;2~':Keys.F21, 
 '\x1b[21;2~':Keys.F22, 
 '\x1b[23;2~':Keys.F23, 
 '\x1b[24;2~':Keys.F24, 
 '\x1b[1;5A':Keys.ControlUp, 
 '\x1b[1;5B':Keys.ControlDown, 
 '\x1b[1;5C':Keys.ControlRight, 
 '\x1b[1;5D':Keys.ControlLeft, 
 '\x1b[1;2A':Keys.ShiftUp, 
 '\x1b[1;2B':Keys.ShiftDown, 
 '\x1b[1;2C':Keys.ShiftRight, 
 '\x1b[1;2D':Keys.ShiftLeft, 
 '\x1bOA':Keys.Up, 
 '\x1bOB':Keys.Down, 
 '\x1bOC':Keys.Right, 
 '\x1bOD':Keys.Left, 
 '\x1b[5A':Keys.ControlUp, 
 '\x1b[5B':Keys.ControlDown, 
 '\x1b[5C':Keys.ControlRight, 
 '\x1b[5D':Keys.ControlLeft, 
 '\x1bOc':Keys.ControlRight, 
 '\x1bOd':Keys.ControlLeft, 
 '\x1b[200~':Keys.BracketedPaste, 
 '\x1b[1;3D':(
  Keys.Escape, Keys.Left), 
 '\x1b[1;3C':(
  Keys.Escape, Keys.Right), 
 '\x1b[1;3A':(
  Keys.Escape, Keys.Up), 
 '\x1b[1;3B':(
  Keys.Escape, Keys.Down), 
 '\x1b[E':Keys.Ignore, 
 '\x1b[G':Keys.Ignore}

class _IsPrefixOfLongerMatchCache(dict):
    __doc__ = '\n    Dictiory that maps input sequences to a boolean indicating whether there is\n    any key that start with this characters.\n    '

    def __missing__(self, prefix):
        if _cpr_response_prefix_re.match(prefix) or _mouse_event_prefix_re.match(prefix):
            result = True
        else:
            result = any(v for k, v in ANSI_SEQUENCES.items() if k.startswith(prefix) if k != prefix)
        self[prefix] = result
        return result


_IS_PREFIX_OF_LONGER_MATCH_CACHE = _IsPrefixOfLongerMatchCache()

class InputStream(object):
    __doc__ = "\n    Parser for VT100 input stream.\n\n    Feed the data through the `feed` method and the correct callbacks of the\n    `input_processor` will be called.\n\n    ::\n\n        def callback(key):\n            pass\n        i = InputStream(callback)\n        i.feed('data\x01...')\n\n    :attr input_processor: :class:`~prompt_tool_kit.key_binding.InputProcessor` instance.\n    "

    def __init__(self, feed_key_callback):
        assert callable(feed_key_callback)
        self.feed_key_callback = feed_key_callback
        self.reset()
        if _DEBUG_RENDERER_INPUT:
            self.LOG = open(_DEBUG_RENDERER_INPUT_FILENAME, 'ab')

    def reset(self, request=False):
        self._in_bracketed_paste = False
        self._start_parser()

    def _start_parser(self):
        """
        Start the parser coroutine.
        """
        self._input_parser = self._input_parser_generator()
        self._input_parser.send(None)

    def _get_match(self, prefix):
        """
        Return the key that maps to this prefix.
        """
        if _cpr_response_re.match(prefix):
            return Keys.CPRResponse
        if _mouse_event_re.match(prefix):
            return Keys.Vt100MouseEvent
        try:
            return ANSI_SEQUENCES[prefix]
        except KeyError:
            return

    def _input_parser_generator(self):
        """
        Coroutine (state machine) for the input parser.
        """
        prefix = ''
        retry = False
        flush = False
        while 1:
            flush = False
            if retry:
                retry = False
            else:
                c = yield
                if c == _Flush:
                    flush = True
                else:
                    prefix += c
            if prefix:
                is_prefix_of_longer_match = _IS_PREFIX_OF_LONGER_MATCH_CACHE[prefix]
                match = self._get_match(prefix)
                if flush or not is_prefix_of_longer_match:
                    if match:
                        self._call_handler(match, prefix)
                        prefix = ''
                if (flush or not is_prefix_of_longer_match) and not match:
                    found = False
                    retry = True
                    for i in range(len(prefix), 0, -1):
                        match = self._get_match(prefix[:i])
                        if match:
                            self._call_handler(match, prefix[:i])
                            prefix = prefix[i:]
                            found = True

                    if not found:
                        self._call_handler(prefix[0], prefix[0])
                        prefix = prefix[1:]

    def _call_handler(self, key, insert_text):
        """
        Callback to handler.
        """
        if isinstance(key, tuple):
            for k in key:
                self._call_handler(k, insert_text)

        else:
            if key == Keys.BracketedPaste:
                self._in_bracketed_paste = True
                self._paste_buffer = ''
            else:
                self.feed_key_callback(KeyPress(key, insert_text))

    def feed(self, data):
        """
        Feed the input stream.

        :param data: Input string (unicode).
        """
        if not isinstance(data, six.text_type):
            raise AssertionError
        elif _DEBUG_RENDERER_INPUT:
            self.LOG.write(repr(data).encode('utf-8') + b'\n')
            self.LOG.flush()
        else:
            if self._in_bracketed_paste:
                self._paste_buffer += data
                end_mark = '\x1b[201~'
                if end_mark in self._paste_buffer:
                    end_index = self._paste_buffer.index(end_mark)
                    paste_content = self._paste_buffer[:end_index]
                    self.feed_key_callback(KeyPress(Keys.BracketedPaste, paste_content))
                    self._in_bracketed_paste = False
                    remaining = self._paste_buffer[end_index + len(end_mark):]
                    self._paste_buffer = ''
                    self.feed(remaining)
            else:
                for i, c in enumerate(data):
                    if self._in_bracketed_paste:
                        self.feed(data[i:])
                        break
                    else:
                        if c == '\r':
                            c = '\n'
                        self._input_parser.send(c)

    def flush(self):
        """
        Flush the buffer of the input stream.

        This will allow us to handle the escape key (or maybe meta) sooner.
        The input received by the escape key is actually the same as the first
        characters of e.g. Arrow-Up, so without knowing what follows the escape
        sequence, we don't know whether escape has been pressed, or whether
        it's something else. This flush function should be called after a
        timeout, and processes everything that's still in the buffer as-is, so
        without assuming any characters will folow.
        """
        self._input_parser.send(_Flush)

    def feed_and_flush(self, data):
        """
        Wrapper around ``feed`` and ``flush``.
        """
        self.feed(data)
        self.flush()


class raw_mode(object):
    __doc__ = "\n    ::\n\n        with raw_mode(stdin):\n            ''' the pseudo-terminal stdin is now used in raw mode '''\n\n    We ignore errors when executing `tcgetattr` fails.\n    "

    def __init__(self, fileno):
        self.fileno = fileno
        try:
            self.attrs_before = termios.tcgetattr(fileno)
        except termios.error:
            self.attrs_before = None

    def __enter__(self):
        try:
            newattr = termios.tcgetattr(self.fileno)
        except termios.error:
            pass
        else:
            newattr[tty.LFLAG] = self._patch_lflag(newattr[tty.LFLAG])
            newattr[tty.IFLAG] = self._patch_iflag(newattr[tty.IFLAG])
            newattr[tty.CC][termios.VMIN] = 1
            termios.tcsetattr(self.fileno, termios.TCSANOW, newattr)
            os.write(self.fileno, b'\x1b[?1l')

    @classmethod
    def _patch_lflag(cls, attrs):
        return attrs & ~(termios.ECHO | termios.ICANON | termios.IEXTEN | termios.ISIG)

    @classmethod
    def _patch_iflag(cls, attrs):
        return attrs & ~(termios.IXON | termios.IXOFF | termios.ICRNL | termios.INLCR | termios.IGNCR)

    def __exit__(self, *a, **kw):
        if self.attrs_before is not None:
            try:
                termios.tcsetattr(self.fileno, termios.TCSANOW, self.attrs_before)
            except termios.error:
                pass


class cooked_mode(raw_mode):
    __doc__ = "\n    The opposide of ``raw_mode``, used when we need cooked mode inside a\n    `raw_mode` block.  Used in `CommandLineInterface.run_in_terminal`.::\n\n        with cooked_mode(stdin):\n            ''' the pseudo-terminal stdin is now used in cooked mode. '''\n    "

    @classmethod
    def _patch_lflag(cls, attrs):
        return attrs | (termios.ECHO | termios.ICANON | termios.IEXTEN | termios.ISIG)

    @classmethod
    def _patch_iflag(cls, attrs):
        return attrs | termios.ICRNL