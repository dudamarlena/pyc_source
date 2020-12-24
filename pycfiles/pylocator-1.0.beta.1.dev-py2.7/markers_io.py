# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/pylocator/misc/markers_io.py
# Compiled at: 2012-04-03 18:28:03


def load_markers(fh):
    if type(fh) == str:
        fh = open(fh, 'r')
    rv = []
    for line in fh.readlines():
        rv.append([])
        parts = line[:-1].split(',')
        rv[(-1)].append(parts[0])
        for i in range(1, len(parts)):
            rv[(-1)].append(float(parts[i]))

    return rv


def load_markers_to_dict(fh):
    if type(fh) == str:
        fh = open(fh, 'r')
    marker_list = []
    for line in fh.readlines():
        marker_list.append([])
        parts = line[:-1].split(',')
        marker_list[(-1)].append(parts[0])
        for i in range(1, len(parts)):
            marker_list[(-1)].append(float(parts[i]))

    return dict([ (marker[0], marker[1:]) for marker in marker_list ])


if __name__ == '__main__':
    fn = '/media/Extern/public/Experimente/AudioStroop/kombinierte_analyse/elec_pos/443.txt'
    print load_markers(fn)
    fh = open(fn, 'r')
    print load_markers(fh)