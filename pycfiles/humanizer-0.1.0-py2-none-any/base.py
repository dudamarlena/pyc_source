# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/grimen/Dev/Private/python-humanizer/humanizer/base.py
# Compiled at: 2019-05-15 01:07:25
import rootpath
rootpath.append()
import mybad

class HumanizerError(mybad.Error):
    pass


class Humanizer(object):

    @classmethod
    def default(klass):
        if not hasattr(klass, 'instance') or klass.instance is None:
            klass.instance = klass()
        return klass.instance


__all__ = [
 'HumanizerError',
 'Humanizer']