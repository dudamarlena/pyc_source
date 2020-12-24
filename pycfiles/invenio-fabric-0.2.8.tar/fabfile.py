# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/lnielsen/src/invenio-fabric/examples/atlantis/fabfile.py
# Compiled at: 2012-11-29 04:26:39
"""
Fabric tasks for bootstrapping, installing, deploying and running Atlantis.

Examples
--------
Setup virtual environment and database with Python 2.4 and Invenio v1.1.0:
  fab loc:py=24,ref=origin/v1.1.0 bootstrap
  fab loc:py=24,ref=origin/v1.1.0 invenio_create_demosite

Dump, load and drop (database and virtual environment):
  fab loc:py=27,ref=master dump
  fab loc:py=27,ref=master load
  fab loc:py=27,ref=master drop

Requirements:
 * pythonbrew must be installed to specify a specific Python version.
"""
from fabric.api import task, abort
from fabric.colors import red
from inveniofab.api import *
import os

@task
def loc(activate=True, py=None, ref=None, **kwargs):
    """
    Local environment (example: loc:py=24,ref=maint-1.1)
    """
    if 'name' not in kwargs:
        kwargs['name'] = env_make_name('atlantis', py or '', ref or '')
    env = env_create('loc', activate=activate, python=py, **kwargs)
    return env_override(env, 'invenio', ref, {'ref': ref})