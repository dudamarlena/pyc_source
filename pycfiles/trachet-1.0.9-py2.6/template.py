# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.4-x86_64/egg/trachet/template.py
# Compiled at: 2014-07-01 10:29:06
_template_char = None
_template_printablechar = None
_template_esc = None
_template_csi = None
_template_cstr = None
_template_ss2 = None
_template_ss3 = None
_template_invalid = None
_template_mouse = None
_template_highlight_mouse = None
_template_highlight_mouse_initial = None
_template_resize = None
_template_outputprompt = None
_template_inputprompt = None

def getchar():
    global _template_char
    return _template_char


def getprintablechar():
    global _template_printablechar
    return _template_printablechar


def getesc():
    global _template_esc
    return _template_esc


def getcsi():
    global _template_csi
    return _template_csi


def getcstr():
    global _template_cstr
    return _template_cstr


def getss2():
    global _template_ss2
    return _template_ss2


def getss3():
    global _template_ss3
    return _template_ss3


def getinvalid():
    global _template_invalid
    return _template_invalid


def getmouse():
    global _template_mouse
    return _template_mouse


def gethighlightmouseinitial():
    global _template_highlight_mouse_initial
    return _template_highlight_mouse_initial


def gethighlightmouse():
    global _template_highlight_mouse
    return _template_highlight_mouse


def getresize():
    global _template_resize
    return _template_resize


def getoutputprompt():
    global _template_outputprompt
    return _template_outputprompt


def getinputprompt():
    global _template_inputprompt
    return _template_inputprompt


def enable_color():
    global _template_char
    global _template_csi
    global _template_cstr
    global _template_esc
    global _template_highlight_mouse
    global _template_highlight_mouse_initial
    global _template_inputprompt
    global _template_invalid
    global _template_mouse
    global _template_outputprompt
    global _template_printablechar
    global _template_resize
    global _template_ss2
    global _template_ss3
    _template_inputprompt = '\x1b[0;7m<<<'
    _template_outputprompt = '\x1b[m>>>'
    _template_char = '\x1b[32m%s\x1b[m'
    _template_printablechar = '\x1b[31m%s\x1b[1;32m\r\x1b[30C%s\x1b[m'
    _template_esc = '\x1b[0;1;31;44m ESC \x1b[36m%s\x1b[33m%s \x1b[0;1;35m\r\x1b[30C%s\x1b[m'
    _template_csi = '\x1b[0;1;31;40m CSI \x1b[35m%s\x1b[36m%s\x1b[33m%s \x1b[0;1;36m\r\x1b[30C%s\x1b[m'
    _template_cstr = '\x1b[0;1;37;44m ESC %s \x1b[0;1;35m%s \x1b[37;44mST\x1b[0;1;36m  %s\x1b[m'
    _template_ss2 = '\x1b[0;1;36;44m ESC N %s \x1b[0;1;31m\r\x1b[30C%s'
    _template_ss3 = '\x1b[0;1;36;44m ESC O %s \x1b[0;1;31m\r\x1b[30C%s'
    _template_invalid = '%s  \x1b[33;41m%s\x1b[m\n'
    _template_mouse = '%s   \x1b[0;1;31mCSI \x1b[35mM \x1b[m%c %c %c \x1b[32;41m%s\x1b[m\n'
    _template_highlight_mouse_initial = '%s   \x1b[0;1;31mCSI \x1b[35mt \x1b[m%c %c \x1b[32;41m%s\x1b[m\n'
    _template_highlight_mouse = '%s   \x1b[0;1;31mCSI \x1b[35mT \x1b[m%c %c %c %c %c %c \x1b[32;41m%s\x1b[m\n'
    _template_resize = '%s  \x1b[33;41m resized: (row=%d, col=%d)\x1b[m\n'


def disable_color():
    global _template_char
    global _template_csi
    global _template_cstr
    global _template_esc
    global _template_highlight_mouse
    global _template_highlight_mouse_initial
    global _template_inputprompt
    global _template_invalid
    global _template_mouse
    global _template_outputprompt
    global _template_printablechar
    global _template_resize
    global _template_ss2
    global _template_ss3
    _template_inputprompt = '<<<'
    _template_outputprompt = '>>>'
    _template_char = '%s'
    _template_printablechar = '%s    %s'
    _template_esc = ' ESC %s%s    %s'
    _template_csi = ' CSI %s%s%s    %s'
    _template_cstr = ' ESC %s %s ST  %s'
    _template_ss2 = ' ESC N %s   %s'
    _template_ss3 = ' ESC O %s   %s'
    _template_invalid = '%s  %s\n'
    _template_mouse = '%s   CSI M %c %c %c %s\n'
    _template_highlight_mouse_initial = '%s   CSI T %c %c %s\n'
    _template_highlight_mouse = '%s   CSI T %c %c %c %c %c %c %s\n'
    _template_resize = '%s   resized: (row=%d, col=%d)\n'


if __name__ == '__main__':
    import doctest
    doctest.testmod()