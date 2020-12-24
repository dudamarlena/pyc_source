# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: py-build/2.7/bdist.linux-x86_64/egg/riak/datatypes/errors.py
# Compiled at: 2016-10-17 19:06:50
from riak import RiakError

class ContextRequired(RiakError):
    """
    This exception is raised when removals of map fields and set
    entries are attempted and the datatype hasn't been initialized
    with a context.
    """
    _default_message = 'A context is required for remove operations, fetch the datatype first'

    def __init__(self, message=None):
        super(ContextRequired, self).__init__(message or self._default_message)