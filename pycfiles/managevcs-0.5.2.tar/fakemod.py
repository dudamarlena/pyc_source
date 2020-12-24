# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/dzhiltsov/Development/vcslib/vcs/utils/fakemod.py
# Compiled at: 2015-05-15 06:06:58
import imp

def create_module(name, path):
    """
    Returns module created *on the fly*. Returned module would have name same
    as given ``name`` and would contain code read from file at the given
    ``path`` (it may also be a zip or package containing *__main__* module).
    """
    module = imp.new_module(name)
    module.__file__ = path
    execfile(path, module.__dict__)
    return module