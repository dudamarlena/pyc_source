# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mabs/test.py
# Compiled at: 2015-03-21 13:59:34
from mabs import *
a = TranTune(['192.168.1.1', '2', '23', '213', 'sdf'], gothreading=False)
a.send_file_support_shell('`date +%F`.bak')