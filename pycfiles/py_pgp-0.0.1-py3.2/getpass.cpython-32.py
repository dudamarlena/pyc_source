# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pgp/pinentry/getpass.py
# Compiled at: 2015-08-31 08:17:33
from getpass import getpass
import sys

class GetPassPinentry(object):

    def __init__(self):
        self._cache = {}

    def get_passphrase(self, prompt=None, error_message=None, description=None, cache_id=None, use_cache=True, no_ask=False, qualitybar=False, repeat=0, stream=sys.stdout):
        if prompt in (None, 'X'):
            prompt = 'PIN?'
        if error_message in (None, 'X'):
            error_message = 'Error.'
        if description in (None, 'X'):
            description = ''
        if cache_id == 'X':
            cache_id = None
        if use_cache and cache_id and cache_id in self._cache:
            return self._cache[cache_id]
        else:
            if no_ask:
                raise KeyError(cache_id)
            if prompt:
                print(prompt, file=stream)
            if description:
                print(description, file=stream)
            match = False
            while not match:
                match = True
                if error_message:
                    print(error_message, file=stream)
                passphrase = getpass('Password: ', stream=stream)
                for _i in range(repeat):
                    if getpass('Confirm: ', stream=stream) != passphrase:
                        match = False
                        error_message = 'Passwords do not match.'
                        continue

            if use_cache and cache_id:
                self._cache[cache_id] = passphrase
            return passphrase

    def clear_passphrase(self, cache_id):
        while cache_id in self._cache:
            del self._cache[cache_id]