# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Library/Frameworks/Python.framework/Versions/3.7/lib/python3.7/site-packages/pyrep/Repository.py
# Compiled at: 2020-01-14 20:23:32
# Size of source mod 2**32: 140032 bytes
__doc__ = '\nUsage:\n======\n\n.. code-block:: python\n\n    from __future__ import print_function\n    import os\n    import warnings\n    from pprint import pprint\n\n    # numpy imports\n    import numpy as np\n\n    # import Repository\n    from pyrep import Repository\n\n    # initialize Repository instance\n    REP=Repository()\n\n    # create a path pointing to user home\n    PATH = os.path.join(os.path.expanduser("~"), \'pyrepTest_canBeDeleted\')\n\n    # check if directory exist\n    if REP.is_repository(PATH):\n        REP.remove_repository(path=PATH, removeEmptyDirs=True)\n\n\n    # print repository path\n    print("repository path --> %s"%str(REP.path))\n\n    # create repository in path\n    print("\\n\\nIs path \'%s\' a repository --> %s"%(PATH, str(REP.is_repository(PATH))))\n    success,message = REP.create_repository(PATH)\n    assert success, message\n    print(\'\\nRepository path --> %s\'%str(REP.path))\n\n    # add directories\n    success,message = REP.add_directory("folder1/folder2/folder3")\n    if not success:\n        print(message)\n\n    success,message = REP.add_directory("folder1/archive1/archive2/archive3/archive3")\n    if not success:\n        print(message)\n\n    success,message = REP.add_directory("directory1/directory2")\n    if not success:\n        print(message)\n\n    # dump files\n    value = "This is a string data to pickle and store in the repository"\n    success,message = REP.dump_file(value, relativePath=\'pickled\', dump=None, pull=None, replace=True)\n    if not success:\n        print(message)\n\n    value = np.random.random(3)\n    dump  = "import numpy as np; dump=lambda path,value:np.savetxt(fname=path, X=value, fmt=\'%.6e\')"\n    pull  = "import numpy as np; pull=lambda path:np.loadtxt(fname=path)"\n\n    success,message = REP.dump(value, relativePath=\'text.dat\', dump=dump, pull=pull, replace=True)\n    if not success:\n        print(message)\n\n    success,message = REP.dump(value, relativePath="folder1/folder2/folder3/folder3Pickled.pkl", replace=True)\n    if not success:\n        print(message)\n\n    success,message = REP.dump(value, relativePath="folder1/archive1/archive1Pickled1", replace=True)\n    if not success:\n        print(message)\n\n    success,message = REP.dump(value, relativePath="folder1/archive1/archive1Pickled2", replace=True)\n    if not success:\n        print(message)\n\n    success,message = REP.dump(value, relativePath="folder1/archive1/archive2/archive2Pickled1", replace=True)\n    if not success:\n        print(message)\n\n    # pull data\n    data = REP.pull(relativePath=\'text.dat\')\n    print(\'\\n\\nPulled text data --> %s\'%str(data))\n\n\n    data = REP.pull(relativePath="folder1/folder2/folder3/folder3Pickled.pkl")\n    print(\'\\n\\nPulled pickled data --> %s\'%str(data))\n\n\n    # update\n    value = "This is an updated string"\n    REP.update(value, relativePath=\'pickled\')\n    print(\'\\nUpdate pickled data to --> %s\'%value)\n\n    # walk repository files\n    print(\'\\n\\nwalk repository files relative path\')\n    print(\'------------------------------------\')\n    for f in REP.walk_files_path(recursive=True):\n        print(f)\n\n\n    # walk repository, directories\n    print(\'\\n\\nwalk repository directories relative path\')\n    print(\'------------------------------------------\')\n    for d in REP.walk_directories_path(recursive=True):\n        print(d)\n\n\n    print(\'\\n\\nRepository print -->\')\n    print(REP)\n\n\n    print(\'\\n\\nRepository representation -->\')\n    print(repr(REP))\n\n\n    print(\'\\n\\nRepository to list -->\')\n    for fdDict in REP.get_repository_state():\n        k = list(fdDict)[0]\n        print("%s: %s"%(k,str(fdDict[k])))\n\n\n    print(\'\\n\\nCreate package from repository ...\')\n    REP.create_package(path=None, name=None)\n\n    # Try to load\n    try:\n        REP.load_repository(PATH)\n    except:\n        loadable = False\n    finally:\n        loadable = True\n\n    # Print whether repository is loadable\n    print(\'\\nIs repository loadable -->\',loadable)\n\n\n    # remove all repo data\n    REP.remove_repository(removeEmptyDirs=True)\n\n    # check if there is a repository in path\n    print( "\\n\\nIs path \'%s\' a repository --> %s"%(PATH, str(REP.is_repository(PATH))) )\n\n\noutput\n======\n\n.. code-block:: python\n\n    repository path --> None\n\n    Is path \'/Users/BA642A/pyrepTest_canBeDeleted\' a repository --> False\n    Repository path --> /Users/BA642A/pyrepTest_canBeDeleted\n\n    Pulled text data --> [ 0.5496571   0.8600462   0.05659633]\n\n    Pulled pickled data --> [ 0.54965711  0.86004617  0.05659633]\n\n    Update pickled data to --> This is an updated string\n\n    walk repository files relative path\n    ------------------------------------\n    pickled\n    text.dat\n    folder1/folder2/folder3/folder3Pickled.pkl\n    folder1/archive1/archive1Pickled1\n    folder1/archive1/archive1Pickled2\n    folder1/archive1/archive2/archive2Pickled1\n\n    walk repository directories relative path\n    ------------------------------------------\n    folder1\n    directory1\n    folder1/folder2\n    folder1/archive1\n    folder1/folder2/folder3\n    folder1/archive1/archive2\n    folder1/archive1/archive2/archive3\n    folder1/archive1/archive2/archive3/archive3\n    directory1/directory2\n\n    Repository print -->\n    /Users/BA642A/pyrepTest_canBeDeleted\n      pickled\n      text.dat\n      /directory1\n        /directory2\n      /folder1\n        /archive1\n        archive1Pickled1\n        archive1Pickled2\n          /archive2\n          archive2Pickled1\n            /archive3\n              /archive3\n        /folder2\n          /folder3\n          folder3Pickled.pkl\n\n    Repository representation -->\n    pyrep Repository (Version 3.0.0) @/Users/BA642A/pyrepTest_canBeDeleted [6 files] [9 directories]\n\n    Repository to list -->\n    : {\'pyrepdirinfo\': True, \'type\': \'dir\', \'exists\': True}\n    pickled: {\'pyrepfileinfo\': True, \'type\': \'file\', \'exists\': True}\n    text.dat: {\'pyrepfileinfo\': True, \'type\': \'file\', \'exists\': True}\n    directory1: {\'pyrepdirinfo\': True, \'type\': \'dir\', \'exists\': True}\n    directory1/directory2: {\'pyrepdirinfo\': True, \'type\': \'dir\', \'exists\': True}\n    folder1: {\'pyrepdirinfo\': True, \'type\': \'dir\', \'exists\': True}\n    folder1/archive1: {\'pyrepdirinfo\': True, \'type\': \'dir\', \'exists\': True}\n    folder1/archive1/archive1Pickled1: {\'pyrepfileinfo\': True, \'type\': \'file\', \'exists\': True}\n    folder1/archive1/archive1Pickled2: {\'pyrepfileinfo\': True, \'type\': \'file\', \'exists\': True}\n    folder1/archive1/archive2: {\'pyrepdirinfo\': True, \'type\': \'dir\', \'exists\': True}\n    folder1/archive1/archive2/archive2Pickled1: {\'pyrepfileinfo\': True, \'type\': \'file\', \'exists\': True}\n    folder1/archive1/archive2/archive3: {\'pyrepdirinfo\': True, \'type\': \'dir\', \'exists\': True}\n    folder1/archive1/archive2/archive3/archive3: {\'pyrepdirinfo\': True, \'type\': \'dir\', \'exists\': True}\n    folder1/folder2: {\'pyrepdirinfo\': True, \'type\': \'dir\', \'exists\': True}\n    folder1/folder2/folder3: {\'pyrepdirinfo\': True, \'type\': \'dir\', \'exists\': True}\n    folder1/folder2/folder3/folder3Pickled.pkl: {\'pyrepfileinfo\': True, \'type\': \'file\', \'exists\': True}\n\n    Create package from repository ...\n\n    Is repository loadable --> True\n\n    Is path \'/Users/BA642A/pyrepTest_canBeDeleted\' a repository --> False\n'
from __future__ import print_function
import os, sys, time, uuid, warnings, tarfile, shutil, traceback, inspect
from datetime import datetime
from functools import wraps
from pprint import pprint
from distutils.dir_util import copy_tree
import copy
try:
    import cPickle as pickle
except:
    import pickle

from pylocker import ServerLocker, FACTORY
from .__pkginfo__ import __version__
if sys.version_info >= (3, 0):
    str = str
    long = int
    unicode = str
    bytes = bytes
    basestring = str

    def makedirs(name, mode=511):
        return os.makedirs(name=name, mode=mode, exist_ok=True)


else:
    str = str
    unicode = unicode
    bytes = str
    long = long
    basestring = basestring

    def makedirs(name, mode=511):
        return os.makedirs(name=name, mode=mode)


warnings.simplefilter('always')

def get_pickling_errors(obj, seen=None):
    """Investigate pickling errors."""
    if seen == None:
        seen = []
    else:
        if hasattr(obj, '__getstate__'):
            state = obj.__getstate__()
        else:
            return
        if state == None:
            return 'object state is None'
        if isinstance(state, tuple):
            if not isinstance(state[0], dict):
                state = state[1]
            else:
                state = state[0].update(state[1])
    result = {}
    for i in state:
        try:
            pickle.dumps((state[i]), protocol=2)
        except pickle.PicklingError as e:
            try:
                if state[i] not in seen:
                    seen.append(state[i])
                    result[i] = get_pickling_errors(state[i], seen)
            finally:
                e = None
                del e

    return result


def get_dump_method(dump, protocol=-1):
    """Get dump function code string"""
    if dump is None:
        dump = 'pickle'
    if dump.startswith('pickle'):
        if dump == 'pickle':
            proto = protocol
        else:
            proto = dump.strip('pickle')
        try:
            proto = int(proto)
            assert proto >= -1
        except:
            raise Exception('protocol must be an integer >=-1')

        code = "\ndef dump(path, value):\n    import os\n    try:\n        import cPickle as pickle\n    except:\n        import pickle\n    with open(path, 'wb') as fd:\n        pickle.dump( value, fd, protocol=%i )\n        fd.flush()\n        os.fsync(fd.fileno())\n" % proto
    elif dump.startswith('dill'):
        if dump == 'dill':
            proto = 2
        else:
            proto = dump.strip('dill')
        try:
            proto = int(proto)
            assert proto >= -1
        except:
            raise Exception('protocol must be an integer >=-1')

        code = "\ndef dump(path, value):\n    import dill, os\n    with open(path, 'wb') as fd:\n        dill.dump( value, fd, protocol=%i )\n        fd.flush()\n        os.fsync(fd.fileno())\n" % proto
    elif dump == 'json':
        code = "\ndef dump(path, value):\n    import json, os\n    with open(path, 'wb') as fd:\n        json.dump( value,fd, ensure_ascii=True, indent=4 )\n        fd.flush()\n        os.fsync(fd.fileno())\n"
    elif dump == 'numpy':
        code = "\ndef dump(path, value):\n    import numpy, os\n    with open(path, 'wb') as fd:\n        numpy.save(file=fd, arr=value)\n        fd.flush()\n        os.fsync(fd.fileno())\n"
    elif dump == 'numpy_text':
        code = "\ndef dump(path, value):\n    import numpy\n    numpy.savetxt(fname=path, X=value, fmt='%.6e')\n"
    else:
        assert isinstance(dump, basestring), 'dump must be None or a string'
        code = dump
    return code


def get_pull_method(pull):
    """Get pull function code string"""
    if pull is None or pull.startswith('pickle'):
        code = "\ndef pull(path):\n    try:\n        import cPickle as pickle\n    except:\n        import pickle\n    with open(path, 'rb') as fd:\n        return pickle.load( fd )\n"
    elif pull.startswith('dill'):
        code = "\ndef pull(path):\n    import dill\n    with open(path, 'rb') as fd:\n        return dill.load( fd )\n"
    elif pull == 'json':
        code = "\ndef pull(path):\n    import json\n    with open(path, 'rb') as fd:\n        return json.load(fd)\n"
    elif pull == 'numpy':
        code = "\ndef pull(path):\n    import numpy\n    with open(path, 'rb') as fd:\n        return numpy.load(file=fd)\n\n"
    elif pull == 'numpy_text':
        code = "\ndef pull(path):\n    import numpy\n    with open(path, 'rb') as fd:\n        return numpy.loadtxt(fname=fd)\n"
    else:
        assert isinstance(pull, basestring), 'pull must be None or a string'
        code = pull
    return code


def path_required(func):
    """Decorate methods when repository path is required."""

    @wraps(func)
    def wrapper(self, *args, **kwargs):
        if self.path is None:
            warnings.warn('Must load (Repository.load_repository) or initialize (Repository.create_repository) the repository first !')
            return
        return func(self, *args, **kwargs)

    return wrapper


class InterpreterError(Exception):
    pass


def my_exec(cmd, name, description):
    try:
        l = {}
        exec(cmd, l)
        func = l[name]
    except SyntaxError as err:
        try:
            error_class = err.__class__.__name__
            detail = err.args[0]
            line_number = err.lineno
        finally:
            err = None
            del err

    except Exception as err:
        try:
            error_class = err.__class__.__name__
            detail = err.args[0]
            cl, exc, tb = sys.exc_info()
            line_number = traceback.extract_tb(tb)[(-1)][1]
        finally:
            err = None
            del err

    else:
        return func
    raise InterpreterError('%s at line %d of %s: %s' % (error_class, line_number, description, detail))


def copy_tree(src, dst, srcDirDict, filAttr=[
 '.%s_pyrepfileinfo', '.%s_pyrepfileclass'], dirAttr=[
 '.pyrepdirinfo', '.pyreprepo']):
    """copy repository directory tree from source to destination
    Stopped using from distutils.dir_util.copy_tree for 2 reasons.
    #. If in the same session dst is removed, this will fail (it's a bug in distutils)
    #. better to reimplement to copy reporsitory files only using srcDirDict
    """
    files = []
    assert os.path.isdir(src), "given source directory '%s' does not exist" % src
    src = src.rstrip(os.sep)
    dst = dst.rstrip(os.sep)
    assert src != dst, "source and destination directories are given the same '%s'" % src
    assert isinstance(srcDirDict, dict), 'source directory dictionary must be a dictionary '
    assert len(srcDirDict) == 1, 'source directory dictionary must be a dictionary of length 1'
    dirName = list(srcDirDict)[0]
    dirList = srcDirDict[dirName]
    srcDirName = os.path.basename(src)
    assert dirName == srcDirName, "source directory dictionary single key must be the source directory name '%s' but '%s' is found" % (srcDirName, dirName)
    if not os.path.isdir(dst):
        makedirs(dst)
        for attr in dirAttr:
            srcp = os.path.join(src, attr)
            if os.path.isfile(srcp):
                dstp = os.path.join(dst, attr)
                shutil.copyfile(srcp, dstp)

    for f in dirList:
        if isinstance(f, basestring):
            srcp = os.path.join(src, f)
            dstp = os.path.join(dst, f)
            shutil.copyfile(srcp, dstp)
            for attr in filAttr:
                srcp = os.path.join(src, attr % f)
                if os.path.isfile(srcp):
                    dstp = os.path.join(dst, attr % f)
                    shutil.copyfile(srcp, dstp)

            files.append(dstp)

    for d in dirList:
        if isinstance(d, dict):
            assert len(d) == 1
            fname = list(d)[0]
            src1 = os.path.join(src, fname)
            dst1 = os.path.join(dst, fname)
            files.extend(copy_tree(src=src1, dst=dst1, srcDirDict=d, filAttr=filAttr, dirAttr=dirAttr))

    return files


class Repository(object):
    """Repository"""
    DEBUG_PRINT_FAILED_TRIALS = False

    def __init__(self, path=None, pickleProtocol=2, timeout=10, password=None):
        self._Repository__repoLock = '.pyreplock'
        self._Repository__repoFile = '.pyreprepo'
        self._Repository__dirInfo = '.pyrepdirinfo'
        self._Repository__dirLock = '.pyrepdirlock'
        self._Repository__fileInfo = '.%s_pyrepfileinfo'
        self._Repository__fileClass = '.%s_pyrepfileclass'
        self._Repository__fileLock = '.%s_pyrepfilelock'
        if password is None:
            password = 'pyrep_repository_b@11a'
        assert isinstance(password, basestring), 'password must be None or a string'
        self._Repository__password = password
        self._Repository__locker = None
        assert isinstance(pickleProtocol, int), 'pickleProtocol must be integer'
        assert pickleProtocol >= -1, 'pickleProtocol must be >=-1'
        self._DEFAULT_PICKLE_PROTOCOL = pickleProtocol
        self.reset()
        if path is not None:
            assert self.is_repository(path), 'given path is not a repository. use create_repository or give a valid repository path'
            self.load_repository(path)
        self.timeout = timeout

    def __str__(self):
        if self._Repository__path is None:
            return ''
        string = os.path.normpath(self._Repository__path)
        reprSt = self.get_repository_state()
        leftAdjust = '  '
        for fdict in reprSt:
            fdname = list(fdict)[0]
            if fdname == '':
                continue
            if fdict[fdname].get('pyrepfileinfo', False):
                string += '\n'
                string += leftAdjust
                string += os.path.basename(fdname)
            elif fdict[fdname].get('pyrepdirinfo', False):
                splitPath = fdname.split(os.sep)
                leftAdjust = ''.join(['  ' * (len(item) > 0) for item in splitPath])
                string += '\n'
                string += leftAdjust
                string += os.sep + str(splitPath[(-1)])
            else:
                raise Exception('Not sure what to do next. Please report issue')

        return string

    def __getstate__(self):
        state = {}
        state.update(self.__dict__)
        state['_Repository__locker'] = None
        return state

    def __setstate__(self, state):
        path = state['_Repository__path']
        locker = None
        if path is not None:
            repoLock = state['_Repository__repoLock']
            password = state['_Repository__password']
            serverFile = os.path.join(path, repoLock)
            locker = FACTORY(key=serverFile, password=password, serverFile=serverFile, autoconnect=False, reconnect=False)
            locker.start()
        state['_Repository__locker'] = locker
        self.__dict__ = state

    def __repr__(self):
        repr = 'pyrep ' + self.__class__.__name__ + ' (Version ' + str(self._Repository__repo['pyrep_version']) + ')'
        if self._Repository__path is None:
            return repr
        ndirs, nfiles = self.get_stats()
        repr += ' @%s [%i directories] [%i files] ' % (self._Repository__path, ndirs, nfiles)
        return repr

    def __sync_files(self, repoPath, dirs):
        errors = []
        synched = []

        def _walk_dir(relPath, relDirList, relSynchedList):
            if not os.path.isdir(os.path.join(repoPath, relPath)):
                errors.append("Repository directory '%s' not found on disk" % relPath)
            else:
                for k in relDirList:
                    if isinstance(k, dict):
                        if len(k) != 1:
                            errors.append("Repository directory found in '%s' info dict length is not 1" % relPath)
                            continue
                        else:
                            dn = list(k)[0]
                            if not isinstance(dn, basestring):
                                errors.append("Repository directory found in '%s' info dict key is not a string" % relPath)
                                continue
                            if not len(dn):
                                errors.append("Repository directory found in '%s' info dict key is an empty string" % relPath)
                                continue
                            os.path.isfile(os.path.join(repoPath, relPath, self._Repository__dirInfo)) or errors.append("Repository directory info file '%s' not found on disk" % os.path.join(repoPath, relPath, self._Repository__dirInfo))
                            continue
                        rp = os.path.join(repoPath, relPath, dn)
                        rsd = {dn: []}
                        relSynchedList.append(rsd)
                        _walk_dir(relPath=rp, relDirList=(k[dn]), relSynchedList=(rsd[dn]))
                    elif isinstance(k, basestring):
                        relFilePath = os.path.join(repoPath, relPath, k)
                        relInfoPath = os.path.join(repoPath, relPath, self._Repository__fileInfo % k)
                        if not os.path.isfile(relFilePath):
                            errors.append("Repository file '%s' not found on disk" % relFilePath)
                            continue
                        elif not os.path.isfile(relInfoPath):
                            errors.append("Repository file info file '%s' not found on disk" % relFilePath)
                            continue
                        relSynchedList.append(k)
                    else:
                        errors.append("Repository file found in '%s' info dict key is not a string" % relPath)
                        continue

        _walk_dir(relPath='', relDirList=dirs, relSynchedList=synched)
        return (
         synched, errors)

    @property
    def len(self):
        ndirs, nfiles = self.get_stats()
        return {'number_of_directories':ndirs, 
         'number_of_files':nfiles}

    @property
    def locker(self):
        return self._Repository__locker

    def __save_dirinfo(self, description, dirInfoPath, create=False):
        oldInfo = None
        if description is None:
            if os.path.isfile(dirInfoPath):
                with open(dirInfoPath, 'rb') as (fd):
                    oldInfo = pickle.load(fd)
                if self._Repository__repo['repository_unique_name'] != oldInfo['repository_unique_name']:
                    description = ''
        if description is None:
            if create:
                description = ''
        if description is not None:
            if os.path.isfile(dirInfoPath):
                if oldInfo is None:
                    with open(dirInfoPath, 'rb') as (fd):
                        oldInfo = pickle.load(fd)
                if self._Repository__repo['repository_unique_name'] != oldInfo['repository_unique_name']:
                    createTime = lastUpdateTime = time.time()
                else:
                    createTime = oldInfo['create_utctime']
                    lastUpdateTime = time.time()
            else:
                createTime = lastUpdateTime = time.time()
            info = {'repository_unique_name':self._Repository__repo['repository_unique_name'], 
             'create_utctime':createTime, 
             'last_update_utctime':lastUpdateTime, 
             'description':description}
            with open(dirInfoPath, 'wb') as (fd):
                pickle.dump(info, fd, protocol=(self._DEFAULT_PICKLE_PROTOCOL))
                fd.flush()
                os.fsync(fd.fileno())

    def __clean_before_after(self, stateBefore, stateAfter, keepNoneEmptyDirectory=True):
        """clean repository given before and after states"""
        errors = []
        afterDict = {}
        [afterDict.setdefault(list(aitem)[0], []).append(aitem) for aitem in stateAfter]
        for bitem in reversed(stateBefore):
            relaPath = list(bitem)[0]
            basename = os.path.basename(relaPath)
            btype = bitem[relaPath]['type']
            alist = afterDict.get(relaPath, [])
            aitem = [a for a in alist if a[relaPath]['type'] == btype]
            if len(aitem) > 1:
                errors.append("Multiple '%s' of type '%s' where found in '%s', this should never had happened. Please report issue" % (basename, btype, relaPath))
                continue
            if not len(aitem):
                removeDirs = []
                removeFiles = []
                if btype == 'dir':
                    if not len(relaPath):
                        errors.append('Removing main repository directory is not allowed')
                        continue
                    removeDirs.append(os.path.join(self._Repository__path, relaPath))
                    removeFiles.append(os.path.join(self._Repository__path, relaPath, self._Repository__dirInfo))
                    removeFiles.append(os.path.join(self._Repository__path, relaPath, self._Repository__dirLock))
                elif btype == 'file':
                    removeFiles.append(os.path.join(self._Repository__path, relaPath))
                    removeFiles.append(os.path.join(self._Repository__path, relaPath, self._Repository__fileInfo % basename))
                    removeFiles.append(os.path.join(self._Repository__path, relaPath, self._Repository__fileLock % basename))
                else:
                    removeDirs.append(os.path.join(self._Repository__path, relaPath))
                    removeFiles.append(os.path.join(self._Repository__path, relaPath, self._Repository__fileInfo % basename))
                for fpath in removeFiles:
                    if os.path.isfile(fpath):
                        try:
                            os.remove(fpath)
                        except Exception as err:
                            try:
                                errors.append("Unable to clean file '%s' (%s)" % (fpath, str(err)))
                            finally:
                                err = None
                                del err

                for dpath in removeDirs:
                    if not (os.path.isdir(dpath)):
                        try:
                            shutil.rmtree(dpath)
                        except Exception as err:
                            try:
                                errors.append("Unable to clean directory '%s' (%s)" % (fpath, str(err)))
                            finally:
                                err = None
                                del err

        return (
         len(errors) == 0, errors)

    def __get_repository_parent_directory(self, relativePath):
        relativePath = self.to_repo_relative_path(path=relativePath, split=False)
        if relativePath == '':
            return
        parentPath = os.path.dirname(relativePath)
        return self._Repository__get_repository_directory(relativePath=parentPath)

    def __get_repository_directory(self, relativePath):
        cDir = self._Repository__repo['walk_repo']
        splitted = self.to_repo_relative_path(path=relativePath, split=True)
        if splitted == ['']:
            return cDir
        for dirname in splitted:
            dList = [d for d in cDir if isinstance(d, dict)]
            if not len(dList):
                cDir = None
                break
            cDict = [d for d in dList if dirname in d]
            if not len(cDict):
                cDir = None
                break
            cDir = cDict[0][dirname]

        return cDir

    def __save_repository_pickle_file(self, lockFirst=False, raiseError=True):
        error = None
        if lockFirst:
            acquired, lockId = self._Repository__locker.acquire_lock(path=(self._Repository__path), timeout=(self.timeout))
            if not acquired:
                error = 'code %s. Unable to aquire the repository lock. You may try again!' % (lockId,)
                if raiseError:
                    raise AssertionError(Exception(error))
                return (
                 False, error)
        try:
            repoInfoPath = os.path.join(self._Repository__path, self._Repository__repoFile)
            with open(repoInfoPath, 'wb') as (fd):
                self._Repository__repo['last_update_utctime'] = time.time()
                pickle.dump((self._Repository__repo), fd, protocol=(self._DEFAULT_PICKLE_PROTOCOL))
                fd.flush()
                os.fsync(fd.fileno())
        except Exception as err:
            try:
                error = 'Unable to save repository (%s)' % str(err)
            finally:
                err = None
                del err

        if lockFirst:
            self._Repository__locker.release_lock(lockId)
        if not error is None:
            if raiseError:
                raise AssertionError(error)
        return (
         error is None, error)

    def __load_repository_pickle_file(self, repoPath):
        try:
            fd = open(repoPath, 'rb')
        except Exception as err:
            try:
                raise Exception('Unable to open repository file(%s)' % str(err))
            finally:
                err = None
                del err

        try:
            repo = pickle.load(fd)
        except Exception as err:
            try:
                fd.close()
                raise Exception('Unable to load pickle repository (%s)' % str(err))
            finally:
                err = None
                del err

        else:
            fd.close()
        assert isinstance(repo, dict), 'pyrep repo must be a dictionary'
        assert 'create_utctime' in repo, "'create_utctime' must be a key in pyrep repo dict"
        assert 'last_update_utctime' in repo, "'last_update_utctime' must be a key in pyrep repo dict"
        assert 'pyrep_version' in repo, "'pyrep_version' must be a key in pyrep repo dict"
        assert 'walk_repo' in repo, "'walk_repo' must be a key in pyrep repo dict"
        assert isinstance(repo['walk_repo'], list), "pyrep info 'walk_repo' key value must be a list"
        return repo

    def __load_repository(self, path, verbose=True, safeMode=True):
        if path.strip() in ('', '.'):
            path = os.getcwd()
        else:
            repoPath = os.path.realpath(os.path.expanduser(path))
            if not self.is_repository(repoPath):
                raise Exception("No repository found in '%s'" % str(repoPath))
            serverFile = os.path.join(repoPath, self._Repository__repoLock)
            self._Repository__locker = FACTORY(key=serverFile, password=(self._Repository__password), serverFile=serverFile, autoconnect=False, reconnect=False)
            self._Repository__locker.start()
            if safeMode:
                acquired, lockId = self._Repository__locker.acquire_lock(path=repoPath, timeout=(self.timeout))
                assert acquired, "code %s. Unable to aquire the lock when calling 'load_repository'" % (lockId,)
            error = None
            try:
                repo = self._Repository__load_repository_pickle_file(os.path.join(repoPath, self._Repository__repoFile))
                repoFiles, errors = self._Repository__sync_files(repoPath=repoPath, dirs=(repo['walk_repo']))
                if len(errors):
                    if verbose:
                        warnings.warn('\n'.join(errors))
                self._Repository__path = repoPath
                self._Repository__repo['repository_unique_name'] = repo['repository_unique_name']
                self._Repository__repo['repository_information'] = repo['repository_information']
                self._Repository__repo['create_utctime'] = repo['create_utctime']
                self._Repository__repo['last_update_utctime'] = repo['last_update_utctime']
                self._Repository__repo['walk_repo'] = repoFiles
            except Exception as err:
                try:
                    error = str(err)
                finally:
                    err = None
                    del err

        if safeMode:
            self._Repository__locker.release_lock(lockId)
        assert error is None, error

    @property
    def info(self):
        """Get repository information"""
        return self._Repository__repo['repository_information']

    @property
    def path(self):
        """The repository instance path which points to the directory where
        .pyreprepo is."""
        return self._Repository__path

    @property
    def uniqueName(self):
        """Get repository unique name as generated when repository was created"""
        return self._Repository__repo['repository_unique_name']

    def close(self):
        if self._Repository__locker is not None:
            self._Repository__locker.stop()

    def get_stats(self):
        """
        Get repository descriptive stats

        :Returns:
            #. numberOfDirectories (integer): Number of diretories in repository
            #. numberOfFiles (integer): Number of files in repository
        """
        if self._Repository__path is None:
            return (0, 0)
        nfiles = 0
        ndirs = 0
        for fdict in self.get_repository_state():
            fdname = list(fdict)[0]
            if fdname == '':
                continue
            else:
                if fdict[fdname].get('pyrepfileinfo', False):
                    nfiles += 1
            if fdict[fdname].get('pyrepdirinfo', False):
                ndirs += 1
            else:
                warnings.warn("'%s' is neither a repository file nor a directory. This can happen when accessing the repository asynchronously." % fdname)
                continue

        return (ndirs, nfiles)

    def reset(self):
        """Reset repository instance.
        """
        self._Repository__path = None
        self._Repository__locker = None
        self._Repository__repo = {'repository_unique_name':str(uuid.uuid1()),  'create_utctime':time.time(), 
         'last_update_utctime':None, 
         'pyrep_version':str(__version__), 
         'repository_information':'', 
         'walk_repo':[]}

    def is_repository(self, path):
        """
        Check if there is a Repository in path.

        :Parameters:
            #. path (string): The real path of the directory where to check if
               there is a repository.

        :Returns:
            #. result (boolean): Whether it's a repository or not.
        """
        if path.strip() in ('', '.'):
            path = os.getcwd()
        repoPath = os.path.realpath(os.path.expanduser(path))
        if os.path.isfile(os.path.join(repoPath, self._Repository__repoFile)):
            return True
        return False

    def load_repository(self, path, verbose=True, ntrials=3, safeMode=True):
        """
        Load repository from a directory path and update the current instance.
        First, new repository still will be loaded. If failed, then old
        style repository load will be tried.

        :Parameters:
            #. path (string): The path of the directory from where to load
               the repository from. If '.' or an empty string is passed,
               the current working directory will be used.
            #. verbose (boolean): Whether to be verbose about abnormalities
            #. ntrials (int): After aquiring all locks, ntrials is the maximum
               number of trials allowed before failing. In rare cases, when
               multiple processes are accessing the same repository components,
               different processes can alter repository components between
               successive lock releases of some other process. Bigger number
               of trials lowers the likelyhood of failure due to multiple
               processes same time alteration.
            #. safeMode (boolean): loading repository can be done without
               acquiring from multiple processes. Not acquiring the lock
               can be unsafe if another process is altering the repository

        :Returns:
             #. repository (pyrep.Repository): returns self repository with loaded data.
        """
        assert isinstance(safeMode, bool), 'safeMode must be boolean'
        assert isinstance(ntrials, int), 'ntrials must be integer'
        assert ntrials > 0, 'ntrials must be >0'
        repo = None
        for _trial in range(ntrials):
            try:
                self._Repository__load_repository(path=path, verbose=True, safeMode=safeMode)
            except Exception as err1:
                try:
                    error = 'Unable to load repository (%s)' % (err1,)
                finally:
                    err1 = None
                    del err1

            else:
                error = None
                repo = self
                break

        assert error is None, error
        return repo

    def create_repository(self, path, info=None, description=None, replace=True, allowNoneEmpty=True, raiseError=True):
        """
        create a repository in a directory. This method insures the creation of
        the directory in the system if it is missing.

        **N.B. If replace is True and existing repository is found in path, create_repository erases all existing files and directories in path.**

        :Parameters:
            #. path (string): The real absolute path where to create the Repository.
               If '.' or an empty string is passed, the current working directory will be used.
            #. description (None, str): Repository main directory information.
            #. info (None, object): Repository information. It can
               be None or any pickle writable type of data.
            #. replace (boolean): Whether to replace existing repository.
            #. allowNoneEmpty (boolean): Allow creating repository in none-empty
               directory.
            #. raiseError (boolean): Whether to raise encountered error instead
               of returning failure.

        :Returns:
            #. success (boolean): Whether creating repository was successful
            #. message (None, str): Any returned message.
        """
        if not isinstance(raiseError, bool):
            raise AssertionError('raiseError must be boolean')
        else:
            if not isinstance(allowNoneEmpty, bool):
                raise AssertionError('allowNoneEmpty must be boolean')
            elif not isinstance(replace, bool):
                raise AssertionError('replace must be boolean')
            else:
                if not isinstance(path, basestring):
                    raise AssertionError('path must be string')
                else:
                    if info is None:
                        info = ''
                    try:
                        pickle.dumps(info)
                    except Exception as err:
                        try:
                            raise Exception('info must be None or any pickle writable type of data (%s)' % str(err))
                        finally:
                            err = None
                            del err

                if description is None:
                    description = ''
                assert isinstance(description, basestring), 'description must be None or a string'
                if path.strip() in ('', '.'):
                    path = os.getcwd()
                realPath = os.path.realpath(os.path.expanduser(path))
                message = []
                if self.is_repository(realPath):
                    if not replace:
                        message.append("A pyrep Repository already exists in the given path '%s' set replace to True if you need to proceed." % path)
                        return (
                         False, message)
                    message.append("Existing pyrep repository existing in the given path '%s' has been replaced." % path)
                    try:
                        for _df in os.listdir(realPath):
                            _p = os.path.join(realPath, _df)
                            if os.path.isdir(_p):
                                shutil.rmtree(_p)
                            else:
                                os.remove(_p)

                    except Exception as err:
                        try:
                            message.append('Unable to clean remove repository before create (%s)' % str(err))
                            return (
                             False, '\n'.join(message))
                        finally:
                            err = None
                            del err

                    if not os.path.isdir(realPath):
                        makedirs(realPath)
                elif len(os.listdir(realPath)):
                    return allowNoneEmpty or (False, 'Not allowed to create repository in a non empty directory')
            oldRepo = self._Repository__repo
            oldPath = self._Repository__path
            self.reset()
            self._Repository__path = realPath.rstrip(os.sep)
            self._Repository__repo['repository_information'] = info
            serverFile = os.path.join(self._Repository__path, self._Repository__repoLock)
            self._Repository__locker = FACTORY(key=serverFile, password=(self._Repository__password), serverFile=serverFile, autoconnect=False, reconnect=False)
            self._Repository__locker.start()
            saved = self.save(description=description)
            self._Repository__repo = saved or oldRepo
            self._Repository__path = oldPath
            message.append('Absolute path and directories might be created but no pyrep Repository is created. Previous repository state restored')
            if self._Repository__path is not None:
                serverFile = os.path.join(self._Repository__path, self._Repository__repoLock)
                self._Repository__locker = FACTORY(key=serverFile, password=(self._Repository__password), serverFile=serverFile, autoconnect=False, reconnect=False)
                self._Repository__locker.start()
            return (False, '\n'.join(message))
        return (
         True, '\n'.join(message))

    def remove_repository(self, path=None, password=None, removeEmptyDirs=True):
        """
        Remove all repository from path along with all repository tracked files.

        :Parameters:
            #. path (None, string): The path the repository to remove.
            #. password (None, string): If path is not for this isntance
               repository, a new Repository must be created and this
               password would be given upon instanciation
            #. removeEmptyDirs (boolean): Whether to remove remaining empty
               directories including repository one.
        """
        if not isinstance(removeEmptyDirs, bool):
            raise AssertionError('removeEmptyDirs must be boolean')
        else:
            if path is not None:
                if path != self._Repository__path:
                    repo = Repository(password=password)
                    repo.load_repository(path)
                else:
                    repo = self
            else:
                repo = self
            assert repo.path is not None, 'path is not given and repository is not initialized'
            assert repo.locker.isServer, "It's not safe to remove repository tree from a client"
            if len(repo.locker._clientsLUT):
                raise AssertionError("It's not safe to remove repository tree when other instances are still connected")
            for fdict in reversed(repo.get_repository_state()):
                relaPath = list(fdict)[0]
                realPath = os.path.join(repo.path, relaPath)
                path, name = os.path.split(realPath)
                if fdict[relaPath]['type'] == 'file':
                    if os.path.isfile(realPath):
                        os.remove(realPath)
                    if os.path.isfile(os.path.join(repo.path, path, self._Repository__fileInfo % name)):
                        os.remove(os.path.join(repo.path, path, self._Repository__fileInfo % name))
                    if os.path.isfile(os.path.join(repo.path, path, self._Repository__fileLock % name)):
                        os.remove(os.path.join(repo.path, path, self._Repository__fileLock % name))
                    if os.path.isfile(os.path.join(repo.path, path, self._Repository__fileClass % name)):
                        os.remove(os.path.join(repo.path, path, self._Repository__fileClass % name))
                    elif fdict[relaPath]['type'] == 'dir':
                        if os.path.isfile(os.path.join(realPath, self._Repository__dirInfo)):
                            os.remove(os.path.join(realPath, self._Repository__dirInfo))
                        if os.path.isfile(os.path.join(realPath, self._Repository__dirLock)):
                            os.remove(os.path.join(realPath, self._Repository__dirLock))
                        if len(os.listdir(realPath)) or removeEmptyDirs:
                            shutil.rmtree(realPath)

            if os.path.isfile(os.path.join(repo.path, self._Repository__repoFile)):
                os.remove(os.path.join(repo.path, self._Repository__repoFile))
            if os.path.isfile(os.path.join(repo.path, self._Repository__repoLock)):
                os.remove(os.path.join(repo.path, self._Repository__repoLock))
            if not len(os.listdir(repo.path)):
                if removeEmptyDirs:
                    shutil.rmtree(repo.path)
        repo.close()

    @path_required
    def save(self, description=None, raiseError=True, ntrials=3):
        """
        Save repository '.pyreprepo' to disk and create (if missing) or
        update (if description is not None) '.pyrepdirinfo'.

        :Parameters:
            #. description (None, str): Repository main directory information.
               If given will be replaced.
            #. raiseError (boolean): Whether to raise encountered error instead
               of returning failure.
            #. ntrials (int): After aquiring all locks, ntrials is the maximum
               number of trials allowed before failing.
               In rare cases, when multiple processes
               are accessing the same repository components, different processes
               can alter repository components between successive lock releases
               of some other process. Bigger number of trials lowers the
               likelyhood of failure due to multiple processes same time
               alteration.

        :Returns:
            #. success (bool): Whether saving was successful.
            #. error (None, string): Fail to save repository message in case
               saving is not successful. If success is True, error will be None.
        """
        if not isinstance(raiseError, bool):
            raise AssertionError('raiseError must be boolean')
        else:
            if not isinstance(ntrials, int):
                raise AssertionError('ntrials must be integer')
            else:
                if not ntrials > 0:
                    raise AssertionError('ntrials must be >0')
                else:
                    if description is not None:
                        assert isinstance(description, basestring), 'description must be None or a string'
                    dirInfoPath = os.path.join(self._Repository__path, self._Repository__dirInfo)
                    if description is None:
                        description = os.path.isfile(dirInfoPath) or ''
                acquired, lockId = self._Repository__locker.acquire_lock((self._Repository__path), timeout=(self.timeout))
                m = acquired or "code %s. Unable to aquire the lock when calling 'save'. You may try again!" % (lockId,)
                if raiseError:
                    raise AssertionError(Exception(m))
                return (
                 False, m)
            for _trial in range(ntrials):
                try:
                    repoInfoPath = os.path.join(self._Repository__path, self._Repository__repoFile)
                    error = None
                    self._Repository__save_dirinfo(description=description, dirInfoPath=dirInfoPath)
                    if os.path.isfile(repoInfoPath):
                        with open(repoInfoPath, 'rb') as (fd):
                            repo = self._Repository__load_repository_pickle_file(os.path.join(self._Repository__path, self._Repository__repoFile))
                            self._Repository__repo['walk_repo'] = repo['walk_repo']
                    with open(repoInfoPath, 'wb') as (fd):
                        self._Repository__repo['last_update_utctime'] = time.time()
                        pickle.dump((self._Repository__repo), fd, protocol=(self._DEFAULT_PICKLE_PROTOCOL))
                        fd.flush()
                        os.fsync(fd.fileno())
                except Exception as err:
                    try:
                        error = 'Unable to save repository (%s)' % err
                        if self.DEBUG_PRINT_FAILED_TRIALS:
                            print('Trial %i failed in Repository.%s (%s). Set Repository.DEBUG_PRINT_FAILED_TRIALS to False to mute' % (_trial, inspect.stack()[1][3], str(error)))
                    finally:
                        err = None
                        del err

                else:
                    break

            self._Repository__locker.release_lock(lockId)
            if not error is None:
                if raiseError:
                    raise AssertionError(error)
        return (
         error is None, error)

    def is_name_allowed(self, path):
        """
        Get whether creating a file or a directory from the basenane of the given
        path is allowed

        :Parameters:
            #. path (str): The absolute or relative path or simply the file
               or directory name.

        :Returns:
            #. allowed (bool): Whether name is allowed.
            #. message (None, str): Reason for the name to be forbidden.
        """
        if not isinstance(path, basestring):
            raise AssertionError('given path must be a string')
        else:
            name = os.path.basename(path)
            return len(name) or (False, 'empty name is not allowed')
        for em in [self._Repository__repoLock, self._Repository__repoFile, self._Repository__dirInfo, self._Repository__dirLock]:
            if name == em:
                return (False, "name '%s' is reserved for pyrep internal usage" % em)

        for pm in [self._Repository__fileInfo, self._Repository__fileLock]:
            if not name == pm:
                if not name.endswith(pm[3:]) or name.startswith('.'):
                    return (
                     False, "name pattern '%s' is not allowed as result may be reserved for pyrep internal usage" % pm)

        return (True, None)

    def to_repo_relative_path(self, path, split=False):
        """
        Given a path, return relative path to diretory

        :Parameters:
            #. path (str): Path as a string
            #. split (boolean): Whether to split path to its components

        :Returns:
            #. relativePath (str, list): Relative path as a string or as a list
               of components if split is True
        """
        path = os.path.normpath(path)
        if path == '.':
            path = ''
        path = path.split(self._Repository__path)[(-1)].strip(os.sep)
        if split:
            return path.split(os.sep)
        return path

    @path_required
    def get_repository_state(self, relaPath=None):
        """
        Get a list representation of repository state along with useful
        information. List state is ordered relativeley to directories level

        :Parameters:
            #. relaPath (None, str): relative directory path from where to
               start. If None all repository representation is returned.

        :Returns:
            #. state (list): List representation of the repository.
               List items are all dictionaries. Every dictionary has a single
               key which is the file or the directory name and the value is a
               dictionary of information including:

                   * 'type': the type of the tracked whether it's file, dir, or objectdir
                   * 'exists': whether file or directory actually exists on disk
                   * 'pyrepfileinfo': In case of a file or an objectdir whether .%s_pyrepfileinfo exists
                   * 'pyrepdirinfo': In case of a directory whether .pyrepdirinfo exists
        """
        state = []

        def _walk_dir(relaPath, dirList):
            dirDict = {'type':'dir', 
             'exists':os.path.isdir(os.path.join(self._Repository__path, relaPath)), 
             'pyrepdirinfo':os.path.isfile(os.path.join(self._Repository__path, relaPath, self._Repository__dirInfo))}
            state.append({relaPath: dirDict})
            for fname in sorted([f for f in dirList if isinstance(f, basestring)]):
                relaFilePath = os.path.join(relaPath, fname)
                realFilePath = os.path.join(self._Repository__path, relaFilePath)
                fileDict = {'type':'file', 
                 'exists':os.path.isfile(realFilePath), 
                 'pyrepfileinfo':os.path.isfile(os.path.join(self._Repository__path, relaPath, self._Repository__fileInfo % fname))}
                state.append({relaFilePath: fileDict})

            for ddict in sorted([d for d in dirList if isinstance(d, dict)],
              key=(lambda k: list(k)[0])):
                dirname = list(ddict)[0]
                _walk_dir(relaPath=(os.path.join(relaPath, dirname)), dirList=(ddict[dirname]))

        if relaPath is None:
            _walk_dir(relaPath='', dirList=(self._Repository__repo['walk_repo']))
        else:
            assert isinstance(relaPath, basestring), 'relaPath must be None or a str'
            relaPath = self.to_repo_relative_path(path=relaPath, split=False)
            spath = relaPath.split(os.sep)
            dirList = self._Repository__repo['walk_repo']
            while len(spath):
                dirname = spath.pop(0)
                dList = [d for d in dirList if isinstance(d, dict)]
                if not len(dList):
                    dirList = None
                    break
                cDict = [d for d in dList if dirname in d]
                if not len(cDict):
                    dirList = None
                    break
                dirList = cDict[0][dirname]

            if dirList is not None:
                _walk_dir(relaPath=relaPath, dirList=dirList)
        return state

    def get_repository_directory(self, relativePath):
        """
        Get repository directory list copy.

        :Parameters:
            #. relativePath (string): The relative to the repository path .

        :Returns:
            #. dirList (None, list): List of directories and files in repository
               directory. If directory is not tracked in repository None is
               returned
        """
        return copy.deepcopy(self._Repository__get_repository_directory(relativePath))

    def get_file_info(self, relativePath):
        """
        Get file information dict from the repository given its relative path.

        :Parameters:
            #. relativePath (string): The relative to the repository path of
               the file.

        :Returns:
            #. info (None, dictionary): The file information dictionary.
               If None, it means an error has occurred.
            #. errorMessage (string): The error message if any error occurred.
        """
        relativePath = self.to_repo_relative_path(path=relativePath, split=False)
        fileName = os.path.basename(relativePath)
        isRepoFile, fileOnDisk, infoOnDisk, classOnDisk = self.is_repository_file(relativePath)
        if not isRepoFile:
            return (None, 'file is not a registered repository file.')
        else:
            return infoOnDisk or (None, 'file is a registered repository file but info file missing')
        fileInfoPath = os.path.join(self._Repository__path, os.path.dirname(relativePath), self._Repository__fileInfo % fileName)
        try:
            with open(fileInfoPath, 'rb') as (fd):
                info = pickle.load(fd)
        except Exception as err:
            try:
                return (
                 None, 'Unable to read file info from disk (%s)' % str(err))
            finally:
                err = None
                del err

        return (
         info, '')

    def is_repository_directory(self, relativePath):
        """
        Get whether directory is registered in repository.

        :Parameters:
            #. relativePath (string): The relative to the repository path.

        :Returns:
            #. result (boolean): Whether directory is tracked and registered.
        """
        return self._Repository__get_repository_directory(relativePath) is not None

    def is_repository_file(self, relativePath):
        """
        Check whether a given relative path is a repository file path

        :Parameters:
            #. relativePath (string): File relative path

        :Returns:
            #. isRepoFile (boolean): Whether file is a repository file.
            #. isFileOnDisk (boolean): Whether file is found on disk.
            #. isFileInfoOnDisk (boolean): Whether file info is found on disk.
            #. isFileClassOnDisk (boolean): Whether file class is found on disk.
        """
        relativePath = self.to_repo_relative_path(path=relativePath, split=False)
        if relativePath == '':
            return (False, False, False, False)
        relaDir, name = os.path.split(relativePath)
        fileOnDisk = os.path.isfile(os.path.join(self._Repository__path, relativePath))
        infoOnDisk = os.path.isfile(os.path.join(self._Repository__path, os.path.dirname(relativePath), self._Repository__fileInfo % name))
        classOnDisk = os.path.isfile(os.path.join(self._Repository__path, os.path.dirname(relativePath), self._Repository__fileClass % name))
        cDir = self._Repository__repo['walk_repo']
        if len(relaDir):
            for dirname in relaDir.split(os.sep):
                dList = [d for d in cDir if isinstance(d, dict)]
                if not len(dList):
                    cDir = None
                    break
                cDict = [d for d in dList if dirname in d]
                if not len(cDict):
                    cDir = None
                    break
                cDir = cDict[0][dirname]

        if cDir is None:
            return (False, fileOnDisk, infoOnDisk, classOnDisk)
        if str(name) not in [str(i) for i in cDir]:
            return (False, fileOnDisk, infoOnDisk, classOnDisk)
        return (
         True, fileOnDisk, infoOnDisk, classOnDisk)

    @path_required
    def walk_files_path(self, relativePath='', fullPath=False, recursive=False):
        """
        Walk the repository relative path and yield file relative/full path.

        :parameters:
            #. relativePath (string): The relative path from which start the walk.
            #. fullPath (boolean): Whether to return full or relative path.
            #. recursive (boolean): Whether walk all directories files recursively
        """
        assert isinstance(fullPath, bool), 'fullPath must be boolean'
        assert isinstance(recursive, bool), 'recursive must be boolean'
        relativePath = self.to_repo_relative_path(path=relativePath, split=False)
        dirList = self._Repository__get_repository_directory(relativePath=relativePath)
        assert dirList is not None, "given relative path '%s' is not a repository directory" % relativePath

        def _walk(rpath, dlist, recursive):
            for fname in dlist:
                if isinstance(fname, basestring):
                    if fullPath:
                        yield os.path.join(self._Repository__path, rpath, fname)
                    else:
                        yield os.path.join(rpath, fname)

            if recursive:
                for ddict in dlist:
                    if isinstance(ddict, dict):
                        dname = list(ddict)[0]
                        for p in _walk(rpath=(os.path.join(rpath, dname)), dlist=(ddict[dname]), recursive=recursive):
                            yield p

        return _walk(rpath=relativePath, dlist=dirList, recursive=recursive)

    def walk_files_info(self, relativePath='', fullPath=False, recursive=False):
        """
        Walk the repository relative path and yield tuple of two items where
        first item is file relative/full path and second item is file info.
        If file info is not found on disk, second item will be None.

        :parameters:
            #. relativePath (string): The relative path from which start the walk.
            #. fullPath (boolean): Whether to return full or relative path.
            #. recursive (boolean): Whether walk all directories files recursively
        """
        assert isinstance(fullPath, bool), 'fullPath must be boolean'
        assert isinstance(recursive, bool), 'recursive must be boolean'
        relativePath = self.to_repo_relative_path(path=relativePath, split=False)
        for relaPath in self.walk_files_path(relativePath=relativePath, fullPath=False, recursive=recursive):
            fpath, fname = os.path.split(relaPath)
            fileInfoPath = os.path.join(self._Repository__path, fpath, self._Repository__fileInfo % fname)
            if os.path.isfile(fileInfoPath):
                with open(fileInfoPath, 'rb') as (fd):
                    info = pickle.load(fd)
            else:
                info = None
            if fullPath:
                yield (
                 os.path.join(self._Repository__path, relaPath), info)
            else:
                yield (
                 relaPath, info)

    def walk_directories_path(self, relativePath='', fullPath=False, recursive=False):
        """
        Walk repository relative path and yield directory relative/full path

        :parameters:
            #. relativePath (string): The relative path from which start the walk.
            #. fullPath (boolean): Whether to return full or relative path.
            #. recursive (boolean): Whether walk all directories files recursively.
        """
        assert isinstance(fullPath, bool), 'fullPath must be boolean'
        assert isinstance(recursive, bool), 'recursive must be boolean'
        relativePath = self.to_repo_relative_path(path=relativePath, split=False)
        dirList = self._Repository__get_repository_directory(relativePath=relativePath)
        assert dirList is not None, "given relative path '%s' is not a repository directory" % relativePath

        def _walk(rpath, dlist, recursive):
            for ddict in dlist:
                if isinstance(ddict, dict):
                    dname = list(ddict)[0]
                    if fullPath:
                        yield os.path.join(self._Repository__path, rpath, dname)
                    else:
                        yield os.path.join(rpath, dname)

            if recursive:
                for ddict in dlist:
                    if isinstance(ddict, dict):
                        dname = list(ddict)[0]
                        for p in _walk(rpath=(os.path.join(rpath, dname)), dlist=(ddict[dname]), recursive=recursive):
                            yield p

        return _walk(rpath=relativePath, dlist=dirList, recursive=recursive)

    def walk_directories_info(self, relativePath='', fullPath=False, recursive=False):
        """
        Walk the repository relative path and yield tuple of two items where
        first item is directory relative/full path and second item is directory
        info. If directory file info is not found on disk, second item will be None.

        :parameters:
            #. relativePath (string): The relative path from which start the walk.
            #. fullPath (boolean): Whether to return full or relative path.
            #. recursive (boolean): Whether walk all directories files recursively.
        """
        assert isinstance(fullPath, bool), 'fullPath must be boolean'
        assert isinstance(recursive, bool), 'recursive must be boolean'
        relativePath = self.to_repo_relative_path(path=relativePath, split=False)
        for dpath in self.walk_directories_path(relativePath=relativePath, fullPath=False, recursive=recursive):
            dirInfoPath = os.path.join(self._Repository__path, dpath, self._Repository__dirInfo)
            if os.path.isfile(dirInfoPath):
                with open(dirInfoPath, 'rb') as (fd):
                    info = pickle.load(fd)
            else:
                info = None
            if fullPath:
                yield (
                 os.path.join(self._Repository__path, dpath), info)
            else:
                yield (
                 dpath, info)

    @path_required
    def create_package(self, path=None, name=None, mode=None):
        """
        Create a tar file package of all the repository files and directories.
        Only files and directories that are tracked in the repository
        are stored in the package tar file.

        **N.B. On some systems packaging requires root permissions.**

        :Parameters:
            #. path (None, string): The real absolute path where to create the
               package. If None, it will be created in the same directory as
               the repository. If '.' or an empty string is passed, the current
               working directory will be used.
            #. name (None, string): The name to give to the package file
               If None, the package directory name will be used with the
               appropriate extension added.
            #. mode (None, string): The writing mode of the tarfile.
               If None, automatically the best compression mode will be chose.
               Available modes are ('w', 'w:', 'w:gz', 'w:bz2')
        """
        if not mode in (None, 'w', 'w:', 'w:gz', 'w:bz2'):
            raise AssertionError('unkown archive mode %s' % str(mode))
        elif mode is None:
            mode = 'w:'
        else:
            if path is None:
                root = os.path.split(self._Repository__path)[0]
            elif path.strip() in ('', '.'):
                root = os.getcwd()
            else:
                root = os.path.realpath(os.path.expanduser(path))
            assert os.path.isdir(root), 'absolute path %s is not a valid directory' % path
            if name is None:
                ext = mode.split(':')
                if len(ext) == 2:
                    if len(ext[1]):
                        ext = '.' + ext[1]
                    else:
                        ext = '.tar'
                else:
                    ext = '.tar'
                name = os.path.split(self._Repository__path)[1] + ext
            tarfilePath = os.path.join(root, name)
            try:
                tarHandler = tarfile.TarFile.open(tarfilePath, mode=mode)
            except Exception as e:
                try:
                    raise Exception('Unable to create package (%s)' % e)
                finally:
                    e = None
                    del e

        for dpath in sorted(list(self.walk_directories_path(recursive=True))):
            t = tarfile.TarInfo(dpath)
            t.type = tarfile.DIRTYPE
            tarHandler.addfile(t)
            tarHandler.add((os.path.join(self._Repository__path, dpath, self._Repository__dirInfo)), arcname=(self._Repository__dirInfo))

        for fpath in self.walk_files_path(recursive=True):
            relaPath, fname = os.path.split(fpath)
            tarHandler.add((os.path.join(self._Repository__path, fpath)), arcname=fname)
            tarHandler.add((os.path.join(self._Repository__path, relaPath, self._Repository__fileInfo % fname)), arcname=(self._Repository__fileInfo % fname))
            tarHandler.add((os.path.join(self._Repository__path, relaPath, self._Repository__fileClass % fname)), arcname=(self._Repository__fileClass % fname))

        tarHandler.add((os.path.join(self._Repository__path, self._Repository__repoFile)), arcname='.pyrepinfo')
        tarHandler.close()

    @path_required
    def add_directory(self, relativePath, description=None, clean=False, raiseError=True, ntrials=3):
        """
        Add a directory in the repository and creates its attribute in the
        Repository with utc timestamp. It insures adding all the missing
        directories in the path.

        :Parameters:
            #. relativePath (string): The relative to the repository path to
               where directory must be added.
            #. description (None, string): Any random description about the
               added directory.
            #. clean (boolean): Whether to remove existing non repository
               tracked files and folders in all created directory chain tree.
            #. raiseError (boolean): Whether to raise encountered error instead
               of returning failure.
            #. ntrials (int): After aquiring all locks, ntrials is the maximum
               number of trials allowed before failing.
               In rare cases, when multiple processes
               are accessing the same repository components, different processes
               can alter repository components between successive lock releases
               of some other process. Bigger number of trials lowers the
               likelyhood of failure due to multiple processes same time
               alteration.

        :Returns:
            #. success (boolean): Whether adding the directory was successful.
            #. message (None, string): Reason why directory was not added or
               random information.
        """
        if not isinstance(raiseError, bool):
            raise AssertionError('raiseError must be boolean')
        else:
            if not isinstance(relativePath, basestring):
                raise AssertionError('relativePath must be a string')
            elif description is not None:
                assert isinstance(description, basestring), 'description must be None or a string'
            else:
                if not isinstance(ntrials, int):
                    raise AssertionError('ntrials must be integer')
                else:
                    assert ntrials > 0, 'ntrials must be >0'
                    path = self.to_repo_relative_path(path=relativePath, split=False)
                    if self.is_repository_directory(path):
                        return (True, 'Directory is already tracked in repository')
                    allowed, reason = self.is_name_allowed(path)
                    if not allowed:
                        if raiseError:
                            raise Exception(reason)
                        return (False, reason)
                    acquired, repoLockId = self._Repository__locker.acquire_lock(path=(self._Repository__path), timeout=(self.timeout))
                    m = acquired or 'code %s. Unable to aquire the lock to add directory. You may try again!' % (repoLockId,)
                    if raiseError:
                        raise Exception(m)
                    return (False, m)
                for _trial in range(ntrials):
                    try:
                        repo = self._Repository__load_repository_pickle_file(os.path.join(self._Repository__path, self._Repository__repoFile))
                        self._Repository__repo['walk_repo'] = repo['walk_repo']
                    except Exception as err:
                        try:
                            error = str(err)
                            if self.DEBUG_PRINT_FAILED_TRIALS:
                                print('Trial %i failed in Repository.%s (%s). Set Repository.DEBUG_PRINT_FAILED_TRIALS to False to mute' % (_trial, inspect.stack()[1][3], str(error)))
                        finally:
                            err = None
                            del err

                    else:
                        error = None
                        break

                if error is not None:
                    self._Repository__locker.release_lock(repoLockId)
                    if raiseError:
                        raise AssertionError(Exception(error))
                    return (
                     False, error)
                error = None
                posList = self._Repository__repo['walk_repo']
                dirPath = self._Repository__path
                spath = path.split(os.sep)
                for idx, name in enumerate(spath):
                    dirLockId = None
                    if dirPath != self._Repository__path:
                        acquired, dirLockId = self._Repository__locker.acquire_lock(path=dirPath, timeout=(self.timeout))
                        if not acquired:
                            error = "Code %s. Unable to aquire the lock when adding '%s'. All prior relative directories were added. You may try again, to finish adding directory" % (dirLockId, dirPath)
                            break
                        for _trial in range(ntrials):
                            try:
                                dirPath = os.path.join(dirPath, name)
                                riPath = os.path.join(dirPath, self._Repository__dirInfo)
                                dList = [d for d in posList if isinstance(d, dict)]
                                dList = [d for d in dList if name in d]
                                if not len(dList):
                                    if clean and os.path.exists(dirPath):
                                        try:
                                            shutil.rmtree(dirPath, ignore_errors=True)
                                        except Exception as err:
                                            try:
                                                error = "Unable to clean directory '%s' (%s)" % (dirPath, err)
                                                break
                                            finally:
                                                err = None
                                                del err

                                if not os.path.exists(dirPath):
                                    try:
                                        os.mkdir(dirPath)
                                    except Exception as err:
                                        try:
                                            error = "Unable to create directory '%s' (%s)" % (dirPath, err)
                                            break
                                        finally:
                                            err = None
                                            del err

                                self._Repository__save_dirinfo(description=([None, description][(idx == len(spath) - 1)]), dirInfoPath=riPath,
                                  create=True)
                                if not len(dList):
                                    rsd = {name: []}
                                    posList.append(rsd)
                                    posList = rsd[name]
                                else:
                                    assert len(dList) == 1, "Same directory name dict is found twice. This should'n have happened. Report issue"
                                    posList = dList[0][name]
                            except Exception as err:
                                try:
                                    error = "Unable to create directory '%s' info file (%s)" % (dirPath, str(err))
                                    if self.DEBUG_PRINT_FAILED_TRIALS:
                                        print('Trial %i failed in Repository.%s (%s). Set Repository.DEBUG_PRINT_FAILED_TRIALS to False to mute' % (_trial, inspect.stack()[1][3], str(error)))
                                finally:
                                    err = None
                                    del err

                            else:
                                break

                        if dirLockId is not None:
                            self._Repository__locker.release_lock(dirLockId)
                        if error is not None:
                            break

                if error is None:
                    try:
                        _, error = self._Repository__save_repository_pickle_file(lockFirst=False, raiseError=False)
                    except Exception as err:
                        try:
                            error = str(err)
                        finally:
                            err = None
                            del err

            if dirLockId is not None:
                self._Repository__locker.release_lock(dirLockId)
            self._Repository__locker.release_lock(repoLockId)
            if not error is None:
                if raiseError:
                    raise AssertionError(error)
        return (
         error is None, error)

    def get_repository_parent_directory(self, relativePath):
        """
        Get repository parent directory list copy.

        :Parameters:
            #. relativePath (string): The relative to the repository path .

        :Returns:
            #. dirList (None, list): List of directories and files in repository
               parent directory. If directory is not tracked in repository
               None is returned
        """
        return copy.deepcopy(self._Repository__get_repository_parent_directory(relativePath))

    @path_required
    def remove_directory(self, relativePath, clean=False, raiseError=True, ntrials=3):
        """
        Remove directory from repository tracking.

        :Parameters:
            #. relativePath (string): The relative to the repository path of the
               directory to remove from the repository.
            #. clean (boolean): Whether to os remove directory. If False only
               tracked files will be removed along with left empty directories.
            #. raiseError (boolean): Whether to raise encountered error instead
               of returning failure.
            #. ntrials (int): After aquiring all locks, ntrials is the maximum
               number of trials allowed before failing.
               In rare cases, when multiple processes
               are accessing the same repository components, different processes
               can alter repository components between successive lock releases
               of some other process. Bigger number of trials lowers the
               likelyhood of failure due to multiple processes same time
               alteration.

        :Returns:
            #. success (boolean): Whether removing the directory was successful.
            #. reason (None, string): Reason why directory was not removed.
        """
        if not isinstance(raiseError, bool):
            raise AssertionError('raiseError must be boolean')
        else:
            if not isinstance(clean, bool):
                raise AssertionError('clean must be boolean')
            else:
                if not isinstance(ntrials, int):
                    raise AssertionError('ntrials must be integer')
                else:
                    if not ntrials > 0:
                        raise AssertionError('ntrials must be >0')
                    else:
                        relativePath = self.to_repo_relative_path(path=relativePath, split=False)
                        parentPath, dirName = os.path.split(relativePath)
                        if relativePath == '':
                            return (False, 'Removing main repository directory is not allowed')
                        if not self.is_repository_directory(relativePath):
                            return (False, "Given relative path '%s' is not a repository path" % relativePath)
                        realPath = os.path.join(self._Repository__path, relativePath)
                        error = os.path.isdir(realPath) or "Repository relative directory '%s' seems to be missing. call maintain_repository to fix all issues"
                        if raiseError:
                            raise AssertionError(error)
                        return (
                         False, error)
                    acquired, dirLockId = self._Repository__locker.acquire_lock(path=(os.path.join(self._Repository__path, parentPath)), timeout=(self.timeout))
                    error = acquired or "Code %s. Unable to aquire the lock when removing '%s'. All prior relative directories were added. You may try again, to finish removing directory" % (dirLockId, realPath)
                    if raiseError:
                        raise AssertionError(error)
                    return (
                     False, error)
                acquired, repoLockId = self._Repository__locker.acquire_lock(path=(self._Repository__path), timeout=(self.timeout))
                m = acquired or 'code %s. Unable to aquire the repository lock. You may try again!' % (repoLockId,)
                assert raiseError, Exception(m)
                return (
                 False, m)
            for _trial in range(ntrials):
                error = None
                try:
                    dirList = self._Repository__get_repository_parent_directory(relativePath=relativePath)
                    assert dirList is not None, "Given relative path '%s' is not a repository directory" % (relativePath,)
                    stateBefore = self.get_repository_state(relaPath=parentPath)
                    _files = [f for f in dirList if isinstance(f, basestring)]
                    _dirs = [d for d in dirList if isinstance(d, dict)]
                    _dirs = [d for d in dirList if dirName not in d]
                    _ = [dirList.pop(0) for _ in range(len(dirList))]
                    dirList.extend(_files)
                    dirList.extend(_dirs)
                    if clean:
                        shutil.rmtree(realPath)
                    else:
                        stateAfter = self.get_repository_state(relaPath=parentPath)
                    success, errors = self._Repository__clean_before_after(stateBefore=stateBefore, stateAfter=stateAfter, keepNoneEmptyDirectory=True)
                    assert success, '\n'.join(errors)
                except Exception as err:
                    try:
                        error = str(err)
                        if self.DEBUG_PRINT_FAILED_TRIALS:
                            print('Trial %i failed in Repository.%s (%s). Set Repository.DEBUG_PRINT_FAILED_TRIALS to False to mute' % (_trial, inspect.stack()[1][3], str(error)))
                    finally:
                        err = None
                        del err

                break

            if error is None:
                _, error = self._Repository__save_repository_pickle_file(lockFirst=False, raiseError=False)
            self._Repository__locker.release_lock(dirLockId)
            self._Repository__locker.release_lock(repoLockId)
            if not error is None:
                if raiseError:
                    raise AssertionError("Unable to remove directory after %i trials '%s' (%s)" % (relativePath, ntrials, error))
        return (
         error is None, error)

    @path_required
    def rename_directory(self, relativePath, newName, raiseError=True, ntrials=3):
        """
        Rename a directory in the repository. It insures renaming the directory in the system.

        :Parameters:
            #. relativePath (string): The relative to the repository path of
               the directory to be renamed.
            #. newName (string): The new directory name.
            #. raiseError (boolean): Whether to raise encountered error instead
               of returning failure.
            #. ntrials (int): After aquiring all locks, ntrials is the maximum
               number of trials allowed before failing.
               In rare cases, when multiple processes
               are accessing the same repository components, different processes
               can alter repository components between successive lock releases
               of some other process. Bigger number of trials lowers the
               likelyhood of failure due to multiple processes same time
               alteration.

        :Returns:
            #. success (boolean): Whether renaming the directory was successful.
            #. message (None, string): Some explanatory message or error reason
               why directory was not renamed.
        """
        if not isinstance(raiseError, bool):
            raise AssertionError('raiseError must be boolean')
        else:
            if not isinstance(ntrials, int):
                raise AssertionError('ntrials must be integer')
            else:
                if not ntrials > 0:
                    raise AssertionError('ntrials must be >0')
                else:
                    relativePath = self.to_repo_relative_path(path=relativePath, split=False)
                    parentPath, dirName = os.path.split(relativePath)
                    if relativePath == '':
                        error = 'Renaming main repository directory is not allowed'
                        if raiseError:
                            raise AssertionError(error)
                        return (
                         False, error)
                    realPath = os.path.join(self._Repository__path, relativePath)
                    newRealPath = os.path.join(os.path.dirname(realPath), newName)
                    if os.path.isdir(newRealPath):
                        error = "New directory path '%s' already exist" % (newRealPath,)
                        if raiseError:
                            raise AssertionError(error)
                        return (
                         False, error)
                    acquired, dirLockId = self._Repository__locker.acquire_lock((os.path.join(self._Repository__path, parentPath)), timeout=(self.timeout))
                    error = acquired or "Code %s. Unable to aquire repository lock when renaming '%s'. All prior directories were added. You may try again, to finish adding the directory" % (dirLockId, dirPath)
                    if raiseError:
                        raise AssertionError(error)
                    return (
                     False, error)
                error = None
                acquired, repoLockId = self._Repository__locker.acquire_lock(path=(self._Repository__path), timeout=(self.timeout))
                m = acquired or "Code %s. Unable to aquire directory lock when renaming '%s'. All prior directories were added. You may try again, to finish adding the directory" % (repoLockId, dirPath)
                assert raiseError, Exception(m)
                return (
                 False, m)
            for _trial in range(ntrials):
                try:
                    repo = self._Repository__load_repository_pickle_file(os.path.join(self._Repository__path, self._Repository__repoFile))
                    self._Repository__repo['walk_repo'] = repo['walk_repo']
                except Exception as err:
                    try:
                        error = str(err)
                        if self.DEBUG_PRINT_FAILED_TRIALS:
                            print('Trial %i failed in Repository.%s (%s). Set Repository.DEBUG_PRINT_FAILED_TRIALS to False to mute' % (_trial, inspect.stack()[1][3], str(error)))
                    finally:
                        err = None
                        del err

                else:
                    error = None
                    break

            if error is not None:
                self._Repository__locker.release_lock(dirLockId)
                self._Repository__locker.release_lock(repoLockId)
                if raiseError:
                    raise AssertionError(Exception(error))
                return (
                 False, error)
            for _trial in range(ntrials):
                error = None
                try:
                    dirList = self._Repository__get_repository_parent_directory(relativePath=relativePath)
                    assert dirList is not None, "Given relative path '%s' is not a repository directory" % (relativePath,)
                    _dirDict = [nd for nd in dirList if isinstance(nd, dict)]
                    _dirDict = [nd for nd in _dirDict if dirName in nd]
                    assert len(_dirDict) == 1, 'This should not have happened. Directory not found in repository. Please report issue'
                    os.rename(realPath, newRealPath)
                    _dirDict[0][newName] = _dirDict[0][dirName]
                    _dirDict[0].pop(dirName)
                    self._Repository__save_dirinfo(description=None, dirInfoPath=parentPath, create=False)
                except Exception as err:
                    try:
                        error = str(err)
                        if self.DEBUG_PRINT_FAILED_TRIALS:
                            print('Trial %i failed in Repository.%s (%s). Set Repository.DEBUG_PRINT_FAILED_TRIALS to False to mute' % (_trial, inspect.stack()[1][3], str(error)))
                    finally:
                        err = None
                        del err

                else:
                    error = None
                    break

            if error is None:
                _, error = self._Repository__save_repository_pickle_file(lockFirst=False, raiseError=False)
            self._Repository__locker.release_lock(dirLockId)
            self._Repository__locker.release_lock(repoLockId)
            if not error is None:
                if raiseError:
                    raise AssertionError("Unable to rename directory '%s' to '%s' after %i trials (%s)" % (relativePath, newName, ntrials, error))
        return (
         error is None, error)

    @path_required
    def copy_directory(self, relativePath, newRelativePath, overwrite=False, raiseError=True, ntrials=3):
        """
        Copy a directory in the repository. New directory must not exist.

        :Parameters:
            #. relativePath (string): The relative to the repository path of
               the directory to be copied.
            #. newRelativePath (string): The new directory relative path.
            #. overwrite (boolean): Whether to overwrite existing but not tracked
               directory in repository.
            #. raiseError (boolean): Whether to raise encountered error instead
               of returning failure.
            #. ntrials (int): After aquiring all locks, ntrials is the maximum
               number of trials allowed before failing.
               In rare cases, when multiple processes
               are accessing the same repository components, different processes
               can alter repository components between successive lock releases
               of some other process. Bigger number of trials lowers the
               likelyhood of failure due to multiple processes same time
               alteration.

        :Returns:
            #. success (boolean): Whether renaming the directory was successful.
            #. message (None, string): Some explanatory message or error reason
               why directory was not renamed.
        """
        if not isinstance(raiseError, bool):
            raise AssertionError('raiseError must be boolean')
        else:
            if not isinstance(overwrite, bool):
                raise AssertionError('overwrite must be boolean')
            else:
                if not isinstance(ntrials, int):
                    raise AssertionError('ntrials must be integer')
                else:
                    if not ntrials > 0:
                        raise AssertionError('ntrials must be >0')
                    else:
                        relativePath = self.to_repo_relative_path(path=relativePath, split=False)
                        if relativePath == '':
                            m = 'Copying to repository main directory is not possible'
                            if raiseError:
                                raise AssertionError(m)
                            return (
                             False, m)
                        realPath = os.path.join(self._Repository__path, relativePath)
                        parentRealPath, dirName = os.path.split(realPath)
                        parentRelativePath = os.path.dirname(relativePath)
                        if not self.is_repository_directory(relativePath):
                            m = "Directory '%s' is not a tracked repository directory" % relativePath
                            if raiseError:
                                raise AssertionError(m)
                            return (
                             False, m)
                        newRelativePath = self.to_repo_relative_path(path=newRelativePath, split=False)
                        newRealPath = os.path.join(self._Repository__path, newRelativePath)
                        newParentRealPath, newDirName = os.path.split(newRealPath)
                        newParentRelativePath = os.path.dirname(newRelativePath)
                        if realPath == newRealPath:
                            m = 'Copying to the same directory is not possible'
                            if raiseError:
                                raise AssertionError(m)
                            return (
                             False, m)
                        if self.is_repository_directory(newRelativePath):
                            m = "Directory '%s' is a tracked repository directory" % newRelativePath
                            if raiseError:
                                raise AssertionError(m)
                            return (
                             False, m)
                        if os.path.isdir(newRealPath):
                            if overwrite:
                                try:
                                    shutil.rmtree(newRealPath)
                                except Exception as err:
                                    try:
                                        if raiseError:
                                            raise AssertionError(str(err))
                                        return (
                                         False, str(err))
                                    finally:
                                        err = None
                                        del err

                            else:
                                error = "New directory path '%s' already exist on disk. Set overwrite to True" % (newRealPath,)
                                if raiseError:
                                    raise AssertionError(error)
                                return (
                                 False, error)
                        try:
                            success, reason = self.add_directory(newParentRelativePath, raiseError=False, ntrials=ntrials)
                        except Exception as err:
                            try:
                                reason = 'Unable to add directory (%s)' % str(err)
                                success = False
                            finally:
                                err = None
                                del err

                        if not success:
                            if raiseError:
                                raise AssertionError(reason)
                            return (
                             False, reason)
                        acquired, repoLockId = self._Repository__locker.acquire_lock(path=(self._Repository__path), timeout=(self.timeout))
                        if not acquired:
                            m = 'code %s. Unable to aquire the repository lock. You may try again!' % (repoLockId,)
                            assert raiseError, Exception(m)
                            return (
                             False, m)
                        try:
                            repo = self._Repository__load_repository_pickle_file(os.path.join(self._Repository__path, self._Repository__repoFile))
                            self._Repository__repo['walk_repo'] = repo['walk_repo']
                        except Exception as err:
                            try:
                                self._Repository__locker.release_lock(repoLockId)
                                if raiseError:
                                    raise AssertionError(Exception(str(err)))
                                return (
                                 False, m)
                            finally:
                                err = None
                                del err

                    acquired, dirLockId = self._Repository__locker.acquire_lock(path=parentRealPath, timeout=(self.timeout))
                    acquired or self._Repository__locker.release_lock(repoLockId)
                    error = "Code %s. Unable to aquire the lock when adding '%s'. All prior directories were added. You may try again, to finish adding directory" % (dirLockId, dirPath)
                    if raiseError:
                        raise AssertionError(error)
                    return (
                     False, error)
                newDirLockId = None
                if parentRealPath != newParentRealPath:
                    acquired, newDirLockId = self._Repository__locker.acquire_lock(path=newParentRealPath, timeout=(self.timeout))
                    if not acquired:
                        self._Repository__locker.release_lock(dirLockId)
                        self._Repository__locker.release_lock(repoLockId)
                        error = "Code %s. Unable to aquire the lock when adding '%s'. All prior directories were added. You may try again, to finish adding directory" % (newDirLockId, dirPath)
                        if raiseError:
                            raise AssertionError(error)
                        return (
                         False, error)
            error = None
            for _trial in range(ntrials):
                try:
                    assert self.is_repository_directory(relativePath), "Directory '%s' is not anymore a tracked repository directory" % relativePath
                    if self.is_repository_directory(newRelativePath):
                        raise AssertionError("Directory '%s' has become a tracked repository directory" % relativePath)
                    dirList = self._Repository__get_repository_parent_directory(relativePath=relativePath)
                    assert dirList is not None, "Given relative path '%s' is not a repository directory" % (relativePath,)
                    newDirList = self._Repository__get_repository_parent_directory(relativePath=newRelativePath)
                    assert newDirList is not None, "Given new relative path '%s' parent directory is not a repository directory" % (newRelativePath,)
                    _dirDict = [nd for nd in dirList if isinstance(nd, dict)]
                    _dirDict = [nd for nd in _dirDict if dirName in nd]
                    assert len(_dirDict) == 1, 'This should not have happened. Directory not found in repository. Please report issue'
                    _dirDict = _dirDict[0]
                    _newDirDict = [nd for nd in newDirList if isinstance(nd, dict)]
                    _newDirDict = [nd for nd in _newDirDict if newDirName in nd]
                    assert len(_newDirDict) == 0, 'This should not have happened. New directory is found in repository. Please report issue'
                    _newDirDict = copy.deepcopy(_dirDict)
                    if dirName != newDirName:
                        _newDirDict[newDirName] = _newDirDict.pop(dirName)
                    _ = copy_tree(src=realPath, dst=newRealPath, srcDirDict=_dirDict, filAttr=[
                     self._Repository__fileInfo, self._Repository__fileClass],
                      dirAttr=[
                     self._Repository__dirInfo, self._Repository__repoFile])
                    newDirList.append(_newDirDict)
                    self._Repository__save_dirinfo(description=None, dirInfoPath=newParentRelativePath, create=False)
                except Exception as err:
                    try:
                        error = str(err)
                        if self.DEBUG_PRINT_FAILED_TRIALS:
                            print('Trial %i failed in Repository.%s (%s). Set Repository.DEBUG_PRINT_FAILED_TRIALS to False to mute' % (_trial, inspect.stack()[1][3], str(error)))
                    finally:
                        err = None
                        del err

                else:
                    error = None
                    break

            if error is None:
                _, error = self._Repository__save_repository_pickle_file(lockFirst=False, raiseError=False)
            self._Repository__locker.release_lock(dirLockId)
            self._Repository__locker.release_lock(repoLockId)
            if newDirLockId is not None:
                self._Repository__locker.release_lock(newDirLockId)
            if not error is None:
                if raiseError:
                    raise AssertionError("Unable to copy directory '%s' to '%s' after %i trials (%s)" % (relativePath, newRelativePath, ntrials, error))
        return (
         error is None, error)

    @path_required
    def dump_file--- This code section failed: ---

 L.2294         0  LOAD_GLOBAL              isinstance
                2  LOAD_FAST                'raiseError'
                4  LOAD_GLOBAL              bool
                6  CALL_FUNCTION_2       2  ''
                8  POP_JUMP_IF_TRUE     18  'to 18'
               10  LOAD_ASSERT              AssertionError
               12  LOAD_STR                 'raiseError must be boolean'
               14  CALL_FUNCTION_1       1  ''
               16  RAISE_VARARGS_1       1  ''
             18_0  COME_FROM             8  '8'

 L.2295        18  LOAD_GLOBAL              isinstance
               20  LOAD_FAST                'replace'
               22  LOAD_GLOBAL              bool
               24  CALL_FUNCTION_2       2  ''
               26  POP_JUMP_IF_TRUE     36  'to 36'
               28  LOAD_ASSERT              AssertionError
               30  LOAD_STR                 'replace must be boolean'
               32  CALL_FUNCTION_1       1  ''
               34  RAISE_VARARGS_1       1  ''
             36_0  COME_FROM            26  '26'

 L.2296        36  LOAD_GLOBAL              isinstance
               38  LOAD_FAST                'ntrials'
               40  LOAD_GLOBAL              int
               42  CALL_FUNCTION_2       2  ''
               44  POP_JUMP_IF_TRUE     54  'to 54'
               46  LOAD_ASSERT              AssertionError
               48  LOAD_STR                 'ntrials must be integer'
               50  CALL_FUNCTION_1       1  ''
               52  RAISE_VARARGS_1       1  ''
             54_0  COME_FROM            44  '44'

 L.2297        54  LOAD_FAST                'ntrials'
               56  LOAD_CONST               0
               58  COMPARE_OP               >
               60  POP_JUMP_IF_TRUE     70  'to 70'
               62  LOAD_ASSERT              AssertionError
               64  LOAD_STR                 'ntrials must be >0'
               66  CALL_FUNCTION_1       1  ''
               68  RAISE_VARARGS_1       1  ''
             70_0  COME_FROM            60  '60'

 L.2298        70  LOAD_FAST                'description'
               72  LOAD_CONST               None
               74  COMPARE_OP               is
               76  POP_JUMP_IF_FALSE    82  'to 82'

 L.2299        78  LOAD_STR                 ''
               80  STORE_FAST               'description'
             82_0  COME_FROM            76  '76'

 L.2300        82  LOAD_GLOBAL              isinstance
               84  LOAD_FAST                'description'
               86  LOAD_GLOBAL              basestring
               88  CALL_FUNCTION_2       2  ''
               90  POP_JUMP_IF_TRUE    100  'to 100'
               92  LOAD_ASSERT              AssertionError
               94  LOAD_STR                 'description must be None or a string'
               96  CALL_FUNCTION_1       1  ''
               98  RAISE_VARARGS_1       1  ''
            100_0  COME_FROM            90  '90'

 L.2302       100  LOAD_FAST                'pull'
              102  LOAD_CONST               None
              104  COMPARE_OP               is
              106  POP_JUMP_IF_FALSE   158  'to 158'
              108  LOAD_FAST                'dump'
              110  LOAD_CONST               None
              112  COMPARE_OP               is-not
              114  POP_JUMP_IF_FALSE   158  'to 158'

 L.2303       116  LOAD_FAST                'dump'
              118  LOAD_METHOD              startswith
              120  LOAD_STR                 'pickle'
              122  CALL_METHOD_1         1  ''
              124  POP_JUMP_IF_TRUE    154  'to 154'
              126  LOAD_FAST                'dump'
              128  LOAD_METHOD              startswith
              130  LOAD_STR                 'dill'
              132  CALL_METHOD_1         1  ''
              134  POP_JUMP_IF_TRUE    154  'to 154'
              136  LOAD_FAST                'dump'
              138  LOAD_METHOD              startswith
              140  LOAD_STR                 'numpy'
              142  CALL_METHOD_1         1  ''
              144  POP_JUMP_IF_TRUE    154  'to 154'
              146  LOAD_FAST                'dump'
              148  LOAD_STR                 'json'
              150  COMPARE_OP               ==
              152  POP_JUMP_IF_FALSE   158  'to 158'
            154_0  COME_FROM           144  '144'
            154_1  COME_FROM           134  '134'
            154_2  COME_FROM           124  '124'

 L.2304       154  LOAD_FAST                'dump'
              156  STORE_FAST               'pull'
            158_0  COME_FROM           152  '152'
            158_1  COME_FROM           114  '114'
            158_2  COME_FROM           106  '106'

 L.2305       158  LOAD_GLOBAL              get_dump_method
              160  LOAD_FAST                'dump'
              162  LOAD_FAST                'self'
              164  LOAD_ATTR                _DEFAULT_PICKLE_PROTOCOL
              166  LOAD_CONST               ('protocol',)
              168  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              170  STORE_FAST               'dump'

 L.2306       172  LOAD_GLOBAL              get_pull_method
              174  LOAD_FAST                'pull'
              176  CALL_FUNCTION_1       1  ''
              178  STORE_FAST               'pull'

 L.2308       180  LOAD_FAST                'self'
              182  LOAD_ATTR                to_repo_relative_path
              184  LOAD_FAST                'relativePath'
              186  LOAD_CONST               False
              188  LOAD_CONST               ('path', 'split')
              190  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              192  STORE_FAST               'relativePath'

 L.2309       194  LOAD_GLOBAL              os
              196  LOAD_ATTR                path
              198  LOAD_METHOD              join
              200  LOAD_FAST                'self'
              202  LOAD_ATTR                _Repository__path
              204  LOAD_FAST                'relativePath'
              206  CALL_METHOD_2         2  ''
              208  STORE_FAST               'savePath'

 L.2310       210  LOAD_GLOBAL              os
              212  LOAD_ATTR                path
              214  LOAD_METHOD              split
              216  LOAD_FAST                'savePath'
              218  CALL_METHOD_1         1  ''
              220  UNPACK_SEQUENCE_2     2 
              222  STORE_FAST               'fPath'
              224  STORE_FAST               'fName'

 L.2312       226  LOAD_FAST                'self'
              228  LOAD_METHOD              is_name_allowed
              230  LOAD_FAST                'savePath'
              232  CALL_METHOD_1         1  ''
              234  UNPACK_SEQUENCE_2     2 
              236  STORE_FAST               'success'
              238  STORE_FAST               'reason'

 L.2313       240  LOAD_FAST                'success'
          242_244  POP_JUMP_IF_TRUE    268  'to 268'

 L.2314       246  LOAD_FAST                'raiseError'
          248_250  POP_JUMP_IF_FALSE   260  'to 260'
              252  LOAD_GLOBAL              AssertionError
              254  LOAD_FAST                'reason'
              256  CALL_FUNCTION_1       1  ''
              258  RAISE_VARARGS_1       1  ''
            260_0  COME_FROM           248  '248'

 L.2315       260  LOAD_CONST               False
              262  LOAD_FAST                'reason'
              264  BUILD_TUPLE_2         2 
              266  RETURN_VALUE     
            268_0  COME_FROM           242  '242'

 L.2317       268  SETUP_EXCEPT        294  'to 294'

 L.2318       270  LOAD_FAST                'self'
              272  LOAD_ATTR                add_directory
              274  LOAD_FAST                'fPath'
              276  LOAD_CONST               False
              278  LOAD_FAST                'ntrials'
              280  LOAD_CONST               ('raiseError', 'ntrials')
              282  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              284  UNPACK_SEQUENCE_2     2 
              286  STORE_FAST               'success'
              288  STORE_FAST               'reason'
              290  POP_BLOCK        
              292  JUMP_FORWARD        346  'to 346'
            294_0  COME_FROM_EXCEPT    268  '268'

 L.2319       294  DUP_TOP          
              296  LOAD_GLOBAL              Exception
              298  COMPARE_OP               exception-match
          300_302  POP_JUMP_IF_FALSE   344  'to 344'
              304  POP_TOP          
              306  STORE_FAST               'err'
              308  POP_TOP          
              310  SETUP_FINALLY       332  'to 332'

 L.2320       312  LOAD_STR                 'Unable to add directory (%s)'
              314  LOAD_GLOBAL              str
              316  LOAD_FAST                'err'
              318  CALL_FUNCTION_1       1  ''
              320  BINARY_MODULO    
              322  STORE_FAST               'reason'

 L.2321       324  LOAD_CONST               False
              326  STORE_FAST               'success'
              328  POP_BLOCK        
              330  LOAD_CONST               None
            332_0  COME_FROM_FINALLY   310  '310'
              332  LOAD_CONST               None
              334  STORE_FAST               'err'
              336  DELETE_FAST              'err'
              338  END_FINALLY      
              340  POP_EXCEPT       
              342  JUMP_FORWARD        346  'to 346'
            344_0  COME_FROM           300  '300'
              344  END_FINALLY      
            346_0  COME_FROM           342  '342'
            346_1  COME_FROM           292  '292'

 L.2322       346  LOAD_FAST                'success'
          348_350  POP_JUMP_IF_TRUE    374  'to 374'

 L.2323       352  LOAD_FAST                'raiseError'
          354_356  POP_JUMP_IF_FALSE   366  'to 366'
              358  LOAD_GLOBAL              AssertionError
              360  LOAD_FAST                'reason'
              362  CALL_FUNCTION_1       1  ''
              364  RAISE_VARARGS_1       1  ''
            366_0  COME_FROM           354  '354'

 L.2324       366  LOAD_CONST               False
              368  LOAD_FAST                'reason'
              370  BUILD_TUPLE_2         2 
              372  RETURN_VALUE     
            374_0  COME_FROM           348  '348'

 L.2326       374  LOAD_FAST                'self'
              376  LOAD_ATTR                _Repository__locker
              378  LOAD_ATTR                acquire_lock
              380  LOAD_FAST                'self'
              382  LOAD_ATTR                _Repository__path
              384  LOAD_FAST                'self'
              386  LOAD_ATTR                timeout
              388  LOAD_CONST               ('path', 'timeout')
              390  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              392  UNPACK_SEQUENCE_2     2 
              394  STORE_FAST               'acquired'
              396  STORE_FAST               'repoLockId'

 L.2327       398  LOAD_FAST                'acquired'
          400_402  POP_JUMP_IF_TRUE    440  'to 440'

 L.2328       404  LOAD_STR                 'code %s. Unable to aquire the repository lock. You may try again!'
              406  LOAD_FAST                'repoLockId'
              408  BUILD_TUPLE_1         1 
              410  BINARY_MODULO    
              412  STORE_FAST               'm'

 L.2329       414  LOAD_FAST                'raiseError'
          416_418  POP_JUMP_IF_TRUE    432  'to 432'
              420  LOAD_ASSERT              AssertionError
              422  LOAD_GLOBAL              Exception
              424  LOAD_FAST                'm'
              426  CALL_FUNCTION_1       1  ''
              428  CALL_FUNCTION_1       1  ''
              430  RAISE_VARARGS_1       1  ''
            432_0  COME_FROM           416  '416'

 L.2330       432  LOAD_CONST               False
              434  LOAD_FAST                'm'
              436  BUILD_TUPLE_2         2 
              438  RETURN_VALUE     
            440_0  COME_FROM           400  '400'

 L.2332       440  LOAD_FAST                'self'
              442  LOAD_ATTR                _Repository__locker
              444  LOAD_ATTR                acquire_lock
              446  LOAD_FAST                'savePath'
              448  LOAD_FAST                'self'
              450  LOAD_ATTR                timeout
              452  LOAD_CONST               ('path', 'timeout')
              454  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              456  UNPACK_SEQUENCE_2     2 
              458  STORE_FAST               'acquired'
              460  STORE_FAST               'fileLockId'

 L.2333       462  LOAD_FAST                'acquired'
          464_466  POP_JUMP_IF_TRUE    514  'to 514'

 L.2334       468  LOAD_FAST                'self'
              470  LOAD_ATTR                _Repository__locker
              472  LOAD_METHOD              release_lock
              474  LOAD_FAST                'repoLockId'
              476  CALL_METHOD_1         1  ''
              478  POP_TOP          

 L.2335       480  LOAD_STR                 "Code %s. Unable to aquire the lock when dumping '%s'"
              482  LOAD_FAST                'fileLockId'
              484  LOAD_FAST                'relativePath'
              486  BUILD_TUPLE_2         2 
              488  BINARY_MODULO    
              490  STORE_FAST               'error'

 L.2336       492  LOAD_FAST                'raiseError'
          494_496  POP_JUMP_IF_FALSE   506  'to 506'
              498  LOAD_GLOBAL              AssertionError
              500  LOAD_FAST                'error'
              502  CALL_FUNCTION_1       1  ''
              504  RAISE_VARARGS_1       1  ''
            506_0  COME_FROM           494  '494'

 L.2337       506  LOAD_CONST               False
              508  LOAD_FAST                'error'
              510  BUILD_TUPLE_2         2 
              512  RETURN_VALUE     
            514_0  COME_FROM           464  '464'

 L.2339       514  SETUP_LOOP          670  'to 670'
              516  LOAD_GLOBAL              range
              518  LOAD_FAST                'ntrials'
              520  CALL_FUNCTION_1       1  ''
              522  GET_ITER         
              524  FOR_ITER            668  'to 668'
              526  STORE_FAST               '_trial'

 L.2340       528  SETUP_EXCEPT        572  'to 572'

 L.2341       530  LOAD_FAST                'self'
              532  LOAD_METHOD              _Repository__load_repository_pickle_file
              534  LOAD_GLOBAL              os
              536  LOAD_ATTR                path
              538  LOAD_METHOD              join
              540  LOAD_FAST                'self'
              542  LOAD_ATTR                _Repository__path
              544  LOAD_FAST                'self'
              546  LOAD_ATTR                _Repository__repoFile
              548  CALL_METHOD_2         2  ''
              550  CALL_METHOD_1         1  ''
              552  STORE_FAST               'repo'

 L.2342       554  LOAD_FAST                'repo'
              556  LOAD_STR                 'walk_repo'
              558  BINARY_SUBSCR    
              560  LOAD_FAST                'self'
              562  LOAD_ATTR                _Repository__repo
              564  LOAD_STR                 'walk_repo'
              566  STORE_SUBSCR     
              568  POP_BLOCK        
              570  JUMP_FORWARD        658  'to 658'
            572_0  COME_FROM_EXCEPT    528  '528'

 L.2343       572  DUP_TOP          
              574  LOAD_GLOBAL              Exception
              576  COMPARE_OP               exception-match
          578_580  POP_JUMP_IF_FALSE   656  'to 656'
              582  POP_TOP          
              584  STORE_FAST               'err'
              586  POP_TOP          
              588  SETUP_FINALLY       644  'to 644'

 L.2344       590  LOAD_GLOBAL              str
              592  LOAD_FAST                'err'
              594  CALL_FUNCTION_1       1  ''
              596  STORE_FAST               'error'

 L.2345       598  LOAD_FAST                'self'
              600  LOAD_ATTR                DEBUG_PRINT_FAILED_TRIALS
          602_604  POP_JUMP_IF_FALSE   640  'to 640'

 L.2345       606  LOAD_GLOBAL              print
              608  LOAD_STR                 'Trial %i failed in Repository.%s (%s). Set Repository.DEBUG_PRINT_FAILED_TRIALS to False to mute'
              610  LOAD_FAST                '_trial'
              612  LOAD_GLOBAL              inspect
              614  LOAD_METHOD              stack
              616  CALL_METHOD_0         0  ''
              618  LOAD_CONST               1
              620  BINARY_SUBSCR    
              622  LOAD_CONST               3
              624  BINARY_SUBSCR    
              626  LOAD_GLOBAL              str
              628  LOAD_FAST                'error'
              630  CALL_FUNCTION_1       1  ''
              632  BUILD_TUPLE_3         3 
              634  BINARY_MODULO    
              636  CALL_FUNCTION_1       1  ''
              638  POP_TOP          
            640_0  COME_FROM           602  '602'
              640  POP_BLOCK        
              642  LOAD_CONST               None
            644_0  COME_FROM_FINALLY   588  '588'
              644  LOAD_CONST               None
              646  STORE_FAST               'err'
              648  DELETE_FAST              'err'
              650  END_FINALLY      
              652  POP_EXCEPT       
              654  JUMP_BACK           524  'to 524'
            656_0  COME_FROM           578  '578'
              656  END_FINALLY      
            658_0  COME_FROM           570  '570'

 L.2347       658  LOAD_CONST               None
              660  STORE_FAST               'error'

 L.2348       662  BREAK_LOOP       
          664_666  JUMP_BACK           524  'to 524'
              668  POP_BLOCK        
            670_0  COME_FROM_LOOP      514  '514'

 L.2349       670  LOAD_FAST                'error'
              672  LOAD_CONST               None
              674  COMPARE_OP               is-not
          676_678  POP_JUMP_IF_FALSE   730  'to 730'

 L.2350       680  LOAD_FAST                'self'
              682  LOAD_ATTR                _Repository__locker
              684  LOAD_METHOD              release_lock
              686  LOAD_GLOBAL              dirLockId
              688  CALL_METHOD_1         1  ''
              690  POP_TOP          

 L.2351       692  LOAD_FAST                'self'
              694  LOAD_ATTR                _Repository__locker
              696  LOAD_METHOD              release_lock
              698  LOAD_FAST                'fileLockId'
              700  CALL_METHOD_1         1  ''
              702  POP_TOP          

 L.2352       704  LOAD_FAST                'raiseError'
          706_708  POP_JUMP_IF_FALSE   722  'to 722'
              710  LOAD_GLOBAL              AssertionError
              712  LOAD_GLOBAL              Exception
              714  LOAD_FAST                'error'
              716  CALL_FUNCTION_1       1  ''
              718  CALL_FUNCTION_1       1  ''
              720  RAISE_VARARGS_1       1  ''
            722_0  COME_FROM           706  '706'

 L.2353       722  LOAD_CONST               False
              724  LOAD_FAST                'error'
              726  BUILD_TUPLE_2         2 
              728  RETURN_VALUE     
            730_0  COME_FROM           676  '676'

 L.2355   730_732  SETUP_LOOP         1380  'to 1380'
              734  LOAD_GLOBAL              range
              736  LOAD_FAST                'ntrials'
              738  CALL_FUNCTION_1       1  ''
              740  GET_ITER         
          742_744  FOR_ITER           1378  'to 1378'
              746  STORE_FAST               '_trial'

 L.2356       748  LOAD_CONST               None
              750  STORE_FAST               'error'

 L.2357   752_754  SETUP_EXCEPT       1214  'to 1214'

 L.2358       756  LOAD_FAST                'self'
              758  LOAD_METHOD              is_repository_file
              760  LOAD_FAST                'relativePath'
              762  CALL_METHOD_1         1  ''
              764  UNPACK_SEQUENCE_4     4 
              766  STORE_FAST               'isRepoFile'
              768  STORE_FAST               'fileOnDisk'
              770  STORE_FAST               'infoOnDisk'
              772  STORE_FAST               'classOnDisk'

 L.2359       774  LOAD_FAST                'isRepoFile'
          776_778  POP_JUMP_IF_FALSE   794  'to 794'

 L.2360       780  LOAD_FAST                'replace'
          782_784  POP_JUMP_IF_TRUE    794  'to 794'
              786  LOAD_ASSERT              AssertionError
              788  LOAD_STR                 'file is a registered repository file. set replace to True to replace'
              790  CALL_FUNCTION_1       1  ''
              792  RAISE_VARARGS_1       1  ''
            794_0  COME_FROM           782  '782'
            794_1  COME_FROM           776  '776'

 L.2361       794  LOAD_GLOBAL              os
              796  LOAD_ATTR                path
              798  LOAD_METHOD              join
              800  LOAD_FAST                'self'
              802  LOAD_ATTR                _Repository__path
              804  LOAD_GLOBAL              os
              806  LOAD_ATTR                path
              808  LOAD_METHOD              dirname
              810  LOAD_FAST                'relativePath'
              812  CALL_METHOD_1         1  ''
              814  LOAD_FAST                'self'
              816  LOAD_ATTR                _Repository__fileInfo
              818  LOAD_FAST                'fName'
              820  BINARY_MODULO    
              822  CALL_METHOD_3         3  ''
              824  STORE_FAST               'fileInfoPath'

 L.2362       826  LOAD_FAST                'isRepoFile'
          828_830  POP_JUMP_IF_FALSE   912  'to 912'
              832  LOAD_FAST                'fileOnDisk'
          834_836  POP_JUMP_IF_FALSE   912  'to 912'

 L.2363       838  LOAD_GLOBAL              open
              840  LOAD_FAST                'fileInfoPath'
              842  LOAD_STR                 'rb'
              844  CALL_FUNCTION_2       2  ''
              846  SETUP_WITH          864  'to 864'
              848  STORE_FAST               'fd'

 L.2364       850  LOAD_GLOBAL              pickle
              852  LOAD_METHOD              load
              854  LOAD_FAST                'fd'
              856  CALL_METHOD_1         1  ''
              858  STORE_FAST               'info'
              860  POP_BLOCK        
              862  LOAD_CONST               None
            864_0  COME_FROM_WITH      846  '846'
              864  WITH_CLEANUP_START
              866  WITH_CLEANUP_FINISH
              868  END_FINALLY      

 L.2365       870  LOAD_FAST                'info'
              872  LOAD_STR                 'repository_unique_name'
              874  BINARY_SUBSCR    
              876  LOAD_FAST                'self'
              878  LOAD_ATTR                _Repository__repo
              880  LOAD_STR                 'repository_unique_name'
              882  BINARY_SUBSCR    
              884  COMPARE_OP               ==
          886_888  POP_JUMP_IF_TRUE    898  'to 898'
              890  LOAD_ASSERT              AssertionError
              892  LOAD_STR                 'it seems that file was created by another repository'
              894  CALL_FUNCTION_1       1  ''
              896  RAISE_VARARGS_1       1  ''
            898_0  COME_FROM           886  '886'

 L.2366       898  LOAD_GLOBAL              time
              900  LOAD_METHOD              time
              902  CALL_METHOD_0         0  ''
              904  LOAD_FAST                'info'
              906  LOAD_STR                 'last_update_utctime'
              908  STORE_SUBSCR     
              910  JUMP_FORWARD        946  'to 946'
            912_0  COME_FROM           834  '834'
            912_1  COME_FROM           828  '828'

 L.2368       912  LOAD_STR                 'repository_unique_name'
              914  LOAD_FAST                'self'
              916  LOAD_ATTR                _Repository__repo
              918  LOAD_STR                 'repository_unique_name'
              920  BINARY_SUBSCR    
              922  BUILD_MAP_1           1 
              924  STORE_FAST               'info'

 L.2369       926  LOAD_GLOBAL              time
              928  LOAD_METHOD              time
              930  CALL_METHOD_0         0  ''
              932  DUP_TOP          
              934  LOAD_FAST                'info'
              936  LOAD_STR                 'create_utctime'
              938  STORE_SUBSCR     
              940  LOAD_FAST                'info'
              942  LOAD_STR                 'last_update_utctime'
              944  STORE_SUBSCR     
            946_0  COME_FROM           910  '910'

 L.2370       946  LOAD_FAST                'dump'
              948  LOAD_FAST                'info'
              950  LOAD_STR                 'dump'
              952  STORE_SUBSCR     

 L.2371       954  LOAD_FAST                'pull'
              956  LOAD_FAST                'info'
              958  LOAD_STR                 'pull'
              960  STORE_SUBSCR     

 L.2372       962  LOAD_FAST                'description'
              964  LOAD_FAST                'info'
              966  LOAD_STR                 'description'
              968  STORE_SUBSCR     

 L.2374       970  LOAD_FAST                'isRepoFile'
          972_974  POP_JUMP_IF_TRUE    986  'to 986'

 L.2375       976  LOAD_FAST                'self'
              978  LOAD_METHOD              _Repository__get_repository_directory
              980  LOAD_FAST                'fPath'
              982  CALL_METHOD_1         1  ''
              984  STORE_FAST               'dirList'
            986_0  COME_FROM           972  '972'

 L.2377       986  LOAD_GLOBAL              my_exec
              988  LOAD_FAST                'dump'
              990  LOAD_STR                 'dump'
              992  LOAD_STR                 'dump'
              994  LOAD_CONST               ('name', 'description')
              996  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              998  STORE_FAST               'dumpFunc'

 L.2378      1000  LOAD_FAST                'dumpFunc'
             1002  LOAD_GLOBAL              str
             1004  LOAD_FAST                'savePath'
             1006  CALL_FUNCTION_1       1  ''
             1008  LOAD_FAST                'value'
             1010  LOAD_CONST               ('path', 'value')
             1012  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1014  POP_TOP          

 L.2380      1016  LOAD_GLOBAL              open
             1018  LOAD_FAST                'fileInfoPath'
             1020  LOAD_STR                 'wb'
             1022  CALL_FUNCTION_2       2  ''
             1024  SETUP_WITH         1072  'to 1072'
             1026  STORE_FAST               'fd'

 L.2381      1028  LOAD_GLOBAL              pickle
             1030  LOAD_ATTR                dump
             1032  LOAD_FAST                'info'
             1034  LOAD_FAST                'fd'
             1036  LOAD_FAST                'self'
             1038  LOAD_ATTR                _DEFAULT_PICKLE_PROTOCOL
             1040  LOAD_CONST               ('protocol',)
             1042  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
             1044  POP_TOP          

 L.2382      1046  LOAD_FAST                'fd'
             1048  LOAD_METHOD              flush
             1050  CALL_METHOD_0         0  ''
             1052  POP_TOP          

 L.2383      1054  LOAD_GLOBAL              os
             1056  LOAD_METHOD              fsync
             1058  LOAD_FAST                'fd'
             1060  LOAD_METHOD              fileno
             1062  CALL_METHOD_0         0  ''
             1064  CALL_METHOD_1         1  ''
             1066  POP_TOP          
             1068  POP_BLOCK        
             1070  LOAD_CONST               None
           1072_0  COME_FROM_WITH     1024  '1024'
             1072  WITH_CLEANUP_START
             1074  WITH_CLEANUP_FINISH
             1076  END_FINALLY      

 L.2385      1078  LOAD_GLOBAL              os
             1080  LOAD_ATTR                path
             1082  LOAD_METHOD              join
             1084  LOAD_FAST                'self'
             1086  LOAD_ATTR                _Repository__path
             1088  LOAD_GLOBAL              os
             1090  LOAD_ATTR                path
             1092  LOAD_METHOD              dirname
             1094  LOAD_FAST                'relativePath'
             1096  CALL_METHOD_1         1  ''
             1098  LOAD_FAST                'self'
             1100  LOAD_ATTR                _Repository__fileClass
             1102  LOAD_FAST                'fName'
             1104  BINARY_MODULO    
             1106  CALL_METHOD_3         3  ''
             1108  STORE_FAST               'fileClassPath'

 L.2386      1110  LOAD_GLOBAL              open
             1112  LOAD_FAST                'fileClassPath'
             1114  LOAD_STR                 'wb'
             1116  CALL_FUNCTION_2       2  ''
             1118  SETUP_WITH         1188  'to 1188'
             1120  STORE_FAST               'fd'

 L.2387      1122  LOAD_FAST                'value'
             1124  LOAD_CONST               None
             1126  COMPARE_OP               is
         1128_1130  POP_JUMP_IF_FALSE  1138  'to 1138'

 L.2388      1132  LOAD_CONST               None
             1134  STORE_FAST               'klass'
             1136  JUMP_FORWARD       1144  'to 1144'
           1138_0  COME_FROM          1128  '1128'

 L.2390      1138  LOAD_FAST                'value'
             1140  LOAD_ATTR                __class__
             1142  STORE_FAST               'klass'
           1144_0  COME_FROM          1136  '1136'

 L.2391      1144  LOAD_GLOBAL              pickle
             1146  LOAD_ATTR                dump
             1148  LOAD_FAST                'klass'
             1150  LOAD_FAST                'fd'
             1152  LOAD_FAST                'self'
             1154  LOAD_ATTR                _DEFAULT_PICKLE_PROTOCOL
             1156  LOAD_CONST               ('protocol',)
             1158  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
             1160  POP_TOP          

 L.2392      1162  LOAD_FAST                'fd'
             1164  LOAD_METHOD              flush
             1166  CALL_METHOD_0         0  ''
             1168  POP_TOP          

 L.2393      1170  LOAD_GLOBAL              os
             1172  LOAD_METHOD              fsync
             1174  LOAD_FAST                'fd'
             1176  LOAD_METHOD              fileno
             1178  CALL_METHOD_0         0  ''
             1180  CALL_METHOD_1         1  ''
             1182  POP_TOP          
             1184  POP_BLOCK        
             1186  LOAD_CONST               None
           1188_0  COME_FROM_WITH     1118  '1118'
             1188  WITH_CLEANUP_START
             1190  WITH_CLEANUP_FINISH
             1192  END_FINALLY      

 L.2395      1194  LOAD_FAST                'isRepoFile'
         1196_1198  POP_JUMP_IF_TRUE   1210  'to 1210'

 L.2396      1200  LOAD_FAST                'dirList'
             1202  LOAD_METHOD              append
             1204  LOAD_FAST                'fName'
             1206  CALL_METHOD_1         1  ''
             1208  POP_TOP          
           1210_0  COME_FROM          1196  '1196'
             1210  POP_BLOCK        
             1212  JUMP_FORWARD       1368  'to 1368'
           1214_0  COME_FROM_EXCEPT    752  '752'

 L.2397      1214  DUP_TOP          
             1216  LOAD_GLOBAL              Exception
             1218  COMPARE_OP               exception-match
         1220_1222  POP_JUMP_IF_FALSE  1366  'to 1366'
             1224  POP_TOP          
             1226  STORE_FAST               'err'
             1228  POP_TOP          
             1230  SETUP_FINALLY      1354  'to 1354'

 L.2398      1232  LOAD_STR                 'unable to dump the file (%s)'
             1234  LOAD_GLOBAL              str
             1236  LOAD_FAST                'err'
             1238  CALL_FUNCTION_1       1  ''
             1240  BUILD_TUPLE_1         1 
             1242  BINARY_MODULO    
             1244  STORE_FAST               'error'

 L.2399      1246  SETUP_EXCEPT       1296  'to 1296'

 L.2400      1248  LOAD_STR                 'pickle.dump('
             1250  LOAD_FAST                'dump'
             1252  COMPARE_OP               in
         1254_1256  POP_JUMP_IF_FALSE  1292  'to 1292'

 L.2401      1258  LOAD_GLOBAL              get_pickling_errors
             1260  LOAD_FAST                'value'
             1262  CALL_FUNCTION_1       1  ''
             1264  STORE_FAST               'mi'

 L.2402      1266  LOAD_FAST                'mi'
             1268  LOAD_CONST               None
             1270  COMPARE_OP               is-not
         1272_1274  POP_JUMP_IF_FALSE  1292  'to 1292'

 L.2403      1276  LOAD_FAST                'error'
             1278  LOAD_STR                 '\nmore info: %s'
             1280  LOAD_GLOBAL              str
             1282  LOAD_FAST                'mi'
             1284  CALL_FUNCTION_1       1  ''
             1286  BINARY_MODULO    
             1288  INPLACE_ADD      
             1290  STORE_FAST               'error'
           1292_0  COME_FROM          1272  '1272'
           1292_1  COME_FROM          1254  '1254'
             1292  POP_BLOCK        
             1294  JUMP_FORWARD       1308  'to 1308'
           1296_0  COME_FROM_EXCEPT   1246  '1246'

 L.2404      1296  POP_TOP          
             1298  POP_TOP          
             1300  POP_TOP          

 L.2405      1302  POP_EXCEPT       
             1304  JUMP_FORWARD       1308  'to 1308'
             1306  END_FINALLY      
           1308_0  COME_FROM          1304  '1304'
           1308_1  COME_FROM          1294  '1294'

 L.2406      1308  LOAD_FAST                'self'
             1310  LOAD_ATTR                DEBUG_PRINT_FAILED_TRIALS
         1312_1314  POP_JUMP_IF_FALSE  1350  'to 1350'

 L.2406      1316  LOAD_GLOBAL              print
             1318  LOAD_STR                 'Trial %i failed in Repository.%s (%s). Set Repository.DEBUG_PRINT_FAILED_TRIALS to False to mute'
             1320  LOAD_FAST                '_trial'
             1322  LOAD_GLOBAL              inspect
             1324  LOAD_METHOD              stack
             1326  CALL_METHOD_0         0  ''
             1328  LOAD_CONST               1
             1330  BINARY_SUBSCR    
             1332  LOAD_CONST               3
             1334  BINARY_SUBSCR    
             1336  LOAD_GLOBAL              str
             1338  LOAD_FAST                'error'
             1340  CALL_FUNCTION_1       1  ''
             1342  BUILD_TUPLE_3         3 
             1344  BINARY_MODULO    
             1346  CALL_FUNCTION_1       1  ''
             1348  POP_TOP          
           1350_0  COME_FROM          1312  '1312'
             1350  POP_BLOCK        
             1352  LOAD_CONST               None
           1354_0  COME_FROM_FINALLY  1230  '1230'
             1354  LOAD_CONST               None
             1356  STORE_FAST               'err'
             1358  DELETE_FAST              'err'
             1360  END_FINALLY      
             1362  POP_EXCEPT       
             1364  JUMP_BACK           742  'to 742'
           1366_0  COME_FROM          1220  '1220'
             1366  END_FINALLY      
           1368_0  COME_FROM          1212  '1212'

 L.2408      1368  LOAD_CONST               None
             1370  STORE_FAST               'error'

 L.2409      1372  BREAK_LOOP       
         1374_1376  JUMP_BACK           742  'to 742'
             1378  POP_BLOCK        
           1380_0  COME_FROM_LOOP      730  '730'

 L.2411      1380  LOAD_FAST                'error'
             1382  LOAD_CONST               None
             1384  COMPARE_OP               is
         1386_1388  POP_JUMP_IF_FALSE  1408  'to 1408'

 L.2412      1390  LOAD_FAST                'self'
             1392  LOAD_ATTR                _Repository__save_repository_pickle_file
             1394  LOAD_CONST               False
             1396  LOAD_CONST               False
             1398  LOAD_CONST               ('lockFirst', 'raiseError')
             1400  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1402  UNPACK_SEQUENCE_2     2 
             1404  STORE_FAST               '_'
             1406  STORE_FAST               'error'
           1408_0  COME_FROM          1386  '1386'

 L.2414      1408  LOAD_FAST                'self'
             1410  LOAD_ATTR                _Repository__locker
             1412  LOAD_METHOD              release_lock
             1414  LOAD_FAST                'fileLockId'
             1416  CALL_METHOD_1         1  ''
             1418  POP_TOP          

 L.2415      1420  LOAD_FAST                'self'
             1422  LOAD_ATTR                _Repository__locker
             1424  LOAD_METHOD              release_lock
             1426  LOAD_FAST                'repoLockId'
             1428  CALL_METHOD_1         1  ''
             1430  POP_TOP          

 L.2417      1432  LOAD_FAST                'raiseError'
         1434_1436  POP_JUMP_IF_FALSE  1466  'to 1466'
             1438  LOAD_FAST                'error'
             1440  LOAD_CONST               None
             1442  COMPARE_OP               is
         1444_1446  POP_JUMP_IF_TRUE   1466  'to 1466'
             1448  LOAD_ASSERT              AssertionError
             1450  LOAD_STR                 "unable to dump file '%s' after %i trials (%s)"
             1452  LOAD_FAST                'relativePath'
             1454  LOAD_FAST                'ntrials'
             1456  LOAD_FAST                'error'
             1458  BUILD_TUPLE_3         3 
             1460  BINARY_MODULO    
             1462  CALL_FUNCTION_1       1  ''
             1464  RAISE_VARARGS_1       1  ''
           1466_0  COME_FROM          1444  '1444'
           1466_1  COME_FROM          1434  '1434'

 L.2418      1466  LOAD_FAST                'success'
             1468  LOAD_FAST                'error'
             1470  BUILD_TUPLE_2         2 
             1472  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `COME_FROM' instruction at offset 158_0

    def dump(self, *args, **kwargs):
        """Alias to dump_file"""
        return (self.dump_file)(*args, **kwargs)

    @path_required
    def copy_file(self, relativePath, newRelativePath, force=False, raiseError=True, ntrials=3):
        """
        Copy a file in the repository.

        :Parameters:
            #. relativePath (string): The relative to the repository path of
               the file that needst to be renamed.
            #. newRelativePath (string): The new relative to the repository path
               of where to move and rename the file.
            #. force (boolean): Whether to force renaming even when another
               repository file exists. In this case old repository file
               will be removed from the repository and the system as well.
            #. raiseError (boolean): Whether to raise encountered error instead
               of returning failure.
            #. ntrials (int): After aquiring all locks, ntrials is the maximum
               number of trials allowed before failing.
               In rare cases, when multiple processes
               are accessing the same repository components, different processes
               can alter repository components between successive lock releases
               of some other process. Bigger number of trials lowers the
               likelyhood of failure due to multiple processes same time
               alteration.

        :Returns:
            #. success (boolean): Whether renaming the file was successful.
            #. message (None, string): Some explanatory message or error reason
               why directory was not updated.
        """
        if not isinstance(raiseError, bool):
            raise AssertionError('raiseError must be boolean')
        else:
            if not isinstance(force, bool):
                raise AssertionError('force must be boolean')
            else:
                if not isinstance(ntrials, int):
                    raise AssertionError('ntrials must be integer')
                else:
                    if not ntrials > 0:
                        raise AssertionError('ntrials must be >0')
                    else:
                        relativePath = self.to_repo_relative_path(path=relativePath, split=False)
                        realPath = os.path.join(self._Repository__path, relativePath)
                        fPath, fName = os.path.split(realPath)
                        newRelativePath = self.to_repo_relative_path(path=newRelativePath, split=False)
                        newRealPath = os.path.join(self._Repository__path, newRelativePath)
                        nfPath, nfName = os.path.split(newRealPath)
                        acquired, fileLockId = self._Repository__locker.acquire_lock(path=realPath, timeout=(self.timeout))
                        if not acquired:
                            error = "Code %s. Unable to aquire the lock for old file '%s'" % (fileLockId, relativePath)
                            if raiseError:
                                raise AssertionError(error)
                            return (
                             False, error)
                        try:
                            success, reason = self.add_directory(nfPath, raiseError=False, ntrials=ntrials)
                        except Exception as err:
                            try:
                                reason = 'Unable to add directory (%s)' % str(err)
                                success = False
                            finally:
                                err = None
                                del err

                    success or self._Repository__locker.release_lock(fileLockId)
                    if raiseError:
                        raise AssertionError(reason)
                    return (
                     False, reason)
                acquired, newFileLockId = self._Repository__locker.acquire_lock(path=newRealPath, timeout=(self.timeout))
                acquired or self._Repository__locker.release_lock(fileLlockId)
                error = "Code %s. Unable to aquire the lock for new file path '%s'" % (newFileLockId, newRelativePath)
                if raiseError:
                    raise AssertionError(error)
                return (
                 False, error)
            for _trial in range(ntrials):
                copied = False
                error = None
                try:
                    isRepoFile, fileOnDisk, infoOnDisk, classOnDisk = self.is_repository_file(relativePath)
                    assert isRepoFile, "file '%s' is not a repository file" % (relativePath,)
                    assert fileOnDisk, "file '%s' is found on disk" % (relativePath,)
                    assert infoOnDisk, '%s is found on disk' % self._Repository__fileInfo % fName
                    assert classOnDisk, '%s is found on disk' % self._Repository__fileClass % fName
                    nisRepoFile, nfileOnDisk, ninfoOnDisk, nclassOnDisk = self.is_repository_file(newRelativePath)
                    if nisRepoFile:
                        assert force, 'New file path is a registered repository file, set force to True to proceed regardless'
                    nDirList = self._Repository__get_repository_directory(nfPath)
                    if os.path.isfile(newRealPath):
                        os.remove(newRealPath)
                    if os.path.isfile(os.path.join(nfPath, self._Repository__fileInfo % nfName)):
                        os.remove(os.path.join(nfPath, self._Repository__fileInfo % nfName))
                    if os.path.isfile(os.path.join(nfPath, self._Repository__fileClass % nfName)):
                        os.remove(os.path.join(nfPath, self._Repository__fileClass % nfName))
                    shutil.copy(realPath, newRealPath)
                    shutil.copy(os.path.join(fPath, self._Repository__fileInfo % fName), os.path.join(nfPath, self._Repository__fileInfo % nfName))
                    shutil.copy(os.path.join(fPath, self._Repository__fileClass % fName), os.path.join(nfPath, self._Repository__fileClass % nfName))
                    if nfName not in nDirList:
                        nDirList.append(nfName)
                except Exception as err:
                    try:
                        copied = False
                        error = str(err)
                        if self.DEBUG_PRINT_FAILED_TRIALS:
                            print('Trial %i failed in Repository.%s (%s). Set Repository.DEBUG_PRINT_FAILED_TRIALS to False to mute' % (_trial, inspect.stack()[1][3], str(error)))
                    finally:
                        err = None
                        del err

                else:
                    error = None
                    copied = True
                    break

            self._Repository__locker.release_lock(fileLockId)
            self._Repository__locker.release_lock(newFileLockId)
            if not copied:
                if raiseError:
                    raise AssertionError("Unable to copy file '%s' to '%s' after %i trials (%s)" % (relativePath, newRelativePath, ntrials, error))
        return (
         copied, '\n'.join(message))

    @path_required
    def update_file(self, value, relativePath, description=False, dump=False, pull=False, raiseError=True, ntrials=3):
        """
        Update the value of a file that is already in the Repository.

        If file is not registered in repository, and error will be thrown.

        If file is missing in the system, it will be regenerated as dump method
        is called.
        Unlike dump_file, update_file won't block the whole repository but only
        the file being updated.

        :Parameters:
            #. value (object): The value of a file to update.
            #. relativePath (str): The relative to the repository path of the
               file to be updated.
            #. description (False, string): Any random description about the file.
               If False is given, the description info won't be updated,
               otherwise it will be update to what description argument value is.
            #. dump (False, string): The new dump method. If False is given,
               the old one will be used.
            #. pull (False, string): The new pull method. If False is given,
               the old one will be used.
            #. raiseError (boolean): Whether to raise encountered error instead
               of returning failure.
            #. ntrials (int): After aquiring all locks, ntrials is the maximum
               number of trials allowed before failing.
               In rare cases, when multiple processes
               are accessing the same repository components, different processes
               can alter repository components between successive lock releases
               of some other process. Bigger number of trials lowers the
               likelyhood of failure due to multiple processes same time
               alteration.

       :Returns:
           #. success (boolean): Whether renaming the directory was successful.
           #. message (None, string): Some explanatory message or error reason
              why directory was not updated.
        """
        if not isinstance(raiseError, bool):
            raise AssertionError('raiseError must be boolean')
        else:
            if not description is False:
                if not description is None:
                    assert isinstance(description, basestring), 'description must be False, None or a string'
                elif not dump is False:
                    if not dump is None:
                        if not isinstance(dump, basestring):
                            raise AssertionError('dump must be False, None or a string')
            else:
                if not pull is False:
                    if not pull is None:
                        assert isinstance(pull, basestring), 'pull must be False, None or a string'
                assert isinstance(ntrials, int), 'ntrials must be integer'
                assert ntrials > 0, 'ntrials must be >0'
                relativePath = self.to_repo_relative_path(path=relativePath, split=False)
                savePath = os.path.join(self._Repository__path, relativePath)
                fPath, fName = os.path.split(savePath)
                acquired, fileLockId = self._Repository__locker.acquire_lock(path=savePath, timeout=(self.timeout))
                error = acquired or "Code %s. Unable to aquire the lock to update '%s'" % (fileLockId, relativePath)
                if raiseError:
                    raise AssertionError(error)
                return (
                 False, error)
            for _trial in range(ntrials):
                message = []
                updated = False
                try:
                    isRepoFile, fileOnDisk, infoOnDisk, classOnDisk = self.is_repository_file(relativePath)
                    if not isRepoFile:
                        raise AssertionError("file '%s' is not registered in repository, no update can be performed." % (relativePath,))
                    elif not fileOnDisk:
                        assert description is not False, "file '%s' is found on disk, description must be provided" % (relativePath,)
                        assert dump is not False, "file '%s' is found on disk, dump must be provided" % (relativePath,)
                        assert pull is not False, "file '%s' is found on disk, pull must be provided" % (relativePath,)
                        info = {}
                        info['repository_unique_name'] = self._Repository__repo['repository_unique_name']
                        info['create_utctime'] = info['last_update_utctime'] = time.time()
                    else:
                        with open(os.path.join(fPath, self._Repository__fileInfo % fName), 'rb') as (fd):
                            info = pickle.load(fd)
                            info['last_update_utctime'] = time.time()
                    if not fileOnDisk:
                        message.append('file %s is registered in repository but it was found on disk prior to updating' % relativePath)
                    if not infoOnDisk:
                        message.append('%s is not found on disk prior to updating' % self._Repository__fileInfo % fName)
                    else:
                        if not classOnDisk:
                            message.append('%s is not found on disk prior to updating' % self._Repository__fileClass % fName)
                        if description is False or dump is False or pull is False:
                            if description is False:
                                description = info['description']
                            elif description is None:
                                description = ''
                            if dump is False:
                                dump = info['dump']
                            elif dump is None:
                                dump = get_dump_method(dump, protocol=(self._DEFAULT_PICKLE_PROTOCOL))
                            if pull is False:
                                pull = info['pull']
                            elif pull is None:
                                pull = get_pull_method(pull)
                    info['dump'] = dump
                    info['pull'] = pull
                    info['description'] = description
                    dumpFunc = my_exec(dump, name='dump', description='update')
                    dumpFunc(path=(str(savePath)), value=value)
                    _path = os.path.join(fPath, self._Repository__fileInfo % fName)
                    with open(_path, 'wb') as (fd):
                        pickle.dump(info, fd, protocol=(self._DEFAULT_PICKLE_PROTOCOL))
                        fd.flush()
                        os.fsync(fd.fileno())
                    fileClassPath = os.path.join(self._Repository__path, os.path.dirname(relativePath), self._Repository__fileClass % fName)
                    with open(fileClassPath, 'wb') as (fd):
                        if value is None:
                            klass = None
                        else:
                            klass = value.__class__
                        pickle.dump(klass, fd, protocol=(self._DEFAULT_PICKLE_PROTOCOL))
                        fd.flush()
                        os.fsync(fd.fileno())
                except Exception as err:
                    try:
                        message.append(str(err))
                        updated = False
                        try:
                            if 'pickle.dump(' in dump:
                                mi = get_pickling_errors(value)
                                if mi is not None:
                                    message.append('more info: %s' % str(mi))
                        except:
                            pass

                        if self.DEBUG_PRINT_FAILED_TRIALS:
                            print('Trial %i failed in Repository.%s (%s). Set Repository.DEBUG_PRINT_FAILED_TRIALS to False to mute' % (_trial, inspect.stack()[1][3], '\n'.join(message)))
                    finally:
                        err = None
                        del err

                else:
                    updated = True
                    break

            self._Repository__locker.release_lock(fileLockId)
            if not updated:
                if raiseError:
                    raise AssertionError("Unable to update file '%s' (%s)" % (relativePath, '\n'.join(message)))
        return (
         updated, '\n'.join(message))

    def update(self, *args, **kwargs):
        """Alias to update_file"""
        return (self.update_file)(*args, **kwargs)

    @path_required
    def pull_file(self, relativePath, pull=None, update=True, ntrials=3):
        """
        Pull a file's data from the Repository.

        :Parameters:
            #. relativePath (string): The relative to the repository path from
               where to pull the file.
            #. pull (None, string): The pulling method.
               If None, the pull method saved in the file info will be used.
               If a string is given, the string should include all the necessary
               imports, a '$FILE_PATH' that replaces the absolute file path when
               the dumping will be performed and finally a PULLED_DATA variable.
               e.g "import numpy as np; PULLED_DATA=np.loadtxt(fname='$FILE_PATH')"
            #. update (boolean): If pull is not None, Whether to update the pull
               method stored in the file info by the given pull method.
            #. ntrials (int): After aquiring all locks, ntrials is the maximum
               number of trials allowed before failing.
               In rare cases, when multiple processes
               are accessing the same repository components, different processes
               can alter repository components between successive lock releases
               of some other process. Bigger number of trials lowers the
               likelyhood of failure due to multiple processes same time
               alteration.

        :Returns:
            #. data (object): The pulled data from the file.
        """
        if not isinstance(ntrials, int):
            raise AssertionError('ntrials must be integer')
        else:
            if not ntrials > 0:
                raise AssertionError('ntrials must be >0')
            else:
                relativePath = self.to_repo_relative_path(path=relativePath, split=False)
                realPath = os.path.join(self._Repository__path, relativePath)
                fPath, fName = os.path.split(realPath)
                isRepoFile, fileOnDisk, infoOnDisk, classOnDisk = self.is_repository_file(relativePath)
                if not isRepoFile:
                    fileOnDisk = [
                     '', '. File itself is found on disk'][fileOnDisk]
                    infoOnDisk = ['', '. %s is found on disk' % self._Repository__fileInfo % fName][infoOnDisk]
                    classOnDisk = ['', '. %s is found on disk' % self._Repository__fileClass % fName][classOnDisk]
                    assert False, "File '%s' is not a repository file%s%s%s" % (relativePath, fileOnDisk, infoOnDisk, classOnDisk)
                assert fileOnDisk, "File '%s' is registered in repository but the file itself was not found on disk" % (relativePath,)
                if not infoOnDisk:
                    if pull is not None:
                        warnings.warn("'%s' was not found on disk but pull method is given" % (self._Repository__fileInfo % fName))
                    else:
                        raise Exception("File '%s' is registered in repository but the '%s' was not found on disk and pull method is not specified" % (relativePath, self._Repository__fileInfo % fName))
            acquired, fileLockId = self._Repository__locker.acquire_lock(path=realPath, timeout=(self.timeout))
            error = acquired or "Code %s. Unable to aquire the lock when pulling '%s'" % (fileLockId, relativePath)
            return (
             False, error)
        for _trial in range(ntrials):
            error = None
            try:
                if pull is not None:
                    pull = get_pull_method(pull)
                else:
                    with open(os.path.join(fPath, self._Repository__fileInfo % fName), 'rb') as (fd):
                        info = pickle.load(fd)
                    pull = info['pull']
                pullFunc = my_exec(pull, name='pull', description='pull')
                pulledVal = pullFunc(path=(str(realPath)))
            except Exception as err:
                try:
                    self._Repository__locker.release_lock(fileLockId)
                    m = str(pull).replace('$FILE_PATH', str(realPath))
                    error = "Unable to pull data using '%s' from file (%s)" % (m, err)
                    if self.DEBUG_PRINT_FAILED_TRIALS:
                        print('Trial %i failed in Repository.%s (%s). Set Repository.DEBUG_PRINT_FAILED_TRIALS to False to mute' % (_trial, inspect.stack()[1][3], str(error)))
                finally:
                    err = None
                    del err

            break

        self._Repository__locker.release_lock(fileLockId)
        assert error is None, 'After %i trials, %s' % (ntrials, error)
        return pulledVal

    def pull(self, *args, **kwargs):
        """Alias to pull_file"""
        return (self.pull_file)(*args, **kwargs)

    @path_required
    def rename_file(self, relativePath, newRelativePath, force=False, raiseError=True, ntrials=3):
        """
        Rename a file in the repository. It insures renaming the file in the system.

        :Parameters:
            #. relativePath (string): The relative to the repository path of
               the file that needst to be renamed.
            #. newRelativePath (string): The new relative to the repository path
               of where to move and rename the file.
            #. force (boolean): Whether to force renaming even when another
               repository file exists. In this case old repository file
               will be removed from the repository and the system as well.
            #. raiseError (boolean): Whether to raise encountered error instead
               of returning failure.
            #. ntrials (int): After aquiring all locks, ntrials is the maximum
               number of trials allowed before failing.
               In rare cases, when multiple processes
               are accessing the same repository components, different processes
               can alter repository components between successive lock releases
               of some other process. Bigger number of trials lowers the
               likelyhood of failure due to multiple processes same time
               alteration.

        :Returns:
            #. success (boolean): Whether renaming the file was successful.
            #. message (None, string): Some explanatory message or error reason
               why directory was not updated.
        """
        if not isinstance(raiseError, bool):
            raise AssertionError('raiseError must be boolean')
        else:
            if not isinstance(force, bool):
                raise AssertionError('force must be boolean')
            elif not isinstance(ntrials, int):
                raise AssertionError('ntrials must be integer')
            else:
                if not ntrials > 0:
                    raise AssertionError('ntrials must be >0')
                else:
                    relativePath = self.to_repo_relative_path(path=relativePath, split=False)
                    realPath = os.path.join(self._Repository__path, relativePath)
                    fPath, fName = os.path.split(realPath)
                    newRelativePath = self.to_repo_relative_path(path=newRelativePath, split=False)
                    newRealPath = os.path.join(self._Repository__path, newRelativePath)
                    nfPath, nfName = os.path.split(newRealPath)
                    acquired, fileLockId = self._Repository__locker.acquire_lock(path=realPath, timeout=(self.timeout))
                    if not acquired:
                        error = "Code %s. Unable to aquire the lock for old file '%s'" % (fileLockId, relativePath)
                        if raiseError:
                            raise AssertionError(error)
                        return (
                         False, error)
                    try:
                        success, reason = self.add_directory(nfPath, raiseError=False, ntrials=ntrials)
                    except Exception as err:
                        try:
                            reason = 'Unable to add directory (%s)' % str(err)
                            success = False
                        finally:
                            err = None
                            del err

                    if not success:
                        self._Repository__locker.release_lock(fileLockId)
                        if raiseError:
                            raise AssertionError(reason)
                        return (
                         False, reason)
                    acquired, newFileLockId = self._Repository__locker.acquire_lock(path=newRealPath, timeout=(self.timeout))
                    acquired or self._Repository__locker.release_lock(fileLockId)
                    error = "Code %s. Unable to aquire the lock for new file path '%s'" % (newFileLockId, newRelativePath)
                    if raiseError:
                        raise AssertionError(error)
                    return (
                     False, error)
                for _trial in range(ntrials):
                    renamed = False
                    error = None
                    try:
                        isRepoFile, fileOnDisk, infoOnDisk, classOnDisk = self.is_repository_file(relativePath)
                        assert isRepoFile, "file '%s' is not a repository file" % (relativePath,)
                        assert fileOnDisk, "file '%s' is found on disk" % (relativePath,)
                        assert infoOnDisk, '%s is found on disk' % self._Repository__fileInfo % fName
                        assert classOnDisk, '%s is found on disk' % self._Repository__fileClass % fName
                        nisRepoFile, nfileOnDisk, ninfoOnDisk, nclassOnDisk = self.is_repository_file(newRelativePath)
                        if nisRepoFile:
                            assert force, 'New file path is a registered repository file, set force to True to proceed regardless'
                        oDirList = self._Repository__get_repository_directory(fPath)
                        nDirList = self._Repository__get_repository_directory(nfPath)
                        if os.path.isfile(newRealPath):
                            os.remove(newRealPath)
                        if os.path.isfile(os.path.join(nfPath, self._Repository__fileInfo % nfName)):
                            os.remove(os.path.join(nfPath, self._Repository__fileInfo % nfName))
                        if os.path.isfile(os.path.join(nfPath, self._Repository__fileClass % nfName)):
                            os.remove(os.path.join(nfPath, self._Repository__fileClass % nfName))
                        os.rename(realPath, newRealPath)
                        os.rename(os.path.join(fPath, self._Repository__fileInfo % fName), os.path.join(nfPath, self._Repository__fileInfo % nfName))
                        os.rename(os.path.join(fPath, self._Repository__fileClass % fName), os.path.join(nfPath, self._Repository__fileClass % nfName))
                        findex = oDirList.index(fName)
                        oDirList.pop(findex)
                        if nfName not in nDirList:
                            nDirList.append(nfName)
                    except Exception as err:
                        try:
                            renamed = False
                            error = str(err)
                            if self.DEBUG_PRINT_FAILED_TRIALS:
                                print('Trial %i failed in Repository.%s (%s). Set Repository.DEBUG_PRINT_FAILED_TRIALS to False to mute' % (_trial, inspect.stack()[1][3], str(error)))
                        finally:
                            err = None
                            del err

                    else:
                        renamed = True
                        break

                self._Repository__locker.release_lock(fileLockId)
                self._Repository__locker.release_lock(newFileLockId)
                try:
                    if os.path.isfile(os.path.join(fPath, self._Repository__fileLock % fName)):
                        os.remove(os.path.join(fPath, self._Repository__fileLock % fName))
                except:
                    pass

            if not renamed:
                if raiseError:
                    raise AssertionError("Unable to rename file '%s' to '%s' after %i trials (%s)" % (relativePath, newRelativePath, ntrials, error))
        return (
         renamed, error)

    @path_required
    def remove_file(self, relativePath, removeFromSystem=False, raiseError=True, ntrials=3):
        """
        Remove file from repository.

        :Parameters:
            #. relativePath (string): The relative to the repository path of the
               file to remove.
            #. removeFromSystem (boolean): Whether to remove file from disk as
               well.
            #. raiseError (boolean): Whether to raise encountered error instead
               of returning failure.
            #. ntrials (int): After aquiring all locks, ntrials is the maximum
               number of trials allowed before failing.
               In rare cases, when multiple processes
               are accessing the same repository components, different processes
               can alter repository components between successive lock releases
               of some other process. Bigger number of trials lowers the
               likelyhood of failure due to multiple processes same time
               alteration.
        """
        if not isinstance(raiseError, bool):
            raise AssertionError('removeFromSystem must be boolean')
        else:
            if not isinstance(removeFromSystem, bool):
                raise AssertionError('removeFromSystem must be boolean')
            elif not isinstance(ntrials, int):
                raise AssertionError('ntrials must be integer')
            else:
                if not ntrials > 0:
                    raise AssertionError('ntrials must be >0')
                else:
                    relativePath = self.to_repo_relative_path(path=relativePath, split=False)
                    realPath = os.path.join(self._Repository__path, relativePath)
                    fPath, fName = os.path.split(realPath)
                    acquired, fileLockId = self._Repository__locker.acquire_lock(path=realPath, timeout=(self.timeout))
                    error = acquired or "Code %s. Unable to aquire the lock when removing '%s'" % (fileLockId, relativePath)
                    if raiseError:
                        raise AssertionError(error)
                    return (
                     False, error)
                for _trial in range(ntrials):
                    removed = False
                    message = []
                    try:
                        isRepoFile, fileOnDisk, infoOnDisk, classOnDisk = self.is_repository_file(relativePath)
                        if not isRepoFile:
                            message("File '%s' is not a repository file" % (relativePath,))
                            if fileOnDisk:
                                message.append('File itself is found on disk')
                            if infoOnDisk:
                                message.append('%s is found on disk' % self._Repository__fileInfo % fName)
                            if classOnDisk:
                                message.append('%s is found on disk' % self._Repository__fileClass % fName)
                        else:
                            dirList = self._Repository__get_repository_directory(fPath)
                            findex = dirList.index(fName)
                            dirList.pop(findex)
                            if os.path.isfile(realPath):
                                os.remove(realPath)
                            if os.path.isfile(os.path.join(fPath, self._Repository__fileInfo % fName)):
                                os.remove(os.path.join(fPath, self._Repository__fileInfo % fName))
                        if os.path.isfile(os.path.join(fPath, self._Repository__fileClass % fName)):
                            os.remove(os.path.join(fPath, self._Repository__fileClass % fName))
                    except Exception as err:
                        try:
                            removed = False
                            message.append(str(err))
                            if self.DEBUG_PRINT_FAILED_TRIALS:
                                print('Trial %i failed in Repository.%s (%s). Set Repository.DEBUG_PRINT_FAILED_TRIALS to False to mute' % (_trial, inspect.stack()[1][3], '\n'.join(message)))
                        finally:
                            err = None
                            del err

                    else:
                        removed = True
                        break

                self._Repository__locker.release_lock(fileLockId)
                try:
                    if os.path.isfile(os.path.join(fPath, self._Repository__fileLock % fName)):
                        os.remove(os.path.join(fPath, self._Repository__fileLock % fName))
                except:
                    pass

            if not removed:
                if raiseError:
                    raise AssertionError("Unable to remove file '%s' after %i trials (%s)" % (relativePath, ntrials, '\n'.join(message)))
        return (
         removed, '\n'.join(message))