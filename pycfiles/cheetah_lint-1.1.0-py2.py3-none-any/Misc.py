# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/lib.macosx-10.13-x86_64-2.7/Cheetah/Utils/Misc.py
# Compiled at: 2019-09-22 10:12:27
__doc__ = '\n    Miscellaneous functions/objects used by Cheetah but also useful standalone.\n'
import os, sys

def die(reason):
    sys.stderr.write(reason + '\n')
    sys.exit(1)


def useOrRaise(thing, errmsg=''):
    """Raise 'thing' if it's a subclass of Exception.  Otherwise return it.

    Called by: Cheetah.Servlet.cgiImport()
    """
    if isinstance(thing, type) and issubclass(thing, Exception):
        raise thing(errmsg)
    return thing


def checkKeywords(dic, legalKeywords, what='argument'):
    """Verify no illegal keyword arguments were passed to a function.

    in : dic, dictionary (**kw in the calling routine).
         legalKeywords, list of strings, the keywords that are allowed.
         what, string, suffix for error message (see function source).
    out: None.
    exc: TypeError if 'dic' contains a key not in 'legalKeywords'.
    called by: Cheetah.Template.__init__()
    """
    for k in dic:
        if k not in legalKeywords:
            raise TypeError("'%s' is not a valid %s" % (k, what))


def removeFromList(list_, *elements):
    """Save as list_.remove(each element) but don't raise an error if
       element is missing.  Modifies 'list_' in place!  Returns None.
    """
    for elm in elements:
        try:
            list_.remove(elm)
        except ValueError:
            pass


def mkdirsWithPyInitFiles(path):
    """Same as os.makedirs (mkdir 'path' and all missing parent directories)
       but also puts a Python '__init__.py' file in every directory it
       creates.  Does nothing (without creating an '__init__.py' file) if the
       directory already exists.
    """
    dir, fil = os.path.split(path)
    if dir and not os.path.exists(dir):
        mkdirsWithPyInitFiles(dir)
    if not os.path.exists(path):
        os.mkdir(path)
        init = os.path.join(path, '__init__.py')
        f = open(init, 'w')
        f.close()