# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/solstice/widgets/window.py
# Compiled at: 2020-03-08 13:23:53
# Size of source mod 2**32: 2081 bytes
"""
Base wrapper classes to create DCC windows for Solstice
"""
from __future__ import print_function, division, absolute_import
__author__ = 'Tomas Poveda'
__license__ = 'MIT'
__maintainer__ = 'Tomas Poveda'
__email__ = 'tpovedatd@gmail.com'
from tpDcc.libs.qt.core import dragger
import artellapipe.register
from artellapipe.widgets import window
from artellapipe.libs.kitsu.widgets import userinfo

class SolsticeWindowDragger(dragger.WindowDragger, object):

    def __init__(self, window=None, on_close=None):
        self._user_info = None
        super(SolsticeWindowDragger, self).__init__(window=window, on_close=on_close)

    def set_project(self, project):
        if self._user_info:
            self._user_info.set_project(project)
        else:
            self._user_info = userinfo.KitsuUserInfo(project=project)
            self.buttons_layout.insertWidget(0, self._user_info)

    def try_kitsu_login(self):
        """
        Function that tries to login into Kitsu with stored credentials
        :return: bool
        """
        if not self._user_info:
            return False
        else:
            valid_login = self._user_info.try_kitsu_login()
            if valid_login:
                return True
            return False


class SolsticeWindow(window.ArtellaWindow, object):
    DRAGGER_CLASS = SolsticeWindowDragger

    def __init__(self, *args, **kwargs):
        (super(SolsticeWindow, self).__init__)(*args, **kwargs)

    def ui(self):
        super(SolsticeWindow, self).ui()
        kitsu_login = self._config.get('kitsu_login', default=True)
        if kitsu_login:
            self._dragger.set_project(self._project)
            self.try_kitsu_login()

    def try_kitsu_login(self):
        """
        Function that tries to login into Kitsu with stored credentials
        :return: bool
        """
        kitsu_login = self._config.get('kitsu_login', default=True)
        if kitsu_login:
            return self._dragger.try_kitsu_login()


artellapipe.register.register_class('Window', SolsticeWindow)