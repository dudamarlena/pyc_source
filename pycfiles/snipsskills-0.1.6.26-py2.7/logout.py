# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-intel/egg/snipsskills/commands/session/logout.py
# Compiled at: 2017-10-03 05:37:48
from ..base import Base
from snipsskillscore import pretty_printer as pp
from ...utils.os_helpers import write_text_file, read_file, file_exists, ask_for_input, ask_for_password
from ...utils.cache import Cache
from ...utils.auth import Auth

class Logout(Base):

    def run(self):
        if Cache.get_login_token() is not None:
            Logout.logout()
            pp.psuccess('You are now signed out')
        else:
            pp.psuccess('You are already signed out')
        return

    @staticmethod
    def logout():
        Cache.clear_login_token()