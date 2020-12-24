# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-i386/egg/blipapi/test.py
# Compiled at: 2010-02-27 14:52:20
import blipapi
from pprint import pprint
import time, sys
b = blipapi.BlipApi(dont_connect=False)
b.authorize('myszapi', 'jsDhzc1')
b.parser = eval
imgs = ('/Users/mysz/test_img/avatar.jpg', '/Users/mysz/test_img/test_jpg/01.jpg')