# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/oyProjectManager/models/errors.py
# Compiled at: 2012-09-24 08:16:34
import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)

class CircularDependencyError(Exception):
    """Raised when there is circular dependencies between Versions
    """

    def __init__(self, value=''):
        super(CircularDependencyError, self).__init__(value)
        self.value = value

    def __str__(self):
        return repr(self.value)