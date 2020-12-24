# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Larco/Documents/Github/pyvenom/framework/venom/vendor.py
# Compiled at: 2016-04-13 20:07:13
from google.appengine.ext import vendor
import os
path = os.path.join(os.path.dirname(__file__), 'vendor')
vendor.add(path)