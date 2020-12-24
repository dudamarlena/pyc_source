# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/gaufung/WorkSpace/SimpleWebFramework/example/app.py
# Compiled at: 2017-09-20 05:37:45
import os
from tindo import Tindo
from example import urls
app = Tindo(os.path.dirname(os.path.abspath(__file__)))
app.add_module(urls)