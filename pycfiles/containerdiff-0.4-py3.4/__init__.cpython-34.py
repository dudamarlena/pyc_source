# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/containerdiff/__init__.py
# Compiled at: 2016-05-23 02:26:04
# Size of source mod 2**32: 1063 bytes
"""Main module of containerdiff.

I contains some options and import all parts of 'run' module.
"""
program_version = '0.4'
program_description = 'Show changes among two container images.'
docker_socket = 'unix://var/run/docker.sock'
silent = False
from containerdiff.run import *