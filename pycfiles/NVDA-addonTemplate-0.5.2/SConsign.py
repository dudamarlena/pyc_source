# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\derek_2\Google Drive\nvda-addon-exploded\notepad++\scons-local-2.5.0\SCons\SConsign.py
# Compiled at: 2016-07-07 03:21:32
"""SCons.SConsign

Writing and reading information to the .sconsign file or files.

"""
__revision__ = 'src/engine/SCons/SConsign.py rel_2.5.0:3543:937e55cd78f7 2016/04/09 11:29:54 bdbaddog'
import SCons.compat, os, pickle, SCons.dblite, SCons.Warnings

def corrupt_dblite_warning(filename):
    SCons.Warnings.warn(SCons.Warnings.CorruptSConsignWarning, 'Ignoring corrupt .sconsign file: %s' % filename)


SCons.dblite.ignore_corrupt_dbfiles = 1
SCons.dblite.corruption_warning = corrupt_dblite_warning
sig_files = []
DataBase = {}
DB_Module = SCons.dblite
DB_Name = '.sconsign'
DB_sync_list = []

def Get_DataBase(dir):
    global DB_Module
    global DB_Name
    global DB_sync_list
    global DataBase
    top = dir.fs.Top
    if not os.path.isabs(DB_Name) and top.repositories:
        mode = 'c'
        for d in [top] + top.repositories:
            if dir.is_under(d):
                try:
                    return (
                     DataBase[d], mode)
                except KeyError:
                    path = d.entry_abspath(DB_Name)
                    try:
                        db = DataBase[d] = DB_Module.open(path, mode)
                    except (IOError, OSError):
                        pass
                    else:
                        if mode != 'r':
                            DB_sync_list.append(db)
                        return (
                         db, mode)

            mode = 'r'

    try:
        return (
         DataBase[top], 'c')
    except KeyError:
        db = DataBase[top] = DB_Module.open(DB_Name, 'c')
        DB_sync_list.append(db)
        return (db, 'c')
    except TypeError:
        print 'DataBase =', DataBase
        raise


def Reset():
    """Reset global state.  Used by unit tests that end up using
    SConsign multiple times to get a clean slate for each test."""
    global DB_sync_list
    global sig_files
    sig_files = []
    DB_sync_list = []


normcase = os.path.normcase

def write():
    for sig_file in sig_files:
        sig_file.write(sync=0)

    for db in DB_sync_list:
        try:
            syncmethod = db.sync
        except AttributeError:
            pass
        else:
            syncmethod()

        try:
            closemethod = db.close
        except AttributeError:
            pass
        else:
            closemethod()


class SConsignEntry(object):
    """
    Wrapper class for the generic entry in a .sconsign file.
    The Node subclass populates it with attributes as it pleases.

    XXX As coded below, we do expect a '.binfo' attribute to be added,
    but we'll probably generalize this in the next refactorings.
    """
    __slots__ = ('binfo', 'ninfo', '__weakref__')
    current_version_id = 2

    def __init__(self):
        pass

    def convert_to_sconsign(self):
        self.binfo.convert_to_sconsign()

    def convert_from_sconsign(self, dir, name):
        self.binfo.convert_from_sconsign(dir, name)

    def __getstate__(self):
        state = getattr(self, '__dict__', {}).copy()
        for obj in type(self).mro():
            for name in getattr(obj, '__slots__', ()):
                if hasattr(self, name):
                    state[name] = getattr(self, name)

        state['_version_id'] = self.current_version_id
        try:
            del state['__weakref__']
        except KeyError:
            pass

        return state

    def __setstate__(self, state):
        for key, value in state.items():
            if key not in ('_version_id', '__weakref__'):
                setattr(self, key, value)


class Base(object):
    """
    This is the controlling class for the signatures for the collection of
    entries associated with a specific directory.  The actual directory
    association will be maintained by a subclass that is specific to
    the underlying storage method.  This class provides a common set of
    methods for fetching and storing the individual bits of information
    that make up signature entry.
    """

    def __init__(self):
        self.entries = {}
        self.dirty = False
        self.to_be_merged = {}

    def get_entry(self, filename):
        """
        Fetch the specified entry attribute.
        """
        return self.entries[filename]

    def set_entry(self, filename, obj):
        """
        Set the entry.
        """
        self.entries[filename] = obj
        self.dirty = True

    def do_not_set_entry(self, filename, obj):
        pass

    def store_info(self, filename, node):
        entry = node.get_stored_info()
        entry.binfo.merge(node.get_binfo())
        self.to_be_merged[filename] = node
        self.dirty = True

    def do_not_store_info(self, filename, node):
        pass

    def merge(self):
        for key, node in self.to_be_merged.items():
            entry = node.get_stored_info()
            try:
                ninfo = entry.ninfo
            except AttributeError:
                pass
            else:
                ninfo.merge(node.get_ninfo())

            self.entries[key] = entry

        self.to_be_merged = {}


class DB(Base):
    """
    A Base subclass that reads and writes signature information
    from a global .sconsign.db* file--the actual file suffix is
    determined by the database module.
    """

    def __init__(self, dir):
        Base.__init__(self)
        self.dir = dir
        db, mode = Get_DataBase(dir)
        path = normcase(dir.get_tpath())
        try:
            rawentries = db[path]
        except KeyError:
            pass
        else:
            try:
                self.entries = pickle.loads(rawentries)
                if not isinstance(self.entries, dict):
                    self.entries = {}
                    raise TypeError
            except KeyboardInterrupt:
                raise
            except Exception as e:
                SCons.Warnings.warn(SCons.Warnings.CorruptSConsignWarning, 'Ignoring corrupt sconsign entry : %s (%s)\n' % (self.dir.get_tpath(), e))

        for key, entry in self.entries.items():
            entry.convert_from_sconsign(dir, key)

        if mode == 'r':
            self.set_entry = self.do_not_set_entry
            self.store_info = self.do_not_store_info
        sig_files.append(self)

    def write(self, sync=1):
        if not self.dirty:
            return
        self.merge()
        db, mode = Get_DataBase(self.dir)
        path = normcase(self.dir.get_internal_path())
        for key, entry in self.entries.items():
            entry.convert_to_sconsign()

        db[path] = pickle.dumps(self.entries, 1)
        if sync:
            try:
                syncmethod = db.sync
            except AttributeError:
                pass
            else:
                syncmethod()


class Dir(Base):

    def __init__(self, fp=None, dir=None):
        """
        fp - file pointer to read entries from
        """
        Base.__init__(self)
        if not fp:
            return
        self.entries = pickle.load(fp)
        if not isinstance(self.entries, dict):
            self.entries = {}
            raise TypeError
        if dir:
            for key, entry in self.entries.items():
                entry.convert_from_sconsign(dir, key)


class DirFile(Dir):
    """
    Encapsulates reading and writing a per-directory .sconsign file.
    """

    def __init__(self, dir):
        """
        dir - the directory for the file
        """
        self.dir = dir
        self.sconsign = os.path.join(dir.get_internal_path(), '.sconsign')
        try:
            fp = open(self.sconsign, 'rb')
        except IOError:
            fp = None

        try:
            Dir.__init__(self, fp, dir)
        except KeyboardInterrupt:
            raise
        except:
            SCons.Warnings.warn(SCons.Warnings.CorruptSConsignWarning, 'Ignoring corrupt .sconsign file: %s' % self.sconsign)

        sig_files.append(self)
        return

    def write(self, sync=1):
        """
        Write the .sconsign file to disk.

        Try to write to a temporary file first, and rename it if we
        succeed.  If we can't write to the temporary file, it's
        probably because the directory isn't writable (and if so,
        how did we build anything in this directory, anyway?), so
        try to write directly to the .sconsign file as a backup.
        If we can't rename, try to copy the temporary contents back
        to the .sconsign file.  Either way, always try to remove
        the temporary file at the end.
        """
        if not self.dirty:
            return
        self.merge()
        temp = os.path.join(self.dir.get_internal_path(), '.scons%d' % os.getpid())
        try:
            file = open(temp, 'wb')
            fname = temp
        except IOError:
            try:
                file = open(self.sconsign, 'wb')
                fname = self.sconsign
            except IOError:
                return

        for key, entry in self.entries.items():
            entry.convert_to_sconsign()

        pickle.dump(self.entries, file, 1)
        file.close()
        if fname != self.sconsign:
            try:
                mode = os.stat(self.sconsign)[0]
                os.chmod(self.sconsign, 438)
                os.unlink(self.sconsign)
            except (IOError, OSError):
                pass

            try:
                os.rename(fname, self.sconsign)
            except OSError:
                open(self.sconsign, 'wb').write(open(fname, 'rb').read())
                os.chmod(self.sconsign, mode)

        try:
            os.unlink(temp)
        except (IOError, OSError):
            pass


ForDirectory = DB

def File(name, dbm_module=None):
    """
    Arrange for all signatures to be stored in a global .sconsign.db*
    file.
    """
    global DB_Module
    global DB_Name
    global ForDirectory
    if name is None:
        ForDirectory = DirFile
        DB_Module = None
    else:
        ForDirectory = DB
        DB_Name = name
        if dbm_module is not None:
            DB_Module = dbm_module
    return