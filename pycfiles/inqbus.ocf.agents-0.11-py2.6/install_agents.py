# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/inqbus/ocf/agents/install_agents.py
# Compiled at: 2011-11-29 09:41:39
import os, pkg_resources

def install():
    group = 'console_scripts'
    import pdb
    pdb.set_trace()
    for entrypoint in pkg_resources.iter_entry_points(group=group):
        plugin = entrypoint.load()


def main():
    """
    Entry point for the python console scripts
    """
    install()


if __name__ == '__main__':
    main()