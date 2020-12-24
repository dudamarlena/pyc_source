# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\derek_2\Google Drive\nvda-addon-exploded\notepad++\scons-local-2.5.0\SCons\dblite.py
# Compiled at: 2016-07-07 03:21:32
import SCons.compat, os, pickle, shutil, time
keep_all_files = 0
ignore_corrupt_dbfiles = 0

def corruption_warning(filename):
    print 'Warning: Discarding corrupt database:', filename


try:
    unicode
except NameError:

    def is_string(s):
        return isinstance(s, str)


else:

    def is_string(s):
        return type(s) in (str, unicode)


try:
    unicode('a')
except NameError:

    def unicode(s):
        return s


dblite_suffix = '.dblite'
tmp_suffix = '.tmp'

class dblite(object):
    _open = open
    _pickle_dump = staticmethod(pickle.dump)
    _os_chmod = os.chmod
    try:
        _os_chown = os.chown
    except AttributeError:
        _os_chown = None

    _os_rename = os.rename
    _os_unlink = os.unlink
    _shutil_copyfile = shutil.copyfile
    _time_time = time.time

    def __init__(self, file_base_name, flag, mode):
        global ignore_corrupt_dbfiles
        assert flag in (None, 'r', 'w', 'c', 'n')
        if flag is None:
            flag = 'r'
        base, ext = os.path.splitext(file_base_name)
        if ext == dblite_suffix:
            self._file_name = file_base_name
            self._tmp_name = base + tmp_suffix
        else:
            self._file_name = file_base_name + dblite_suffix
            self._tmp_name = file_base_name + tmp_suffix
        self._flag = flag
        self._mode = mode
        self._dict = {}
        self._needs_sync = 0
        if self._os_chown is not None and (os.geteuid() == 0 or os.getuid() == 0):
            try:
                statinfo = os.stat(self._file_name)
                self._chown_to = statinfo.st_uid
                self._chgrp_to = statinfo.st_gid
            except OSError as e:
                self._chown_to = int(os.environ.get('SUDO_UID', -1))
                self._chgrp_to = int(os.environ.get('SUDO_GID', -1))

        else:
            self._chown_to = -1
            self._chgrp_to = -1
        if self._flag == 'n':
            self._open(self._file_name, 'wb', self._mode)
        else:
            try:
                f = self._open(self._file_name, 'rb')
            except IOError as e:
                if self._flag != 'c':
                    raise e
                self._open(self._file_name, 'wb', self._mode)

            p = f.read()
            if len(p) > 0:
                try:
                    self._dict = pickle.loads(p)
                except (pickle.UnpicklingError, EOFError, KeyError):
                    if ignore_corrupt_dbfiles == 0:
                        raise
                    if ignore_corrupt_dbfiles == 1:
                        corruption_warning(self._file_name)

        return

    def close(self):
        if self._needs_sync:
            self.sync()

    def __del__(self):
        self.close()

    def sync(self):
        self._check_writable()
        f = self._open(self._tmp_name, 'wb', self._mode)
        self._pickle_dump(self._dict, f, 1)
        f.close()
        try:
            self._os_chmod(self._file_name, 511)
        except OSError:
            pass

        self._os_unlink(self._file_name)
        self._os_rename(self._tmp_name, self._file_name)
        if self._os_chown is not None and self._chown_to > 0:
            try:
                self._os_chown(self._file_name, self._chown_to, self._chgrp_to)
            except OSError:
                pass

        self._needs_sync = 0
        if keep_all_files:
            self._shutil_copyfile(self._file_name, self._file_name + '_' + str(int(self._time_time())))
        return

    def _check_writable(self):
        if self._flag == 'r':
            raise IOError('Read-only database: %s' % self._file_name)

    def __getitem__(self, key):
        return self._dict[key]

    def __setitem__(self, key, value):
        self._check_writable()
        if not is_string(key):
            raise TypeError("key `%s' must be a string but is %s" % (key, type(key)))
        if not is_string(value):
            raise TypeError("value `%s' must be a string but is %s" % (value, type(value)))
        self._dict[key] = value
        self._needs_sync = 1

    def keys(self):
        return list(self._dict.keys())

    def has_key(self, key):
        return key in self._dict

    def __contains__(self, key):
        return key in self._dict

    def iterkeys(self):
        return self._dict.iterkeys()

    __iter__ = iterkeys

    def __len__(self):
        return len(self._dict)


def open(file, flag=None, mode=438):
    return dblite(file, flag, mode)


def _exercise():
    global ignore_corrupt_dbfiles
    db = open('tmp', 'n')
    assert len(db) == 0
    db['foo'] = 'bar'
    assert db['foo'] == 'bar'
    db[unicode('ufoo')] = unicode('ubar')
    assert db[unicode('ufoo')] == unicode('ubar')
    db.sync()
    db = open('tmp', 'c')
    assert len(db) == 2, len(db)
    assert db['foo'] == 'bar'
    db['bar'] = 'foo'
    assert db['bar'] == 'foo'
    db[unicode('ubar')] = unicode('ufoo')
    assert db[unicode('ubar')] == unicode('ufoo')
    db.sync()
    db = open('tmp', 'r')
    assert len(db) == 4, len(db)
    assert db['foo'] == 'bar'
    assert db['bar'] == 'foo'
    assert db[unicode('ufoo')] == unicode('ubar')
    assert db[unicode('ubar')] == unicode('ufoo')
    try:
        db.sync()
    except IOError as e:
        assert str(e) == 'Read-only database: tmp.dblite'
    else:
        raise RuntimeError('IOError expected.')

    db = open('tmp', 'w')
    assert len(db) == 4
    db['ping'] = 'pong'
    db.sync()
    try:
        db[(1, 2)] = 'tuple'
    except TypeError as e:
        assert str(e) == "key `(1, 2)' must be a string but is <type 'tuple'>", str(e)
    else:
        raise RuntimeError('TypeError exception expected')

    try:
        db['list'] = [
         1, 2]
    except TypeError as e:
        assert str(e) == "value `[1, 2]' must be a string but is <type 'list'>", str(e)
    else:
        raise RuntimeError('TypeError exception expected')

    db = open('tmp', 'r')
    assert len(db) == 5
    db = open('tmp', 'n')
    assert len(db) == 0
    dblite._open('tmp.dblite', 'w')
    db = open('tmp', 'r')
    dblite._open('tmp.dblite', 'w').write('x')
    try:
        db = open('tmp', 'r')
    except pickle.UnpicklingError:
        pass
    else:
        raise RuntimeError('pickle exception expected.')

    ignore_corrupt_dbfiles = 2
    db = open('tmp', 'r')
    assert len(db) == 0
    os.unlink('tmp.dblite')
    try:
        db = open('tmp', 'w')
    except IOError as e:
        assert str(e) == "[Errno 2] No such file or directory: 'tmp.dblite'", str(e)
    else:
        raise RuntimeError('IOError expected.')

    print 'OK'


if __name__ == '__main__':
    _exercise()