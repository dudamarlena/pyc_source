# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/extenteten/embedding/embeddings.py
# Compiled at: 2017-01-06 05:01:09
# Size of source mod 2**32: 305 bytes
import tensorflow as tf
from ..variable import variable
from ..util import func_scope

@func_scope()
def embeddings(initial=None, id_space_size=None, embedding_size=None, name=None):
    return variable((initial or [id_space_size, embedding_size]), name=name)