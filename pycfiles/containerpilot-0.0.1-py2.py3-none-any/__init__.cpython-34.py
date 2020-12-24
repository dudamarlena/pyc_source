# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/containerdiff/__init__.py
# Compiled at: 2016-05-23 02:26:04
# Size of source mod 2**32: 1063 bytes
__doc__ = "Main module of containerdiff.\n\nI contains some options and import all parts of 'run' module.\n"
program_version = '0.4'
program_description = 'Show changes among two container images.'
docker_socket = 'unix://var/run/docker.sock'
silent = False
from containerdiff.run import *