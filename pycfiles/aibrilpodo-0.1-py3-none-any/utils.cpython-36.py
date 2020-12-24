# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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