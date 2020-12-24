# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/shodh/Projects/django_ginger/ginger/stash/compat.py
# Compiled at: 2014-05-21 01:38:00
try:
    import six
except ImportError:
    from django.utils import six

import hashlib
if six.PY2:
    md5 = hashlib.md5
else:

    class md5:

        def __init__(self, s=None):
            self.md5 = hashlib.md5()
            if s is not None:
                self.update(s)
            return

        def update(self, s):
            return self.md5.update(s.encode('utf-8'))

        def hexdigest(self):
            return self.md5.hexdigest()


__all__ = [
 'six', 'md5']