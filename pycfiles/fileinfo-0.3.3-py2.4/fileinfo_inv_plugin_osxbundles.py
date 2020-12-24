# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-i386/egg/fileinfo/plugins/fileinfo_inv_plugin_osxbundles.py
# Compiled at: 2008-06-17 03:14:06
"""A fileinfo plug-in for Mac OS X bundles.

This makes sense only on Mac OS X.
"""
import os, sys, shutil, tempfile
from os.path import join, exists, basename, splitext, dirname
from fileinfo.investigator import BaseInvestigator

def readPlistFile(path):
    """Read content of property list file, either XML or binary."""
    try:
        from Foundation import NSDictionary
        plist = NSDictionary.dictionaryWithContentsOfFile_(path)
    except:
        try:
            from plistlib import readPlist
            plist = readPlist(path)
        except:
            (fd, destPath) = tempfile.mkstemp()
            shutil.copy2(path, destPath)
            os.popen("plutil -convert xml1 '%s'" % destPath)
            plist = readPlist(destPath)
            os.remove(destPath)

    return plist


class OSXBundleInvestigator(BaseInvestigator):
    """A class for determining attributes of OS X bundles."""
    __module__ = __name__
    attrMap = {'bundlename': 'getName', 'bundleversion': 'getVersion', 'bundleminsysversion': 'getMinSysVersion'}
    totals = ()

    def activate(self):
        """Try activating self, setting 'active' variable."""
        path = self.path
        base = splitext(basename(path))[0]
        if exists(join(path, 'Contents', 'Info.plist')):
            plPath = join(path, 'Contents', 'Info.plist')
            self.active = True
            self.plist = readPlistFile(plPath)
        elif exists(join(path, 'Info.plist')):
            plPath = join(path, 'Info.plist')
            self.plist = readPlistFile(plPath)
            self.active = True
        else:
            self.active = False
        return self.active

    def getName(self):
        """Return OS X bundle name."""
        if not self.active:
            return 'n/a'
        try:
            nameString = self.plist['CFBundleName']
        except:
            nameString = 'n/a'

        return nameString

    def getVersion(self):
        """Return OS X bundle version."""
        if not self.active:
            return 'n/a'
        try:
            versionString = self.plist['CFBundleShortVersionString']
        except:
            try:
                versionString = self.plist['CFBundleVersion']
            except:
                versionString = 'n/a'

        return versionString

    def getMinSysVersion(self):
        """Return OS X bundle minimum system version."""
        if not self.active:
            return 'n/a'
        try:
            versionString = self.plist['LSMinimumSystemVersion']
        except:
            versionString = 'n/a'

        return versionString