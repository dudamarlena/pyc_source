# uncompyle6 version 3.6.7
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/cifitlib/classes.py
# Compiled at: 2011-01-27 14:39:21
__doc__ = '\nclasses.py\n\nCreated by Craig Sawyer on 2010-01-14.\nCopyright (c) 2010 Craig Sawyer. All rights reserved.\n\nStorage stolen from web.py see LICENSE for details.\nhttp://www.web.py\n'
import re, os, time, socket, sys
from files import run

class Storage(dict):
    """
    A Storage object is like a dictionary except `obj.foo` can be used
    instead of `obj['foo']`. Create one by doing `storage({'a':1})`.
    """

    def __getattr__(self, key):
        if self.has_key(key):
            return self[key]
        raise AttributeError, repr(key)

    def __setattr__(self, key, value):
        self[key] = value

    def __repr__(self):
        return '<Storage ' + dict.__repr__(self) + '>'


classes = Storage()
dow = {0: 'Monday', 
   1: 'Tuesday', 
   2: 'Wednesday', 
   3: 'Thursday', 
   4: 'Friday', 
   5: 'Saturday', 
   6: 'Sunday'}

def roundDown(num, rounder=5):
    """this does the rounding for the min_ classes
        rounder should be set to whatever your crontab is set to probably.
        """
    return num // rounder * rounder


classes.DISTRIB_ID = 'Unknown'
if os.path.exists('/etc/lsb-release'):
    for line in open('/etc/lsb-release', 'r'):
        (key, value) = line.split('=')
        classes[key] = value.strip()

if os.path.exists('/etc/debian_version'):
    for line in open('/etc/debian_version', 'r'):
        classes['DISTRIB_ID'] = 'Debian'
        classes['DISTRIB_RELEASE'] = line.strip()

if os.path.exists('/etc/redhat-release'):
    line = open('/etc/redhat-release').readline()
    match = re.match('(\\S*) release (\\S*) \\((\\S*)\\)', line)
    classes['DISTRIB_ID'] = match.group(1)
    classes['DISTRIB_RELEASE'] = match.group(2).split('.')
abspath = os.path.abspath(sys.argv[0])
classes.cifitlocation = os.path.dirname(abspath)
classes.hostname = socket.gethostname()
classes.hour = time.localtime()[3]
classes.dow = dow[time.localtime()[6]]
classes.minutes = roundDown(time.localtime()[4])
hour = time.localtime()[3]
classes.platform = sys.platform
classes.mainip = socket.gethostbyname(socket.gethostname())
if classes.platform in ('Linux', 'Darwin'):
    classes.kernelver = run('uname -r')[1][0]
if __name__ == '__main__':
    for (k, v) in classes.items():
        print '%s: %s' % (k, v)