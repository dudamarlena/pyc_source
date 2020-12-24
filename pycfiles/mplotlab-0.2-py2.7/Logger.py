# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\mplotlab\utils\Logger.py
# Compiled at: 2016-02-07 09:44:32
import logging
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
root = logging.getLogger('')
root.propagate
root.setLevel(logging.DEBUG)
root.addHandler(ch)
log = logging.getLogger()