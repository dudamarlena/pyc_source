# uncompyle6 version 3.6.7
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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