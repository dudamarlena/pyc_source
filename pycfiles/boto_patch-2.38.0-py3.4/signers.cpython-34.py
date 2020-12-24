# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/boto/cloudfront/signers.py
# Compiled at: 2015-11-24 05:02:18
# Size of source mod 2**32: 2074 bytes


class Signer(object):

    def __init__(self):
        self.id = None
        self.key_pair_ids = []

    def startElement(self, name, attrs, connection):
        pass

    def endElement(self, name, value, connection):
        if name == 'Self':
            self.id = 'Self'
        else:
            if name == 'AwsAccountNumber':
                self.id = value
            elif name == 'KeyPairId':
                self.key_pair_ids.append(value)


class ActiveTrustedSigners(list):

    def startElement(self, name, attrs, connection):
        if name == 'Signer':
            s = Signer()
            self.append(s)
            return s

    def endElement(self, name, value, connection):
        pass


class TrustedSigners(list):

    def startElement(self, name, attrs, connection):
        pass

    def endElement(self, name, value, connection):
        if name == 'Self':
            self.append(name)
        elif name == 'AwsAccountNumber':
            self.append(value)