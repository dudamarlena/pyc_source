# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/toxiproxy/toxic.py
# Compiled at: 2018-08-22 09:02:13
# Size of source mod 2**32: 525 bytes


class Toxic(object):
    __doc__ = ' Represents a Proxy object '

    def __init__(self, **kwargs):
        """ Initializing the Toxic object """
        self.type = kwargs['type']
        self.stream = kwargs['stream'] if 'stream' in kwargs else 'downstream'
        self.name = kwargs['name'] if 'name' in kwargs else '%s_%s' % (self.type, self.stream)
        self.toxicity = kwargs['toxicity'] if 'toxicity' in kwargs else 1.0
        self.attributes = kwargs['attributes'] if 'attributes' in kwargs else {}