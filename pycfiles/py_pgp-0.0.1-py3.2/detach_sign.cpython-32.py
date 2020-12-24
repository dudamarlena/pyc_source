# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pgp/commands/gpg/detach_sign.py
# Compiled at: 2015-08-31 08:17:33
from pgp.commands.gpg.sign import Command as SignCommand

class Command(SignCommand):

    def output(self, message, filename):
        output_filename = self.formatter.make_output_filename(filename)
        signature = message.signatures[0]
        self.io_helper.write_output(self.formatter.format_signature(signature), output_filename=output_filename)