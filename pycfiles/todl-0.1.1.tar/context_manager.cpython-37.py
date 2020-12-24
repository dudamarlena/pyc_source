# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/svpino/dev/tensorflow-object-detection-sagemaker/todl/tensorflow-object-detection/research/object_detection/utils/context_manager.py
# Compiled at: 2020-04-05 19:50:58
# Size of source mod 2**32: 1277 bytes
"""Python context management helper."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

class IdentityContextManager(object):
    __doc__ = 'Returns an identity context manager that does nothing.\n\n  This is helpful in setting up conditional `with` statement as below:\n\n  with slim.arg_scope(x) if use_slim_scope else IdentityContextManager():\n    do_stuff()\n\n  '

    def __enter__(self):
        pass

    def __exit__(self, exec_type, exec_value, traceback):
        del exec_type
        del exec_value
        del traceback
        return False