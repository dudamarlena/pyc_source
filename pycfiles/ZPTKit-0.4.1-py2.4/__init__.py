# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/ZPTKit/__init__.py
# Compiled at: 2006-06-20 16:13:48
try:
    from pkg_resource import require
except ImportError:
    pass
else:
    require('Component')

try:
    from zptcomponent import ZPTComponent
except ImportError, e:
    pass

def InstallInWebKit(appServer):
    pass