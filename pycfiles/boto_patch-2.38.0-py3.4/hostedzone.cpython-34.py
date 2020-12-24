# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/boto/route53/hostedzone.py
# Compiled at: 2015-11-24 05:02:18
# Size of source mod 2**32: 1961 bytes


class HostedZone(object):

    def __init__(self, id=None, name=None, owner=None, version=None, caller_reference=None):
        self.id = id
        self.name = name
        self.owner = owner
        self.version = version
        self.caller_reference = caller_reference

    def startElement(self, name, attrs, connection):
        pass

    def endElement(self, name, value, connection):
        if name == 'Id':
            self.id = value
        else:
            if name == 'Name':
                self.name = value
            else:
                if name == 'Owner':
                    self.owner = value
                else:
                    if name == 'Version':
                        self.version = value
                    else:
                        if name == 'CallerReference':
                            self.caller_reference = value
                        else:
                            setattr(self, name, value)