# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/nwlongb/dlcode/dgsamples/dgsamples/_registerdata.py
# Compiled at: 2018-07-06 20:11:47
# Size of source mod 2**32: 2403 bytes
import os, tinytools as tt, inspect

def _runit():
    pkg_dir = os.path.dirname(os.path.abspath(inspect.stack()[0][1]))
    pkg_dirs = tt.files.search(pkg_dir, '*', ret_files=False, ret_dirs=True)
    pkg_samples = tt.bunch.OrderedBunch()
    for d in pkg_dirs:
        name = os.path.basename(d)
        pkg_samples[name] = tt.bunch.OrderedBunch()
        if os.path.isdir(d):
            pkg_samples[name]['path'] = d
        tmpnote = tt.files.search(d, 'notes.txt', case_sensitive=False)
        if tmpnote:
            with open(tmpnote[0], 'r') as (f):
                pkg_samples[name]['notes'] = f.read()
        tmptil = tt.files.search(d, '*.TIL', case_sensitive=False, depth=3)
        tmptif = tt.files.search(d, ['*.TIF', '*.TIFF'], case_sensitive=False,
          depth=3)
        tmpvec = tt.files.search(d, ['*.SHP', '*.json', '*.geojson'], case_sensitive=False,
          depth=3)
        if tmptil:
            pkg_samples[name]['files'] = tmptil
        else:
            if tmptif:
                pkg_samples[name]['files'] = tmptif
            else:
                if tmpvec:
                    pkg_samples[name]['files'] = tmpvec
                try:
                    name_map = tt.pvl.read_from_pvl(os.path.join(d, 'filename_map.PVL'))
                except:
                    name_map = {}

        for k, v in list(name_map.items()):
            v = tt.files.search(d, ('*' + v), depth=3)
            if v[0] in pkg_samples[name]['files']:
                pkg_samples[name][k] = v[0]

    return pkg_samples