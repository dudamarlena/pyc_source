# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-ed191__6/grpcio/grpc/framework/foundation/abandonment.py
# Compiled at: 2020-01-10 16:25:22
# Size of source mod 2**32: 872 bytes
"""Utilities for indicating abandonment of computation."""

class Abandoned(Exception):
    __doc__ = 'Indicates that some computation is being abandoned.\n\n  Abandoning a computation is different than returning a value or raising\n  an exception indicating some operational or programming defect.\n  '