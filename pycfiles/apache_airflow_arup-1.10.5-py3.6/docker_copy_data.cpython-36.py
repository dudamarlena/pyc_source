# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/example_dags/docker_copy_data.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 3845 bytes
"""
This sample "listen to directory". move the new file and print it,
using docker-containers.
The following operators are being used: DockerOperator,
BashOperator & ShortCircuitOperator.
TODO: Review the workflow, change it accordingly to
      your environment & enable the code.
"""