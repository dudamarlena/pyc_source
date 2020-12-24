# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\qduan\Stanmo\git\github\stanmo\stanmo\spec\churn\__init__.py
# Compiled at: 2016-01-01 21:41:52
""" model implementation classes
Each class in model package should implement one mining model as a sub-class of the BaseMiningModel.
"""
__author__ = 'duan'
__model_spec_name__ = 'churn.ChurnMiningModel'
__model_spec_desc__ = 'Churn Prediction for Telco'
from .churnmodelspec import ChurnMiningModel