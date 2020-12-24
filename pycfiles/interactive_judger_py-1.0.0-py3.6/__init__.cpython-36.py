# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/interactive_judger/__init__.py
# Compiled at: 2018-08-03 00:04:51
# Size of source mod 2**32: 274 bytes


def start_judge():
    from . import judge
    return judge.main()


def remove_config():
    from . import conf_generator
    import sys
    return conf_generator.remove_config(sys.argv)


def add_config():
    from . import conf_generator
    return conf_generator.main()