# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/sampedro/Documents/Dev/oide-project/dev-env/local/lib/python2.7/site-packages/oide_slurm_assist-0.0.dev1-py2.7.egg/oideslurm/urls.py
# Compiled at: 2015-10-12 18:05:23
from oideslurm.handlers import FormConfigHandler
from oideslurm.handlers import JobListHandler
from oideslurm.handlers import JobHandler
URL_SCHEMA = [
 (
  '/slurm/a/config', FormConfigHandler),
 (
  '/slurm/a/jobs', JobListHandler),
 (
  '/slurm/a/jobs/?(?P<jobid>[0-9]+)?', JobHandler)]