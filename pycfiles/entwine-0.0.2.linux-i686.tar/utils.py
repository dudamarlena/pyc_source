# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python2.5/site-packages/entwine/utils.py
# Compiled at: 2008-03-13 14:54:53
"""

utils.py
===========

Misc helper funcitions 
----------------------

Author: Rob Cakebread <cakebread@ gmail. com>

License  : New BSD (See COPYING)

"""
__docformat__ = 'restructuredtext'
import os
from configobj import ConfigObj

def get_user_passwd():
    """Return a tuple of (username, password)"""
    get_rcfile_path()
    config = ConfigObj(get_rcfile_path())
    return (config['username'], config['password'])


def get_entwine_dir():
    """Return path where we store config files and data"""
    twinedir = os.path.abspath(os.path.expanduser('~/.entwine'))
    if not os.path.exists(twinedir):
        os.mkdir(twinedir)
        template = 'username = "twine_username"\npassword = "twine_password"\n        '
        open('%s/entwinerc' % twinedir, 'w').write(template)
    return twinedir


def get_rcfile_path():
    """Return path of rc config file"""
    return os.path.abspath('%s/entwinerc' % get_entwine_dir())