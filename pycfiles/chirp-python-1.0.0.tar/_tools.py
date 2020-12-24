# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\chirp\common\_tools.py
# Compiled at: 2013-12-11 23:17:46
__doc__ = '\nProgramming tools\n\nconsumer:       a decorator for consumer generators\nalnumkey:       yield the alphabetical and numeric components of a string\n\nCopyright (C) 2012 Dan Meliza <dmeliza@gmail.com>\nCreated 2012-01-31\n'

def consumer(func):

    def wrapper(*args, **kw):
        gen = func(*args, **kw)
        gen.next()
        return gen

    wrapper.__name__ = func.__name__
    wrapper.__dict__ = func.__dict__
    wrapper.__doc__ = func.__doc__
    return wrapper


def alnumkey(s):
    """
    Turn a string into component string and number chunks.
    "z23a" -> ("z", 23, "a")

    Use as a key in sorting filenames naturally
    """
    import re
    convert = lambda text: int(text) if text.isdigit() else text
    return [ convert(c) for c in re.split('([0-9]+)', s) ]