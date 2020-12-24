# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/martin/Workspace/django-staticinline/staticinline/tests/testapp/apps.py
# Compiled at: 2018-08-14 07:55:12
# Size of source mod 2**32: 879 bytes
"""
Custom app config for staticinline to demonstrate and test
the 'custom encoder' functionality.
"""
from staticinline.apps import StaticInlineAppConfig

class CustomizedStaticInlineAppConfig(StaticInlineAppConfig):
    __doc__ = '\n    Add a custom encoder to the list to test that behavior\n    '

    def get_encoder(self):
        encoder = super(CustomizedStaticInlineAppConfig, self).get_encoder()
        encoder.update({'uppercase': self.uppercase, 
         'broken': self.broken})
        return encoder

    def uppercase(self, data, path):
        """
        Sample encoder that turns the incoming text data uppercase.
        """
        return data.decode(self.encoder_response_format).upper()

    def broken(self, data, path):
        """
        This intentionally raises an Exception to test error reporting.
        """
        return 1 / 0