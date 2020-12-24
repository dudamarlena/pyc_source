# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/user/src_import/ryo-iso/ryo_iso/tasks/init.py
# Compiled at: 2019-11-12 05:13:56
# Size of source mod 2**32: 1097 bytes
import ryo_iso as _ryo_iso
if 'DOIT_CONFIG' not in globals():
    DOIT_CONFIG = {'backend':'json',  'default_tasks':[
      'init'], 
     'verbosity':2, 
     'failure_verbosity':0}

def task_init():
    """
    Initialize a new project

    Create :ref:`iso.yml` config file in the current directory and
    install :ref:`$XDG_CONFIG_HOME/ryo-iso/config.yml <config.yml>` and
    :ref:`$XDG_CONFIG_HOME/ryo-iso/iso_base.yml <iso_base.yml>`

    :actions:
      - :func:`ryo_iso.config.Config.install`
    :params:
      - ``-f``, ``--force`` Force installation
    :targets:
      - :ref:`config.yml`
      - :ref:`iso_base.yml`
      - :ref:`iso.yml`
    :uptodate:
      - False
    """
    return {'actions':[
      _ryo_iso.Config.install], 
     'params':[
      {'name':'force', 
       'short':'f', 
       'long':'force', 
       'type':bool, 
       'default':False, 
       'help':'Force installation'}], 
     'targets':list(_ryo_iso.Config.data.values()), 
     'uptodate':[
      False]}