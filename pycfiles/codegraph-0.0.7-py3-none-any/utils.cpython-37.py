# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/thomas/software/codegra.fs/env/lib/python3.7/site-packages/codegra_fs/utils.py
# Compiled at: 2019-02-14 08:40:52
# Size of source mod 2**32: 2560 bytes
import sys, typing as t
from collections import defaultdict
import requests, codegra_fs
T = t.TypeVar('T')
Y = t.TypeVar('Y')

def _get_fuse_version_info() -> t.Tuple[(int, int)]:
    if not sys.platform.startswith('win32'):
        return (-1, -1)
    import winfspy, cffi
    ffi = cffi.FFI()
    res = ffi.new('unsigned int *')
    if winfspy.lib.FspVersion(res) != 0:
        return (0, 0)
    return (res[0] >> 16 & 65535, res[0] & 65535)


def get_fuse_install_message() -> t.Optional[t.Tuple[(str, t.Optional[str])]]:
    try:
        import fuse
    except:
        pass
    else:
        if sys.platform.startswith('win32'):
            winfsp_version = _get_fuse_version_info()
            if winfsp_version < (1, 4):
                return ('You need at least WinFsp version 1.4 (currently in beta).',
                        'https://github.com/billziss-gh/winfsp/releases')
        return
        if sys.platform.startswith('darwin'):
            return ('Fuse is not installed, this can be done by installing OSXFuse',
                    'https://osxfuse.github.io/')
        if sys.platform.startswith('linux'):
            return ('Fuse is not installed, this can be done by doing `sudo apt install fuse` on ubuntu',
                    None)
        if sys.platform.startswith('win32'):
            return ('WinFsp not installed, please download version 1.4 (currently in beta) or later.',
                    'https://github.com/billziss-gh/winfsp/releases')
        return ('Unsupported platform, only GNU/Linux, Mac and Windows are supported',
                None)


def newer_version_available() -> bool:
    req = requests.get('https://codegra.de/.cgfs.version', timeout=2)
    return req.status_code < 300 and tuple((int(p) for p in req.content.decode('utf8').strip().split('.'))) > codegra_fs.__version__


def find_all_dups(seq: t.Sequence[T], key: t.Callable[([T], Y)]) -> t.List[t.Tuple[(T, ...)]]:
    dct = defaultdict(list)
    for el in seq:
        dct[key(el)].append(el)

    return [tuple(v) for v in dct.values() if len(v) > 1]


def name_of_user(user: t.Dict[(str, t.Any)]) -> str:
    if user.get('group') is not None:
        return 'Group "{}"'.format(user['group']['name'])
    return user['name']


def format_datestring(datestring: str) -> str:
    return datestring.replace('T', ' ').split('.')[0]