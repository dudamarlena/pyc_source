# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/sskk/title.py
# Compiled at: 2014-03-11 11:34:49
_enabled = True
_dirty = True
_mode = '@'
_message = ''
_original = ''

def get():
    """
    >>> get()
    u'   [@] '
    """
    global _enabled
    global _message
    global _mode
    global _original
    if _enabled:
        if _mode:
            return '%s   [%s] %s' % (_original, _mode, _message)
        return '%s   %s' % (_original, _message)


def getenabled():
    """
    >>> setenabled(True)
    >>> getenabled()
    True
    """
    return _enabled


def setenabled(value):
    """
    >>> getenabled()
    True
    >>> setenabled(False)
    >>> getenabled()
    False
    >>> setenabled(True)
    >>> getenabled()
    True
    """
    global _dirty
    global _enabled
    _enabled = value
    _dirty = True


def setmode(value):
    global _dirty
    global _mode
    if value != _mode:
        _mode = value
        _dirty = True


def setmessage(value):
    global _dirty
    global _message
    if value != _message:
        _message = value
        _dirty = True


def setoriginal(value):
    global _original
    _original = value


def draw(output):
    global _dirty
    if _enabled and _dirty:
        output.write('\x1b]2;%s\x1b\\' % get())
        _dirty = False


def test():
    import doctest
    doctest.testmod()


if __name__ == '__main__':
    test()