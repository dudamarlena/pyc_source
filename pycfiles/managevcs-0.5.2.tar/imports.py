# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/dzhiltsov/Development/vcslib/managevcs/utils/imports.py
# Compiled at: 2015-06-08 06:25:02
from managevcs.exceptions import VCSError

def import_class(class_path):
    """
    Returns class from the given path.

    For example, in order to get class located at
    ``managevcs.backends.hg.MercurialRepository``:

        try:
            hgrepo = import_class('managevcs.backends.hg.MercurialRepository')
        except VCSError:
            # hadle error
    """
    splitted = class_path.split('.')
    mod_path = ('.').join(splitted[:-1])
    class_name = splitted[(-1)]
    try:
        class_mod = __import__(mod_path, {}, {}, [class_name])
    except ImportError as err:
        msg = 'There was problem while trying to import backend class. Original error was:\n%s' % err
        raise VCSError(msg)

    cls = getattr(class_mod, class_name)
    return cls