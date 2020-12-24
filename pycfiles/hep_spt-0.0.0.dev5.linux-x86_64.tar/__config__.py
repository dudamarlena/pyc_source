# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/hep_spt/__config__.py
# Compiled at: 2019-11-15 13:21:57
__all__ = [
 'get_info', 'show']
import os, sys
extra_dll_dir = os.path.join(os.path.dirname(__file__), '.libs')
if sys.platform == 'win32' and os.path.isdir(extra_dll_dir):
    os.environ.setdefault('PATH', '')
    os.environ['PATH'] += os.pathsep + extra_dll_dir

def get_info(name):
    g = globals()
    return g.get(name, g.get(name + '_info', {}))


def show():
    for name, info_dict in globals().items():
        if name[0] == '_' or type(info_dict) is not type({}):
            continue
        print name + ':'
        if not info_dict:
            print '  NOT AVAILABLE'
        for k, v in info_dict.items():
            v = str(v)
            if k == 'sources' and len(v) > 200:
                v = v[:60] + ' ...\n... ' + v[-60:]
            print '    %s = %s' % (k, v)