# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pgp/commands/gpg/sign_key.py
# Compiled at: 2015-08-31 08:17:33
from pgp.commands.gpg.sign_ import SignCommand

class Command(SignCommand):

    def __init__(self, formatter, io_helper, force_v3_sigs, force_v4_certs, signature_notations, certification_notations, notations, sig_policy_url, cert_policy_url, policy_url, preferred_keyserver, default_keyserver_url, message_filename):
        SignCommand.__init__(self, io_helper, force_v3_sigs, force_v4_certs, signature_notations, certification_notations, notations, sig_policy_url, cert_policy_url, policy_url, preferred_keyserver, default_keyserver_url, message_filename)