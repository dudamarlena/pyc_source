# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/trac_captcha/cryptobox.py
# Compiled at: 2010-06-24 12:58:36
from datetime import datetime, timedelta
from hmac import HMAC
import re
from trac.util import hex_entropy
from trac.util.datefmt import localtz, to_timestamp, utc
__all__ = [
 'CryptoBox']

class CryptoBox(object):

    def __init__(self, key=None):
        self.key = key
        self.hash_algorithm = None
        return

    def generate_key(self):
        return hex_entropy(32)

    def generate_token(self):
        message = self.token_payload()
        return message + '||' + self.sign_message(message)

    def is_token_valid(self, token):
        if not self.is_syntactically_valid_token(token):
            return False
        message, hash = self.parse_token(token)
        if not self.is_correct_hash(hash, message):
            return False
        return self.token_is_valid_until(message) >= datetime.now(localtz)

    def best_hash_algorithm(self):
        if self.hash_algorithm is not None:
            return self.hash_algorithm
        else:
            try:
                from hashlib import sha512
                self.hash_algorithm = sha512
                return sha512
            except ImportError:
                pass

            try:
                from Crypto.Hash import SHA256
                self.hash_algorithm = SHA256
                return SHA256
            except ImportError:
                pass

            import sha
            self.hash_algorithm = sha
            return sha

    def sign_message(self, message):
        if self.key is None:
            self.key = self.generate_key()
        return HMAC(self.key, message, digestmod=self.best_hash_algorithm()).hexdigest()

    def token_payload(self, valid_until=None):
        if valid_until is None:
            valid_until = datetime.now(localtz) + timedelta(hours=4)
        return str(to_timestamp(valid_until))

    def is_syntactically_valid_token(self, token):
        if not hasattr(token, 'split'):
            return False
        parts = token.split('||')
        if len(parts) != 2:
            return False
        return True

    def token_is_valid_until(self, timestamp):
        if re.search('\\D', timestamp) is not None:
            return datetime.fromtimestamp(0, utc)
        else:
            return datetime.fromtimestamp(int(timestamp), utc)

    def parse_token(self, token):
        return token.split('||', 1)

    def is_correct_hash(self, hash, message):
        return hash == self.sign_message(message)