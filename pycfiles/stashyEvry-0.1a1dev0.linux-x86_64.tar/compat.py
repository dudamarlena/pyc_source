# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/e210990/bin/python26/lib/python2.6/site-packages/stashy/compat.py
# Compiled at: 2014-06-25 10:41:27
import sys
_ver = sys.version_info
is_py2 = _ver[0] == 2
is_py3 = _ver[0] == 3
if is_py2:

    def update_doc(method, newdoc):
        method.im_func.func_doc = newdoc


    basestring = basestring
elif is_py3:

    def update_doc(method, newdoc):
        method.__doc__ = newdoc


    basestring = (
     str, bytes)