# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/r/repo/aibolit/utils/utils.py
# Compiled at: 2020-04-10 11:54:00
# Size of source mod 2**32: 485 bytes
import re

class RemoveComments:

    def __init__(self):
        pass

    @staticmethod
    def remove_comments(string):
        string = re.sub(re.compile('/\\*.*?\\*/', re.DOTALL), '', string)
        string = re.sub(re.compile('//.*?\\n'), '', string)
        return string