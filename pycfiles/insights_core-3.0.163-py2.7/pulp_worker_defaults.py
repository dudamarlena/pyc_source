# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/pulp_worker_defaults.py
# Compiled at: 2019-05-16 13:41:33
"""
PulpWorkerDefaults - file ``/etc/default/pulp_workers``
=======================================================

The PulpWorkerDefaults parser reads the shell options set in the
``/etc/default/pulp_worker`` file.  These are made available using the
:class:`insights.core.SysconfigOptions` class methods.

Sample file contents::

    # Configuration file for Pulp's Celery workers

    # Define the number of worker nodes you wish to have here. This defaults to the number of processors
    # that are detected on the system if left commented here.
    PULP_CONCURRENCY=1

    # Configure Python's encoding for writing all logs, stdout and stderr
    PYTHONIOENCODING="UTF-8"

Examples:
    >>> pulp_defs = shared[PulpWorkerDefaults]
    >>> type(pulp_defs)
    <class 'insights.parsers.pulp_worker_defaults.PulpWorkerDefaults'>
    >>> 'PULP_CONCURRENCY' in pulp_defs
    True
    >>> pulp_defs['PULP_CONCURRENCY']  # Note string return value
    '1'
    >>> 'PULP_MAX_TASKS_PER_CHILD' in pulp_defs
    False
    >>> pulp_defs['PYTHONIOENCODING']  # Values are dequoted as per bash
    'UTF-8'

"""
from .. import parser, SysconfigOptions
from insights.specs import Specs

@parser(Specs.pulp_worker_defaults)
class PulpWorkerDefaults(SysconfigOptions):
    """
    Parse the ``/etc/default/pulp_workers`` file.
    """
    pass