# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/linguist/libs/md5.py
# Compiled at: 2013-08-28 13:39:08
import hashlib

class MD5(object):

    def __repr__(self):
        return '<MD5>'

    @classmethod
    def hexdigest(cls, obj):
        digest = hashlib.md5()
        if isinstance(obj, (str, int)):
            digest.update(obj.__class__.__name__)
            digest.update('%s' % obj)
        elif isinstance(obj, bool) or obj is None:
            digest.update(obj.__class__.__name__)
        elif isinstance(obj, (list, tuple)):
            digest.update(obj.__class__.__name__)
            for e in obj:
                digest.update(cls.hexdigest(e))

        elif isinstance(obj, dict):
            digest.update(obj.__class__.__name__)
            hexs = [ cls.hexdigest([k, v]) for k, v in obj.iteritems() ]
            hexs.sort()
            for e in hexs:
                digest.update(e)

        else:
            raise TypeError("can't convert %s into String" % obj)
        return digest.hexdigest()