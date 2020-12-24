# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-ppc/egg/zif/jsmin/javascript.py
# Compiled at: 2006-12-16 06:43:22
"""The javascript compressor uses the 3rdparty packer module
that is taken from Plone's ResourceRegistries."""
from thirdparty.packer import JavascriptPacker
jspacker_safe = JavascriptPacker('safe')
jspacker_full = JavascriptPacker('full')

def compress(data, compress_level):
    if compress_level == 'safe':
        return jspacker_safe.pack(data)
    elif compress_level == 'full':
        return jspacker_full.pack(data)
    else:
        return data