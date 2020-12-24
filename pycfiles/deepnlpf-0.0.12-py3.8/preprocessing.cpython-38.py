# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/deepnlpf/modules/utils/preprocessing.py
# Compiled at: 2020-03-16 10:45:56
# Size of source mod 2**32: 215 bytes
"""
"""

class PreProcessing(object):
    __doc__ = '\n    '

    def remove_special_characters(self, sentence):
        import re
        return re.sub('[-_./?,`":;=+()|@#$%&*^~\\\']', '', sentence)