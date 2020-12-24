# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/eplus/shell.py
# Compiled at: 2019-09-05 08:50:09
from .embed import embed
from .environment import init, setup_local, tear_down_local, setup_remote, init_lib
from .appcfg_update import simulate_legacy_update

def shell_local():
    init()
    setup_local()
    embed()
    tear_down_local()


def shell_remote():
    init()
    setup_remote()
    embed()


def appcfg_update():
    init()
    init_lib()
    simulate_legacy_update()


if __name__ == '__main__':
    shell_local()