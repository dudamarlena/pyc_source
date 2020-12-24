# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/mozilla/core/l10nconfigparser.py
# Compiled at: 2009-10-11 12:01:44
import os
from ConfigParser import ConfigParser, NoSectionError, NoOptionError
from urlparse import urlparse, urljoin
from urllib import pathname2url, url2pathname
from urllib2 import urlopen

class L10nConfigParser(object):
    """Helper class to gather application information from l10n.ini files.

  This class is working on synchronous open to read files or web data.
  Subclass this and overwrite loadConfigs and addChild if you need async.
  """

    def __init__(self, inipath, **kwargs):
        if os.path.isabs(inipath) and os.name != 'nt':
            self.inipath = 'file:%s' % pathname2url(inipath)
        else:
            pwdurl = 'file:%s/' % pathname2url(os.getcwd())
            self.inipath = urljoin(pwdurl, inipath)
        self.children = []
        self.dirs = []
        self.defaults = kwargs

    def loadConfigs(self, optional=False):
        try:
            ini = urlopen(self.inipath)
        except OSError:
            raise OSError('L10n.ini File not found: ' + self.inipath)

        self.onLoadConfig(ini, optional)

    def onLoadConfig(self, inifile, optional=False):
        cp = ConfigParser(self.defaults)
        cp.readfp(inifile)
        try:
            depth = cp.get('general', 'depth')
        except:
            depth = '.'

        self.baseurl = urljoin(self.inipath, depth)
        try:
            for (title, path) in cp.items('includes'):
                if title in self.defaults:
                    continue
                self.addChild(title, path, cp, False)

        except NoSectionError:
            pass

        try:
            for (title, path) in cp.items('optional_includes'):
                if title in self.defaults:
                    continue
                self.addChild(title, path, cp, True)

        except NoSectionError:
            pass

        try:
            for item in cp.get('compare', 'dirs').split():
                self.dirs.append({'dir': item, 'optional': optional})

        except (NoOptionError, NoSectionError):
            pass

        try:
            self.all_path = cp.get('general', 'all')
            self.all_url = urljoin(self.baseurl, self.all_path)
        except (NoOptionError, NoSectionError):
            self.all_path = None
            self.all_url = None

        return

    def addChild(self, title, path, orig_cp, optional=False):
        cp = L10nConfigParser(urljoin(self.baseurl, path), **self.defaults)
        cp.loadConfigs(optional)
        self.children.append(cp)

    def directories(self):
        dirlist = []
        url = urlparse(self.baseurl)
        basepath = None
        if url[0] == 'file':
            basepath = url2pathname(url[2])
        for dir in self.dirs:
            dirlist.append({'dir': dir['dir'], 'path': basepath, 'locales': self.allLocales(), 'optional': dir['optional']})

        t = ''
        try:
            for child in self.children:
                for t in child.directories():
                    dirlist.append(t)

        except TypeError, e:
            raise TypeError(' in file: ' + t + '; ' + str(e))

        return dirlist

    def allLocales(self):
        if self.all_url is not None:
            return urlopen(self.all_url).read().splitlines()
        return