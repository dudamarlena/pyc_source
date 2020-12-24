# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/pydirduplicatefinder/raw_input_defaulted.py
# Compiled at: 2009-06-28 06:50:28
try:
    import readline
    READLINE_AVAILABLE = True
except ImportError:
    READLINE_AVAILABLE = False

def _input_default(prompt, default):

    def startup_hook():
        readline.insert_text(default)

    readline.set_startup_hook(startup_hook)
    try:
        return raw_input(prompt)
    finally:
        readline.set_startup_hook(None)

    return


def raw_input_defaulted(msg, default=''):
    """A raw_input implementation with default value already specified
    Is based on readline module, avaiable only on UNIX systems; if the readline if not found
    no default is given.
    """
    if not default or not READLINE_AVAILABLE:
        return raw_input(msg)
    return _input_default(msg, default=default)