# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/build/honeynet/beeswarm/beeswarm/shared/vnc/decoder.py
# Compiled at: 2016-11-12 07:38:04
from beeswarm.shared.vnc.des import RFBDes

class VNCDecoder(object):

    def __init__(self, challenge, response, passwd_list):
        self.challenge = challenge
        self.response = response
        self.passwd_list = passwd_list

    def decode(self):
        for password in self.passwd_list:
            password = password.strip('\n')
            key = (password + '\x00\x00\x00\x00\x00\x00\x00\x00')[:8]
            encryptor = RFBDes(key)
            resp = encryptor.encrypt(self.challenge)
            if resp == self.response:
                return key