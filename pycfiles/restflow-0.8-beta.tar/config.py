# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /homes/students/weigl/workspace1/restflow/restflow/config.py
# Compiled at: 2014-08-27 05:13:16
__author__ = 'Alexander Weigl'
import os, sys
from path import path
ELASTICITY_PROGRAM = os.environ.get('ELASTICIY', '/home/weigl/workspace/hiflow_1.4/build/examples/elasticity/elasticity')