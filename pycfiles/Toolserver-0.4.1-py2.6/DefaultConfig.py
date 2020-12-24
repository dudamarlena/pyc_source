# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/Toolserver/DefaultConfig.py
# Compiled at: 2010-03-01 05:50:25
"""

Toolserver Framework for Python - Default Configuration

Copyright (c) 2002, Georg Bauer <gb@rfc1437.de>

Permission is hereby granted, free of charge, to any person obtaining a copy of 
this software and associated documentation files (the "Software"), to deal in 
the Software without restriction, including without limitation the rights to 
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
 
the Software, and to permit persons to whom the Software is furnished to do so, 
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all 
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR 
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
 
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR 
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER 
IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN 
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

"""
import os, sys, copy
from distutils.sysconfig import PREFIX
try:
    import Crypto
    hasCrypto = 1
except ImportError:
    hasCrypto = 0

def constructPath(*args, **kw):
    path = apply(os.path.join, args)
    try:
        os.makedirs(path)
    except:
        pass

    if kw.get('mode', 0):
        os.chmod(path, kw['mode'])
    return path


class Configuration:

    def __getitem__(self, key):
        return getattr(self, key)

    def __setitem__(self, key, value):
        setattr(self, key, value)

    def has_key(self, key):
        return hasattr(self, key)

    def keys(self):
        liste = filter(lambda a: a[0] >= 'a' and a[0] <= 'z', self.__dict__.keys())
        liste.sort()
        return liste

    def write(self, filename):
        cfg = open(filename, 'w')
        for k in self.keys():
            cfg.write('%s=%s\n' % (k, repr(self[k])))

        cfg.close()


class SystemConfiguration(Configuration):

    def __init__(self, prefix, homedir):
        self.setPathVars(prefix, homedir)
        self.setPidFileVar()
        self._sections = []

    def setPathVars(self, prefix, homedir):
        self.PREFIX = prefix
        self.HOMEDIR = homedir
        self.SHAREDDIR = constructPath(self.PREFIX, 'share', 'toolserver')
        self.MASTERTOOLDIR = constructPath(self.SHAREDDIR, 'tools')
        self.ROOTDIR = constructPath(self.HOMEDIR, 'www', mode=448)
        self.LOGDIR = constructPath(self.HOMEDIR, 'log', mode=448)
        self.VARDIR = constructPath(self.HOMEDIR, 'var', mode=448)
        self.ETCDIR = constructPath(self.HOMEDIR, 'etc', mode=448)
        self.TOOLDIR = constructPath(self.HOMEDIR, 'tools', mode=448)
        self.LIBDIR = constructPath(self.HOMEDIR, 'lib', mode=448)
        self.PRIVKEYDIR = constructPath(self.HOMEDIR, 'privkeys', mode=448)
        self.PUBKEYDIR = constructPath(self.HOMEDIR, 'pubkeys', mode=448)

    def setPidFileVar(self):
        self.PIDFILE = os.path.join(self.VARDIR, 'toolserver.pid')

    def append(self, title, **vars):
        self._sections.append((title, vars.keys()))
        for k in vars.keys():
            setattr(self, k, vars[k])

    def sections(self):
        return self._sections

    def write(self, filename):
        cfg = open(filename, 'w')
        for (sec, keys) in self.sections():
            for line in sec.split('\n'):
                cfg.write('# %s\n' % line)

            for k in keys:
                cfg.write('%s=%s\n' % (k, repr(config[k])))

            cfg.write('\n')

        cfg.close()


try:
    HOMEDIR = os.environ['TOOLSERVER_HOME']
except KeyError:
    if sys.platform == 'win32':
        try:
            home = os.environ['HOME']
        except KeyError:
            try:
                home = os.environ['APPDATA']
            except KeyError:
                try:
                    home = os.environ['USERPROFILE']
                except KeyError:
                    home = os.environ['HOMEDRIVE'] + os.environ['HOMEPATH']

    else:
        home = os.environ['HOME']
    HOMEDIR = constructPath(home, '.Toolserver', mode=448)

config = SystemConfiguration(PREFIX, HOMEDIR)
config.append('how is your server called?', serverhostname='localhost', serverip='127.0.0.1', serverport=4334)
config.append('should the monitor server be started? If yes, set monitorport\nto something different than 0 and add a monitor password.\nThe monitor will run on serverip.', monitorport=0, monitorpassword='')
config.append('character encoding used for document data', documentEncoding='iso-8859-1')
config.append('these are switches that are set by tsctl', daemon=1, verbose=0, debugrpc=0, contract=0, basicauth=0, autoreload=0)
config.append('this activates simplification of SOAP arguments\nto python base types. This slows down processing\na lot (due to recursive traversal of all parameters),\nbut allows easier migration of existing code.', simplify=0)
config.append('this sets the default timeout for socket communication', timeout=30)
config.append('these values are for managing worker threads dynamically.\nthey are usefull for a moderate load. minfreeworkers says\nhow much workers must be free as a minimum (checked every\nfreecheckinterval seconds), maxfreeworkers says how much workers\nshould be free as a maximum and startfreeworkers says how much\nworkers should be started when there are less than minfreeworkers\nfree workers. If maxfreeworkers is bigger than minfreeworkers,\nthe number of running workers will never fall below maxfreeworkers.', freecheckinterval=5, minfreeworkers=4, maxfreeworkers=6, startfreeworkers=4, maxworkers=100)
config.append('these values are for managing transient tool caches', maxage=300, maxitems=1000)
if hasCrypto:
    config.append('activating PickleRPC should only be done if you can trust\nall systems that can connect to your server or you took security measures to\nprotect yourself from unpickling exploits! If you enable the PickleRPC\nprotocol, you must enable RSA authentication, too. PickleRPC traffic\nis encrypted by session keys that themselves are encrypted using RSA.', allowpicklerpc=0)
if hasCrypto:
    config.append('You can activate RSA authentication for RPC calls. If you\ndo, you need to generate keys of a given keysize and need to store all\nallowed public keys in your pubkeys directory where they are checked\nautomatically. The keys need to be stored under the servername of the\ntoolservers (or actually clients) calling.', rsakeysize=1024, rsaauthenticate=0)