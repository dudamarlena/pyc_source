# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/kieffer/workspace/sift_pyocl/build/lib.linux-x86_64-2.7/sift_pyocl/__init__.py
# Compiled at: 2014-10-28 04:09:13
"""
Module Sift for calculating SIFT keypoint using PyOpenCL
"""
version = '0.3.0'
import os
sift_home = os.path.dirname(os.path.abspath(__file__))
import sys, logging
logging.basicConfig()
from .plan import SiftPlan
from .match import MatchPlan
from .alignment import LinearAlign