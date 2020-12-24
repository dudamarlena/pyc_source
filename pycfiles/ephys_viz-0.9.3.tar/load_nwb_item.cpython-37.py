# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/magland/src/ephys-viz/generated/ephys_viz/ephys_viz/widgets/pycommon/load_nwb_item.py
# Compiled at: 2019-11-15 11:26:28
# Size of source mod 2**32: 905 bytes
import h5py, numpy as np

def load_nwb_item(file, *, nwb_path, verbose=False):
    opts = dict(verbose=verbose)
    opts['file'] = file
    return _load_nwb_item(file, opts=opts, nwb_path=nwb_path)


def _load_nwb_item(f, *, opts, nwb_path):
    if opts.get('verbose', None):
        print('_load_nwb_item', nwb_path)
    else:
        list0 = [a for a in nwb_path.split('/') if a]
        if len(list0) == 0:
            raise Exception('Problem in _load_nwb_item: path is too short')
        name0 = list0[0]
        if name0 not in f.keys():
            raise Exception('Problem in _load_nwb_item: Missing key {}'.format(name0))
        item = f[name0]
        if len(list0) == 1:
            return item
        assert isinstance(item, h5py.Group), 'Problem in _load_nwb_item: Not a group {}'.format(name0)
    return _load_nwb_item(item, opts=opts, nwb_path=('/' + '/'.join(list0[1:])))