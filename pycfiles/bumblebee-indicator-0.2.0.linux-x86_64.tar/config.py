# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/bumblebee_indicator/config.py
# Compiled at: 2014-07-01 13:33:04
import os.path as p, logging
FORMAT = '%(asctime)-15s %(levelname)-10s %(message)s'
logging.basicConfig(level=logging.INFO, format=FORMAT)

class ConfigDict:
    """The recursive class for building and representing objects with."""

    def __init__(self, obj):
        for k, v in obj.iteritems():
            if isinstance(v, dict):
                setattr(self, k, Struct(v))
            else:
                setattr(self, k, v)

    def __getitem__(self, val):
        return self.__dict__[val]

    def __repr__(self):
        return '{%s}' % str((', ').join('%s : %s' % (k, repr(v)) for k, v in self.__dict__.iteritems()))


__dirname = p.dirname(p.abspath(__file__))
paths = ConfigDict({'python': __dirname, 
   'resources': p.join(__dirname, 'resources')})
PING_FREQUENCY = 500

def get_resource(*args):
    sub = p.join(*args)
    return p.join(paths.resources, sub)