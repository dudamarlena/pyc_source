# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /users/payno/.local/share/virtualenvs/est_venv/lib/python3.7/site-packages/est/pushworkflowactors/actor.py
# Compiled at: 2020-03-05 02:52:24
# Size of source mod 2**32: 1835 bytes
"""This module contains the task to be implemented by the pushworkflow"""
__authors__ = [
 'H. Payno']
__license__ = 'MIT'
__date__ = '06/12/2019'
from est.pushworkflow.scheme.node import Node

class PyMcaFTTask(Node):
    callback = 'est.core.process.ft.PyMca_ft'


class PyMcaExafsTask(Node):
    callback = 'est.core.process.exafs.PyMca_exafs'


class PyMcaKWeightTask(Node):
    callback = 'est.core.process.k_weight.PyMca_k_weight'


class PyMcaNormalizationTask(Node):
    callback = 'est.core.process.normalization.process'