# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-intel/egg/snipsskills/commands/session/login.py
# Compiled at: 2017-10-03 05:19:03
from ..base import Base
from .logout import Logout
from snipsskillscore import pretty_printer as pp
from ...utils.os_helpers import write_text_file, read_file, file_exists, ask_for_input, ask_for_password
from ...utils.cache import Cache
from ...utils.auth import Auth

class InvalidTokenException(Exception):
    pass


class Login(Base):

    def run(self):
        try:
            Login.login(email=self.options['--email'], password=self.options['--password'])
        except Exception as e:
            pp.perror(('Error logging in: {}').format(str(e)))

    @staticmethod
    def login(email=None, password=None, greeting=None, silent=False):
        has_credentials = email is not None and password is not None
        silent = silent or has_credentials
        if has_credentials:
            Logout.logout()
        token = Cache.get_login_token()
        if not token:
            if not has_credentials:
                pp.pcommand(greeting or 'Please enter your Snips Console credentials')
                email = ask_for_input('Email address:')
                password = ask_for_password('Password:')
            token = Auth.retrieve_token(email, password)
            if token is not None:
                Cache.save_login_token(token)
                if not silent:
                    pp.psuccess('You are now signed in')
            else:
                raise InvalidTokenException('Could not validate authentication token')
        elif not silent:
            pp.psuccess('You are already signed in')
        return token