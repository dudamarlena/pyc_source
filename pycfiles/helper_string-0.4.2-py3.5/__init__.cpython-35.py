# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/helper_string/__init__.py
# Compiled at: 2018-10-30 09:29:14
# Size of source mod 2**32: 1931 bytes
import os, datetime, sys

class HelperString(object):

    @staticmethod
    def to_uni(obj):
        if isinstance(obj, bytes):
            try:
                return obj.decode('utf-8')
            except UnicodeDecodeError:
                return obj.decode('gbk')

        else:
            if isinstance(obj, int):
                return unicode(obj)
            else:
                if isinstance(obj, (datetime.date, datetime.datetime)):
                    return obj.isoformat()
                if isinstance(obj, dict):
                    m = dict()
                    for k in obj.keys():
                        v = obj[k]
                        m[HelperString.to_uni(k)] = HelperString.to_uni(v)

                    return m
                if isinstance(obj, list):
                    return [HelperString.to_uni(i) for i in obj]
                return obj

    @staticmethod
    def to_str(obj):
        if sys.version_info.major == 2 and isinstance(obj, unicode):
            return obj.encode('utf-8')
        else:
            if isinstance(obj, list):
                return [HelperString.to_str(i) for i in obj]
            if isinstance(obj, dict):
                m = dict()
                for k in obj.keys():
                    v = obj[k]
                    m[HelperString.to_str(k)] = HelperString.to_str(v)

                return m
            return obj

    @staticmethod
    def shorten(s, placeholder='...', max_legnth=64):
        if len(s) > len(placeholder) and len(s) > max_legnth:
            return s[:max_legnth - 3] + placeholder + s[-len(placeholder):]
        return s

    @staticmethod
    def shorten_filename(filename, placeholder='...', max_length=64):
        filename = HelperString.to_uni(filename)
        if len(filename) > len(placeholder) and len(filename) > max_length:
            fn, ext = os.path.splitext(filename)
            shorten = fn[:max_length - len(placeholder)] + placeholder + fn[-len(placeholder):] + ext
        else:
            shorten = filename
        return shorten