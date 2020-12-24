# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/funkload/DemoInstaller.py
# Compiled at: 2015-05-06 05:03:08
"""Extract the demo from the funkload egg into the current path."""
import os
from shutil import copytree
from pkg_resources import resource_filename, cleanup_resources

def main():
    """main."""
    demo_path = 'funkload-demo'
    print 'Extract FunkLoad examples into ./%s : ... ' % demo_path,
    cache_path = resource_filename('funkload', 'demo')
    demo_path = os.path.join(os.path.abspath(os.path.curdir), demo_path)
    copytree(cache_path, demo_path)
    cleanup_resources()
    print 'done.'


if __name__ == '__main__':
    main()