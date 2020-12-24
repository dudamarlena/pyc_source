# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/tal/Dropbox/Code/neurosynth/neurosynth/utils.py
# Compiled at: 2015-01-24 15:30:45
# Size of source mod 2**32: 599 bytes
import warnings

def deprecated(*args):
    """ Deprecation warning decorator. Takes optional deprecation message,
    otherwise will use a generic warning. """

    def wrap(func):

        def wrapped_func(*args, **kwargs):
            warnings.warn(msg, category=DeprecationWarning)
            return func(*args, **kwargs)

        return wrapped_func

    if len(args) == 1 and callable(args[0]):
        msg = "Function '%s' will be deprecated in future versions of Neurosynth." % args[0].__name__
        return wrap(args[0])
    else:
        msg = args[0]
        return wrap