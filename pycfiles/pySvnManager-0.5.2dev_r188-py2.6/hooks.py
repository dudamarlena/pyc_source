# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pysvnmanager/model/hooks.py
# Compiled at: 2010-08-08 03:18:44
"""Subversion repos hooks plugin.

Basic classes used for Subversion hooks management.
"""
import re, sys, os, StringIO, logging
log = logging.getLogger(__name__)
from pylons import config
config_path = config['here'] + '/config'
if config_path not in sys.path:
    sys.path.insert(0, config_path)
from localconfig import LocalConfig as cfg
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from pysvnmanager.hooks import plugins
from pysvnmanager.model import repos
if not config.has_key('unittest'):
    from pylons.i18n import _
else:

    def _(message):
        return message


class Hooks:

    def __init__(self, repos_path):
        self.__repos_path = os.path.abspath(repos_path)
        self.__repos_root = os.path.dirname(self.__repos_path)
        self.__repos_name = os.path.basename(self.__repos_path)
        self.repos = repos.Repos(self.__repos_root)
        assert self.repos.is_svn_repos(self.__repos_name)
        self.plugins = {}
        for m in plugins.modules:
            self.plugins[m] = plugins.getHandler(m)(self.__repos_path)
            self.plugins[m].id = m

        self.pluginnames = [ m.id for m in sorted(self.plugins.values()) ]

    def __get_applied_plugins(self):
        return [ m for m in self.pluginnames if self.plugins[m].enabled() ]

    applied_plugins = property(__get_applied_plugins)

    def __get_unapplied_plugins(self):
        return [ m for m in self.pluginnames if not self.plugins[m].enabled() ]

    unapplied_plugins = property(__get_unapplied_plugins)

    def __get_repos_root(self):
        return self.__repos_root

    repos_root = property(__get_repos_root)

    def __get_repos_name(self):
        return self.__repos_name

    repos_name = property(__get_repos_name)

    def __get_repos_path(self):
        return self.__repos_path

    repos_path = property(__get_repos_path)


if __name__ == '__main__':
    import doctest
    doctest.testmod()