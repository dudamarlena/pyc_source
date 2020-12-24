# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\chitwanabm\__init__.py
# Compiled at: 2013-02-23 23:08:00
"""
'chitwanabm' is an agent-based model of the Western Chitwan Valley, Nepal. The 
model represents a subset of the population of the Valley using a number of 
agent types (person, household and neighborhood agents), environmental 
variables (topography, land use and land cover) and social context variables.

Construction of the model is supported as part of an ongoing National Science 
Foundation Partnerships for International Research and Education (NSF PIRE) 
project (grant OISE 0729709) investigating human-environment interactions in 
the Western Chitwan Valley.
"""
__version__ = '1.5'
from pyabm import rc_params, np
rc_params._initialized = False