# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pgp/commands/gpg/clearsign.py
# Compiled at: 2015-08-31 08:17:33
from pgp.commands.gpg.sign import Command as SignCommand
from pgp.packets.constants import SIGNATURE_OF_A_CANONICAL_TEXT_DOCUMENT

class Command(SignCommand):

    def sign_message(self, msg, signature_type=None, one_pass=True):
        if signature_type is None:
            signature_type = SIGNATURE_OF_A_CANONICAL_TEXT_DOCUMENT
        return SignCommand.sign_message(self, msg, signature_type, one_pass)

    def postprocess_message(self, msg):
        return msg

    def output(self, message, filename):
        output_filename = self.formatter.make_output_filename(filename)
        self.io_helper.write_output(self.formatter.format_message(message, armor=True), output_filename=output_filename)