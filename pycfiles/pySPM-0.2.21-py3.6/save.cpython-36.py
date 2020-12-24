# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\pySPM\utils\save.py
# Compiled at: 2019-05-21 08:54:40
# Size of source mod 2**32: 6395 bytes
import pickle, zipfile, os, shutil, tempfile
data_path = '.'

def set_datapath(path):
    global data_path
    data_path = path


def findPKZ(filename):
    if os.path.splitext(filename)[1] == '':
        filename += '.pkz'
    p2 = os.path.join(data_path, filename)
    if os.path.exists(p2):
        return p2
    if os.path.exists(filename):
        return filename
    else:
        if not os.path.exists(filename):
            raise IOError('File "{}" not found'.format(filename))
        return filename


def inarxiv(filename, obj):
    if os.path.splitext(filename)[1] == '':
        filename += '.pkz'
    filename = os.path.join(data_path, filename)
    out = zipfile.ZipFile(filename, 'a', zipfile.ZIP_DEFLATED)
    file_list = out.namelist()
    return obj in file_list


def save(filename, *objs, **obj):
    """
    save python objects to file
    """
    if os.path.splitext(filename)[1] == '':
        filename += '.pkz'
    else:
        filename = os.path.join(data_path, filename)
        out = zipfile.ZipFile(filename, 'a', zipfile.ZIP_DEFLATED)
        file_list = out.namelist()
        update = []
        for i, o in enumerate(objs):
            obj[i] = o

        for k in obj:
            if k in file_list:
                update.append(k)

        if len(update) == 0:
            for k in obj:
                out.writestr(k, pickle.dumps(obj[k], pickle.HIGHEST_PROTOCOL))

        else:
            out.close()
            ft, temp = tempfile.mkstemp()
            shutil.copy(filename, temp)
            out = zipfile.ZipFile(filename, 'w', zipfile.ZIP_DEFLATED)
            old = zipfile.ZipFile(temp, 'r')
            for k in [x for x in file_list if x not in update]:
                out.writestr(k, old.read(k))

            old.close()
            os.fdopen(ft).close()
            os.remove(temp)
            for k in obj:
                out.writestr(k, pickle.dumps(obj[k], pickle.HIGHEST_PROTOCOL))

    out.close()


def load(filename, *keys):
    """
    load python objects from saved pkz files
    """
    filename = findPKZ(filename)
    if len(keys) == 0:
        keys = [
         '0']
    else:
        if len(keys) == 1:
            if ',' in keys[0]:
                keys = keys[0].split(',')
    f = zipfile.ZipFile(filename, 'r')
    res = []
    for key in keys:
        if type(key) is int:
            key = str(key)
        try:
            raw = f.read(key)
        except Exception as e:
            raise KeyError('There is no key {} found in the data {}'.format(key, filename))

        try:
            res.append(pickle.loads(raw))
        except:
            raise Exception('Cannot pickle recorded data for key {}'.format(key))

    f.close()
    if len(keys) == 1:
        return res[0]
    else:
        return res


class loader:
    __doc__ = '\n    This class act as a dictionary and read default value for compressed pkz files.\n    Values can be set to new values without changing the content of the saved data.\n    Only retrieved data are kept in memory and not all the data.\n    '

    def __init__(self, filename):
        self.filename = findPKZ(filename)
        self.local = {}

    def __iter__(self):
        f = zipfile.ZipFile(self.filename, 'r')
        self.keys = set(f.namelist() + list(self.local.keys()))
        f.close()
        return self

    def __next__(self):
        if len(self.keys) == 0:
            raise StopIteration()
        else:
            return self.keys.pop()

    def __getitem__(self, key):
        if key not in self.local:
            f = zipfile.ZipFile(self.filename, 'r')
            self.local[key] = pickle.loads(f.read(key))
            f.close()
        return self.local[key]

    def __setitem__(self, key, value):
        self.local[key] = value

    def __delitem__(self, key):
        delf.local.delitem(key)


class BidirData:
    __doc__ = '\n    This class act as a dictionary and read default value for compressed pkz files.\n    Values can be set to new values without changing the content of the saved data.\n    Only retrieved data are kept in memory and not all the data.\n    '

    def __init__(self, filename):
        try:
            self.filename = findPKZ(filename)
        except IOError:
            if os.path.splitext(filename)[1] == '':
                filename += '.pkz'
            self.filename = os.path.join(data_path, filename)
            out = zipfile.ZipFile(filename, 'a', zipfile.ZIP_DEFLATED)
            out.close()

        self.local = {}

    def __iter__(self):
        f = zipfile.ZipFile(self.filename, 'r')
        self.keys = set(f.namelist() + list(self.local.keys()))
        f.close()
        return self

    def __next__(self):
        if len(self.keys) == 0:
            raise StopIteration()
        else:
            return self.keys.pop()

    def __getitem__(self, key):
        if key not in self.local:
            f = zipfile.ZipFile(self.filename, 'r')
            self.local[key] = pickle.loads(f.read(key))
            f.close()
        return self.local[key]

    def __setitem__(self, key, value):
        self.local[key] = value
        save((self.filename), **{key: value})

    def __delitem__(self, key):
        delf.local.delitem(key)

    def keys(self):
        f = zipfile.ZipFile(self.filename, 'r')
        keys = f.filelist
        f.close()
        return [x.filename for x in keys]