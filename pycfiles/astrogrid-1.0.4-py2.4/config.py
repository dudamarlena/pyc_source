# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.darwin-9.6.0-i386/egg/astrogrid/config.py
# Compiled at: 2008-03-28 05:44:05
import sys, os, stat, md5
from astrogrid.configobj import ConfigObj
import getpass, StringIO, operator, urllib
python_acr = '\n# This is a skeleton configuration file for ACR access from Python\n# Add your credentials to the different communities and copy it to\n# $HOME/.python-acr (UNIX) or $HOME/_python-acr (Windows) and make sure \n# that it is only readable for the owner: chmod 0600 $HOME/.python-acr\n\ndebug = False\nverbose = True\nautologin = True\nplastic = False\ntimeout = None\n\n[community]\n# We choose Leicester as the default community\ndefault = leicester\n\n[[ukidss]] # UKIDSS community.\nusername = \npassword = \ncommunity = ukidss.roe.ac.uk\n\n[[leicester]] # Leicester community\nusername = \npassword = \ncommunity = uk.ac.le.star\n'
ipythonrc = '# -*- Mode: Shell-Script -*-  Not really, but shows comments correctly\n#***************************************************************************\n#\n# Configuration file for ipython -- ipythonrc format\n#\n# The format of this file is one of \'key value\' lines.\n# Lines containing only whitespace at the beginning and then a # are ignored\n# as comments. But comments can NOT be put on lines with data.\n#***************************************************************************\n\n# This is an example of a \'profile\' file which includes a base file and adds\n# some customizaton for a particular purpose.\n\n# If this file is found in the user\'s ~/.ipython directory as ipythonrc-astrogr\nid,\n# it can be loaded by calling passing the \'-profile astrogrid\' (or \'-p astrogri\nd\')\n# option to IPython.\n\n# load our basic configuration with generic options\ninclude ipythonrc\n\n# import ...\nimport_mod astrogrid\n\n# from ... import ...\nimport_some astrogrid aghelp\nimport_some astrogrid acr\nimport_some astrogrid ConeSearch\nimport_some astrogrid SiapSearch\nimport_some astrogrid MySpace\nimport_some astrogrid Applications\nimport_some astrogrid DSA\n\nexecute print ""\nexecute print "  Welcome to the Astrogrid from Python environment."\nexecute print "  For more information, type aghelp()."\n# execute if not acr._connected: acr.starthub()\n'

def cryptXOR(str2, pw):
    sr = StringIO.StringIO(str2)
    sw = StringIO.StringIO(str2)
    sr.seek(0)
    sw.seek(0)
    n = 0
    for k in range(len(str2)):
        if n >= len(pw) - 1:
            n = 0
        p = ord(pw[n])
        n += 1
        c = sr.read(1)
        b = ord(c)
        t = operator.xor(b, p)
        z = chr(t)
        sw.seek(k)
        sw.write(z)

    sw.seek(0)
    res = sw.read()
    sr.close()
    sw.close()
    return res


def cryptconf():
    """Encrypt/decrypt configuration file"""
    home = os.path.expanduser('~')
    if sys.platform[:3] == 'win':
        conffile = os.path.join(home, '_python-acr')
    else:
        conffile = os.path.join(home, '.python-acr')
    buffer = open(conffile, 'rb').read()
    pw = getpass.getpass('Please insert your password: ')
    res = cryptXOR(buffer, pw)
    open(conffile, 'wb').write(res)


def which(filename):
    """Find executable in PATH"""
    if not os.environ.has_key('PATH') or os.environ['PATH'] == '':
        p = os.defpath
    else:
        p = os.environ['PATH']
    pathlist = p.split(os.pathsep)
    for path in pathlist:
        f = os.path.join(path, filename)
        if os.access(f, os.X_OK):
            return f

    return


def write_config():
    """Write current config values to configuration file."""
    if sys.platform[:3] == 'win':
        configfile = os.path.expanduser('~/_python-acr')
    else:
        configfile = os.path.expanduser('~/.python-acr')
    _config.write(configfile)


def install_ar(path):
    """Download the AR and instal it in some path. Update the configuration file."""
    filename = 'asr-2007.1.1-app.jar'
    url = 'http://www2.astrogrid.org/desktop/download/' + filename
    urllib.urlretrieve(url, os.path.join(path, filename))
    javapath = which('java')
    if not javapath:
        javapth = '<path to your java executable>'
    print 'AR installed. In order to start the AR from Python, the following have been added'
    print 'lines to your .python-acr configuration file:'
    print ''
    print 'javapath = %s' % javapath
    print 'acrpath = %s' % os.path.join(path, filename)
    _config['javapath'] = javapath
    _config['acrpath'] = os.path.join(path, filename)
    write_config()


if sys.platform[:3] == 'win':
    configfile = os.path.expanduser('~/_python-acr')
else:
    configfile = os.path.expanduser('~/.python-acr')
if not os.access(configfile, os.F_OK):
    open(configfile, 'w').write(python_acr)
try:
    fmode = stat.S_IMODE(os.stat(configfile)[stat.ST_MODE])
    cmode = stat.S_IWRITE + stat.S_IREAD
    if fmode != cmode:
        os.chmod(configfile, cmode)
except:
    pass

buffer = open(configfile, 'rb').read()
if md5.new(python_acr).hexdigest() == md5.new(buffer).hexdigest():
    print 'Default configuration file written in %s. Please edit it with your details.' % configfile
    sys.exit()
try:
    _config = ConfigObj(StringIO.StringIO(buffer))
except:
    print 'Your configuration file looks encrypted.'
    pw = getpass.getpass('Please type your password: ')
    buffer = cryptXOR(buffer, pw)
    _config = ConfigObj(StringIO.StringIO(buffer))

for k in ['debug', 'verbose', 'autologin', 'plastic', 'starthub']:
    _config[k] = _config.get(k, 'False') == 'True'

if not _config.has_key('community'):
    _config['community'] = {}