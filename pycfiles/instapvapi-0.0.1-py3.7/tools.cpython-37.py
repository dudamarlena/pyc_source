# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/client/utils/tools.py
# Compiled at: 2020-03-30 11:33:28
# Size of source mod 2**32: 876 bytes
from uuid import uuid4
import hmac, urllib, hashlib
from client.config import Config

class Tools:

    def __init__(self):
        self.config = Config()
        super().__init__()

    def generate_uuid(self, type):
        generated_uuid = str(uuid4())
        if type:
            return generated_uuid
        return generated_uuid.replace('-', '')

    def generate_signature(self, data, skip_quote=False):
        if not skip_quote:
            try:
                parsedData = urllib.parse.quote(data)
            except AttributeError:
                parsedData = urllib.quote(data)

        else:
            parsedData = data
        return 'ig_sig_key_version=' + self.config.SIG_KEY_VERSION + '&signed_body=' + hmac.new(self.config.IG_SIG_KEY.encode('utf-8'), data.encode('utf-8'), hashlib.sha256).hexdigest() + '.' + parsedData