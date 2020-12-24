# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/aha/controller/util.py
# Compiled at: 2010-10-22 05:12:42
__author__ = 'Atsushi Shibata <shibata@webcore.co.jp>'
__docformat__ = 'plaintext'
__licence__ = 'BSD'
import logging
from google.appengine.api import mail

def get_controller_class(cnt, plugin=''):
    """
    A function to obtain controller associated to given content object.
    When the argument plugin given,
        the controller will be read via given plugin directory.
    """
    try:
        exec 'from application.controller import %s' % cnt.lower() in globals()
        ctrl_clz = eval('%s.%sController' % (cnt.lower(), cnt.capitalize()))
        return ctrl_clz
    except ImportError:
        if not plugin:
            plugin = cnt
        exec 'from plugin.%s import %s' % (plugin.lower(), cnt.lower()) in globals()
        ctrl_clz = eval('%s.%sController' % (cnt.lower(), cnt.capitalize()))
        return ctrl_clz


def get_current_user():
    """
    A function to obtain current login user.
    """
    from coregae import Config
    config = Config()
    return config.auth_obj().get_user(None)