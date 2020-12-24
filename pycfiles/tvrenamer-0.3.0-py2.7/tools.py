# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.cygwin-2.2.1-i686/egg/tvrenamer/common/tools.py
# Compiled at: 2015-11-08 18:30:19
import copy, itertools

def make_opt_list(opts, group):
    """Generate a list of tuple containing group, options

    :param opts: option lists associated with a group
    :type opts: list
    :param group: name of an option group
    :type group: str
    :return: a list of (group_name, opts) tuples
    :rtype: list
    """
    _opts = [
     (
      group, list(itertools.chain(*opts)))]
    return [ (g, copy.deepcopy(o)) for g, o in _opts ]