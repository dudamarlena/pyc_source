# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/hermit/signer/echo_signer.py
# Compiled at: 2019-07-11 16:56:25
# Size of source mod 2**32: 825 bytes
from hermit.qrcode import displayer
from hermit.signer.base import Signer

class EchoSigner(Signer):
    __doc__ = 'Returns the signature request data as a signature.\n\n    This class is useful for debugging signature requests.\n    '

    def validate_request(self) -> None:
        """Validate the signature request
        
        Does nothing :)
        """
        pass

    def display_request(self) -> None:
        """Prints the signature request"""
        print('QR Code:\n        {}\n        '.format(self.request))

    def create_signature(self) -> None:
        """Create a fake signature

        The signature data is just the request data.
        """
        self.signature = self.request

    def _signature_label(self) -> str:
        return 'Request'