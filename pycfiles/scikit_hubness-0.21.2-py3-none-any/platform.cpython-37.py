# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/user/feldbauer/PycharmProjects/hubness/skhubness/utils/platform.py
# Compiled at: 2019-10-29 11:02:04
# Size of source mod 2**32: 1588 bytes
import sys

def available_ann_algorithms_on_current_platform():
    """ Get approximate nearest neighbor algorithms available for the current platform/OS

    Currently, the algorithms are provided by the following libraries:

        * 'hnsw': nmslib
        * 'rptree': annoy
        * 'lsh': puffinn
        * 'falconn_lsh': falconn
        * 'onng': NGT

    Returns
    -------
    algorithms: Tuple[str]
        A tuple of available algorithms
    """
    if sys.platform == 'win32':
        algorithms = ('hnsw', 'rptree')
    else:
        if sys.platform == 'darwin':
            if 'pytest' in sys.modules:
                algorithms = ('falconn_lsh', 'hnsw', 'rptree', 'onng')
            else:
                algorithms = ('falconn_lsh', 'lsh', 'hnsw', 'rptree', 'onng')
        elif sys.platform == 'linux':
            algorithms = ('lsh', 'falconn_lsh', 'hnsw', 'rptree', 'onng')
        else:
            algorithms = ()
    return algorithms