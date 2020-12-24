# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/kalimaha/Development/git-repositories/Geobricks/pgeo/pgeo/db/postgresql/postgis_utils/util.py
# Compiled at: 2014-07-31 04:42:27
from os.path import join, isdir, islink
from os import listdir

def read_until(stream, separator, buffer_size=32768):
    datalist = []
    done = False
    while not done:
        chunk = stream.read(buffer_size)
        done = len(chunk) == 0
        while separator in chunk:
            i = chunk.find(separator)
            datalist.append(chunk[:i + 1])
            yield ('').join(datalist)
            datalist = []
            if i < len(chunk) - 1:
                chunk = chunk[i + 1:len(chunk)]
            else:
                chunk = ''

        if chunk != '':
            datalist.append(chunk)

    if len(datalist) > 0:
        yield ('').join(datalist)


def groupsgen(seq, size):
    it = iter(seq)
    while True:
        values = ()
        for n in xrange(size):
            try:
                values += (it.next(),)
            except StopIteration:
                yield values
                return

        yield values


from os.path import join, isdir, islink
from os import listdir

def walk2(top, topdown=True, onerror=None, deeplevel=0):
    """Modified directory tree generator.

    For each directory in the directory tree rooted at top (including top
    itself, but excluding '.' and '..'), yields a 4-tuple

        dirpath, dirnames, filenames, deeplevel

    dirpath is a string, the path to the directory.  dirnames is a list of
    the names of the subdirectories in dirpath (excluding '.' and '..').
    filenames is a list of the names of the non-directory files in dirpath.
    Note that the names in the lists are just names, with no path components.
    To get a full path (which begins with top) to a file or directory in
    dirpath, do os.path.join(dirpath, name).

    ----------------------------------------------------------------------
    + deeplevel is 0-based deep level from top directory
    ----------------------------------------------------------------------
    ...

    """
    try:
        names = listdir(top)
    except Exception as err:
        if onerror is not None:
            onerror(err)
        return

    dirs, nondirs = [], []
    for name in names:
        if isdir(join(top, name)):
            dirs.append(name)
        else:
            nondirs.append(name)

    if topdown:
        yield (
         top, dirs, nondirs, deeplevel)
    for name in dirs:
        path = join(top, name)
        if not islink(path):
            for x in walk2(path, topdown, onerror, deeplevel + 1):
                yield x

    if not topdown:
        yield (
         top, dirs, nondirs, deeplevel)
    return