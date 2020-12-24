# uncompyle6 version 3.6.7
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\pyjld\system\registry\reg_linux.py
# Compiled at: 2009-04-02 21:58:17
__doc__ = ' \nLinux Registry class\n'
__author__ = 'Jean-Lou Dupont'
__fileid = '$Id: reg_linux.py 37 2009-04-03 01:58:16Z jeanlou.dupont $'
import sys, yaml, os.path
from types import *
from pyjld.system.registry import RegistryException

class LinuxRegistry(object):
    """Simple Registry class
    """
    _lin = '/etc/python/registry/%s'
    _lind = 'c:\\etc\\python\\registry\\%s'

    def __init__(self, file=None, debug=False):
        self._debug = debug
        self.file = file
        self.cache = {}

    def __getitem__(self, key):
        if self.file is None:
            raise Exception('file property must be set to use the dict interface')
        return self.getKey(self.file, key)

    def __setitem__(self, key, value):
        if self.file is None:
            raise Exception('file property must be set to use the dict interface')
        return self.setKey(self.file, key, value)

    def __contains__(self, key):
        if self.file is None:
            raise Exception('file property must be set to use the dict interface')
        return self.getKey(self.file, key) is not None

    def getKey(self, file, key):
        """Retrieves a key and its corresponding value
            Returns None if the key does not exist
        """
        d = self._load(file)
        return self._extractKey(d, key)

    def setKey(self, file, key, value):
        """Sets the value for a key.
            Creates the registry file if it does not already exist.
        """
        d = self._load(file)
        if d is not None:
            d[key] = value
        else:
            d = {key: value}
        self._save(file, yaml.dump(d))
        return

    def _extractKey(self, obj, key):
        """ Extracts the value of 'key' from 'obj'.
            Obj is really a YAML object accessible
            through normal Dict/List interface
        """
        if type(obj) is ListType:
            for i in obj:
                if type(i) is DictType:
                    found = False
                    try:
                        value = i[key]
                        found = True
                    except:
                        pass
                    else:
                        if found:
                            return value

        if type(obj) is DictType:
            try:
                return obj[key]
            except:
                return

        return

    def _load(self, file):
        path = self._getPath(file)
        if not os.path.exists(path) or not os.path.isfile(path):
            return
        mtime = os.path.getmtime(path)
        if path in self.cache:
            if mtime == self.cache[path][0]:
                return self.cache[path][1]
        try:
            infile = open(path, 'r')
        except:
            raise RegistryException('LinuxRegistry: error loading file[%s]' % file)

        result = None
        try:
            try:
                result = yaml.load(infile)
                self.cache[path] = (mtime, result)
            except:
                raise RegistryException('LinuxRegistry: error parsing yaml from file [%s]' % file)

        finally:
            infile.close()

        return result

    def _save(self, file, content):
        self._prepareDir()
        path = self._getPath(file)
        try:
            outfile = open(path, 'w')
            outfile.write(content)
            outfile.close()
        except:
            raise RegistryException('LinuxRegistry: error writing file[%s]' % path)

    def _getPath(self, file, trim=False):
        if self._debug:
            path = self._lind % file
        else:
            path = self._lin % file
        if trim:
            path.rstrip(os.sep)
        return path

    def _prepareDir(self):
        """Creates the registry directory if it does not already exists
        """
        path = self._getPath('', trim=True)
        if os.path.isdir(path):
            return
        bits = path.split(os.sep)
        spath = bits.pop(0)
        bit = bits.pop(0)
        while bit is not None:
            spath = spath + os.sep + bit
            if not os.path.isdir(spath):
                os.mkdir(spath)
            try:
                bit = bits.pop(0)
            except:
                bit = None

        return