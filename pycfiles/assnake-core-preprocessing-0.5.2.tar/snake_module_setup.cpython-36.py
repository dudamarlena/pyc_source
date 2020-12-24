# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/fedorov/GitHub/assnake-core-preprocessing/assnake_core_preprocessing/snake_module_setup.py
# Compiled at: 2020-03-25 14:43:38
# Size of source mod 2**32: 895 bytes
import os, assnake, assnake_core_preprocessing.count.result, assnake_core_preprocessing.remove_human_bbmap.result, assnake_core_preprocessing.trimmomatic.result, assnake_core_preprocessing.multiqc.result, assnake_core_preprocessing.count.result
from assnake_core_preprocessing.fastqc.result_fastqc import result_fastqc
from assnake.utils import read_yaml
this_dir = os.path.dirname(os.path.abspath(__file__))
snake_module = assnake.SnakeModule(name='assnake-core-preprocessing',
  install_dir=this_dir,
  results=[
 assnake_core_preprocessing.count.result,
 assnake_core_preprocessing.trimmomatic.result,
 result_fastqc,
 assnake_core_preprocessing.remove_human_bbmap.result,
 assnake_core_preprocessing.multiqc.result],
  snakefiles=[],
  invocation_commands=[])