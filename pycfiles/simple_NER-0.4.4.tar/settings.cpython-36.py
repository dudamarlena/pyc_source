# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/user/PycharmProjects/simple_NER/simple_NER/settings.py
# Compiled at: 2019-12-12 21:17:29
# Size of source mod 2**32: 125 bytes
from os.path import join, dirname
STOPLIST = join(dirname(__file__), 'annotators', 'utils', 'keywords', 'SmartStoplist.txt')