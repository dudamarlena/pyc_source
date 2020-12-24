# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: C:\Anaconda2\lib\site-packages\pySAXS\guisaxs\qt\preferences.py
# Compiled at: 2019-10-30 09:35:35
__doc__ = '\na module to manage preference\n'
import sys
if sys.version_info.major >= 3:
    import configparser
else:
    import ConfigParser as configparser
from os import path
KEYS = [
 'defaultdirectory', 'recent']
SECTION = 'guisaxs qt'
MEMORY = 5

class prefs:

    def __init__(self, filename='guisaxs.ini', section=None):
        self.filename = filename
        if section is None:
            self.section = SECTION
        else:
            self.section = section
        self.parser = configparser.SafeConfigParser()
        self.parser.add_section(self.section)
        for name in KEYS:
            self.parser.set(self.section, name, '')

        self.recent = []
        return

    def getName(self):
        return self.filename

    def fileExist(self, filename=None):
        """
        return True if preference file exist
        """
        if filename is not None:
            self.filename = filename
        return path.exists(self.filename)

    def save(self, filename=None):
        """
        save preferences in filename
        """
        print (
         'save pref in : ', filename)
        if filename is not None:
            self.filename = filename
        f = open(self.filename, 'w')
        print ('save pref in : ', filename)
        self.parser.write(f)
        f.close()
        return

    def read(self, filename=None):
        """
        read preferences from filename
        """
        if filename is not None:
            self.filename = filename
        self.parser = configparser.SafeConfigParser()
        self.parser.read(self.filename)
        rec = self.get('recent')
        self.recent = []
        if rec is not None:
            rec = rec.replace("'", '')
            rec = rec.replace(' ', '')
            rec = rec.split(',')
            for f in rec:
                if f != '':
                    self.recent.append(path.normpath(f))

        for i in range(MEMORY):
            rec = self.get('recent' + str(i))
            if rec is None:
                break
            self.recent.append(path.normpath(rec))

        return

    def get(self, name, section=None, defaultValue=None):
        """
        get the specified preferences
        if the key name don't exist, return None
        """
        if section is None:
            section = self.section
        if self.parser.has_option(section, name):
            return self.parser.get(section, name)
        else:
            if defaultValue is not None:
                return defaultvalue
            else:
                return

            return

    def getSet(self, name, section=None, defaultValue=None):
        """
        get the specified preferences
        if the key name don't exist, return None
        """
        if section is None:
            section = self.section
        if self.parser.has_option(section, name):
            return self.parser.get(section, name)
        else:
            if defaultValue is not None:
                if not self.parser.has_section(section):
                    self.parser.add_section(section)
                    self.parser.set(section, name, str(defaultValue))
                return defaultValue
            return
            return

    def set(self, name, value, section=None):
        """
        set the preference
        """
        if section is None:
            section = self.section
        if not self.parser.has_section(section):
            self.parser.add_section(section)
        self.parser.set(section, name, value)
        return

    def getRecentFiles(self):
        """
        return the list of recent files
        """
        return self.recent

    def getLastFile(self):
        if len(self.recent) > 0:
            return self.recent[0]
        else:
            return
            return

    def addRecentFile(self, filename):
        """
        add a recent file
        """
        filename = path.normpath(filename)
        if filename in self.recent:
            return False
        nl = [
         filename]
        self.recent = nl + self.recent[:MEMORY - 1]
        for i in range(len(self.recent)):
            self.set('recent' + str(i), self.recent[i])

        return True