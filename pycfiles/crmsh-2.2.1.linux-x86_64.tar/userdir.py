# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python2.7/site-packages/crmsh/userdir.py
# Compiled at: 2016-05-04 07:56:27
import os

def getuser():
    """Returns the name of the current user"""
    import getpass
    return getpass.getuser()


def gethomedir(user=''):
    return os.path.expanduser('~' + user)


CONFIG_HOME = os.path.join(os.path.expanduser('~/.config'), 'crm')
CACHE_HOME = os.path.join(os.path.expanduser('~/.cache'), 'crm')
try:
    from xdg import BaseDirectory
    CONFIG_HOME = os.path.join(BaseDirectory.xdg_config_home, 'crm')
    CACHE_HOME = os.path.join(BaseDirectory.xdg_cache_home, 'crm')
except:
    pass

HISTORY_FILE = os.path.expanduser('~/.crm_history')
RC_FILE = os.path.expanduser('~/.crm.rc')
CRMCONF_DIR = os.path.expanduser('~/.crmconf')
GRAPHVIZ_USER_FILE = os.path.join(CONFIG_HOME, 'graphviz')

def mv_user_files():
    """
    Called from main
    """
    global CRMCONF_DIR
    global HISTORY_FILE
    global RC_FILE

    def _xdg_file(name, xdg_name, chk_fun, directory):
        from .msg import common_warn, common_info, common_debug
        if not name:
            return name
        if not os.path.isdir(directory):
            os.makedirs(directory, 448)
        new = os.path.join(directory, xdg_name)
        if directory == CONFIG_HOME and chk_fun(new) and chk_fun(name):
            common_warn('both %s and %s exist, please cleanup' % (name, new))
            return name
        if chk_fun(name):
            if directory == CONFIG_HOME:
                common_info('moving %s to %s' % (name, new))
            else:
                common_debug('moving %s to %s' % (name, new))
            os.rename(name, new)
        return new

    HISTORY_FILE = _xdg_file(HISTORY_FILE, 'history', os.path.isfile, CACHE_HOME)
    RC_FILE = _xdg_file(RC_FILE, 'rc', os.path.isfile, CONFIG_HOME)
    CRMCONF_DIR = _xdg_file(CRMCONF_DIR, 'crmconf', os.path.isdir, CONFIG_HOME)