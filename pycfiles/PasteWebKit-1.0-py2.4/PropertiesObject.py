# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/paste/webkit/FakeWebware/MiscUtils/PropertiesObject.py
# Compiled at: 2006-10-22 17:01:01
from UserDict import UserDict
import os, string, sys, types

class WillNotRunError(Exception):
    __module__ = __name__


class PropertiesObject(UserDict):
    """
        A PropertiesObject represents, in a dictionary-like fashion,
        the values found in a Properties.py file. That file is always
        included with a Webware component to advertise its name,
        version, status, etc. Note that a Webware component is a
        Python package that follows additional conventions. Also, the
        top level Webware directory contains a Properties.py.

        Component properties are often used for:
        
        * generation of documentation
        * runtime examination of components, especially prior to loading

        PropertiesObject provides additional keys:
        
        * filename - the filename from which the properties were read
        * versionString - a nicely printable string of the version
        * requiredPyVersionString - like versionString but for requiredPyVersion instead
        * willRun - 1 if the component will run. So far that means having the right Python version.
        * willNotRunReason - defined only if willRun is 0. contains a readable error message

        Using a PropertiesObject is better than investigating the Properties.py file directly, because the rules for determining derived keys and any future convenience methods will all be provided here.

        Usage example::

                from MiscUtils.PropertiesObject import PropertiesObject
                props = PropertiesObject(filename)
                for item in props.items():
                        print '%s: %s' % item

        Note: We don't normally suffix a class name with "Object" as we have with this class, however, the name Properties.py is already used in our containing package and all other packages.
        """
    __module__ = __name__

    def __init__(self, filename=None):
        UserDict.__init__(self)
        if filename:
            self.readFileNamed(filename)

    def loadValues(self, dict):
        self.update(dict)
        self.cleanPrivateItems()

    def readFileNamed(self, filename):
        self['filename'] = filename
        results = {}
        exec open(filename) in results
        self.update(results)
        self.cleanPrivateItems()
        self.createDerivedItems()

    def cleanPrivateItems(self):
        """ Removes items whose keys start with a double underscore, such as __builtins__. """
        for key in self.keys():
            if key[:2] == '__':
                del self[key]

    def createDerivedItems(self):
        self.createVersionString()
        self.createRequiredPyVersionString()
        self.createWillRun()

    def _versionString(self, version):
        """ For a sequence containing version information such as (2, 0, 0, 'pre'), this returns a printable string such as '2.0-pre'. The micro version number is only excluded from the string if it is zero. """
        ver = map(lambda x: str(x), version)
        if ver[2] == '0':
            numbers = ver[:2]
        else:
            numbers = ver[:3]
        rest = ver[3:]
        numbers = string.join(numbers, '.')
        rest = string.join(rest, '-')
        if rest:
            return numbers + rest
        else:
            return numbers

    def createVersionString(self):
        self['versionString'] = self._versionString(self['version'])

    def createRequiredPyVersionString(self):
        self['requiredPyVersionString'] = self._versionString(self['requiredPyVersion'])

    def createWillRun(self):
        self['willRun'] = 0
        try:
            for key in self.willRunKeys():
                methodName = 'check' + string.upper(key[0]) + key[1:]
                method = getattr(self, methodName)
                method()

        except WillNotRunError, msg:
            self['willNotRunReason'] = msg
            return

        self['willRun'] = 1

    def willRunKeys(self):
        """ Returns a list of keys whose values should be examined in order to determine if the component will run. Used by createWillRun(). """
        return [
         'requiredPyVersion', 'requiredOpSys', 'deniedOpSys', 'willRunFunc']

    def checkRequiredPyVersion(self):
        pyVer = getattr(sys, 'version_info', None)
        if not pyVer:
            pyVer = string.split(sys.version)[0]
            pyVer = string.split(pyVer, '.')
            pyVer = map(lambda x: int(x), pyVer)
        if tuple(pyVer) < tuple(self['requiredPyVersion']):
            raise WillNotRunError, 'Required python ver is %s, but actual ver is %s.' % (self['requiredPyVersion'], pyVer)
        return

    def checkRequiredOpSys(self):
        requiredOpSys = self.get('requiredOpSys', None)
        if requiredOpSys:
            if type(requiredOpSys) == types.StringType:
                requiredOpSys = [
                 requiredOpSys]
            if os.name not in requiredOpSys:
                raise WillNotRunError, 'Required op sys is %s, but actual op sys is %s.' % (requiredOpSys, os.name)
        return

    def checkDeniedOpSys(self):
        deniedOpSys = self.get('deniedOpSys', None)
        if deniedOpSys:
            if type(deniedOpSys) == types.StringType:
                deniedOpSys = [
                 deniedOpSys]
            if os.name in deniedOpSys:
                raise WillNotRunError, 'Will not run on op sys %s and actual op sys is %s.' % (deniedOpSys, os.name)
        return

    def checkRequiredSoftware(self):
        """ Not implemented. No op right now. """
        reqSoft = self.get('requiredSoftware', None)
        if reqSoft:
            for soft in reqSoft:
                pass

        return

    def checkWillRunFunc(self):
        willRunFunc = self.get('willRunFunc', None)
        if willRunFunc:
            whyNotMsg = willRunFunc()
            if whyNotMsg:
                raise WillNotRunError, whyNotMsg
        return