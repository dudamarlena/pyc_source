# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mafju/current/icm/iis_cr/vipe/vipe/__init__.py
# Compiled at: 2016-02-15 13:44:30
# Size of source mod 2**32: 893 bytes
import os.path
__title__ = 'vipe'
__author__ = 'Mateusz Kobos'
__email__ = 'mkobos@icm.edu.pl'
__version__ = open(os.path.join(os.path.dirname(__file__), 'RELEASE-VERSION')).read().strip()
__description__ = 'Tool for visualizing Apache Oozie pipelines'
__license__ = 'Apache License, Version 2.0'